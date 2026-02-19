from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.gallery_store import index_outputs, stats


if __name__ == "__main__":
    result = index_outputs()
    summary = stats()
    print("index_result:", result)
    print("stats:", summary)
