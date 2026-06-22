---
name: wechat-article-to-markdown
description: 抓取微信公众号文章并转换为 Markdown 格式，先用 httpx 快路径（一秒内），失败再用 Camoufox 反检测浏览器
---

# WeChat Article to Markdown

将微信公众号文章抓取并转换为干净的 Markdown 文件。

## 使用场景

当需要将微信公众号文章保存为 Markdown 格式时使用此 skill。适用于：
- 归档微信文章为本地 Markdown
- 提取文章内容用于后续处理（如 AI 摘要、知识库导入）
- 批量保存公众号内容

## 前置条件

- Python 3.8+ 已安装
- [uv](https://docs.astral.sh/uv/) 已安装（推荐），或手动 `pip install -r requirements.txt`

## 使用方法

```bash
cd <path-to-skill>/wechat-article
uv run main.py "<微信文章URL>"
```

**输入**: 微信公众号文章 URL (形如 `https://mp.weixin.qq.com/s/...`)

**输出**: `output/<文章标题>/` 目录下：
- `<文章标题>.md` — Markdown 文件，包含标题、作者、发布时间、原文链接和正文
- `images/` — 文章配图（自动从微信 CDN 下载到本地）

## 抓取策略

1. **快路径 (httpx)** — 伪装微信客户端 UA 直接 HTTP 请求，<1 秒完成
2. **慢路径 (Camoufox)** — 快路径被验证码拦截时自动切换，启动反检测 Firefox 浏览器绕过

## 功能特性

1. **两级抓取** — httpx 快路径优先，Camoufox 反检测浏览器兜底
2. **元数据提取** — 标题、公众号名称、发布时间、原文链接
3. **图片本地化** — 微信 CDN 图片自动下载到本地 `images/` 目录，Markdown 引用本地路径
4. **代码块处理** — 正确提取微信 `code-snippet` 代码块，识别语言标识，过滤 CSS counter 垃圾
5. **HTML → Markdown** — 使用 markdownify 转换，保留标题层级、列表、引用块、粗体等格式
6. **并发下载** — 图片并发下载（默认 5 并发），加速处理

## 限制

- 部分文章的代码块使用图片/SVG 渲染而非文本，这些无法提取为代码
- 需要文章的公开 URL（`mp.weixin.qq.com` 域名）
