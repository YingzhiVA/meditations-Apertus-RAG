"""HuggingFace Space entry point: the public web UI (src/meditations_rag/web.py)."""

import os
import sys
from pathlib import Path

# The page needs no GPU: one query embedding against 487 passages is
# milliseconds on CPU. On ZeroGPU hardware CUDA is only emulated outside
# @spaces.GPU functions, so the embedder is pinned to CPU before config is
# read. Set before any meditations_rag import.
os.environ.setdefault("MEDITATIONS_EMBED_DEVICE", "cpu")

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

try:
    import spaces  # preinstalled on ZeroGPU Spaces; absent elsewhere

    @spaces.GPU(duration=1)
    def _never_called() -> None:
        """ZeroGPU expects at least one @spaces.GPU function at startup.
        Nothing calls this one, so the page uses no GPU quota."""
except ImportError:
    pass

from meditations_rag.web import main  # noqa: E402

if __name__ == "__main__":
    main()
