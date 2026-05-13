param(
    [string]$SkillDir = (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))
)

Write-Host "=== Audio Transcriber Skill Setup (Proactive Mode) ===" -ForegroundColor Cyan

# =========================================================
# HuggingFace Token
# =========================================================

# Dán token của bạn vào đây (hoặc set qua biến môi trường HF_TOKEN trước khi chạy)
# $env:HF_TOKEN = "hf_your_token_here"

# =========================================================
# 1. Kiem tra Python
# =========================================================

if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "[!] Khong tim thay Python!" -ForegroundColor Red
    Write-Host "Tai Python tai: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

Write-Host "[+] Python da san sang." -ForegroundColor Green

# =========================================================
# 2. Cap nhat pip
# =========================================================

Write-Host "Dang cap nhat pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# =========================================================
# 3. Kiem tra va cai dat FFmpeg
# =========================================================

if (!(Get-Command ffmpeg -ErrorAction SilentlyContinue)) {

    Write-Host "[-] Khong tim thay FFmpeg. Dang thu cai dat qua winget..." -ForegroundColor Yellow

    winget install ffmpeg `
        --source winget `
        --accept-package-agreements `
        --accept-source-agreements

    if (!(Get-Command ffmpeg -ErrorAction SilentlyContinue)) {

        Write-Host "[!] Khong the tu dong cai FFmpeg." -ForegroundColor Red
        Write-Host "[!] Vui long tai thu cong tai https://ffmpeg.org/" -ForegroundColor Yellow

    } else {

        Write-Host "[+] Da cai dat FFmpeg thanh cong!" -ForegroundColor Green
    }

} else {

    Write-Host "[+] FFmpeg da san sang." -ForegroundColor Green
}

# =========================================================
# 4. Tao models directory
# =========================================================

$ModelsDir = Join-Path $SkillDir "models"

if (!(Test-Path $ModelsDir)) {
    New-Item -ItemType Directory -Path $ModelsDir -Force | Out-Null
}

Write-Host "[+] Models Dir: $ModelsDir" -ForegroundColor Green

# =========================================================
# 5. Cai dat Python packages
# =========================================================

Write-Host "Dang cai dat/cap nhat thu vien Python..." -ForegroundColor Yellow

$Packages = @(
    "yt-dlp",
    "faster-whisper",
    "ctranslate2",
    "torch",
    "torchaudio",
    "silero-vad",
    "soundfile",
    "pydub",
    "speechbrain",
    "numpy",
    "scipy",
    "scikit-learn",
    "tqdm",
    "noisereduce",
    "librosa"
)

foreach ($pkg in $Packages) {

    Write-Host "Installing $pkg..." -ForegroundColor Green

    try {
        python -m pip install $pkg --upgrade
    }
    catch {
        Write-Host "[!] Loi khi cai $pkg" -ForegroundColor Red
    }
}

# =========================================================
# 6. Download Whisper Model
# =========================================================

Write-Host "Dang tai Whisper Model (large-v3-turbo) ve thu muc local..." -ForegroundColor Yellow

try {

    python -c "
from faster_whisper import WhisperModel

print('Loading Whisper model...')

model = WhisperModel(
    'large-v3-turbo',
    download_root=r'$($ModelsDir)'
)

print('Whisper model downloaded successfully!')
"

    Write-Host "[+] Whisper model da san sang." -ForegroundColor Green
}
catch {

    Write-Host "[!] Loi download Whisper model." -ForegroundColor Red
}

# =========================================================
# 7. Download Silero VAD
# =========================================================

Write-Host "Dang tai Silero VAD Model..." -ForegroundColor Yellow

try {

    python -c "
import torch

print('Downloading Silero VAD...')

model, utils = torch.hub.load(
    repo_or_dir='snakers4/silero-vad',
    model='silero_vad',
    force_reload=False,
    trust_repo=True
)

print('Silero VAD downloaded successfully!')
"

    Write-Host "[+] Silero VAD da san sang." -ForegroundColor Green
}
catch {

    Write-Host "[!] Loi download Silero VAD." -ForegroundColor Red
}

# =========================================================
# DONE
# =========================================================

Write-Host "=== Setup hoan tat! ===" -ForegroundColor Cyan
Write-Host "Moi truong da duoc toi uu hoa de chay Offline." -ForegroundColor Green
Write-Host "Models duoc luu tai: $ModelsDir" -ForegroundColor Yellow