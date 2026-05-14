# Fast Mode Reference

## Output format
- **File suffix**: `_Fast.md`
- **Header**: `### [FAST] Transcript: {title}`
- **Timestamps**: `[mm:ss]` per segment, no speaker labels
- **Pipeline**: download → denoise → transcribe → format_fast
- **No diarization**: fastest, lowest resource usage

## When to use
- Content needs quick skimming by timestamp
- Single speaker / commentary-style videos
- YouTube clips under 10 minutes
- Any video where speaker identity doesn't matter

## Caveats
- `[LOW_CONFIDENCE]` tags indicate avg_logprob < -1.0
- No speaker separation — all text in one stream
- Vietnamese mixing with English is normal (Whisper handles both)
