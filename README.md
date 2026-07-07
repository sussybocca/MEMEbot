# 🤖 MEMEBOT - Desktop Character System

**Modular v4.0** | Desktop virtual character with voice, media playback, Lua scripting, mini‑games, standalone EXE, marketplace, and full body customization

![Version](https://img.shields.io/badge/version-4.0-purple?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.13+-yellow?style=flat-square&logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows-blue?style=flat-square&logo=windows)
![License](https://img.shields.io/badge/License-Custom-orange?style=flat-square)

---

> **⚠️ IMPORTANT: Support for this repository and MediaFire has been dropped.**  
> The new platform contains the **full source code**, **latest EXE builds**, **organised content**, and **much more**.  
> All future development happens there.

---

## 📖 Overview

MEMEBOT is a full‑featured desktop character application that displays an animated character on your screen using a transparent fullscreen overlay. It plays memes, videos, GIFs, and speaks sentences using a vocabulary of 57+ voice files. The system supports encrypted `.MSK` skins, Lua‑based addons, Python extensions, a built‑in game creator (MEMEEngine), a water‑survival mini‑game, a disco party mode, and now ships as a **fully standalone executable** requiring no Python installation.

The application is built with a modular architecture, making it easy to extend and customise. It includes a built‑in marketplace for community‑created content, a 3D racing minigame, pet mode, holiday themes, screen saver, multi‑character mode, and much more. This is the ultimate desktop companion for meme lovers and customisation enthusiasts.

---

## 🌐 Platform Servers

The new MEMEBOT ecosystem runs on **three interconnected servers**:

| Server | URL | Purpose |
|--------|-----|---------|
| **Main / Marketplace** | [https://packarcade.win/](https://packarcade.win/) | Community content marketplace – download skins, addons, voice packs, DLC, etc. |
| **Source & Builds** | [http://main.packarcade.win/](http://main.packarcade.win/) | Full source code, EXE builds, fun games, and all resources. |
| **Web Demo** | [https://memebot.packarcade.win/](https://memebot.packarcade.win/) | Browser‑based test demo of MEMEBOT (skins are display‑only, lower FPS, limited features). |

> **The EXE version is the full experience** – better performance, all features working, and full body customisation. The web version is just a demonstration.

---

## 🆕 What's New in v4.0

### ✨ Major Changes
- 🏪 **MEMEBOT Marketplace** – Browse and download community content directly from inside the app (`Ctrl+Shift+M`). The marketplace connects to the public HTTP API via a local WebSocket bridge, allowing seamless downloads of skins, addons, voice packs, meme packs, and DLC.
- 🎮 **3D Racing Minigame** – Full Node.js + Three.js racing game with MPOINTS, time limits, leveling, and high‑score tracking (`Ctrl+R`). The game runs in your default browser and communicates with the EXE to save progress.
- 🐾 **Pet Mode** – Character follows your cursor like a desktop pet (`Ctrl+P`). Includes states like following, playing, sleeping, curious, and excited, with energy/happiness/hunger stats.
- 🎭 **Holiday Themes** – Auto‑switches outfits for holidays like Christmas, Halloween, Valentine's, St. Patrick's, Easter, New Year's, and even a birthday mode (`Ctrl+H`). Each holiday has custom colors, accessories, and greetings.
- 🖥️ **Screen Saver Mode** – Custom animated screensaver with MEMEBOT characters, floating memes, bouncing bots, and multiple themes (space, underwater, disco, matrix, stars, bubbles) (`Ctrl+S`).
- 👥 **Multi‑Character Mode** – Spawn multiple bots that interact, dance together, and talk (`Ctrl+N`, `Ctrl+B` to add/remove bots). Bots have personalities, wander, start conversations, and can group‑dance.
- 🔒 **Enhanced SK3 Skin Encryption** – AES‑256‑GCM + block‑character encoding with SHA‑256 integrity checks. This provides both confidentiality and tamper‑detection for skin files.
- 📦 **Package Manager** – Handles downloading, installing, and auto‑zipping of marketplace content. Content is stored in an external `CONTENT` folder next to the EXE, with PIN‑protected vaults for auto‑zipped items.
- 🔗 **Local Bridge Server** – WebSocket bridge that connects the EXE to the public HTTP marketplace API. This allows the EXE to fetch catalogs and download content without exposing sensitive APIs.
- 🧩 **Content Verifier** – Verifies downloaded skins, addons, extensions, voice packs, and DLC for integrity and compatibility.
- 🗣️ **Dedicated Voice Channel** – Uses `pygame.mixer.Channel(0)` to prevent overlapping words and ensures each voice file plays completely.
- 🕺 **Disco Party** – Automatic 30‑minute disco party with strobe lights, disco ball, and crazy dance moves, triggered every 30 minutes of idle time.
- 🎯 **Standalone EXE** – Single portable executable built with PyInstaller, bundling all dependencies including Python runtime, pygame, Pillow, and more.

### 🐛 Bug Fixes
- Fixed word cutoff – each voice word plays completely before the next starts.
- Fixed meme/voice audio conflict – dedicated channels prevent overlap.
- Fixed auto‑play toggle to properly switch between meme and word modes.
- Fixed skin loading for legacy `.MSK` and SK3 formats.
- Fixed PyInstaller bundling for Pillow, tkinter, and all dependencies.
- Fixed memory leaks in video/GIF playback.
- Fixed particle system performance issues.

---

## 🎮 Features

### 🧑 Desktop Character
- **Animated character** on a transparent fullscreen overlay using tkinter canvas.
- **Multiple skins** with legacy binary (`.MSK`) and enhanced SK3 v4.0 format.
- **8+ skins included**: Default, add, dude, fire, Jake, Lets, Super, Custom Skin.
- **50+ idle animations**: Shuffle, Dab, Floss, Griddy, Twerk, Air Guitar, Breakdance, and more.
- **5 dance animations**: Worm, Moonwalk, Thriller, Robot, Disco (triggered by keys 1‑5).
- **Disco Party Mode** – automatic 30‑minute disco with lights, ball, and music.
- **Water Survival (W)** – dodge rising water and falling heart meteors.
- **Particle effects** – sparkles, music notes, water drops, hearts, explosions.
- **Speech bubbles** – animated text appears above the character when speaking.
- **Full body customisation** – hair, ears, outfit, tail, wings, cape, scarf, hat, mask, glasses, shoes, and more, all defined in the skin file.
- **Custom Lua scripts** per skin for dynamic behavior (on load, frame, dance, meme, speak, draw, particles).

### 🎤 Voice & Speech System
- **57+ word vocabulary** from individual `.wav` files stored in `vocabulary_voice/`.
- **Sentence assembly** – words are combined dynamically to form full sentences.
- **6 sentence categories**:
  - Greetings (27 variations)
  - Random sentences (55 variations)
  - Meme reactions (23 variations)
  - Video reactions (18 variations)
  - GIF reactions (16 variations)
  - Idle chatter (30 variations)
- **Dedicated audio channel** – words play sequentially on `pygame.mixer.Channel(0)` without overlapping.
- **WAV duration detection** – uses `wave` module to read actual file duration for perfect timing and waits for channel to become free.
- **Auto‑play modes**: When auto‑play is ON, the character plays random memes at intervals; when OFF, it speaks random sentences instead.

### 🎬 Media Playback
| Type | Formats | Controls |
|------|---------|----------|
| **Memes** | MP3, WAV | Click anywhere, `M` key, auto‑play |
| **Sounds** | WAV, MP3 | `S` key, right‑click |
| **Videos** | MP4, AVI, MKV, MOV, WEBM | `V` key, displays in a separate video window |
| **GIFs** | GIF | `G` key, animated overlay on the canvas |

The media manager automatically selects random files from the respective folders (`memes/`, `sounds/`, `videos/`, `gifs/`). Video playback uses ffplay (bundled) or a fallback window.

### 🛠️ Mod Menu (Ctrl+M)
The circular mod menu is a radial interface that provides quick access to:
- 🎭 **Skin switching** – browse and select installed skins.
- 🕺 **Dance selection** – trigger any dance animation.
- 🎬 **Media playback** – play memes, videos, GIFs, sounds.
- 🎤 **Voice controls** – greetings, sentences, chatter.
- ⚙ **Settings** – volume, auto‑play, etc.
- 🎨 **Skin creation** – integrated skin editor (Drawer) for creating custom skins with layers and animation frames.

### 🔧 Addons & Extensions

#### 📜 Lua Addons (Ctrl+A)
- Written in **Lua** using the `lupa` library (Lua-Python bridge).
- Stored in `Addons/` folder (or external `CONTENT/Addons/`).
- Each addon has its own folder with a `main.lua` entry point.
- Can access MEMEBOT API for character control, media playback, voice, and more.
- Toggle all addons with `Ctrl+A`. Active addons are loaded/unloaded dynamically.

#### 🐍 Python Extensions (Ctrl+E)
- Written in **Python**.
- Stored in `Extensions/` folder (or external `CONTENT/Extensions/`).
- Each extension is a Python module with `load()` and `unload()` functions.
- Full access to MEMEBOT internals – can extend functionality, add new commands, etc.
- Toggle all extensions with `Ctrl+E`.

### 🎭 Skin System

#### Supported Formats
1. **Legacy Binary (.MSK)** – original encrypted skin format using Fernet.
2. **SK3 v4.0** – enhanced format with AES‑256‑GCM, block‑character encoding (Unicode block chars), and SHA‑256 integrity checks. The encryption is multi‑layer: PBKDF2 key derivation, AES‑256‑GCM for authenticated encryption, then block‑character encoding for obfuscation.

#### Skin Structure
A skin file (`.msk`) contains a JSON dictionary with the following sections:
- `name`, `version`, `author`, `description`
- `body_scale`: height, width, head size, limb length
- `body_shape`: type, torso width/height, belly size, shoulder/hip width, custom points
- `limbs`: arm/leg style, length, width, hand/foot style
- `head`: shape, size, face position, ear style and size
- `hair`: style, length, volume, bangs, custom points
- `outfit`: type, primary/secondary colors, custom shapes
- `colors`: all body part colors (body, skin, hair, eyes, mouth, etc.)
- `clothing`: hat, shirt, pants, shoes, cape, wings, scarf, mask, glasses
- `accessories`: tail type, custom accessories
- `animations`: speed multipliers, custom animation frames
- `particles`: sparkle/music/heart colors, custom particles
- `sprite_data`: base64‑encoded layers (body, head, hair, etc.) for the skin preview
- `animation_frames`: frame‑by‑frame animation data for each state (idle, walking, dancing, etc.)
- `lua_script`: embedded Lua script for skin behavior

#### Included Skins
| Skin | Type | Description |
|------|------|-------------|
| Default | Legacy | Original MEMEBOT character |
| add | Legacy | Alternate character style |
| dude | Legacy | Casual character |
| fire | Legacy | Fire‑themed character |
| Jake | SK3 v4.0 | Enhanced character |
| Lets | SK3 v4.0 | Enhanced character |
| Super | SK3 v4.0 | Custom Skin variant |
| Custom Skin | SK3 v4.0 | User customizable |

### 🏊 Mini‑Games

#### 🌊 Water Survival (W key)
- Dodge rising water and falling heart meteors.
- Character auto‑floats and moves to avoid drowning.
- Score tracking with death/respawn mechanics.
- Particle effects and animations during gameplay.

#### 🕹 MEMEEngine (Built‑in Game Creator)
- **No‑code drag‑and‑drop** game editor with modern dark UI.
- **5 game templates**: Platformer, Endless Runner, Meme Collector, Dodge Meteor, Boss Battle.
- **5 preset maps**: Grassy Hills, Spooky Cave, Meme City, Space Station, Beach Party.
- **5 playable characters**: MEMEBOT, Pixel Knight, Ninja Cat, Space Blob, Robot Dude.
- **Collectibles**: Coins (+10), Gems (+25), Stars (+50), Meme Coins (+30).
- **Enemies**: Slimes, Skeletons, Ghosts, Robots, Meme Trolls, Boss Slimes.
- **Hazards**: Meteors, Lava pits.
- **Platform types**: Static, Moving, Crumbling, Sinking, Bouncy.
- **Save/Load** game files as JSON.

#### 🕺 Disco Party (Automatic every 30 minutes)
- Strobe lights with colour cycling.
- Rotating disco ball with mirror reflections.
- Animated floor tiles.
- Crazy dance moves (Disco Fever, Rave, Strobe Dance).
- Music playback from `music/` folder.
- Particle explosions and confetti.

#### 🏎️ Racing Minigame (Ctrl+R)
- Full 3D racing game using Node.js + Three.js.
- Earn MPOINTS by beating time limits.
- Level up and track progress.
- Launches in your default browser.
- Requires Node.js installed (auto‑detected) and the `racing_server/` folder with server.js, index.html, game.js, style.css.

### 🐾 Pet Mode (Ctrl+P)
- Character follows your cursor like a desktop pet.
- States: idle, following, playing, sleeping, excited, curious.
- Energy, happiness, hunger stats that affect behavior.
- Click to pet (increases happiness), double‑click to feed (decreases hunger).
- Reacts to mouse movement and clicks.
- Tail wagging, bouncing, and custom animations.

### 🎭 Holiday Themes (Ctrl+H)
- Auto‑switches outfits for holidays.
- Built‑in holidays: New Year's, Valentine's, St. Patrick's, Easter, Halloween, Christmas, Birthday.
- Each holiday has custom colors, accessories, and greetings.
- Can be manually cycled with `Ctrl+H`.

### 🖥️ Screen Saver Mode (Ctrl+S)
- Activates after 2 minutes of idle time (or manually with `Ctrl+S`).
- Full‑screen animated screensaver with MEMEBOT character, floating memes, bouncing bots, and stars.
- Themes: space, underwater, disco, matrix, stars, bubbles (auto‑cycles every 5 minutes).
- Move mouse or press any key to deactivate.

### 👥 Multi‑Character Mode (Ctrl+N)
- Spawn multiple MEMEBOT bots on screen.
- Bots have personalities (names, colours, speed, talkative/dance lover).
- Bots wander, interact with each other (conversations, group dances), and interact with the main character.
- Add/remove bots with `Ctrl+B` and `Ctrl+Shift+B`.
- Group activities like dance parties and conversations happen automatically.

### 🛒 Marketplace (Ctrl+Shift+M)
- Browse community content: skins, addons, extensions, voice packs, meme packs, sound packs, DLC.
- Download and install directly into the `CONTENT/` folder.
- Automatic verification of downloaded files.
- Installed content is tracked and can be uninstalled.
- Auto‑zip feature: after 5 minutes of inactivity, installed content is zipped with a PIN to save space.

---

## ⌨️ Controls

| Key | Action |
|-----|--------|
| **Click** | Move character + play meme (or speak if auto‑play OFF) |
| **Double‑Click** | Voice greeting |
| **Right‑Click** | Sound effect + sentence |
| **Space / X** | Toggle auto‑play (ON=memes, OFF=words only) |
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
| **W** | Water Survival mini‑game |
| **Ctrl+M** | Open circular Mod Menu |
| **Ctrl+A** | Toggle Lua Addons |
| **Ctrl+E** | Toggle Python Extensions |
| **Ctrl+P** | Toggle Pet Mode |
| **Ctrl+H** | Cycle Holiday Theme |
| **Ctrl+S** | Activate Screen Saver |
| **Ctrl+N** | Toggle Multi‑Character Mode |
| **Ctrl+B** | Add Bot |
| **Ctrl+Shift+B** | Remove Bot |
| **Ctrl+R** | Racing Minigame |
| **Ctrl+Shift+M** | Open Marketplace |
| **ESC** | Exit MEMEBOT |

---

## 🧱 Architecture & Codebase Organization

MEMEBOT follows a modular architecture with clear separation of concerns. The code is split into several core modules, each responsible for a specific aspect of the application. Below is the detailed folder structure with explanations.

### 📁 File Structure (Full Graph)
MEMEBOT/
├── 📄 app.py # Main entry point – initializes the application and runs the main loop
├── 📄 imports.py # Centralised imports – loads all modules dynamically
├── 📄 ARCHIVES.py # Legacy version explorer – opens .tar.bz2 archives and runs old versions
├── 📄 MEMEBOT.spec # PyInstaller spec for building the main EXE
├── 📄 ARCHIVES.spec # PyInstaller spec for building the ARCHIVES EXE
├── 📄 run.py # MEMEEngine launcher – starts the game creator
├── 📁 SRC/ # Core source code
│ ├── 📁 Config/
│ │ └── config.py # MemeBotConfig – manages settings, paths, and persistence
│ ├── 📁 Character-Drawing/
│ │ └── 📁 2D/
│ │ ├── character_renderer_part1.py # Main CharacterRenderer class, state, particles, disco, water survival
│ │ ├── character_renderer_part2.py # Extends CharacterRenderer with idle bonuses, MSK sprites, drawing methods
│ │ ├── character_drawing_part1.py # Drawing functions: torso, legs, feet
│ │ ├── character_drawing_part2.py # Drawing functions: standing/laying character, arms, hands, head, eyes, nose, mouth, ears
│ │ ├── character_renderer_accessories_part1.py # Accessories: speech bubble, tail, cape, wings, scarf, outfit details
│ │ └── character_renderer_accessories_part2.py # Accessories: hats, masks, glasses, shirts, pants, shoes, hair styles, ear styles
│ ├── 📁 Player/
│ │ ├── 📁 AudioPlayer/
│ │ │ └── audio_player.py # AudioPlayer – plays sounds, memes, music using pygame.mixer
│ │ ├── 📁 VideoPlayer/
│ │ │ └── video_player.py # VideoPlayerWindow – displays videos in a separate window using ffplay
│ │ └── 📁 GifPlayer/
│ │ └── gif_player.py # GifPlayer – plays animated GIFs on the canvas
│ ├── 📁 Audio/
│ │ └── voice_manager.py # VoiceManager – loads and plays voice files (.wav) from vocabulary_voice/
│ ├── 📁 Media/
│ │ └── media_manager.py # MediaManager – manages selection and playback of memes, sounds, videos, GIFs
│ ├── 📁 UI/
│ │ ├── mod_menu_part1.py # Circular mod menu – UI rendering, navigation, core logic
│ │ ├── mod_menu_part2.py # Mod menu – action handlers, skin editor, Lua, preview, apply functions
│ │ └── tray_controller.py # System tray icon (optional, uses pystray)
│ ├── 📁 Skin/
│ │ ├── skin_loader.py # SkinLoader – loads and manages .MSK skins
│ │ └── skin_encryptor.py # SkinEncryptor – encryption/decryption of SK3 skins with AES‑256‑GCM and block encoding
│ ├── 📁 Addons/
│ │ └── addon_manager.py # AddonManager – loads/unloads Lua addons and Python extensions
│ ├── 📁 Animations/
│ │ └── DanceMoves/
│ │ └── dance_engine.py # DanceEngine – computes dance parameters for character animation
│ ├── 📁 vocab.py # Vocabulary – builds sentence templates from available voice words
│ ├── 📁 connection.py # ConnectionManager + LocalBridgeServer – WebSocket bridge to marketplace API
│ ├── 📁 content_verifier.py # ContentVerifier – validates downloaded content (skins, addons, extensions, voice packs, DLC)
│ ├── 📁 package_manager.py # PackageManager – downloads, installs, uninstalls, and auto-zips marketplace content
│ ├── 📁 marketplace.py # Marketplace – UI for browsing and downloading community content
│ ├── 📁 pet_mode.py # PetMode – desktop pet behavior (follows cursor)
│ ├── 📁 holiday_themes.py # HolidayThemes – auto‑switches outfits for holidays
│ ├── 📁 screen_saver.py # ScreenSaverMode – custom animated screensaver
│ ├── 📁 multi_character.py # MultiCharacterMode – spawns multiple interacting bots
│ └── 📁 racing_game.py # RacingGame – launches the 3D racing minigame (Node.js + Three.js)
├── 📁 vocabulary_voice/ # Contains 57+ WAV voice files (e.g., hello.wav, im.wav, ready.wav)
├── 📁 memes/ # MP3 meme files
├── 📁 sounds/ # Sound effect files (WAV, MP3)
├── 📁 videos/ # Video files (MP4, AVI, MKV, MOV, WEBM)
├── 📁 gifs/ # GIF files
├── 📁 MemeBotSkins/ # Default location for .MSK skin files
├── 📁 voice_lines/ # Voice line definitions (if any)
├── 📁 MEMEEngine/ # Game creation engine – contains run.py and game editor files
├── 📁 music/ # Background music files for disco party and other features
├── 📁 Addons/ # Lua addons (external, can be symlinked to CONTENT/Addons)
├── 📁 Extensions/ # Python extensions (external, can be symlinked to CONTENT/Extensions)
├── 📁 CONTENT/ # External content folder (managed by PackageManager)
│ ├── MemeBotSkins/ # Downloaded skins
│ ├── Addons/ # Downloaded addons
│ ├── Extensions/ # Downloaded extensions
│ ├── vocabulary_voice/ # Downloaded voice packs
│ ├── memes/ # Downloaded meme packs
│ ├── sounds/ # Downloaded sound packs
│ ├── DLC/ # Downloaded DLC packages
│ └── .vault/ # Zipped, PIN‑protected content (auto‑zipped after inactivity)
├── 📁 racing_server/ # Node.js + Three.js racing game files
│ ├── server.js # Node.js server
│ ├── index.html # Main HTML page
│ ├── game.js # Three.js game logic
│ └── style.css # CSS styling for the game
└── 📁 .memebot_id # Unique EXE identifier (generated on first run)

text

---

## 🚀 Quick Start

### 📋 Prerequisites
- **Python 3.13+** (with tkinter support) – *or use the standalone EXE*.
- **Windows OS** (uses Win32 API for transparency, but may work on Linux with X11).
- **Optional**: Node.js (for the racing minigame), ffmpeg/ffplay (for video playback).

### 💻 Installation (from source)
```powershell
# Clone or download MEMEBOT from the new platform
cd MEMEBOT

# Install dependencies (use the provided requirements.txt or install manually)
pip install pygame pystray Pillow cryptography lupa websockets

# Run MEMEBOT
python app.py

# Run MEMEEngine (game creator)
cd MEMEEngine
python run.py
🎯 Standalone EXE (No Python required)
Download the latest EXE from http://main.packarcade.win/.

Double‑click MEMEBOT_v4.0.exe.

For legacy versions, run ARCHIVES.exe to explore and run older builds.

⚙️ Configuration
All settings are stored in MemeBotConfig and saved automatically. You can modify settings via the Mod Menu or directly in the config.json file (located in the user's AppData or alongside the EXE).

Key settings:

auto_play_interval: seconds between auto‑play memes (default 15)

volume: master volume (0.0 – 1.0)

walk_speed, run_speed: character movement speeds

auto_walk: enable/disable random wandering

start_x, start_y: initial character position

voice_path, skins_path, memes_path, etc.: paths to media folders

🛠️ Development
📜 Creating Lua Addons
Create a folder in Addons/ with your addon name.

Inside, create a main.lua file.

Implement functions like onLoad(), onUnload(), onFrame(frame), etc.

Use the memebot global object to interact with the character.

Press Ctrl+A to toggle addons.

Example main.lua:

lua
function onLoad()
    memebot.log("Addon loaded!")
    memebot.setEmotion("happy")
end

function onFrame(frame)
    if frame % 60 == 0 then
        memebot.say("Hello from Lua!")
    end
end
🐍 Creating Python Extensions
Create a folder in Extensions/ with your extension name.

Inside, create a Python module (e.g., main.py).

Implement load() and unload() functions.

Access the app global to interact with MEMEBOT.

Press Ctrl+E to toggle extensions.

Example main.py:

python
def load(app):
    app.character.say("Extension loaded!")
    app.character.add_particle(240, 300, "sparkle", 10)

def unload(app):
    app.character.say("Extension unloaded!")
🎨 Creating Custom Skins
Use the built‑in Drawer tool (accessible from the Mod Menu) to create custom skins. You can draw on layers, add animation frames, and save as .MSK files. The Drawer uses a command‑based system or classic tools for pixel‑by‑pixel editing.

📦 Standalone EXE & Downloads
All standalone executables are now hosted on the new platform – not on MediaFire.

Main EXE: MEMEBOT_v4.0.exe – the full desktop application.

ARCHIVES.exe – legacy version explorer that can open .tar.bz2 archives, extract old versions, auto‑install dependencies, and run them.

Download from the new platform: http://main.packarcade.win/

🔄 Version Rotation Rules (for the archive explorer)
The latest 2‑3 versions are kept in the New/ folder.

Older versions are moved to Old/ following a 2‑version rotation pattern.

🔨 Building the EXE
powershell
# Main MEMEBOT EXE
pyinstaller MEMEBOT.spec --clean --noconfirm

# ARCHIVES Explorer EXE
pyinstaller ARCHIVES.spec --clean --noconfirm
Ensure you have PyInstaller installed and all dependencies available. The spec files handle the inclusion of all necessary modules and data files.

📝 Changelog
Version	Date	Highlights
v4.0	2026‑07‑07	Marketplace, 3D Racing, Pet Mode, Holiday Themes, Screen Saver, Multi‑Character, PKGB manager, SK3 encryption, three‑server platform
v3.1	2026‑07‑05	Standalone EXE, ARCHIVES explorer, 57+ words, disco party, codebase split, dedicated voice channel, auto‑play word mode
v3.0	2026‑06‑27	Modular addons/extensions, Lua scripting, Python extensions, circular mod menu, water survival, SK3 skin format
v2.0	2026‑06‑01	MEMEEngine, skin loader, video/GIF player, particle effects, dance animations
v1.0	2026‑05‑01	Initial release – desktop character, meme playback, voice system, basic animations
🤝 Contributing
While this repository is no longer actively maintained, you are welcome to fork and modify the code for personal use. For official contributions, please refer to the new platform's contribution guidelines.

📄 License
MEMEBOT – Modular Desktop Character System
Created for entertainment and desktop customisation.
All rights reserved. Redistribution or commercial use is prohibited without explicit permission.

🔗 Links
🌐 Main Server (Marketplace): https://packarcade.win/

💻 Source & Builds: http://main.packarcade.win/

🌍 Web Demo: https://memebot.packarcade.win/

✨ MEMEBOT v4.0 – Your desktop companion, now with a marketplace and racing! ✨
