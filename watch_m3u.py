from __future__ import annotations
from pathlib import Path
import json, time, hashlib

from build_m3u import build_m3u, load_config

def fingerprint(music_dir: Path, exts: list[str]) -> str:
    # cheap fingerprint: (name, size, mtime) hash
    parts = []
    for ext in exts:
        for p in music_dir.glob(f"*{ext}"):
            if p.is_file():
                st = p.stat()
                parts.append(f"{p.name}|{st.st_size}|{int(st.st_mtime)}")
    parts.sort()
    h = hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()
    return h

def main():
    cfg = load_config()
    music_dir = Path(cfg["music_dir"]).expanduser()
    out_path = music_dir / cfg.get("m3u_name", "playlist.m3u8")
    exts = cfg.get("extensions", [".mp3"])
    max_tracks = int(cfg.get("max_tracks", 0))
    newest_first = (cfg.get("sort", "newest_first") == "newest_first")

    music_dir.mkdir(parents=True, exist_ok=True)
    last = ""

    print(f"[watch_m3u] watching: {music_dir}")
    while True:
        try:
            cur = fingerprint(music_dir, exts)
            if cur != last:
                n = build_m3u(music_dir, out_path, exts, max_tracks, newest_first)
                print(f"[watch_m3u] updated {out_path} ({n} tracks)")
                last = cur
        except Exception as e:
            print("[watch_m3u] error:", e)
        time.sleep(3)

if __name__ == "__main__":
    main()
