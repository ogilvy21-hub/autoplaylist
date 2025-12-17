
-- Suno -> Apple Music playlist sync (macOS)
-- Reads config.json in the repo root.
-- Imports audio files from the configured folder into Music and adds them to a playlist.

on readFile(posixPath)
	set f to POSIX file posixPath as alias
	set fh to open for access f
	set txt to read fh as «class utf8»
	close access fh
	return txt
end readFile

on jsonValue(jsonText, keyName)
	-- Minimal JSON getter for simple config.json (string values only)
	set AppleScript's text item delimiters to "\"" & keyName & "\""
	set parts to text items of jsonText
	if (count of parts) < 2 then return missing value
	set AppleScript's text item delimiters to ":"
	set tailPart to item 2 of parts
	set kvParts to text items of tailPart
	if (count of kvParts) < 2 then return missing value
	set AppleScript's text item delimiters to "\""
	set afterColon to item 2 of kvParts
	set strParts to text items of afterColon
	if (count of strParts) < 2 then return missing value
	return item 2 of strParts
end jsonValue

set repoRoot to (POSIX path of (path to me)) & "/../"
set cfgText to readFile(repoRoot & "config.json")
set musicDir to jsonValue(cfgText, "music_dir")
set playlistName to jsonValue(cfgText, "playlist_name")

if musicDir is missing value then error "music_dir not found in config.json"
if playlistName is missing value then set playlistName to "Suno Daily"

tell application "Music"
	activate

	-- Ensure playlist exists
	if not (exists playlist playlistName) then
		set targetPlaylist to make new playlist with properties {name:playlistName}
	else
		set targetPlaylist to playlist playlistName
	end if

	-- Get files
	set audioFolder to POSIX file musicDir as alias
	tell application "System Events"
		set audioFiles to files of folder audioFolder whose name extension is "mp3" or name extension is "m4a" or name extension is "wav"
	end tell

	repeat with f in audioFiles
		try
			-- 'add' imports into library; returns a track (or list of tracks)
			set addedTrack to add (f as alias) to library
			try
				duplicate addedTrack to targetPlaylist
			end try
		end try
	end repeat
end tell

return "Done"
