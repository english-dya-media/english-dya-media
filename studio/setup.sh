#!/bin/bash
# One-time setup in a fresh container: python packages, voice model, fonts, emoji images.
set -e
cd "$(dirname "$0")"
pip install --break-system-packages -q "kokoro-onnx==0.6.1" soundfile
python3 -c "import playwright" 2>/dev/null || pip install --break-system-packages -q playwright
command -v ffmpeg >/dev/null || { echo "ffmpeg missing"; exit 1; }
mkdir -p voice assets/fonts assets/emoji build out content weeks
REL=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
[ -s voice/kokoro-v1.0.onnx ] || curl -sSL -o voice/kokoro-v1.0.onnx "$REL/kokoro-v1.0.onnx"
[ -s voice/voices-v1.0.bin ] || curl -sSL -o voice/voices-v1.0.bin "$REL/voices-v1.0.bin"
if [ ! -s assets/fonts/Vazirmatn.woff2 ]; then
  mkdir -p node
  (cd node && npm init -y >/dev/null 2>&1 && npm install --silent vazirmatn @fontsource/poppins @fontsource/noto-sans)
  cp "node/node_modules/vazirmatn/fonts/webfonts/Vazirmatn[wght].woff2" assets/fonts/Vazirmatn.woff2
  cp node/node_modules/@fontsource/poppins/files/poppins-latin-{600,700,800}-normal.woff2 assets/fonts/
  cp node/node_modules/@fontsource/noto-sans/files/noto-sans-latin{,-ext}-{500,600}-normal.woff2 assets/fonts/
fi
python3 fetch_emoji.py
echo "setup ok"
