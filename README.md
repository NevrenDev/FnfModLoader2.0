# FnfModLoader2.0
version 2.0 and up of Fnf Mod Loader
## Overview
Open-source mod loader for Friday Night Funkin game

You can customize the look by selecting a theme (currently there are only 2), you can download and use different image for background
In the settings you can change the language (available languages are for now English and Polish, but write to me if you want other languages) and you can change the icon to legacy one (from ver 1) or keep it a default (new one)

Later I'll add mod browser (in-app web browser for gamebanana/gamejolt) maybe in full release (2.0) or 2.1
In maybe 2.1 or 2.2 I'll add the support for other engines for now you have to stick to PsychEngine

## Screenshots
### Mod list
![obraz](https://github.com/user-attachments/assets/68f56734-9f89-4d6f-8c58-c977cb885ca2)
### Settings
![obraz](https://github.com/user-attachments/assets/692e222d-59ab-4bdc-a4cd-175789e93d47)
### Mod tab (mod with exe)
![obraz](https://github.com/user-attachments/assets/475b4980-4f70-4dfc-88b5-31bd6da30789)
### Mod tab (mod without exe)
![obraz](https://github.com/user-attachments/assets/1d811e08-5fd4-41f3-b900-5cd0a20191dd)

## Source Code guide
In order to use the source code you'll need to download PyQt6 and use at least Python3.12.2 (started on 3.12.2 later moved to 3.12.6
After downloading the source code read the note at the beginning of the file
You'll also need to download PsychEngine in order to run non-exe mods

## Install guide
1. Download latest version
2. Unpack it anywhere you want
3. Put PsychEngine in the 'engine' folder which should be located inside Mod Loader folder
4. Open the exe file
5. Play


## Mod installation guide
1. Download fnf mod from gamebanana or gamejolt
2. Unpack it and put it into 'mods' folder (now it doesn't have to be mods/mod-folder/mod-files it can be mods/folder/mod-folder/mod-files)
3. Open or reload the Mod Loader
4. Double click the mod on the list
5. Run it
6. If it crashes create an issue and provide the mod. If it pops an error popup then you don't have PsychEngine correctly placed (only if the popup title is "Engine error" if it's different make an issue and provide useful information)
