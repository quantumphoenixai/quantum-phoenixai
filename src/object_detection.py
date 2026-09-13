import torch

print("PyTorch version:", torch.__version__)

if torch.cuda.is_available():
    print("GPU available")
else:
    print("Running on CPU")