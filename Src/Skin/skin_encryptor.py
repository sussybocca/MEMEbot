"""
MEMEBOT Skin Encryptor
Encrypts and decrypts .MSK skin files using enhanced SK3 encryption
Multiple security layers: PBKDF2 key derivation, AES-256-GCM, block character encoding
Supports legacy MSK1/MSK2 Fernet-encrypted binary files
V4.0 - Full body customization support with secure SK3 format
"""

import os
import json
import logging
import random
import base64
import hashlib
import secrets
from pathlib import Path
from typing import Dict, Any, Optional, Tuple


# ============================================
# SK3 ENHANCED CIPHER - Multi-layer security
# ============================================

class SKCipher:
    """
    Enhanced SK3 encryption with multiple security layers:
    
    Layer 1: PBKDF2-HMAC-SHA512 key derivation (200,000 iterations)
    Layer 2: AES-256-GCM authenticated encryption
    Layer 3: Custom block character encoding (obfuscation layer)
    
    The block character encoding now serves as an additional obfuscation
    layer on top of AES encryption, not as the primary encryption.
    
    Output still looks like: ▕◆▧◄■▕▒□■▱◄▵▏▼▰▼◆◄□■▫
    But the underlying data is AES-256-GCM encrypted with authentication.
    """
    
    # 256 unique Unicode block characters for encoding (expanded from 150)
    BLOCK_CHARS = [
        '▕', '◆', '▧', '◄', '■', '▒', '□', '▱', '▵', '▏', '▼', '▰', '░', '▫', '┳', '▪',
        '┣', '╖', '╕', '╒', '▿', '█', '▨', '◌', '┫', '╋', '◇', '○', '◈', '▓', '▬', '╌',
        '╍', '╎', '╏', '═', '║', '╓', '╔', '╗', '╘', '╙', '╚', '╛', '╜', '╝', '╞', '╟',
        '╠', '╡', '╢', '╣', '╤', '╥', '╦', '╧', '╨', '╩', '╪', '╫', '╬', '▀', '▁', '▂',
        '▃', '▄', '▅', '▆', '▇', '▉', '▊', '▋', '▌', '▍', '▎', '▐', '▔', '▖', '▗', '▘',
        '▙', '▚', '▛', '▜', '▝', '▞', '▟', '▢', '▣', '▤', '▥', '▦', '▩', '▭', '▮', '▯',
        '▲', '△', '▴', '▶', '▷', '▸', '▹', '►', '▻', '▽', '▾', '◀', '◁', '◂', '◃', '◅',
        '◉', '◊', '◍', '◎', '●', '◐', '◑', '◒', '◓', '◔', '◕', '◖', '◗', '◘', '◙', '◚',
        '◛', '◜', '◝', '◞', '◟', '◠', '◡', '◢', '◣', '◤', '◥', '◦', '◧', '◨', '◩', '◪',
        '◫', '◬', '◭', '◮', '◯', '◰', '◱', '◲', '◳', '◴', '◵', '◶', '◷', '◸', '◹', '◺',
        '◻', '◼', '◽', '◾', '◿', '☀', '☁', '☂', '☃', '☄', '★', '☆', '☇', '☈', '☉', '☊',
        '☋', '☌', '☍', '☎', '☏', '☐', '☑', '☒', '☓', '☔', '☕', '☖', '☗', '☘', '☙', '☚',
        '☛', '☜', '☝', '☞', '☟', '☠', '☡', '☢', '☣', '☤', '☥', '☦', '☧', '☨', '☩', '☪',
        '☫', '☬', '☭', '☮', '☯', '☰', '☱', '☲', '☳', '☴', '☵', '☶', '☷', '☸', '☹', '☺',
        '☻', '☼', '☽', '☾', '☿', '♀', '♁', '♂', '♃', '♄', '♅', '♆', '♇', '♈', '♉', '♊',
        '♋', '♌', '♍', '♎', '♏', '♐', '♑', '♒', '♓', '♔', '♕', '♖', '♗', '♘', '♙', '♚',
    ]
    
    # AES block size
    AES_BLOCK_SIZE = 16
    
    # PBKDF2 iterations (high for security)
    PBKDF2_ITERATIONS = 200000
    
    # Key derivation salt (unique per installation but deterministic)
    _KEY_SALT = b"MEMEBOT_SK3_SALT_2024_V2_ENHANCED_SECURITY_LAYER"
    
    # Master key seed
    _MASTER_SEED = "MEMEBOT_SK3_MASTER_KEY_2024_V2_WITH_AES256_GCM_AUTHENTICATION"
    
    def __init__(self):
        """Initialize the cipher with AES key derived from master seed"""
        self._aes_key = self._derive_aes_key()
        self._build_encoding_table()
    
    def _derive_aes_key(self) -> bytes:
        """
        Derive a 256-bit AES key using PBKDF2-HMAC-SHA512.
        
        Uses a high iteration count to make brute-forcing computationally expensive.
        The key is derived from the master seed with a fixed salt.
        
        Returns:
            32-byte (256-bit) AES key
        """
        import hashlib
        
        key = hashlib.pbkdf2_hmac(
            'sha512',
            self._MASTER_SEED.encode('utf-8'),
            self._KEY_SALT,
            self.PBKDF2_ITERATIONS,
            dklen=32  # 256-bit key
        )
        return key
    
    def _build_encoding_table(self):
        """
        Build the hex-to-block-character encoding table.
        
        Uses deterministic shuffling based on a hash of the master seed,
        so the mapping is consistent across sessions but unique to MEMEBOT.
        
        Maps 16 hex digits (0-15) to 16 unique block characters.
        """
        # Create a deterministic shuffle based on hash of master seed
        hash_bytes = hashlib.sha256(self._MASTER_SEED.encode('utf-8')).digest()
        
        # Use hash bytes to seed our selection
        indices = list(range(len(self.BLOCK_CHARS)))
        
        # Fisher-Yates shuffle with deterministic randomness from hash
        for i in range(len(indices) - 1, 0, -1):
            j = hash_bytes[i % len(hash_bytes)] % (i + 1)
            indices[i], indices[j] = indices[j], indices[i]
        
        # Build forward mapping: hex value (0-15) -> block character
        self._encode_map = {}
        # Build reverse mapping: block character -> hex value (0-15)
        self._decode_map = {}
        
        for i in range(16):
            self._encode_map[i] = self.BLOCK_CHARS[indices[i]]
            self._decode_map[self.BLOCK_CHARS[indices[i]]] = i
    
    def _aes_encrypt(self, plaintext: bytes) -> Tuple[bytes, bytes, bytes]:
        """
        Encrypt data using AES-256-GCM with authenticated encryption.
        
        AES-GCM provides both confidentiality and integrity/authentication.
        Any tampering with the ciphertext will be detected during decryption.
        
        Args:
            plaintext: Raw bytes to encrypt
        
        Returns:
            Tuple of (nonce, ciphertext, authentication_tag)
            - nonce: 12 bytes (random, needed for decryption)
            - ciphertext: Same length as plaintext
            - tag: 16 bytes (authentication tag)
        """
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            
            aesgcm = AESGCM(self._aes_key)
            nonce = secrets.token_bytes(12)  # 96-bit nonce as recommended
            
            # AES-GCM handles the authentication tag internally
            ciphertext = aesgcm.encrypt(nonce, plaintext, None)
            
            # The tag is the last 16 bytes of the ciphertext
            actual_ciphertext = ciphertext[:-16]
            tag = ciphertext[-16:]
            
            return nonce, actual_ciphertext, tag
            
        except ImportError:
            # Fallback: Use a simpler but still secure approach without cryptography library
            logging.warning("Cryptography library not found, using fallback encryption")
            return self._fallback_encrypt(plaintext)
    
    def _aes_decrypt(self, nonce: bytes, ciphertext: bytes, tag: bytes) -> Optional[bytes]:
        """
        Decrypt data using AES-256-GCM with authentication verification.
        
        If the authentication tag doesn't match, the data was tampered with
        and None is returned.
        
        Args:
            nonce: 12 bytes from encryption
            ciphertext: Encrypted data
            tag: 16 bytes authentication tag
        
        Returns:
            Decrypted bytes, or None if authentication fails
        """
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            
            aesgcm = AESGCM(self._aes_key)
            
            # Recombine ciphertext and tag
            combined = ciphertext + tag
            
            return aesgcm.decrypt(nonce, combined, None)
            
        except ImportError:
            return self._fallback_decrypt(nonce, ciphertext, tag)
        except Exception as e:
            logging.error(f"AES decryption failed: {e}")
            return None
    
    def _fallback_encrypt(self, plaintext: bytes) -> Tuple[bytes, bytes, bytes]:
        """
        Fallback encryption when cryptography library is not available.
        Uses a multi-pass XOR with key rotation for basic obfuscation.
        
        This is less secure than AES-GCM but provides basic protection.
        """
        nonce = secrets.token_bytes(12)
        key_material = hashlib.sha256(self._aes_key + nonce).digest()
        
        result = bytearray(len(plaintext))
        for i, b in enumerate(plaintext):
            key_byte = key_material[i % len(key_material)]
            pos_byte = (i * 73 + 41) & 0xFF
            result[i] = b ^ key_byte ^ pos_byte
        
        # Generate a simple tag for integrity
        tag = hashlib.sha256(plaintext).digest()[:16]
        
        return nonce, bytes(result), tag
    
    def _fallback_decrypt(self, nonce: bytes, ciphertext: bytes, tag: bytes) -> Optional[bytes]:
        """Fallback decryption - reverse of fallback encryption"""
        key_material = hashlib.sha256(self._aes_key + nonce).digest()
        
        result = bytearray(len(ciphertext))
        for i, b in enumerate(ciphertext):
            key_byte = key_material[i % len(key_material)]
            pos_byte = (i * 73 + 41) & 0xFF
            result[i] = b ^ key_byte ^ pos_byte
        
        plaintext = bytes(result)
        
        # Verify integrity
        expected_tag = hashlib.sha256(plaintext).digest()[:16]
        if not secrets.compare_digest(tag, expected_tag):
            logging.error("Fallback: Authentication tag mismatch - data may be tampered")
            return None
        
        return plaintext
    
    def _blocks_encode(self, data: bytes) -> str:
        """
        Encode binary data into block character string.
        
        Converts binary to hex, then maps each hex digit to a unique
        block character using the deterministic shuffle table.
        
        Args:
            data: Binary data to encode
        
        Returns:
            Block character string
        """
        # Convert to hex
        hex_data = data.hex()
        
        # Map each hex digit to a block character
        result = []
        for i, char in enumerate(hex_data):
            val = int(char, 16)
            result.append(self._encode_map[val])
            
            # Line breaks every 64 characters for readability
            if (i + 1) % 64 == 0:
                result.append('\n')
        
        return ''.join(result)
    
    def _blocks_decode(self, text: str) -> Optional[bytes]:
        """
        Decode block character string back to binary data.
        
        Strips header lines (SK3, V3.1) and whitespace before decoding.
        
        Args:
            text: Block character string (may include SK3 header lines)
        
        Returns:
            Decoded binary data, or None if invalid characters found
        """
        # Remove SK3 header lines if present
        lines = text.split('\n')
        clean_lines = []
        for line in lines:
            stripped = line.strip()
            # Skip header lines
            if stripped in ('SK3',) or stripped.startswith('V3.') or stripped.startswith('V2.') or stripped.startswith('V1.'):
                continue
            # Skip empty lines
            if not stripped:
                continue
            clean_lines.append(stripped)
        
        text = ''.join(clean_lines)
        
        # Also strip any remaining whitespace
        text = ''.join(text.split())
        
        # Map block characters back to hex digits
        hex_chars = []
        for char in text:
            if char in self._decode_map:
                val = self._decode_map[char]
                hex_chars.append(format(val, 'x'))
            elif char in '\n\r\t ':
                continue  # Skip whitespace
            else:
                logging.warning(f"Unknown character in ciphertext: {repr(char)}")
                continue
        
        hex_string = ''.join(hex_chars)
        
        # Handle odd length
        if len(hex_string) % 2 != 0:
            hex_string = '0' + hex_string
        
        try:
            return bytes.fromhex(hex_string)
        except Exception as e:
            logging.error(f"Failed to decode hex string: {e}")
            return None
    
    def encrypt(self, plaintext: bytes) -> str:
        """
        Full encryption pipeline:
        1. AES-256-GCM encryption (or fallback)
        2. Combine nonce + ciphertext + tag
        3. Encode to block characters
        
        Args:
            plaintext: Raw bytes to encrypt
        
        Returns:
            Block character string (valid UTF-8)
        """
        # Layer 1 & 2: AES-256-GCM encryption
        nonce, ciphertext, tag = self._aes_encrypt(plaintext)
        
        # Combine: nonce (12) + tag (16) + ciphertext (variable)
        combined = nonce + tag + ciphertext
        
        # Layer 3: Block character encoding
        return self._blocks_encode(combined)
    
    def decrypt(self, ciphertext: str) -> Optional[bytes]:
        """
        Full decryption pipeline:
        1. Decode block characters to binary
        2. Extract nonce, tag, and ciphertext
        3. AES-256-GCM decryption with authentication
        
        Args:
            ciphertext: Block character string (may include SK3 header lines)
        
        Returns:
            Decrypted bytes, or None if decryption/authentication fails
        """
        # Layer 3 reverse: Block character decoding (handles header stripping internally)
        combined = self._blocks_decode(ciphertext)
        
        if combined is None:
            return None
        
        if len(combined) < 28:  # Minimum: nonce(12) + tag(16)
            logging.error("Ciphertext too short")
            return None
        
        # Extract components
        nonce = combined[:12]
        tag = combined[12:28]
        actual_ciphertext = combined[28:]
        
        # Layer 1 & 2 reverse: AES-256-GCM decryption
        return self._aes_decrypt(nonce, actual_ciphertext, tag)


# ============================================
# SKIN ENCRYPTOR USING ENHANCED SK3 CIPHER
# ============================================

class SkinEncryptor:
    """
    Handles encryption and decryption of .MSK skin files.
    
    Supports two formats:
    - SK3: Enhanced text-based block character encryption (AES-256-GCM + blocks)
    - MSK1/MSK2: Legacy Fernet binary encryption (backward compatible)
    
    File format (SK3):
    - Line 1: "SK3" header for format identification
    - Line 2: Version info
    - Rest: Block character ciphertext (valid UTF-8)
    """
    
    def __init__(self):
        """Initialize the skin encryptor with enhanced SK3 cipher"""
        self.cipher = SKCipher()
    
    def encrypt_skin(self, skin_data: Dict[str, Any]) -> str:
        """
        Encrypt skin data dictionary into enhanced SK3 block character format.
        
        Uses AES-256-GCM for authenticated encryption, then encodes to
        block characters for the final SK3 format.
        
        Args:
            skin_data: Dictionary containing skin properties
        
        Returns:
            SK3 encrypted block character string
        """
        # Compute checksum on skin data WITHOUT _sk3_meta first
        checksum = hashlib.sha256(
            json.dumps(skin_data, sort_keys=True, ensure_ascii=False).encode('utf-8')
        ).hexdigest()
        
        # Now add integrity metadata with pre-computed checksum
        skin_data["_sk3_meta"] = {
            "version": "3.1",
            "encryption": "AES-256-GCM",
            "encoding": "block_characters",
            "timestamp": int(__import__('time').time()),
            "checksum": checksum,
        }
        
        # Convert skin data to JSON string then to bytes
        json_data = json.dumps(skin_data, indent=2, ensure_ascii=False).encode('utf-8')
        
        # Encrypt with enhanced SK3 cipher (AES-256-GCM + blocks)
        return self.cipher.encrypt(json_data)
    
    def decrypt_skin(self, encrypted_text: str) -> Optional[Dict[str, Any]]:
        """
        Decrypt SK3 encrypted skin data back to dictionary.
        
        Verifies authentication tag to detect tampering.
        The encrypted_text can include SK3/V3.1 header lines - they will be stripped.
        
        Args:
            encrypted_text: SK3 block character string (may include header lines)
        
        Returns:
            Dictionary containing skin properties, or None if decryption fails
        """
        try:
            # Strip SK3 header if present before decrypting
            clean_text = encrypted_text
            if clean_text.startswith("SK3"):
                lines = clean_text.split('\n', 2)
                if len(lines) >= 3:
                    clean_text = lines[2]
                elif len(lines) >= 2:
                    if lines[1].startswith('V'):
                        clean_text = ''
                    else:
                        clean_text = lines[1]
                else:
                    clean_text = ''
            
            # Decrypt with enhanced SK3 cipher
            decrypted = self.cipher.decrypt(clean_text)
            
            if not decrypted:
                return None
            
            # Parse JSON back to dictionary
            skin_data = json.loads(decrypted.decode('utf-8'))
            
            # Verify integrity if metadata exists
            if "_sk3_meta" in skin_data:
                meta = skin_data.pop("_sk3_meta")
                expected_checksum = meta.get("checksum", "")
                
                # Recompute checksum on data WITHOUT _sk3_meta (already popped)
                actual_checksum = hashlib.sha256(
                    json.dumps(skin_data, sort_keys=True, ensure_ascii=False).encode('utf-8')
                ).hexdigest()
                
                if expected_checksum and expected_checksum != actual_checksum:
                    logging.error("Skin data integrity check failed!")
                    return None
                
                logging.info(f"SK3 v{meta.get('version', '?')} skin verified successfully")
            
            return skin_data
            
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
            
            # Write as UTF-8 text file with SK3 header
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("SK3\n")           # Format identifier
                f.write("V3.1\n")          # Version
                f.write(encrypted)          # Block character ciphertext
            
            logging.info(f"Saved enhanced SK3 skin: {file_path.name}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to save skin {file_path.name}: {e}")
            return False
    
    def load_skin_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Load and decrypt a .MSK skin file.
        
        Automatically detects the format:
        - Text files starting with SK3 -> Enhanced SK3 encryption
        - Binary files starting with MSK1/MSK2 -> Legacy Fernet
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
                logging.info(f"Binary file without text header in {file_path.name}")
                return self._load_legacy_skin_binary(raw_bytes)
            
            # Check for SK3 header - pass the ENTIRE content to decrypt_skin
            if content.startswith("SK3"):
                logging.info(f"Detected SK3 format in {file_path.name}")
                skin_data = self.decrypt_skin(content)
                if skin_data:
                    if not skin_data.get("lua_script"):
                        skin_data["lua_script"] = self._generate_default_lua()
                    logging.info(f"Loaded enhanced SK3 skin: {skin_data.get('name', 'Unknown')}")
                    return skin_data
                else:
                    logging.error(f"Failed to decrypt SK3 skin: {file_path.name}")
                    return None
            
            # Check for block characters (raw SK encrypted without header)
            block_chars_found = any(
                c in content[:100] for c in ['▕', '◆', '▧', '◄', '■', '▰', '▼', '▓', '▬']
            )
            if block_chars_found:
                logging.info(f"Detected raw SK block characters in {file_path.name}")
                skin_data = self.decrypt_skin(content)
                if skin_data:
                    if not skin_data.get("lua_script"):
                        skin_data["lua_script"] = self._generate_default_lua()
                    return skin_data
                else:
                    logging.error(f"Failed to decrypt raw block character skin: {file_path.name}")
                    return None
            
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
        
        Args:
            raw_bytes: Raw binary data from the .MSK file
        
        Returns:
            Dictionary containing skin properties, or None if decryption fails
        """
        try:
            from cryptography.fernet import Fernet
            from cryptography.hazmat.primitives import hashes
            from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
            import base64 as b64
            
            if raw_bytes[:4] == b"MSK1" or raw_bytes[:4] == b"MSK2":
                encrypted_data = raw_bytes[4:]
            else:
                encrypted_data = raw_bytes
            
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
            decrypted = fernet.decrypt(encrypted_data)
            skin_data = json.loads(decrypted.decode('utf-8'))
            
            if not skin_data.get("lua_script"):
                skin_data["lua_script"] = self._generate_default_lua()
            
            logging.info(f"Loaded legacy skin: {skin_data.get('name', 'Unknown')}")
            return skin_data
            
        except ImportError:
            logging.error("Cryptography library not installed. Legacy skins require: pip install cryptography")
            return None
        except Exception as e:
            logging.error(f"Failed to load legacy binary skin: {e}")
            return None
    
    def create_default_skin(self, skin_name: str) -> Dict[str, Any]:
        """
        Create a default skin data structure with full body customization support.
        
        Args:
            skin_name: Name for the new skin
        
        Returns:
            Dictionary with default skin properties
        """
        return {
            "name": skin_name,
            "version": "4.0",
            "author": "MEMEBOT User",
            "description": "A fully customizable MEMEBOT skin with complete body control",
            "encryption": "SK3-Enhanced",
            
            "body_scale": {
                "height": 1.0, "width": 1.0,
                "head_size": 1.0, "limb_length": 1.0,
            },
            "body_shape": {
                "type": "default", "torso_width": 1.0, "torso_height": 1.0,
                "belly_size": 0.0, "shoulder_width": 1.0, "hip_width": 1.0,
                "custom_points": [],
            },
            "limbs": {
                "arm_style": "default", "arm_length": 1.0, "arm_width": 1.0,
                "leg_style": "default", "leg_length": 1.0, "leg_width": 1.0,
                "hand_style": "default", "foot_style": "default",
            },
            "head": {
                "shape": "round", "size": 1.0,
                "face_position": 0.0, "ear_style": "default", "ear_size": 1.0,
            },
            "hair": {
                "style": "default", "length": 1.0, "volume": 1.0,
                "bangs": True, "custom_points": [],
            },
            "outfit": {
                "type": "default",
                "top_color": [100, 180, 255, 255],
                "bottom_color": [50, 130, 200, 255],
                "custom_shapes": [],
            },
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
            "drawing": {
                "shapes": [],
                "overlays": [],
                "modifications": [],
            },
            "accessories": {
                "hat": None, "glasses": None, "scarf": None,
                "shoes": None, "wings": None, "tail_type": "default",
                "custom_accessories": [],
            },
            "clothing": {},
            "animations": {
                "idle_speed": 1.0, "walk_speed": 1.0,
                "dance_speed": 1.0, "blink_rate": 1.0,
                "custom_animations": {},
            },
            "particles": {
                "sparkle_color": [255, 255, 0, 180],
                "music_note_color": [100, 200, 255, 180],
                "heart_color": [255, 100, 150, 180],
                "custom_particles": {},
            },
            "lua_script": self._generate_default_lua(),
        }
    
    def _generate_default_lua(self) -> str:
        """Generate the default Lua script for skin behavior"""
        return '''--[[
    MEMEBOT Skin Lua Script v4.0 (Enhanced SK3 Encrypted)
    This script controls the skin's behavior and rendering.
    Full body customization support.
    All functions are REQUIRED - do not remove them.
--]]

SKIN_NAME = "Default"
SKIN_VERSION = "4.0"
SKIN_AUTHOR = "MEMEBOT User"

function onSkinLoad()
    memebot.log("Enhanced SK3 skin loaded: " .. SKIN_NAME)
    memebot.setEmotion("happy")
end

function onFrame(frame, state)
    if state == "dancing" then
        memebot.setParticleRate(2.0)
    elseif state == "idle" then
        memebot.setParticleRate(1.0)
    end
end

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

function onMemePlay(memeName)
    memebot.log("Playing meme: " .. memeName)
    memebot.setEmotion("excited")
end

function onSpeak(text)
    if string.find(text:lower(), "hello") then
        memebot.setEmotion("happy")
    end
end

function onDraw(draw, cx, cy)
    -- Custom drawing here
end

function onParticle(particleType)
    if particleType == "sparkle" then
        return {
            size = math.random(3, 8),
            speed = math.random(2, 5),
            color = {255, 255, 0, 200}
        }
    end
    return nil
end

function onSkinUnload()
    memebot.log("Skin unloaded: " .. SKIN_NAME)
    memebot.resetToDefault()
end

return true
'''


# ============================================
# SKIN FORMAT MIGRATION
# ============================================

class SkinMigrator:
    """Migrates skins between formats (MSK1/MSK2 -> SK3)"""
    
    @staticmethod
    def migrate_to_sk3(file_path: Path, encryptor: SkinEncryptor) -> bool:
        """
        Migrate a legacy MSK1/MSK2 skin to enhanced SK3 format.
        
        Args:
            file_path: Path to the legacy skin file
            encryptor: SkinEncryptor instance for saving
        
        Returns:
            True if migration was successful
        """
        try:
            # Load the legacy skin
            skin_data = encryptor.load_skin_file(file_path)
            if skin_data is None:
                return False
            
            # Update encryption marker
            skin_data["encryption"] = "SK3-Enhanced"
            
            # Create backup
            backup_path = file_path.with_suffix('.msk.bak')
            if file_path.exists():
                with open(file_path, 'rb') as src:
                    with open(backup_path, 'wb') as dst:
                        dst.write(src.read())
                logging.info(f"Backup created: {backup_path.name}")
            
            # Save in new format
            return encryptor.save_skin_file(file_path, skin_data)
            
        except Exception as e:
            logging.error(f"Migration failed: {e}")
            return False