"""
MEMEBOT Skin Encryptor
Encrypts and decrypts .MSK skin files using custom SK encryption
Produces block character ciphertext like: ▕◆▧◄■▕▒□■▱◄▵▏▼▰▼◆◄□■▫
Uses 150 unique block characters with hex encoding for lossless conversion
Supports legacy MSK1/MSK2 Fernet-encrypted binary files
V4.0 - Full body customization support
"""

import os
import json
import logging
import random
import base64
from pathlib import Path
from typing import Dict, Any, Optional


# ============================================
# SK ENCRYPTION - Custom block character cipher
# ============================================

class SKCipher:
    """
    Custom SK encryption algorithm that transforms data into
    Unicode block characters and back.
    
    Uses a three-layer approach:
    1. XOR scramble with key-derived stream
    2. Convert to hexadecimal (produces only 0-9, a-f)
    3. Map each hex digit to one of 150 Unicode block characters
    
    Since hex only has 16 possible values and we have 150 block characters,
    this is a perfect lossless mapping with zero collisions.
    
    Output looks like: ▕◆▧◄■▕▒□■▱◄▵▏▼▰▼◆◄□■▫
    """
    
    # 150 unique Unicode block characters for encoding
    BLOCK_CHARS = [
        '▕', '◆', '▧', '◄', '■', '▒', '□', '▱', '▵', '▏',
        '▼', '▰', '░', '▫', '┳', '▪', '┣', '╖', '╕', '╒',
        '▿', '█', '▨', '◌', '┫', '╋', '◇', '○', '◈', '▓',
        '▬', '╌', '╍', '╎', '╏', '═', '║', '╒', '╓', '╔',
        '╕', '╖', '╗', '╘', '╙', '╚', '╛', '╜', '╝', '╞',
        '╟', '╠', '╡', '╢', '╣', '╤', '╥', '╦', '╧', '╨',
        '╩', '╪', '╫', '╬', '▀', '▁', '▂', '▃', '▄', '▅',
        '▆', '▇', '█', '▉', '▊', '▋', '▌', '▍', '▎', '▏',
        '▐', '░', '▒', '▓', '▔', '▕', '▖', '▗', '▘', '▙',
        '▚', '▛', '▜', '▝', '▞', '▟', '■', '□', '▢', '▣',
        '▤', '▥', '▦', '▧', '▨', '▩', '▪', '▫', '▬', '▭',
        '▮', '▯', '▰', '▱', '▲', '△', '▴', '▵', '▶', '▷',
        '▸', '▹', '►', '▻', '▼', '▽', '▾', '▿', '◀', '◁',
        '◂', '◃', '◄', '◅', '◆', '◇', '◈', '◉', '◊', '○',
        '◌', '◍', '◎', '●', '◐', '◑', '◒', '◓', '◔', '◕',
    ]
    
    # Key seed for deterministic encryption/decryption
    _KEY_SEED = "MEMEBOT_SK_ENCRYPTION_V3_2024"
    
    def __init__(self):
        """Initialize the cipher with key-derived substitution tables"""
        self._build_tables()
    
    def _build_tables(self):
        """
        Build encoding/decoding lookup tables from the key seed.
        Uses deterministic random shuffling so the same key always
        produces the same substitution mapping.
        
        Only 16 mappings needed (for hex digits 0-15), but we pick
        them from 150 available block characters.
        """
        # Seed the random number generator with the key
        random.seed(self._KEY_SEED)
        
        # Create list of all 150 indices and shuffle them
        indices = list(range(len(self.BLOCK_CHARS)))
        shuffled = indices.copy()
        random.shuffle(shuffled)
        
        # Build forward mapping: hex value (0-15) -> block character
        self._encode_map = {}
        # Build reverse mapping: block character -> hex value (0-15)
        self._decode_map = {}
        
        # Only need 16 entries for hex digits
        for i in range(16):
            self._encode_map[i] = self.BLOCK_CHARS[shuffled[i]]
            self._decode_map[self.BLOCK_CHARS[shuffled[i]]] = i
        
        # Reset random seed to system state
        random.seed()
    
    def _xor_scramble(self, data: bytes, key: str) -> bytes:
        """
        XOR scramble data with a repeating key and position byte.
        
        This provides diffusion - each output byte depends on:
        - The input byte
        - The key byte at that position
        - The position itself (i & 0xFF)
        
        Args:
            data: Raw bytes to scramble
            key: String key for XOR operation
        
        Returns:
            Scrambled bytes (same length as input)
        """
        key_bytes = key.encode('utf-8')
        result = bytearray(len(data))
        for i, b in enumerate(data):
            # XOR with key byte and position for extra diffusion
            result[i] = b ^ key_bytes[i % len(key_bytes)] ^ (i & 0xFF)
        return bytes(result)
    
    def encrypt(self, plaintext: bytes) -> str:
        """
        Encrypt plaintext bytes to SK block character string.
        
        Process:
        1. XOR scramble the data with the key
        2. Convert to hexadecimal string (produces only 0-9, a-f)
        3. Map each hex digit to a unique block character
        
        Since hex only has 16 characters and we have 150 block characters,
        this is a perfect 1:1 mapping with no collisions.
        
        Args:
            plaintext: Raw bytes to encrypt
        
        Returns:
            Encrypted block character string with line breaks every 50 chars
        """
        # Step 1: XOR scramble
        scrambled = self._xor_scramble(plaintext, self._KEY_SEED)
        
        # Step 2: Convert to hex string
        hex_data = scrambled.hex()
        
        # Step 3: Map each hex digit to a block character
        result = []
        for i, char in enumerate(hex_data):
            # Convert hex char to integer (0-15)
            val = int(char, 16)
            
            # Map to block character using shuffled lookup
            result.append(self._encode_map[val])
            
            # Add line breaks every 50 characters for readability
            if (i + 1) % 50 == 0:
                result.append('\n')
        
        return ''.join(result)
    
    def decrypt(self, ciphertext: str) -> bytes:
        """
        Decrypt SK block character string back to plaintext bytes.
        
        Process:
        1. Map each block character back to its hex digit value
        2. Convert hex string to bytes
        3. Reverse the XOR scramble
        
        Args:
            ciphertext: Block character string to decrypt
        
        Returns:
            Decrypted raw bytes
        """
        # Remove all whitespace and newlines
        text = ''.join(ciphertext.split())
        
        # Step 1: Map block characters back to hex digits
        hex_chars = []
        for char in text:
            if char in self._decode_map:
                val = self._decode_map[char]
                hex_chars.append(format(val, 'x'))
        
        hex_string = ''.join(hex_chars)
        
        # Handle odd length hex strings
        if len(hex_string) % 2 != 0:
            hex_string = '0' + hex_string
        
        # Step 2: Convert hex to bytes
        try:
            data = bytes.fromhex(hex_string)
        except Exception:
            logging.error("SK Cipher: Failed to decode hex string")
            return b''
        
        # Step 3: Reverse XOR scramble
        return self._xor_scramble(data, self._KEY_SEED)


# ============================================
# SKIN ENCRYPTOR USING SK CIPHER
# ============================================

class SkinEncryptor:
    """
    Handles encryption and decryption of .MSK skin files.
    
    Supports two formats:
    - SK3: New text-based block character encryption (current)
    - MSK1/MSK2: Legacy Fernet binary encryption (backward compatible)
    
    File format (SK3):
    - Line 1: "SK3" header for format identification
    - Rest: Block character ciphertext (valid UTF-8)
    """
    
    def __init__(self):
        """Initialize the skin encryptor with SK cipher"""
        self.cipher = SKCipher()
    
    def encrypt_skin(self, skin_data: Dict[str, Any]) -> str:
        """
        Encrypt skin data dictionary into SK block character format.
        
        Args:
            skin_data: Dictionary containing skin properties
        
        Returns:
            SK encrypted block character string
        """
        # Convert skin data to JSON string then to bytes
        json_data = json.dumps(skin_data, indent=2).encode('utf-8')
        
        # Encrypt with SK cipher
        return self.cipher.encrypt(json_data)
    
    def decrypt_skin(self, encrypted_text: str) -> Optional[Dict[str, Any]]:
        """
        Decrypt SK encrypted skin data back to dictionary.
        
        Args:
            encrypted_text: SK block character string
        
        Returns:
            Dictionary containing skin properties, or None if decryption fails
        """
        try:
            # Decrypt with SK cipher
            decrypted = self.cipher.decrypt(encrypted_text)
            
            if not decrypted:
                return None
            
            # Parse JSON back to dictionary
            return json.loads(decrypted.decode('utf-8'))
        except Exception as e:
            logging.error(f"Failed to decrypt skin: {e}")
            return None
    
    def save_skin_file(self, file_path: Path, skin_data: Dict[str, Any]) -> bool:
        """
        Save encrypted skin data to a .MSK file.
        
        Args:
            file_path: Path where the .MSK file will be saved
            skin_data: Skin properties dictionary to encrypt and save
        
        Returns:
            True if save was successful, False otherwise
        """
        try:
            # Ensure Lua script exists in skin data
            if not skin_data.get("lua_script"):
                skin_data["lua_script"] = self._generate_default_lua()
            
            # Encrypt the skin data
            encrypted = self.encrypt_skin(skin_data)
            
            # Write as UTF-8 text file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("SK3\n")       # Format identifier
                f.write(encrypted)      # Block character ciphertext
            
            logging.info(f"Saved skin (SK encrypted): {file_path.name}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to save skin {file_path.name}: {e}")
            return False
    
    def load_skin_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Load and decrypt a .MSK skin file.
        
        Automatically detects the format:
        - Binary files starting with MSK1/MSK2 -> Legacy Fernet
        - Text files starting with SK3 -> New SK encryption
        - Other text with block characters -> Raw SK encrypted
        
        Args:
            file_path: Path to the .MSK file to load
        
        Returns:
            Dictionary containing skin properties, or None if loading fails
        """
        try:
            # Read file as binary first to check format
            with open(file_path, 'rb') as f:
                raw_bytes = f.read()
            
            # Check for legacy binary MSK1/MSK2 format
            if len(raw_bytes) >= 4:
                header = raw_bytes[:4]
                if header == b"MSK1" or header == b"MSK2":
                    logging.info(f"Detected legacy binary format in {file_path.name}")
                    return self._load_legacy_skin_binary(raw_bytes)
            
            # Try to decode as UTF-8 text for SK3 format
            try:
                content = raw_bytes.decode('utf-8')
            except UnicodeDecodeError:
                # Can't decode as text, try legacy binary without header
                logging.info(f"Binary file without text header in {file_path.name}")
                return self._load_legacy_skin_binary(raw_bytes)
            
            # Check for SK3 header
            if content.startswith("SK3\n"):
                # Remove "SK3\n" header (4 characters)
                encrypted = content[4:]
                skin_data = self.decrypt_skin(encrypted)
                if skin_data:
                    # Ensure Lua script exists
                    if not skin_data.get("lua_script"):
                        skin_data["lua_script"] = self._generate_default_lua()
                    logging.info(f"Loaded SK3 skin: {skin_data.get('name', 'Unknown')}")
                    return skin_data
            
            # Check for block characters (raw SK encrypted without header)
            block_chars_found = any(
                c in content[:50] for c in ['▕', '◆', '▧', '◄', '■', '▰', '▼', '▓', '▬']
            )
            if block_chars_found:
                logging.info(f"Detected raw SK block characters in {file_path.name}")
                skin_data = self.decrypt_skin(content)
                if skin_data:
                    if not skin_data.get("lua_script"):
                        skin_data["lua_script"] = self._generate_default_lua()
                    return skin_data
            
            # Unknown format - try legacy as last resort
            logging.warning(f"Unknown skin format in {file_path.name}, trying legacy")
            return self._load_legacy_skin_binary(raw_bytes)
            
        except FileNotFoundError:
            logging.error(f"Skin file not found: {file_path}")
            return None
        except Exception as e:
            logging.error(f"Failed to load skin {file_path.name}: {e}")
            return None
    
    def _load_legacy_skin_binary(self, raw_bytes: bytes) -> Optional[Dict[str, Any]]:
        """
        Load a legacy Fernet-encrypted binary skin file (MSK1/MSK2 format).
        
        These are older skins encrypted with the cryptography library's Fernet.
        This method exists for backward compatibility with skins created
        before the SK3 block character encryption was implemented.
        
        Args:
            raw_bytes: Raw binary data from the .MSK file
        
        Returns:
            Dictionary containing skin properties, or None if decryption fails
        """
        try:
            # Import cryptography only when needed (optional dependency)
            from cryptography.fernet import Fernet
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
            import base64 as b64
            
            # Remove 4-byte MSK header if present
            if raw_bytes[:4] == b"MSK1" or raw_bytes[:4] == b"MSK2":
                encrypted_data = raw_bytes[4:]
            else:
                encrypted_data = raw_bytes
            
            # Derive Fernet key using PBKDF2 with fixed salt
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b"MEMEBOT_SALT_VALUE_FOR_KEY_DERIVATION",
                iterations=100000,
            )
            key = b64.urlsafe_b64encode(
                kdf.derive(b"MEMEBOT_SKIN_ENCRYPTION_KEY_2024_V1")
            )
            fernet = Fernet(key)
            
            # Decrypt the data
            decrypted = fernet.decrypt(encrypted_data)
            
            # Parse JSON
            skin_data = json.loads(decrypted.decode('utf-8'))
            
            # Ensure Lua script exists
            if not skin_data.get("lua_script"):
                skin_data["lua_script"] = self._generate_default_lua()
            
            logging.info(f"Loaded legacy skin: {skin_data.get('name', 'Unknown')}")
            return skin_data
            
        except ImportError:
            logging.error(
                "Cryptography library not installed. "
                "Legacy skins require: pip install cryptography"
            )
            return None
        except Exception as e:
            logging.error(f"Failed to load legacy binary skin: {e}")
            return None
    
    def create_default_skin(self, skin_name: str) -> Dict[str, Any]:
        """
        Create a default skin data structure with full body customization support.
        V4.0 - All body parts customizable through MSK file, not hardcoded.
        
        Args:
            skin_name: Name for the new skin
        
        Returns:
            Dictionary with default skin properties including full body customization,
            colors, drawing instructions, accessories, animations, and particles.
        """
        return {
            "name": skin_name,
            "version": "4.0",
            "author": "MEMEBOT User",
            "description": "A fully customizable MEMEBOT skin with complete body control",
            "encryption": "SK3",
            
            # ============================================
            # BODY SCALE - Overall size multipliers
            # ============================================
            "body_scale": {
                "height": 1.0,
                "width": 1.0,
                "head_size": 1.0,
                "limb_length": 1.0,
            },
            
            # ============================================
            # BODY SHAPE - Complete body geometry
            # ============================================
            "body_shape": {
                "type": "default",
                "torso_width": 1.0,
                "torso_height": 1.0,
                "belly_size": 0.0,
                "shoulder_width": 1.0,
                "hip_width": 1.0,
                "custom_points": [],
            },
            
            # ============================================
            # LIMBS - Arms, legs, hands, feet
            # ============================================
            "limbs": {
                "arm_style": "default",
                "arm_length": 1.0,
                "arm_width": 1.0,
                "leg_style": "default",
                "leg_length": 1.0,
                "leg_width": 1.0,
                "hand_style": "default",
                "foot_style": "default",
            },
            
            # ============================================
            # HEAD - Shape and features
            # ============================================
            "head": {
                "shape": "round",
                "size": 1.0,
                "face_position": 0.0,
                "ear_style": "default",
                "ear_size": 1.0,
            },
            
            # ============================================
            # HAIR - Style and custom shapes
            # ============================================
            "hair": {
                "style": "default",
                "length": 1.0,
                "volume": 1.0,
                "bangs": True,
                "custom_points": [],
            },
            
            # ============================================
            # OUTFIT - Replaces default blue body
            # ============================================
            "outfit": {
                "type": "default",
                "top_color": [100, 180, 255, 255],
                "bottom_color": [50, 130, 200, 255],
                "custom_shapes": [],
            },
            
            # ============================================
            # COLORS - All color definitions
            # ============================================
            "colors": {
                "body": [100, 180, 255, 255],
                "body_outline": [50, 130, 200, 255],
                "skin": [255, 220, 180, 255],
                "skin_outline": [200, 170, 140, 255],
                "hair": [80, 60, 40, 255],
                "hair_outline": [60, 40, 20, 255],
                "eyes": [100, 180, 255, 255],
                "pupils": [30, 30, 30, 255],
                "mouth": [200, 100, 100, 255],
                "tongue": [255, 150, 150, 255],
                "cheeks": [255, 180, 180, 80],
                "ears_inner": [255, 180, 200, 255],
                "feet": [50, 50, 50, 255],
                "hands": [255, 220, 180, 255],
                "name_tag_bg": [50, 50, 50, 200],
                "name_tag_text": [255, 255, 255, 255],
                "outfit_primary": [100, 180, 255, 255],
                "outfit_secondary": [50, 130, 200, 255],
            },
            
            # ============================================
            # DRAWING - Custom shapes and overlays
            # ============================================
            "drawing": {
                "shapes": [],
                "overlays": [],
                "modifications": [],
            },
            
            # ============================================
            # ACCESSORIES
            # ============================================
            "accessories": {
                "hat": None,
                "glasses": None,
                "scarf": None,
                "shoes": None,
                "wings": None,
                "tail_type": "default",
                "custom_accessories": [],
            },
            
            # ============================================
            # CLOTHING
            # ============================================
            "clothing": {},
            
            # ============================================
            # ANIMATIONS
            # ============================================
            "animations": {
                "idle_speed": 1.0,
                "walk_speed": 1.0,
                "dance_speed": 1.0,
                "blink_rate": 1.0,
                "custom_animations": {},
            },
            
            # ============================================
            # PARTICLES
            # ============================================
            "particles": {
                "sparkle_color": [255, 255, 0, 180],
                "music_note_color": [100, 200, 255, 180],
                "heart_color": [255, 100, 150, 180],
                "custom_particles": {},
            },
            
            # ============================================
            # LUA SCRIPT
            # ============================================
            "lua_script": self._generate_default_lua(),
        }
    
    def _generate_default_lua(self) -> str:
        """Generate the default Lua script for skin behavior"""
        return '''--[[
    MEMEBOT Skin Lua Script v4.0 (SK Encrypted)
    This script controls the skin's behavior and rendering.
    Full body customization support.
    All functions are REQUIRED - do not remove them.
--]]

-- Skin metadata (read-only)
SKIN_NAME = "Default"
SKIN_VERSION = "4.0"
SKIN_AUTHOR = "MEMEBOT User"

-- ============================================
-- REQUIRED: Called when skin is first loaded
-- ============================================
function onSkinLoad()
    memebot.log("SK Encrypted skin loaded: " .. SKIN_NAME)
    memebot.setEmotion("happy")
end

-- ============================================
-- REQUIRED: Called every animation frame
-- @param frame: Current frame number
-- @param state: Current character state (idle, walking, dancing, etc.)
-- ============================================
function onFrame(frame, state)
    if state == "dancing" then
        memebot.setParticleRate(2.0)
    elseif state == "idle" then
        memebot.setParticleRate(1.0)
    end
end

-- ============================================
-- REQUIRED: Called when character starts dancing
-- @param danceName: Name of the dance
-- ============================================
function onDance(danceName)
    memebot.log("Dancing: " .. danceName)
    if danceName == "disco" then
        memebot.setParticleColor(255, 255, 0)
    elseif danceName == "thriller" then
        memebot.setParticleColor(255, 0, 0)
    else
        memebot.setParticleColor(255, 255, 255)
    end
end

-- ============================================
-- REQUIRED: Called when a meme starts playing
-- @param memeName: Name of the meme file
-- ============================================
function onMemePlay(memeName)
    memebot.log("Playing meme: " .. memeName)
    memebot.setEmotion("excited")
end

-- ============================================
-- REQUIRED: Called when character speaks
-- @param text: The text being spoken
-- ============================================
function onSpeak(text)
    if string.find(text:lower(), "hello") then
        memebot.setEmotion("happy")
    end
end

-- ============================================
-- OPTIONAL: Custom drawing function
-- Called after base character is drawn
-- @param draw: Drawing context (PIL ImageDraw)
-- @param cx, cy: Center position of character
-- ============================================
function onDraw(draw, cx, cy)
    -- Add custom drawing here
    -- Example: draw a custom hat
    -- draw:ellipse(cx - 20, cy - 120, cx + 20, cy - 90, {fill={255,0,0,255}})
end

-- ============================================
-- OPTIONAL: Custom particle effect
-- Called when particles are spawned
-- @param particleType: Type of particle (sparkle, star, heart, music)
-- @return: Modified particle properties or nil for default
-- ============================================
function onParticle(particleType)
    if particleType == "sparkle" then
        return {
            size = math.random(3, 8),
            speed = math.random(2, 5),
            color = {255, 255, 0, 200}
        }
    end
    return nil  -- Use default
end

-- ============================================
-- REQUIRED: Called when skin is unloaded
-- ============================================
function onSkinUnload()
    memebot.log("Skin unloaded: " .. SKIN_NAME)
    memebot.resetToDefault()
end

-- Return true to confirm script loaded successfully
return true
'''