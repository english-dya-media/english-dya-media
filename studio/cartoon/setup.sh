#!/bin/bash
# Setup for the cartoon story series in a fresh container: packages and the Piper voice model (~140 MB).
set -e
cd "$(dirname "$0")"
pip install --break-system-packages -q "resvg-py==0.5.0" "piper-tts==1.8.0" numpy scipy pillow
python3 -c "import resvg_py, piper, scipy; print('python packages ok')"
python3 -c "from PIL import features; assert features.check('raqm'), 'Pillow without raqm: Persian text would break'"
command -v ffmpeg >/dev/null || { echo "ffmpeg missing"; exit 1; }
ffmpeg -hide_banner -filters 2>/dev/null | grep -q " subtitles " || { echo "ffmpeg without libass (subtitles filter)"; exit 1; }
mkdir -p build/piper
if [ ! -s build/piper/en-us-libritts-high.onnx ]; then
  curl -sSL -o build/piper/v.tar.gz https://github.com/rhasspy/piper/releases/download/v0.0.2/voice-en-us-libritts-high.tar.gz
  tar -xzf build/piper/v.tar.gz -C build/piper && rm build/piper/v.tar.gz
fi
ls build/piper/en-us-libritts-high.onnx build/piper/en-us-libritts-high.onnx.json
python3 -c "import series, json; print('series:', ', '.join(series.queue()['order'])); print('setup ok')"
