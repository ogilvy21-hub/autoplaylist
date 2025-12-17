from __future__ import annotations
from pathlib import Path
import json

def load_config() -> dict:
    cfg_path = Path(__file__).resolve().parent / "config.json"
    return json.loads(cfg_path.read_text(encoding="utf-8"))

def build_m3u(music_dir: Path, out_path: Path, exts: list[str], max_tracks: int, newest_first: bool) -> int:
    music_dir.mkdir(parents=True, exist_ok=True)
    files = []
    for ext in exts:
        files.extend(music_dir.glob(f"*{ext}"))
    files = [p for p in files if p.is_file()]

    files.sort(key=lambda p: p.stat().st_mtime, reverse=newest_first)
    if max_tracks and max_tracks > 0:
        files = files[:max_tracks]

    lines = ["#EXTM3U"]
    for f in files:
        title = f.stem
        lines.append(f"#EXTINF:-1,{title}")
        # Use relative paths so playlist works if you move folder as a unit
        lines.append(f.name)

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(files)

def main():
    cfg = load_config()
    music_dir = Path(cfg["music_dir"]).expanduser()
    out_path = music_dir / cfg.get("m3u_name", "playlist.m3u8")
    exts = cfg.get("extensions", [".mp3"])
    max_tracks = int(cfg.get("max_tracks", 0))
    newest_first = (cfg.get("sort", "newest_first") == "newest_first")

    n = build_m3u(music_dir, out_path, exts, max_tracks, newest_first)
    print(f"[build_m3u] wrote {out_path} with {n} tracks")

if __name__ == "__main__":
    main()
