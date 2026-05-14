# Normal Mode Reference

## Output format
- **File suffix**: `_Normal.md`
- **Header**: `### [NORMAL] {title}`
- **Speaker labels**: `**Nhân vật N:**` with paragraphs grouped by speaker
- **Pipeline**: download → denoise → transcribe → diarize → format_normal
- **With diarization**: detects speaker changes, groups text

## When to use
- Multi-speaker content (podcasts, debates, interviews)
- Need readable narrative without timestamps
- Balance between readability and processing speed
- Default choice for most content

## Caveats
- Diarization adds ~30-50% processing time over Fast
- Speaker labels use generic "Nhân vật 1/2/3" (not real names)
- Background noise can confuse speaker clustering
- Paragraphs auto-split at ~10 segments — adjust in script if needed
