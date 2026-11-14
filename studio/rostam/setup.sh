#!/bin/bash
# Setup for the Rostam & Sohrab series in a fresh container: packages and the Kokoro voice model (~330 MB).
set -e
cd "$(dirname "$0")"
pip install --break-system-packages -q "skia-python==144.1" "sherpa-onnx==1.13.8" numpy pillow
python3 -c "from PIL import features; assert features.check('raqm'), 'Pillow without raqm: Persian text would break'"
command -v ffmpeg >/dev/null || { echo "ffmpeg missing"; exit 1; }
mkdir -p voice
if [ ! -s voice/kokoro-multi-lang-v1_0/model.onnx ]; then
  curl -sSL -o voice/kokoro.tar.bz2 https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/kokoro-multi-lang-v1_0.tar.bz2
  tar -xjf voice/kokoro.tar.bz2 -C voice && rm voice/kokoro.tar.bz2
fi
python3 -c "import skia, sherpa_onnx; print('setup ok')"
