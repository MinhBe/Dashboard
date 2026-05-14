# Max Mode Reference

## Output format
- **File suffix**: `_Max.md`
- **Header**: `### [MAX] Transcript: {title}`
- **Full metadata**: source URL, author, duration, language, date
- **Detailed speaker blocks**: `**Nhân vật N** [start - end]` with quoted text
- **Pipeline**: download → denoise → transcribe → diarize → format_max

## When to use
- Archival / reference-quality transcripts
- Content where speaker timing matters
- Need full metadata (channel, duration, etc.)
- Post-processing with AI editing (rich structure is easier to parse)

## Caveats
- Diarization required — highest resource usage
- Processing time ~2x Fast mode
- Same speaker label limitations as Normal (generic names)
- Best results on clean audio with distinct speakers
