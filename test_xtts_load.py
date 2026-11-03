import os

os.environ["TEMP"] = r"D:\Temp"
os.environ["TMP"] = r"D:\Temp"
os.environ["TTS_HOME"] = r"D:\XTTS_Models"

import torch

# Tương thích checkpoint XTTS với PyTorch 2.6
old_torch_load = torch.load

def compatible_torch_load(*args, **kwargs):
    kwargs.setdefault("weights_only", False)
    return old_torch_load(*args, **kwargs)

torch.load = compatible_torch_load

from TTS.api import TTS

model_dir = r"D:\XTTS_Models\tts\tts_models--multilingual--multi-dataset--xtts_v2"

print("CUDA:", torch.cuda.is_available())
print("Đang nạp XTTS-v2...")

tts = TTS(
    model_path=model_dir,
    config_path=os.path.join(model_dir, "config.json"),
    gpu=True
)

print("NAP XTTS THANH CONG!")
print("GPU:", torch.cuda.get_device_name(0))