param(
    [string]$SkillDir = (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
)

Write-Host "=== Audio Transcriber Skill Setup (Proactive Mode) ===" -ForegroundColor Cyan

# 1. Kiem tra va cai dat FFmpeg
if (!(Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
    Write-Host "[-] Khong tim thay FFmpeg. Dang thu cai dat qua winget..." -ForegroundColor Yellow
    winget install ffmpeg --source winget --accept-package-agreements --accept-source-agreements
    if (!(Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
        Write-Host "[!] Khong the tu dong cai FFmpeg. Vui long tai thu cong tai https://ffmpeg.org/" -ForegroundColor Red
    } else {
        Write-Host "[+] Da cai dat FFmpeg thanh cong!" -ForegroundColor Green
    }
} else {
    Write-Host "[+] FFmpeg da san sang." -ForegroundColor Green
}

# 2. Tao models directory
$ModelsDir = Join-Path $SkillDir "models"
if (!(Test-Path $ModelsDir)) {
    New-Item -ItemType Directory -Path $ModelsDir -Force | Out-Null
}

# 3. Cai dat Python packages
Write-Host "Dang cai dat/cap nhat thu vien Python..." -ForegroundColor Yellow
$Packages = @(
    "yt-dlp", "faster-whisper", "torchaudio", "silero-vad", 
    "soundfile", "pydub", "speechbrain", "numpy", "scipy", 
    "scikit-learn", "tqdm", "noisereduce", "librosa"
)

foreach ($pkg in $Packages) {
    Write-Host "Installing $pkg..." -ForegroundColor Green
    python -m pip install $pkg --quiet --upgrade
}

# 4. Download Models for Offline Use
Write-Host "Dang tai Whisper Model (large-v3-turbo) ve thu muc local..." -ForegroundColor Yellow
python -c "from faster_whisper import WhisperModel; WhisperModel('large-v3-turbo', download_root='$($ModelsDir -replace '\\', '/')')"

Write-Host "Dang tai Silero VAD Model..." -ForegroundColor Yellow
python -c "import torch; torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad', force_reload=True, trust_repo=True)"

Write-Host "=== Setup hoan tat! ===" -ForegroundColor Cyan
Write-Host "Moi truong da duoc toi uu hoa de chay Offline." -ForegroundColor Green
