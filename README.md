# 🤖 MEMEBOT - Desktop Character System

**Modular v3.0** | Desktop virtual character with voice, media playback, Lua scripting, and mini-games

---

## 📖 Overview

MEMEBOT is a full-featured desktop character application that displays an animated character on your screen. It plays memes, videos, GIFs, and speaks sentences using a vocabulary of voice files. The system supports encrypted `.MSK` skins, Lua-based addons, Python extensions, and includes a mini-game engine.

---

## 🎮 Features

### Desktop Character
- **Animated character** rendered on a transparent fullscreen overlay
- **Multiple skins** with legacy binary (`.MSK`) and enhanced SK3 v3.1 format support
- **8 skins included**: Default, add, dude, fire, Jake, Lets, Super, Custom Skin
- **Dance animations**: Worm (1), Moonwalk (2), Thriller (3), Robot (4), Disco (5)
- **Particle effects**: sparkles, music notes, explosions on interactions
- **Speech bubbles**: Text appears above the character when speaking

### Voice & Speech System
- **42+ word vocabulary** from individual `.wav` files
- **Sentence assembly**: Words are combined dynamically to form full sentences
- **5 sentence categories**:
  - Greetings (15 variations)
  - Random sentences (20 variations)
  - Meme reactions (10 variations)
  - Video/GIF reactions (8 variations each)
  - Idle chatter (10 variations)
- **Dedicated audio channel**: Words play sequentially without overlapping

### Media Playback
| Type | Formats | Controls |
|------|---------|----------|
| **Memes** | MP3 | Click anywhere, `M` key, auto-play |
| **Sounds** | WAV, MP3 | `S` key, right-click |
| **Videos** | MP4, AVI, MKV, MOV, WEBM | `V` key, displays in video window |
| **GIFs** | GIF | `G` key, animated overlay |

### Controls

| Key | Action |
|-----|--------|
| **Click** | Move character + play meme (or speak if auto-play OFF) |
| **Double-Click** | Voice greeting |
| **Right-Click** | Sound effect + sentence |
| **Space / X** | Toggle auto-play (ON=memes, OFF=words only) |
| **M** | Play random meme |
| **V** | Play random video |
| **G** | Play random GIF |
| **S** | Play random sound |
| **H** | Say hello |
| **T** | Speak random sentence |
| **Y** | Random idle chatter |
| **1-5** | Dance animations |
| **W** | Water Survival mini-game |
| **Ctrl+M** | Open Mod Menu |
| **Ctrl+A** | Toggle Addons |
| **Ctrl+E** | Toggle Extensions |
| **ESC** | Exit MEMEBOT |

### Auto-Play Modes
- **ON (default)**: Automatically plays memes at intervals (configurable, default 15s)
- **OFF**: Speaks random sentences every 8 seconds instead of memes

---

## 🎨 Mod Menu (Ctrl+M)

The circular mod menu provides quick access to:
- **Skin switching**: Browse and select from installed skins
- **Dance selection**: Trigger any dance animation
- **Media playback**: Play memes, videos, GIFs, and sounds
- **Voice controls**: Trigger greetings, sentences, and chatter
- **Settings**: Configure auto-play and other options

---

## 🔧 Addons & Extensions

### Lua Addons (Ctrl+A)
- Written in **Lua scripting language**
- Stored in `Addons/` folder
- Each addon has its own folder with a `main.lua` entry point
- Can access MEMEBOT API for character control, media playback, and voice

### Python Extensions (Ctrl+E)
- Written in **Python**
- Stored in `Extensions/` folder
- Full access to MEMEBOT internals
- Can extend functionality with custom modules

---

## 🎭 Skin System

### Supported Formats
1. **Legacy Binary (.MSK)**: Original encrypted skin format
2. **SK3 v3.1**: Enhanced format with verification and additional metadata

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

### Water Survival (W key)
- Dodge rising water and falling meteors
- Character must survive as long as possible
- Particle effects and animations during gameplay

### MEMEEngine (Built-in Game Creator)
- **No-code drag-and-drop** game editor
- **5 game templates**: Platformer, Endless Runner, Meme Collector, Dodge Meteor, Boss Battle
- **5 preset maps**: Grassy Hills, Spooky Cave, Meme City, Space Station, Beach Party
- **5 playable characters**: MEMEBOT, Pixel Knight, Ninja Cat, Space Blob, Robot Dude
- **Collectibles**: Coins, Gems, Stars, Meme Coins
- **Enemies**: Slimes, Skeletons, Ghosts, Robots, Meme Trolls, Boss Slimes
- **Hazards**: Meteors, Lava pits
- **Platform types**: Static, Moving, Crumbling, Sinking, Bouncy
- **Save/Load** game files as JSON

---

## 📁 File Structure
MEMEBOT/
├── app.py # Main entry point
├── run.py # MEMEEngine launcher
├── Src/
│ ├── Config/ # Configuration management
│ ├── Character-Drawing/ # Character rendering engine
│ ├── Player/ # Audio, Video, GIF players
│ ├── Audio/ # Voice manager
│ ├── Media/ # Media file management
│ ├── UI/ # Mod menu, tray controller
│ ├── Skin/ # Skin loader (.MSK format)
│ ├── Addons/ # Lua addon system
│ ├── Extensions/ # Python extension system
│ └── MEMEEngine/ # Game creation engine
│ ├── SRC/
│ │ ├── Core/ # Game assets, templates, particles
│ │ ├── Characters/ # Character presets
│ │ ├── Maps/ # Map presets (5 maps)
│ │ ├── Enemies/ # Enemy definitions
│ │ ├── Hazards/ # Hazard definitions
│ │ ├── Engine/ # Game engine + renderer
│ │ └── Editor/ # Modern UI game editor
│ └── games/ # Saved game files
├── vocabulary_voice/ # 42+ WAV voice files
├── memes/ # MP3 meme files
├── sounds/ # Sound effect files
├── videos/ # Video files
├── gifs/ # GIF files
├── MemeBotSkins/ # .MSK skin files
└── voice_lines/ # Voice line definitions

text

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.12+** (with tkinter support)
- **Windows OS** (uses Win32 API for transparency)

### Installation

```powershell
# Clone or download MEMEBOT
cd D:\MODZ4

# Install dependencies
pip install pygame pystray

# Run MEMEBOT
python app.py

# Run MEMEEngine (game creator)
cd MEMEEngine
python run.py
Required Python Packages
Package	Purpose
pygame	Audio playback, rendering
tkinter	GUI windows, canvas
pystray	System tray icon (optional)
wave	WAV file duration reading
json	Game save/load
threading	Async operations
🎵 Voice System
How It Works
MEMEBOT builds sentences by combining individual word .wav files. For example, the sentence "im ready for anything" plays:

im.Wav

ready.Wav

for.Wav

anything.wav

Each word plays sequentially on a dedicated audio channel, ensuring no overlap or cutoff.

Adding New Words
Add a .wav file to vocabulary_voice/

The filename (without extension) becomes the word

Add the word to sentence templates in app.py

🔒 Skin Encryption
Legacy .MSK: Binary encrypted format

SK3 v3.1: Enhanced format with SHA-256 verification

Skins are verified on load for integrity

⚙️ Configuration
Settings are stored in MemeBotConfig and include:

auto_play_interval: Seconds between auto meme playback (default: 15)

VOICE_PATH: Path to vocabulary voice files

Skin selection and display preferences

Media paths for memes, sounds, videos, GIFs

🛠️ Development
Creating Addons (Lua)
Create folder in Addons/YourAddon/

Add main.lua with required functions

Use Ctrl+A to toggle

Creating Extensions (Python)
Create folder in Extensions/YourExtension/

Add Python module with load/unload hooks

Use Ctrl+E to toggle

📝 License
MEMEBOT - Modular Desktop Character System
Created for entertainment and desktop customization.

🎯 Tips & Tricks
Auto-play OFF mode: Great for when you want the character to just talk

Right-click: Quick way to hear a random sentence + sound effect

Dance keys 1-5: Chain dances for fun animations

Water Survival (W): Challenging mini-game with increasing difficulty

Ctrl+M: Quick access to all features through the circular mod menu

MEMEBOT v3.0 - Your desktop companion


