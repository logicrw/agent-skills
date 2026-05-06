---
name: gemini-transcribe
description: Transcribe or analyze local audio/video files (mp3, m4a, wav, flac, mp4, webm, mov, avi) up to 2 hours via Google Gemini API. Supports speech transcription, speaker identification, and visual content analysis for video.
---

# Gemini Transcribe

Transcribe or analyze audio and video files via Google Gemini's multimodal API. Handles files up to 2 hours. For video, Gemini processes both the audio track and visual frames, so it can describe on-screen content (slides, code, whiteboard, demos) alongside speech.

## When to use this vs other tools

| Situation | Use this | Use video-transcript-downloader |
|---|---|---|
| Local audio file (mp3/m4a/wav/flac) | ✅ | ❌ |
| Local video file (mp4/webm/mov) | ✅ | ❌ |
| YouTube with available subtitles | ❌ (overkill) | ✅ |
| YouTube without subtitles | ✅ (download first) | ❌ |
| Need visual analysis (slides, code on screen) | ✅ | ❌ |
| Need analysis/extraction, not just transcript | ✅ | ❌ |
| File > 2 hours | Split first, then ✅ | ❌ |

## Prerequisites

- Python 3.10+
- `httpx` package (`pip install httpx`)
- Gemini API key in `.env` file (auto-loaded) or `GEMINI_API_KEY` env var

## Quick Start

```bash
SKILL_DIR="<path-to-this-skill>"

# Verbatim transcription of audio
python $SKILL_DIR/scripts/transcribe.py "/path/to/podcast.mp3"

# Transcription with speaker identification
python $SKILL_DIR/scripts/transcribe.py "/path/to/interview.mp3" \
  --speakers "Sam Altman,Greg Brockman,Host"

# Video transcription (audio + visual description)
python $SKILL_DIR/scripts/transcribe.py "/path/to/presentation.mp4"

# Video with visual emphasis
python $SKILL_DIR/scripts/transcribe.py "/path/to/demo.mp4" \
  --prompt "Transcribe all speech AND describe what is shown on screen (slides, UI, code). Format: timestamps + [Visual: description] + speech."

# Custom analysis (not transcription)
python $SKILL_DIR/scripts/transcribe.py "/path/to/meeting.mp3" \
  --prompt "Extract all action items, decisions, and deadlines. Format as a checklist."

# Specify output path and model
python $SKILL_DIR/scripts/transcribe.py "/path/to/lecture.mp4" \
  -o ~/Documents/lecture_notes.md --model gemini-2.5-pro

# Re-run and overwrite existing output
python $SKILL_DIR/scripts/transcribe.py "/path/to/podcast.mp3" --force
```

## How It Works

### Key design decisions from real-world usage

1. **Unicode path workaround**: `httpx` chokes on non-ASCII filenames (Chinese characters, em dashes). When detected, the script copies the file to `/tmp/` with a sanitized name before uploading. ASCII filenames skip this step entirely.

2. **File upload + activation wait**: Gemini File API uses a two-step resumable upload, then the file transitions from PROCESSING → ACTIVE. Video files take longer (up to 5 minutes). The script polls automatically.

3. **Non-streaming default**: For long files, SSE streaming sometimes returns 0 events (the server buffers the entire response while thinking). Non-streaming is more reliable. If it returns empty, the script automatically retries with streaming as a fallback.

4. **Video = audio + vision**: When you upload a video file, Gemini processes both tracks. The default transcription prompt focuses on speech, but you can use `--prompt` to request visual descriptions too.

## Script Reference

```
usage: transcribe.py [-h] [--api-key KEY] [--model MODEL]
                     [--speakers SPEAKERS] [--prompt PROMPT]
                     [--lang LANG] [-o OUTPUT] [--streaming]
                     [--force]
                     media_file

positional arguments:
  media_file            Path to audio or video file

options:
  --api-key KEY         Gemini API key (default: .env or $GEMINI_API_KEY)
  --model MODEL         Model name (default: gemini-2.5-flash)
  --speakers SPEAKERS   Comma-separated speaker names for identification
  --prompt PROMPT       Custom prompt (overrides default transcription prompt)
  --lang LANG           Output language (e.g. 'Chinese', 'Japanese'). Translates if source differs.
  -o, --output OUTPUT   Output file path (default: <input_name>_transcript.md)
  --streaming           Force SSE streaming mode
  --force               Overwrite output file without prompting
```

## Supported Formats

**Audio**: `mp3`, `m4a`, `wav`, `flac`, `ogg`, `aac`, `opus`
**Video**: `mp4`, `webm`, `mov`, `avi`

Max file size ~2GB, max duration ~2 hours. MIME type auto-detected from extension; unsupported extensions are rejected with an error.

## Typical Workflows

### Workflow 1: Podcast / Interview transcription
```bash
python scripts/transcribe.py ~/Downloads/podcast.mp3 \
  --speakers "Host,Guest1,Guest2" \
  -o ~/Documents/podcast_transcript.md
```

### Workflow 2: Meeting recording with visual notes
```bash
python scripts/transcribe.py ~/Downloads/zoom_recording.mp4 \
  --prompt "Transcribe speech with speaker labels. When slides or screen shares are shown, describe the key content in [Slide: ...] annotations." \
  -o ~/Documents/meeting_notes.md
```

### Workflow 3: Extract specific insights from audio
```bash
python scripts/transcribe.py ~/Downloads/earnings_call.mp3 \
  --prompt "Extract all financial figures, guidance, and forward-looking statements with exact quotes." \
  -o ~/Documents/earnings_insights.md
```

### Workflow 4: YouTube video (no subtitles)
```bash
# Step 1: Download
yt-dlp -x --audio-format mp3 -o ~/Downloads/video.mp3 "https://youtube.com/watch?v=..."
# Step 2: Transcribe
python scripts/transcribe.py ~/Downloads/video.mp3 -o transcript.md
```

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `File never became ACTIVE` | Large video still processing | Wait longer; check file < 2GB |
| Empty output (0 chars) | Model thinking timeout | Script auto-retries with streaming fallback; try `gemini-2.5-pro` |
| Truncated transcript | Output token limit | Script warns (`⚠ TRUNCATED`) in both modes; split file and transcribe in parts |
| Upload fails after retries | Network instability on large files | Script auto-retries 3× with fresh upload URL and backoff; check network or split file |
| Server 500/503 on generate | Gemini transient error | Script auto-retries 3× with backoff; if persistent, try later |
| `httpx.ReadTimeout` on generate | Response > 10 min | Script auto-retries; also try `--streaming` or split file |
| `Unsupported file type` | Extension not in MIME map | Convert to a supported format (see list above) |
| `Output file already exists` | Previous run left a file | Use `--force` to overwrite, or `-o` for a different path |
| No visual descriptions | Default prompt is speech-only | Use `--prompt` to request visual analysis |

## Cost Estimate

Gemini 2.5 Flash (approximate, subject to change):
- Audio: ~1,750 tokens/min → 90 min ≈ 158K tokens
- Video: additional ~250 tokens/min for visual frames
- Output: ~20K tokens for verbatim transcript
- Cost: ~$0.02–0.05 per 90-minute audio, ~$0.05–0.10 for video
- See [official pricing](https://ai.google.dev/pricing) for current rates
