# 🤖 MEMEBOT - Desktop Character System

**Modular v3.1** | Desktop virtual character with voice, media playback, Lua scripting, mini-games, standalone EXE, and legacy archive explorer

[![MediaFire](https://img.shields.io/badge/📦%20Download-MediaFire-blue?style=for-the-badge&logo=mediafire)](https://www.mediafire.com/folder/1ho6kzdpqdk92/MEMEBOT)
[![Version](https://img.shields.io/badge/version-3.1-purple?style=flat-square)](#)
[![Python](https://img.shields.io/badge/Python-3.13+-yellow?style=flat-square&logo=python)](#)
[![Platform](https://img.shields.io/badge/Platform-Windows-blue?style=flat-square&logo=windows)](#)
[![License](https://img.shields.io/badge/License-Custom-orange?style=flat-square)](#)

---

## 📖 Overview

MEMEBOT is a full-featured desktop character application that displays an animated character on your screen using a transparent fullscreen overlay. It plays memes, videos, GIFs, and speaks sentences using a vocabulary of 57+ voice files. The system supports encrypted `.MSK` skins, Lua-based addons, Python extensions, a built-in game creator (MEMEEngine), water survival mini-game, disco party mode, and now ships as a **fully standalone executable** requiring no Python installation.

---

## 🆕 What's New in v3.1

### ✨ Major Changes
- 🎯 **Standalone EXE** - MEMEBOT now builds as a single portable executable via PyInstaller
- 📦 **ARCHIVES.exe** - Legacy version explorer that opens `.tar.bz2` archives, extracts old versions, auto-installs dependencies, and runs them
- 🎨 **Extended Vocabulary** - 57+ voice words with casual slang (bro, dude, fire, space, yeah, yo, DF, DFL)
- 🕺 **Disco Party Mode** - Automatic 30-minute disco party with strobe lights, disco ball, music, and crazy dance moves
- 🔧 **Codebase Split** - Character renderer refactored into 6 modular files (~500 lines each) for maintainability
- 🗣 **Dedicated Voice Channel** - Uses `pygame.mixer.Channel(0)` to prevent word overlapping
- 📝 **Auto-Play Word Mode** - When auto-play is OFF, character speaks random sentences instead of playing memes
- ⌨ **Global Keybinds** - Launcher supports configurable keyboard shortcuts for all components
- 🎭 **Enhanced Skin System** - Full V4.0 body customization with accessories, outfits, hair styles, and more

### 🐛 Bug Fixes
- Fixed word cutoff issue - each voice word now plays completely before the next starts
- Fixed meme/voice audio conflict - dedicated channels prevent overlap
- Fixed auto-play toggle to properly switch between meme and word modes
- Fixed skin loading for legacy `.MSK` and SK3 formats
- Fixed PyInstaller bundling for Pillow, tkinter, and all dependencies

---

## 🎮 Features

### 🧑 Desktop Character
- **Animated character** rendered on a transparent fullscreen overlay
- **Multiple skins** with legacy binary (`.MSK`) and enhanced SK3 v3.1 format support
- **8+ skins included**: Default, add, dude, fire, Jake, Lets, Super, Custom Skin
- **50+ idle animations**: Shuffle, Dab, Floss, Griddy, Twerk, Air Guitar, Breakdance, and more
- **5 dance animations**: Worm (1), Moonwalk (2), Thriller (3), Robot (4), Disco (5)
- **Disco Party Mode**: Automatic 30-minute disco with lights, ball, and music
- **Water Survival (W)**: Dodge rising water and falling heart meteors
- **Particle effects**: sparkles, music notes, water drops, hearts, explosions
- **Speech bubbles**: Animated text appears above the character when speaking
- **Full body customization**: Hair, ears, outfit, tail, wings, cape, scarf, hat, mask, glasses, shoes

### 🎤 Voice & Speech System
- **57+ word vocabulary** from individual `.wav` files
- **Sentence assembly**: Words are combined dynamically to form full sentences
- **6 sentence categories**:
  - Greetings (27 variations)
  - Random sentences (55 variations)
  - Meme reactions (23 variations)
  - Video reactions (18 variations)
  - GIF reactions (16 variations)
  - Idle chatter (30 variations)
- **Dedicated audio channel**: Words play sequentially on `pygame.mixer.Channel(0)` without overlapping
- **WAV duration detection**: Uses `wave` module to read actual file duration for perfect timing

### 🎬 Media Playback
| Type | Formats | Controls |
|------|---------|----------|
| **Memes** | MP3 | Click anywhere, `M` key, auto-play |
| **Sounds** | WAV, MP3 | `S` key, right-click |
| **Videos** | MP4, AVI, MKV, MOV, WEBM | `V` key, displays in video window |
| **GIFs** | GIF | `G` key, animated overlay |

### 🎮 Controls

| Key | Action |
|-----|--------|
| **Click** | Move character + play meme (or speak if auto-play OFF) |
| **Double-Click** | Voice greeting |
| **Right-Click** | Sound effect + sentence |
| **Space / X** | Toggle auto-play (ON=memes, OFF=words only) |
| **M** | Play random meme with voice reaction |
| **V** | Play random video with voice reaction |
| **G** | Play random GIF with voice reaction |
| **S** | Play random sound effect |
| **H** | Say hello (random greeting) |
| **T** | Speak random sentence |
| **Y** | Random idle chatter |
| **1** | Worm dance |
| **2** | Moonwalk dance |
| **3** | Thriller dance |
| **4** | Robot dance |
| **5** | Disco dance |
| **W** | Water Survival mini-game |
| **Ctrl+M** | Open circular Mod Menu |
| **Ctrl+A** | Toggle Lua Addons |
| **Ctrl+E** | Toggle Python Extensions |
| **ESC** | Exit MEMEBOT |

### ⚡ Auto-Play Modes
- **ON (default)**: Automatically plays memes at configurable intervals (default 15s) with voice reactions
- **OFF**: Speaks random sentences every 8 seconds instead of memes, clicks trigger speech

---

## 🎨 Mod Menu (Ctrl+M)

The circular mod menu provides quick access to:
- 🎭 **Skin switching**: Browse and select from installed skins
- 🕺 **Dance selection**: Trigger any dance animation
- 🎬 **Media playback**: Play memes, videos, GIFs, and sounds
- 🎤 **Voice controls**: Trigger greetings, sentences, and chatter
- ⚙ **Settings**: Configure auto-play and other options

---

## 🔧 Addons & Extensions

### 📜 Lua Addons (Ctrl+A)
- Written in **Lua scripting language**
- Stored in `Addons/` folder
- Each addon has its own folder with a `main.lua` entry point
- Can access MEMEBOT API for character control, media playback, and voice
- Toggle all addons with `Ctrl+A`

### 🐍 Python Extensions (Ctrl+E)
- Written in **Python**
- Stored in `Extensions/` folder
- Full access to MEMEBOT internals
- Can extend functionality with custom modules
- Toggle all extensions with `Ctrl+E`

---

## 🎭 Skin System

### Supported Formats
1. **Legacy Binary (.MSK)**: Original encrypted skin format
2. **SK3 v3.1**: Enhanced format with SHA-256 verification and metadata

### Included Skins
| Skin | Type | Description |
|------|------|-------------|
| Default | Legacy | Original MEMEBOT character |
| add | Legacy | Alternate character style |
| dude | Legacy | Casual character |
| fire | Legacy | Fire-themed character |
| Jake | SK3 v3.1 | Enhanced character |
| Lets | SK3 v3.1 | Enhanced character |
| Super | SK3 v3.1 | Custom Skin variant |
| Custom Skin | SK3 v3.1 | User customizable |

---

## 🏊 Mini-Games

### 🌊 Water Survival (W key)
- Dodge rising water and falling heart meteors
- Character auto-floats and moves to avoid drowning
- Score tracking with death/respawn mechanics
- Particle effects and animations during gameplay

### 🕹 MEMEEngine (Built-in Game Creator)
- **No-code drag-and-drop** game editor with modern dark UI
- **5 game templates**: Platformer, Endless Runner, Meme Collector, Dodge Meteor, Boss Battle
- **5 preset maps**: Grassy Hills, Spooky Cave, Meme City, Space Station, Beach Party
- **5 playable characters**: MEMEBOT, Pixel Knight, Ninja Cat, Space Blob, Robot Dude
- **Collectibles**: Coins (+10), Gems (+25), Stars (+50), Meme Coins (+30)
- **Enemies**: Slimes, Skeletons, Ghosts, Robots, Meme Trolls, Boss Slimes
- **Hazards**: Meteors, Lava pits
- **Platform types**: Static, Moving, Crumbling, Sinking, Bouncy
- **Save/Load** game files as JSON

### 🕺 Disco Party (Automatic every 30 minutes)
- Strobe lights with color cycling
- Rotating disco ball with mirror reflections
- Animated floor tiles
- Crazy dance moves (Disco Fever, Rave, Strobe Dance)
- Music playback
- Particle explosions

---

## 📦 Standalone EXE & Downloads

All standalone executables are available on MediaFire:

### 🔗 [Download from MediaFire](https://www.mediafire.com/folder/1ho6kzdpqdk92/MEMEBOT)

### 📁 Standalone Folder Structure

The `Standalone/` folder on MediaFire contains:
Standalone/
├── 📂 New/
│ ├── MEMEBOT_v1.1.exe ✅ Current
│ ├── MEMEBOT_v1.2.exe ✅ Current
│ ├── MEMEBOT_v1.3.exe ✅ Current
│ ├── MEMEBOT_v1.4.exe ✅ Current
│ └── ...
│
├── 📂 Old/
│ ├── MEMEBOT_v1.1.exe 🗄 Archived
│ ├── MEMEBOT_v1.2.exe 🗄 Archived
│ └── ...
│
└── ARCHIVES.exe 📦 Legacy Version Explorer

text

### 🔄 Version Rotation Rules

Every 2 versions, the older of the pair gets moved to the `Old/` folder:

| New Versions | Old Versions | Pattern |
|-------------|-------------|---------|
| v1.1, v1.2 | v1.1 | After v1.2 release, v1.1 → Old |
| v1.2, v1.3, v1.4 | v1.2 | After v1.4 release, v1.2 → Old |
| v1.4, v1.5, v1.6 | v1.4 | After v1.6 release, v1.4 → Old |
| v1.5, v1.6, v1.7, v1.8 | v1.6 | After v1.8 release, v1.6 → Old |
| v1.7, v1.8, v1.9, v1.10 | v1.8 | After v1.10 release, v1.8 → Old |
| v1.9, v1.10, v1.11 | v1.9 | After v1.11 release, v1.9 → Old |
| v1.10, v1.11, v1.12 | ... | Pattern continues |

**Rule**: Keep the newest 2-3 versions in `New/`, archive older ones to `Old/` following the 2-version rotation pattern.

---

## 🗄 ARCHIVES.exe - Legacy Version Explorer

The `ARCHIVES.exe` is a standalone application that lets you explore and run older versions of MEMEBOT:

- 📦 Opens `ARCHIVE.tar.bz2` containing all legacy versions
- 📁 Browse file tree with icons for folders, Python files, ZIPs, and media
- 📤 Extract individual ZIP archives
- ▶ Run any `app.py` from archived versions
- 📥 Auto-detects and installs required Python packages (`pygame`, `Pillow`, `pystray`, etc.)
- 🖥 Real-time console output
- 📂 Open folders in Windows Explorer
- 🔧 Fully embedded Python runtime - no installation needed

---

## 📁 File Structure
MEMEBOT/
├── 📄 app.py # Main entry point
├── 📄 imports.py # Centralized imports
├── 📄 ARCHIVES.py # Legacy version explorer
├── 📄 MEMEBOT.spec # PyInstaller spec for main EXE
├── 📄 ARCHIVES.spec # PyInstaller spec for ARCHIVES EXE
├── 📄 run.py # MEMEEngine launcher
├── 📁 Src/
│ ├── 📁 Config/ # Configuration management
│ ├── 📁 Character-Drawing/ # Character rendering engine
│ │ └── 📁 2D/
│ │ ├── character_renderer_part1.py # Core class & state
│ │ ├── character_renderer_part2.py # Drawing & animation
│ │ ├── character_drawing_part1.py # Torso, legs, feet
│ │ ├── character_drawing_part2.py # Standing, arms, head
│ │ ├── character_renderer_accessories_part1.py # Bubble, tail, cape, wings, scarf
│ │ └── character_renderer_accessories_part2.py # Hats, masks, clothes, hair, ears
│ ├── 📁 Player/ # Audio, Video, GIF players
│ ├── 📁 Audio/ # Voice manager
│ ├── 📁 Media/ # Media file management
│ ├── 📁 UI/ # Mod menu, tray controller
│ ├── 📁 Skin/ # Skin loader (.MSK format)
│ ├── 📁 Addons/ # Lua addon system
│ ├── 📁 Extensions/ # Python extension system
│ ├── 📁 Animations/ # Dance move engine
│ └── 📁 vocab.py # Vocabulary & sentence builder
├── 📁 vocabulary_voice/ # 57+ WAV voice files
├── 📁 memes/ # MP3 meme files
├── 📁 sounds/ # Sound effect files
├── 📁 videos/ # Video files
├── 📁 gifs/ # GIF files
├── 📁 MemeBotSkins/ # .MSK skin files
├── 📁 voice_lines/ # Voice line definitions
├── 📁 MEMEEngine/ # Game creation engine
└── 📁 music/ # Background music files

text

---

## 🚀 Quick Start

### 📋 Prerequisites
- **Python 3.13+** (with tkinter support) - *or use the standalone EXE*
- **Windows OS** (uses Win32 API for transparency)

### 💻 Installation (Python)

```powershell
# Clone or download MEMEBOT
cd D:\MODZ4

# Install dependencies
pip install pygame pystray Pillow

# Run MEMEBOT
python app.py

# Run MEMEEngine (game creator)
cd MEMEEngine
python run.py
🎯 Standalone EXE (No Python Required)
powershell
# Download from MediaFire
# https://www.mediafire.com/folder/1ho6kzdpqdk92/MEMEBOT

# Navigate to Standalone/New/
# Double-click MEMEBOT_vX.X.exe

# For legacy versions, run ARCHIVES.exe
📦 Required Python Packages
Package	Purpose
pygame	Audio playback, rendering, mixer channels
tkinter	GUI windows, canvas, dialogs
Pillow	Image processing, character drawing
pystray	System tray icon (optional)
wave	WAV file duration reading
json	Game save/load, configuration
threading	Async operations, background tasks
🎵 Voice System
🗣 How It Works
MEMEBOT builds sentences by combining individual word .wav files. For example, the sentence "im ready for anything" plays:

im.Wav → waits for completion

ready.Wav → waits for completion

for.Wav → waits for completion

anything.wav → waits for completion

Each word plays sequentially on pygame.mixer.Channel(0), a dedicated voice channel. The system reads the actual WAV file duration using the wave module and waits for channel.get_busy() to return False before playing the next word.

➕ Adding New Words
Add a .wav file to vocabulary_voice/

The filename (without extension) becomes the word

Add the word to sentence templates in Src/vocab.py

📚 Current Vocabulary (57 words)
a, anything, back, beautiful, been, bonjour, bro, crackin, day, DF, DFL, dude, fire, for, french, friend, fun, going, good, greetings, happy, hello, hey, heya, hi, hows, human, im, ive, looking, me, memebot, or, ready, see, so, some, space, thats, the, there, to, today, waiting, watch, welcome, well, what, whats, whatsup, yeah, yo, you, youre

🔒 Skin Encryption
Legacy .MSK: Binary encrypted format

SK3 v3.1: Enhanced format with SHA-256 verification

Skins are verified on load for integrity

Supports custom sprite data, animation frames, and full body customization

⚙️ Configuration
Settings are stored in MemeBotConfig and include:

auto_play_interval: Seconds between auto meme playback (default: 15)

VOICE_PATH: Path to vocabulary voice files

Skin selection and display preferences

Media paths for memes, sounds, videos, GIFs

Start position, walk speed, run speed, auto-walk settings

🛠️ Development
📜 Creating Addons (Lua)
Create folder in Addons/YourAddon/

Add main.lua with required functions

Use Ctrl+A to toggle

🐍 Creating Extensions (Python)
Create folder in Extensions/YourExtension/

Add Python module with load/unload hooks

Use Ctrl+E to toggle

🔨 Building the EXE
powershell
# Main MEMEBOT EXE
cd D:\MODZ4
pyinstaller MEMEBOT.spec --clean --noconfirm

# ARCHIVES Explorer EXE
pyinstaller ARCHIVES.spec --clean --noconfirm
📝 Changelog
Version	Date	Changes
v3.1	2026-07-05	Standalone EXE, ARCHIVES explorer, 57+ words, disco party, codebase split, dedicated voice channel, auto-play word mode, global keybinds, PyInstaller fixes
v3.0	2026-06-27	Modular addons/extensions, Lua scripting, Python extensions, circular mod menu, water survival mini-game, SK3 skin format, 42+ voice words, auto-play toggle
v2.0	2026-06-01	MEMEEngine game creator, skin loader, video/GIF player, particle effects, dance animations
v1.0	2026-05-01	Initial release, desktop character, meme playback, voice system, basic animations
Changelog file: CHANGELOG.md

🎯 Tips & Tricks
🎤 Auto-play OFF mode: Great for when you want the character to just talk

🖱 Right-click: Quick way to hear a random sentence + sound effect

💃 Dance keys 1-5: Chain dances for fun animations

🌊 Water Survival (W): Challenging mini-game with increasing difficulty

🎨 Ctrl+M: Quick access to all features through the circular mod menu

🕺 Wait 30 minutes: Disco party starts automatically!

📦 ARCHIVES.exe: Explore and run old versions without installing anything

🔊 Voice files: Replace any .wav in vocabulary_voice/ with your own voice

📄 License
MEMEBOT - Modular Desktop Character System
Created for entertainment and desktop customization.

🔗 Links
📦 Downloads: MediaFire Folder

📂 Standalone EXEs: Standalone/New/ and Standalone/Old/

🗄 Legacy Explorer: Standalone/ARCHIVES.exe

✨ MEMEBOT v3.1 - Your desktop companion, now standalone! ✨
