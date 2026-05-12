from huggingface_hub import hf_hub_download
import os, shutil

REPO_ID = os.getenv("MODEL_REPO_ID", "Qwen/Qwen2.5-0.5B-Instruct-GGUF")
FILENAME = os.getenv("MODEL_FILENAME", "qwen2.5-0.5b-instruct-q4_0.gguf")
OUT_PATH = os.getenv("LLM_MODEL_PATH", "models/qwen2.5-0.5b-instruct-q4.gguf")

os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
print(f"Downloading {REPO_ID}/{FILENAME} ...")
path = hf_hub_download(repo_id=REPO_ID, filename=FILENAME, local_dir="models/_hf_cache", local_dir_use_symlinks=False)
shutil.copyfile(path, OUT_PATH)
print(f"Saved to {OUT_PATH}")
