import sys

FORBIDDEN = ("old-artlomo", "old-dev", "old-dev-files")
for p in sys.path:
    for f in FORBIDDEN:
        if p.endswith("/" + f) or p.endswith("\\" + f) or ("/" + f + "/") in p or ("\\" + f + "\\") in p:
            raise RuntimeError(f"Forbidden legacy path detected in sys.path: {p}")
