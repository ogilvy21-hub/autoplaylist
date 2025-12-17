# Suno (semi-manual) -> Local Playlist Automation (Option A + B1/B2)

This repo is designed for:
- **A (Suno side):** You create songs in Suno manually (fast routine). Download MP3s into a folder.
- **B1 (Local):** Automatically build/update an `.m3u8` playlist file from that folder.
- **B2 (Optional, macOS):** Import new MP3s into Apple Music and keep a playlist updated.

> No third-party Suno API, no browser automation.

## 0) Requirements
- macOS recommended (B2 uses Apple Music app scripting)
- Python 3.10+ (works with system python on many Macs, but Python.org install is fine)

## 1) Configure
Edit `config.json`:
- `music_dir`: where Suno downloads go (example: `~/Downloads/Suno`)
- `playlist_name`: name for the Apple Music playlist (B2)
- `m3u_name`: output playlist file name (B1)

## 2) Run B1 (build/update m3u8 playlist)
```bash
python3 scripts/build_m3u.py
```

## 3) Run B1 (watch mode: auto-update when new mp3 appears)
```bash
python3 scripts/watch_m3u.py
```

## 4) Run B2 (Apple Music import + playlist sync)
```bash
osascript scripts/music_sync.applescript
```

## 5) (Optional) Auto-run at login (macOS LaunchAgent)
Edit `launchd/com.example.suno-watch.plist` paths, then:
```bash
mkdir -p ~/Library/LaunchAgents
cp launchd/com.example.suno-watch.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.example.suno-watch.plist
```

To unload:
```bash
launchctl unload ~/Library/LaunchAgents/com.example.suno-watch.plist
```

## Notes
- `watch_m3u.py` uses a lightweight polling approach (no extra dependencies).
- `music_sync.applescript` may trigger macOS privacy prompts (Automation permission for Music).
