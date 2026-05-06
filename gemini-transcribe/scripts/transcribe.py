#!/usr/bin/env python3
"""
Transcribe or analyze audio and video files via Google Gemini API.

Supports audio (mp3, m4a, wav, flac, ogg, aac, opus) and video (mp4, webm, mov, avi).
For video, Gemini processes both the audio track and visual frames.

Handles: file upload, ACTIVE wait, non-streaming (default) + streaming fallback,
Unicode path workaround, and remote file cleanup.

Usage:
  python transcribe.py podcast.mp3
  python transcribe.py interview.mp4 --speakers "Host,Guest"
  python transcribe.py demo.mp4 --prompt "Describe slides and transcribe speech"
  python transcribe.py lecture.mp4 -o notes.md --model gemini-2.5-pro
"""

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
import time
from pathlib import Path

# Auto-load .env from skill root (../  relative to scripts/)
_SKILL_DIR = Path(__file__).resolve().parent.parent
_ENV_FILE = _SKILL_DIR / ".env"
if _ENV_FILE.exists():
    for line in _ENV_FILE.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, val = line.partition("=")
            os.environ.setdefault(key.strip(), val.strip())

try:
    import httpx
except ImportError:
    print("Error: httpx not installed. Run: pip install httpx", file=sys.stderr)
    sys.exit(1)

BASE_URL = "https://generativelanguage.googleapis.com"
DEFAULT_MODEL = "gemini-2.5-flash"
MAX_OUTPUT_TOKENS = 65536
READ_TIMEOUT = 600  # 10 minutes for long audio
POLL_INTERVAL = 5
MAX_POLL_ATTEMPTS = 60  # 5 minutes

MIME_MAP = {
    ".mp3": "audio/mpeg",
    ".m4a": "audio/mp4",
    ".wav": "audio/wav",
    ".flac": "audio/flac",
    ".ogg": "audio/ogg",
    ".mp4": "video/mp4",
    ".webm": "video/webm",
    ".mov": "video/quicktime",
    ".aac": "audio/aac",
    ".opus": "audio/opus",
    ".avi": "video/avi",
}


VIDEO_EXTENSIONS = {".mp4", ".webm", ".mov", ".avi"}


def is_video(path: str) -> bool:
    return Path(path).suffix.lower() in VIDEO_EXTENSIONS


def detect_mime(path: str) -> str:
    ext = Path(path).suffix.lower()
    mime = MIME_MAP.get(ext)
    if not mime:
        supported = ", ".join(sorted(MIME_MAP.keys()))
        print(f"Error: Unsupported file type '{ext}'. Supported: {supported}", file=sys.stderr)
        sys.exit(1)
    return mime


def safe_copy(src: str) -> str | None:
    """Copy file to /tmp with ASCII-safe name only if filename has non-ASCII chars.
    Returns the temp path, or None if no copy was needed.
    """
    src_path = Path(src)
    if src_path.name.isascii():
        return None
    safe_stem = re.sub(r"[^a-zA-Z0-9_-]", "_", src_path.stem)[:50]
    suffix = os.urandom(4).hex()
    safe_name = f"{safe_stem}_{suffix}{src_path.suffix}"
    tmp_path = Path(tempfile.gettempdir()) / safe_name
    shutil.copy2(src, tmp_path)
    return str(tmp_path)


def _initiate_resumable_upload(path: str, api_key: str, mime: str, sz: int) -> str:
    """Step 1: Get a fresh resumable upload URL."""
    resp = httpx.post(
        f"{BASE_URL}/upload/v1beta/files?key={api_key}",
        headers={
            "X-Goog-Upload-Protocol": "resumable",
            "X-Goog-Upload-Command": "start",
            "X-Goog-Upload-Header-Content-Length": str(sz),
            "X-Goog-Upload-Header-Content-Type": mime,
            "Content-Type": "application/json",
        },
        json={"file": {"display_name": Path(path).stem}},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.headers["X-Goog-Upload-URL"]


def upload_file(path: str, api_key: str, mime: str) -> tuple[str, str]:
    """Upload file to Gemini File API with retry. Returns (file_uri, file_name)."""
    sz = os.path.getsize(path)
    print(f"  Uploading {sz / 1024 / 1024:.1f} MB ...", flush=True)

    # Dynamic timeout: base 60s + 30s per 10MB, capped at 30 min
    upload_timeout = min(max(60, 30 * (sz // (10 * 1024 * 1024) + 1)), 1800)
    max_retries = 3

    for attempt in range(max_retries):
        try:
            # Get fresh upload URL each attempt (URLs expire after partial failure)
            upload_url = _initiate_resumable_upload(path, api_key, mime, sz)
            with open(path, "rb") as f:
                resp = httpx.post(
                    upload_url,
                    headers={
                        "X-Goog-Upload-Command": "upload, finalize",
                        "X-Goog-Upload-Offset": "0",
                        "Content-Length": str(sz),
                    },
                    content=f,
                    timeout=upload_timeout,
                )
            resp.raise_for_status()
            break
        except (httpx.TimeoutException, httpx.NetworkError) as e:
            if attempt == max_retries - 1:
                raise
            wait = 5 * (attempt + 1)
            print(f"  Upload failed ({e}), retrying in {wait}s ({attempt + 1}/{max_retries}) ...", flush=True)
            time.sleep(wait)

    info = resp.json()["file"]
    uri = info["uri"]
    name = info["name"]
    print(f"  Uploaded: {name} (state={info['state']})", flush=True)

    # Step 3: Poll until ACTIVE
    for i in range(MAX_POLL_ATTEMPTS):
        r = httpx.get(f"{BASE_URL}/v1beta/{name}?key={api_key}", timeout=15)
        state = r.json().get("state", "UNKNOWN")
        if state == "ACTIVE":
            elapsed = i * POLL_INTERVAL
            print(f"  File ready ({elapsed}s)", flush=True)
            return uri, name
        if state == "FAILED":
            raise RuntimeError(f"File processing failed: {r.json()}")
        if i > 0 and i % 6 == 0:
            print(f"  Still processing... ({i * POLL_INTERVAL}s)", flush=True)
        time.sleep(POLL_INTERVAL)

    raise RuntimeError(f"File not ACTIVE after {MAX_POLL_ATTEMPTS * POLL_INTERVAL}s")


def build_prompt(
    speakers: str | None,
    custom_prompt: str | None,
    video: bool = False,
    lang: str | None = None,
) -> str:
    """Build the transcription or analysis prompt."""
    if custom_prompt:
        return custom_prompt

    speaker_line = ""
    if speakers:
        names = [s.strip() for s in speakers.split(",")]
        speaker_line = f"Identify speakers by name: {', '.join(names)}. If unsure, use \"Speaker\".\n"

    video_line = ""
    if video:
        video_line = """When significant visual content appears (slides, code, UI, whiteboard, demos),
add a [Visual: brief description] annotation inline.
"""

    lang_line = ""
    if lang:
        lang_line = f"Output the transcript in {lang}. If the original speech is in a different language, translate it.\n"

    media_type = "audio and video" if video else "audio"
    return f"""Transcribe this entire {media_type} verbatim into Markdown.

{speaker_line}{video_line}{lang_line}Format each speaker turn as: **Speaker Name:** text
Preserve filler words (um, uh, like, you know) for accuracy.
Do NOT summarize or skip any sections. Transcribe EVERYTHING from start to finish.
For unclear words, use [inaudible].
Separate speaker turns with blank lines."""


def _extract_response(data: dict) -> str:
    """Extract text from Gemini response and report warnings."""
    text = ""
    for cand in data.get("candidates", []):
        finish = cand.get("finishReason", "")
        if finish == "MAX_TOKENS":
            print(
                f"  ⚠ Transcript TRUNCATED (hit {MAX_OUTPUT_TOKENS:,} token limit). "
                f"Split the file and transcribe in parts.",
                file=sys.stderr,
            )
        elif finish and finish not in ("STOP", ""):
            print(f"  Warning: finishReason={finish}", file=sys.stderr)
        for part in cand.get("content", {}).get("parts", []):
            text += part.get("text", "")

    usage = data.get("usageMetadata", {})
    if usage:
        prompt_tok = usage.get("promptTokenCount", 0)
        out_tok = usage.get("candidatesTokenCount", 0)
        print(f"  Tokens: {prompt_tok:,} in / {out_tok:,} out", flush=True)

    return text


def generate_non_streaming(
    file_uri: str, mime: str, prompt: str, model: str, api_key: str
) -> str:
    """Non-streaming generateContent call with retry on transient errors."""
    url = f"{BASE_URL}/v1beta/models/{model}:generateContent?key={api_key}"
    body = {
        "contents": [
            {
                "parts": [
                    {"file_data": {"mime_type": mime, "file_uri": file_uri}},
                    {"text": prompt},
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": MAX_OUTPUT_TOKENS,
        },
    }

    max_retries = 3
    for attempt in range(max_retries):
        print(f"  Generating (non-streaming, up to {READ_TIMEOUT // 60} min) ...", flush=True)
        try:
            resp = httpx.post(
                url,
                json=body,
                timeout=httpx.Timeout(connect=30, read=READ_TIMEOUT, write=30, pool=30),
            )
        except (httpx.TimeoutException, httpx.NetworkError) as e:
            if attempt == max_retries - 1:
                print(f"  Generate failed after {max_retries} attempts: {e}", file=sys.stderr)
                return ""
            wait = 10 * (attempt + 1)
            print(f"  Generate failed ({e}), retrying in {wait}s ({attempt + 1}/{max_retries}) ...", flush=True)
            time.sleep(wait)
            continue

        # Retry on 500/503 (Gemini transient errors)
        if resp.status_code in (500, 502, 503):
            if attempt < max_retries - 1:
                wait = 10 * (attempt + 1)
                print(f"  Server error {resp.status_code}, retrying in {wait}s ({attempt + 1}/{max_retries}) ...", flush=True)
                time.sleep(wait)
                continue
            print(f"  API error {resp.status_code} after {max_retries} attempts: {resp.text[:500]}", file=sys.stderr)
            return ""

        if resp.status_code != 200:
            print(f"  API error {resp.status_code}: {resp.text[:500]}", file=sys.stderr)
            return ""

        data = resp.json()
        if "error" in data:
            print(f"  API error: {data['error']}", file=sys.stderr)
            return ""

        return _extract_response(data)

    return ""  # all retries exhausted


def generate_streaming(
    file_uri: str, mime: str, prompt: str, model: str, api_key: str
) -> str:
    """SSE streaming generateContent call with retry. Fallback if non-streaming returns empty."""
    url = f"{BASE_URL}/v1beta/models/{model}:streamGenerateContent?alt=sse&key={api_key}"
    body = {
        "contents": [
            {
                "parts": [
                    {"file_data": {"mime_type": mime, "file_uri": file_uri}},
                    {"text": prompt},
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.1,
            "maxOutputTokens": MAX_OUTPUT_TOKENS,
        },
    }

    max_retries = 3
    for attempt in range(max_retries):
        print(f"  Generating (streaming) ...", flush=True)
        chunks = []
        char_count = 0
        truncated = False

        try:
            with httpx.Client(
                timeout=httpx.Timeout(connect=30, read=READ_TIMEOUT, write=30, pool=30)
            ) as client:
                with client.stream("POST", url, json=body) as resp:
                    if resp.status_code in (500, 502, 503):
                        err = "".join(resp.iter_text())
                        if attempt < max_retries - 1:
                            wait = 10 * (attempt + 1)
                            print(f"  Server error {resp.status_code}, retrying in {wait}s ({attempt + 1}/{max_retries}) ...", flush=True)
                            time.sleep(wait)
                            continue
                        print(f"  API error {resp.status_code} after {max_retries} attempts: {err[:500]}", file=sys.stderr)
                        return ""

                    if resp.status_code != 200:
                        err = "".join(resp.iter_text())
                        print(f"  API error {resp.status_code}: {err[:500]}", file=sys.stderr)
                        return ""

                    buf = ""
                    for raw in resp.iter_text():
                        buf += raw.replace("\r\n", "\n").replace("\r", "\n")
                        while "\n\n" in buf:
                            event, buf = buf.split("\n\n", 1)
                            for line in event.split("\n"):
                                if line.startswith("data: "):
                                    try:
                                        obj = json.loads(line[6:])
                                        for cand in obj.get("candidates", []):
                                            finish = cand.get("finishReason", "")
                                            if finish == "MAX_TOKENS":
                                                truncated = True
                                            elif finish and finish not in ("STOP", ""):
                                                print(f"  Warning: finishReason={finish}", file=sys.stderr)
                                            for part in cand.get("content", {}).get("parts", []):
                                                t = part.get("text", "")
                                                if t:
                                                    chunks.append(t)
                                                    char_count += len(t)
                                                    if char_count % 10000 < len(t):
                                                        print(
                                                            f"  {char_count:,} chars ...",
                                                            flush=True,
                                                        )
                                    except json.JSONDecodeError:
                                        pass

        except (httpx.TimeoutException, httpx.NetworkError) as e:
            if attempt == max_retries - 1:
                print(f"  Streaming failed after {max_retries} attempts: {e}", file=sys.stderr)
                return ""
            wait = 10 * (attempt + 1)
            print(f"  Streaming failed ({e}), retrying in {wait}s ({attempt + 1}/{max_retries}) ...", flush=True)
            time.sleep(wait)
            continue

        # Success — break out of retry loop
        if truncated:
            print(
                f"  ⚠ Transcript TRUNCATED (hit {MAX_OUTPUT_TOKENS:,} token limit). "
                f"Split the file and transcribe in parts.",
                file=sys.stderr,
            )

        text = "".join(chunks)
        print(f"  Streaming done: {len(text):,} chars", flush=True)
        return text

    return ""  # all retries exhausted


def cleanup_file(name: str, api_key: str):
    """Delete uploaded file from Gemini."""
    try:
        httpx.delete(f"{BASE_URL}/v1beta/{name}?key={api_key}", timeout=15)
        print("  Remote file cleaned up", flush=True)
    except Exception as e:
        print(f"  Cleanup warning: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe/analyze audio and video via Gemini API"
    )
    parser.add_argument("media_file", help="Path to audio or video file")
    parser.add_argument(
        "--api-key",
        default=os.environ.get("GEMINI_API_KEY", ""),
        help="Gemini API key (default: $GEMINI_API_KEY)",
    )
    parser.add_argument(
        "--model", default=DEFAULT_MODEL, help=f"Model (default: {DEFAULT_MODEL})"
    )
    parser.add_argument(
        "--speakers",
        help="Comma-separated speaker names for identification",
    )
    parser.add_argument(
        "--prompt",
        help="Custom prompt (overrides default transcription)",
    )
    parser.add_argument(
        "--lang",
        help="Output language (e.g. 'Chinese', 'Japanese'). Translates if source differs.",
    )
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument(
        "--streaming", action="store_true", help="Force SSE streaming mode"
    )
    parser.add_argument(
        "--force", action="store_true", help="Overwrite output file without prompting"
    )
    args = parser.parse_args()

    if not args.api_key:
        print("Error: No API key. Set GEMINI_API_KEY or use --api-key", file=sys.stderr)
        sys.exit(1)

    src = args.media_file
    if not os.path.exists(src):
        print(f"Error: File not found: {src}", file=sys.stderr)
        sys.exit(1)

    # Default output path
    if args.output:
        output_path = args.output
    else:
        src_path = Path(src)
        output_path = str(src_path.parent / f"{src_path.stem}_transcript.md")

    mime = detect_mime(src)
    video = is_video(src)
    prompt = build_prompt(args.speakers, args.prompt, video=video, lang=args.lang)
    media_label = "Video" if video else "Audio"

    print(f"{media_label}: {src} ({os.path.getsize(src) / 1024 / 1024:.1f} MB)")
    print(f"Model: {args.model}")
    print(f"Output: {output_path}")

    # Overwrite protection
    if os.path.exists(output_path) and not args.force:
        print(f"\n⚠ Output file already exists: {output_path}")
        print("  Use --force to overwrite, or -o to specify a different path.")
        sys.exit(1)

    # Copy to safe path only if filename has non-ASCII chars
    tmp_path = safe_copy(src)
    upload_path = tmp_path or src
    file_name = None

    try:
        # Upload
        file_uri, file_name = upload_file(upload_path, args.api_key, mime)

        # Generate
        if args.streaming:
            text = generate_streaming(file_uri, mime, prompt, args.model, args.api_key)
        else:
            text = generate_non_streaming(
                file_uri, mime, prompt, args.model, args.api_key
            )
            # Fallback to streaming if empty
            if not text:
                print("  Non-streaming returned empty, trying streaming ...", flush=True)
                text = generate_streaming(
                    file_uri, mime, prompt, args.model, args.api_key
                )

        if text:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"\n✓ Saved: {output_path} ({len(text):,} chars)")
        else:
            print("\n✗ No output received. Try a different model or split the audio.", file=sys.stderr)
            sys.exit(1)

    finally:
        # Cleanup
        if file_name:
            cleanup_file(file_name, args.api_key)
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)

    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
