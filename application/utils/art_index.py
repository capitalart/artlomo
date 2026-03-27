from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple
import application.config as config

UNAN = Path(getattr(config, "UNANALYSED_ROOT", Path("art-processing")/"unanalysed-artwork"))
PROC = Path(getattr(config, "PROCESSED_ROOT", Path("art-processing")/"processed-artwork"))
FIN  = Path(getattr(config, "FINALISED_ROOT", Path("art-processing")/"finalised-artwork"))
VAULT= Path(getattr(config, "ARTWORK_VAULT_ROOT", Path("art-processing")/"artwork-vault"))

_ORDER = [
    ("vault", VAULT),
    ("finalised", FIN),
    ("processed", PROC),
    ("unanalysed", UNAN),
]

def _scan(root: Path) -> List[str]:
    try:
        return [d.name for d in root.iterdir() if d.is_dir() and not d.name.startswith('.')]
    except Exception:
        return []

def list_artworks() -> List[Dict[str, str]]:
    """Return one entry per slug with precedence vault>finalised>processed>unanalysed."""
    seen: Dict[str, Tuple[str, Path]] = {}
    for stage, root in _ORDER:
        for slug in _scan(root):
            if slug not in seen:
                seen[slug] = (stage, root / slug)
    out: List[Dict[str, str]] = []
    for slug, (stage, path) in seen.items():
        out.append({"slug": slug, "stage": stage, "path": str(path)})
    return out

__all__ = ["list_artworks"]
