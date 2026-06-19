"""
MEMEBOT Addon & Extension Manager
Handles loading Lua addons and Python extensions
Injects them into MEMEBOT without modifying core files
"""

import os
import sys
import json
import logging
import importlib
from pathlib import Path
from typing import Dict, Any, List, Optional


class AddonManager:
    """Manages all addons (Lua) and extensions (Python) for MEMEBOT"""
    
    def __init__(self, config, app):
        self.config = config
        self.app = app
        self.addons = {}
        self.extensions = {}
        self.active_addons = []
        self.active_extensions = []
        self.lua_states = {}
        
        self._scan_addons()
        self._scan_extensions()
        self._auto_load()
    
    def _scan_addons(self):
        """Scan addons directory for Lua-based addons"""
        self.addons = {}
        addons_path = self.config.BASE_PATH / "Addons"
        if not addons_path.exists():
            addons_path.mkdir(parents=True, exist_ok=True)
            return
        
        for folder in addons_path.iterdir():
            if folder.is_dir():
                lua_files = list(folder.glob("*.lua"))
                if lua_files:
                    config_file = folder / "addon.json"
                    addon_info = {
                        "name": folder.name,
                        "path": str(folder),
                        "entry": str(lua_files[0]),
                        "enabled": False,
                        "version": "1.0",
                        "author": "Unknown",
                        "description": "",
                        "type": "addon"
                    }
                    
                    if config_file.exists():
                        try:
                            with open(config_file, 'r', encoding='utf-8') as f:
                                info = json.load(f)
                                addon_info.update(info)
                        except:
                            pass
                    
                    self.addons[folder.name] = addon_info
    
    def _scan_extensions(self):
        """Scan extensions directory for Python-based extensions"""
        self.extensions = {}
        extensions_path = self.config.BASE_PATH / "Extensions"
        if not extensions_path.exists():
            extensions_path.mkdir(parents=True, exist_ok=True)
            return
        
        for folder in extensions_path.iterdir():
            if folder.is_dir():
                py_files = list(folder.glob("*.py"))
                if py_files:
                    config_file = folder / "extension.json"
                    ext_info = {
                        "name": folder.name,
                        "path": str(folder),
                        "entry": str(py_files[0]),
                        "enabled": False,
                        "version": "1.0",
                        "author": "Unknown",
                        "description": "",
                        "type": "extension"
                    }
                    
                    if config_file.exists():
                        try:
                            with open(config_file, 'r', encoding='utf-8') as f:
                                info = json.load(f)
                                ext_info.update(info)
                        except:
                            pass
                    
                    self.extensions[folder.name] = ext_info
    
    def _auto_load(self):
        """Auto-load addons/extensions that are enabled"""
        for name, info in self.addons.items():
            if info.get("enabled", False):
                self.load_addon(name)
        
        for name, info in self.extensions.items():
            if info.get("enabled", False):
                self.load_extension(name)
    
    def load_addon(self, name: str) -> bool:
        """Load a Lua addon"""
        if name not in self.addons:
            logging.warning(f"Addon not found: {name}")
            return False
        
        if name in self.active_addons:
            logging.info(f"Addon already loaded: {name}")
            return True
        
        info = self.addons[name]
        lua_file = info["entry"]
        
        if not os.path.exists(lua_file):
            logging.error(f"Addon Lua file not found: {lua_file}")
            return False
        
        lua_available = False
        try:
            import lupa
            lua_available = True
        except ImportError:
            pass
        
        if not lua_available:
            logging.warning("Lua not available - addon requires Lua (pip install lupa)")
            self.app.character.say("Lua not installed!")
            return False
        
        try:
            with open(lua_file, 'r', encoding='utf-8') as f:
                lua_code = f.read()
            
            import lupa
            lua = lupa.LuaRuntime(unpack_returned_tuples=True)
            
            # Set up Python callbacks using lua.execute to define globals
            setup_code = """
            _python_log = nil
            _python_say = nil
            _python_playMeme = nil
            _python_playSound = nil
            _python_setEmotion = nil
            _python_getState = nil
            _python_setDance = nil
            _python_getBasePath = nil
            _python_getX = nil
            _python_getY = nil
            _python_createDirectory = nil
            
            addon = {}
            function addon.log(msg) 
                if _python_log then _python_log(msg) end 
            end
            function addon.say(text) 
                if _python_say then _python_say(text) end 
            end
            function addon.playMeme() 
                if _python_playMeme then _python_playMeme() end 
            end
            function addon.playSound() 
                if _python_playSound then _python_playSound() end 
            end
            function addon.setEmotion(e) 
                if _python_setEmotion then _python_setEmotion(e) end 
            end
            function addon.getState() 
                if _python_getState then return _python_getState() end
                return "idle"
            end
            function addon.setDance(d) 
                if _python_setDance then _python_setDance(d) end 
            end
            function addon.getBasePath() 
                if _python_getBasePath then return _python_getBasePath() end
                return ""
            end
            function addon.getX() 
                if _python_getX then return _python_getX() end
                return 0
            end
            function addon.getY() 
                if _python_getY then return _python_getY() end
                return 0
            end
            function addon.createDirectory(path)
                if _python_createDirectory then _python_createDirectory(path) end
            end
            memebot = addon
            """
            
            lua.execute(setup_code)
            
            # Expose Python functions to Lua globals
            lua.execute('_python_log = nil')
            lua.globals()['_python_log'] = lambda msg: logging.info(f"[Addon:{name}] {str(msg)}")
            
            lua.execute('_python_say = nil')
            lua.globals()['_python_say'] = lambda text: self.app.root.after(0, lambda t=text: self.app.say(str(t)))
            
            lua.execute('_python_playMeme = nil')
            lua.globals()['_python_playMeme'] = lambda: self.app.root.after(0, self.app.play_random_meme)
            
            lua.execute('_python_playSound = nil')
            lua.globals()['_python_playSound'] = lambda: self.app.root.after(0, self.app.play_random_sound)
            
            lua.execute('_python_setEmotion = nil')
            lua.globals()['_python_setEmotion'] = lambda e: setattr(self.app.character, 'emotion', str(e))
            
            lua.execute('_python_getState = nil')
            lua.globals()['_python_getState'] = lambda: str(self.app.character.state)
            
            lua.execute('_python_setDance = nil')
            lua.globals()['_python_setDance'] = lambda d: self.app.character.set_dance(str(d))
            
            lua.execute('_python_getBasePath = nil')
            lua.globals()['_python_getBasePath'] = lambda: str(self.config.BASE_PATH)
            
            lua.execute('_python_getX = nil')
            lua.globals()['_python_getX'] = lambda: self.app.character.x
            
            lua.execute('_python_getY = nil')
            lua.globals()['_python_getY'] = lambda: self.app.character.y
            
            lua.execute('_python_createDirectory = nil')
            lua.globals()['_python_createDirectory'] = lambda path: Path(str(path)).mkdir(parents=True, exist_ok=True)
            
            # Execute the addon's Lua code
            lua.execute(lua_code)
            
            # Try to call onLoad
            try:
                result = lua.execute("""
                    if onLoad ~= nil then
                        onLoad()
                        return true
                    end
                    return false
                """)
                if result:
                    logging.info(f"Addon {name} onLoad() called successfully")
                else:
                    logging.info(f"Addon {name} has no onLoad() function")
            except Exception as e:
                logging.warning(f"Addon {name} onLoad() error: {e}")
            
            # Store the Lua state
            self.lua_states[name] = {'lua': lua}
            
            info["enabled"] = True
            self.active_addons.append(name)
            logging.info(f"Addon loaded successfully: {name}")
            self.app.character.say(f"Addon: {name}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to load addon {name}: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def load_extension(self, name: str) -> bool:
        """Load a Python extension"""
        if name not in self.extensions:
            logging.warning(f"Extension not found: {name}")
            return False
        
        if name in self.active_extensions:
            logging.info(f"Extension already loaded: {name}")
            return True
        
        info = self.extensions[name]
        py_file = info["entry"]
        
        if not os.path.exists(py_file):
            logging.error(f"Extension Python file not found: {py_file}")
            return False
        
        try:
            ext_folder = info["path"]
            if ext_folder not in sys.path:
                sys.path.insert(0, ext_folder)
            
            module_name = Path(py_file).stem
            spec = importlib.util.spec_from_file_location(
                f"extensions.{name}.{module_name}", py_file
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, 'setup'):
                module.setup(self.app, self.config)
            
            info["enabled"] = True
            info["module"] = module
            self.active_extensions.append(name)
            logging.info(f"Extension loaded: {name}")
            self.app.character.say(f"Extension: {name}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to load extension {name}: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def unload_addon(self, name: str) -> bool:
        """Unload a Lua addon"""
        if name in self.active_addons:
            if name in self.lua_states:
                try:
                    self.lua_states[name]['lua'].execute("""
                        if onUnload ~= nil then
                            onUnload()
                        end
                    """)
                except:
                    pass
                del self.lua_states[name]
            
            self.active_addons.remove(name)
            if name in self.addons:
                self.addons[name]["enabled"] = False
            logging.info(f"Addon unloaded: {name}")
            return True
        return False
    
    def unload_extension(self, name: str) -> bool:
        """Unload a Python extension"""
        if name in self.active_extensions:
            self.active_extensions.remove(name)
            if name in self.extensions:
                info = self.extensions[name]
                if "module" in info and hasattr(info["module"], 'cleanup'):
                    try:
                        info["module"].cleanup()
                    except:
                        pass
                info["enabled"] = False
            logging.info(f"Extension unloaded: {name}")
            return True
        return False
    
    def get_addons(self) -> List[Dict[str, Any]]:
        """Get list of all addons"""
        result = []
        for k, v in self.addons.items():
            item = {"name": k}
            item.update(v)
            result.append(item)
        return result
    
    def get_extensions(self) -> List[Dict[str, Any]]:
        """Get list of all extensions"""
        result = []
        for k, v in self.extensions.items():
            item = {"name": k}
            item.update(v)
            result.append(item)
        return result
    
    def create_addon(self, name: str) -> bool:
        """Create a new addon template"""
        addon_path = self.config.BASE_PATH / "Addons" / name
        addon_path.mkdir(parents=True, exist_ok=True)
        
        config = {
            "name": name,
            "version": "1.0",
            "author": "MEMEBOT User",
            "description": "A custom addon",
            "enabled": False,
            "type": "addon"
        }
        with open(addon_path / "addon.json", 'w') as f:
            json.dump(config, f, indent=2)
        
        lua_code = '''--[[ MEMEBOT Addon: ''' + name + ''' --]]
ADDON_NAME = "''' + name + '''"

function onLoad()
    addon.log("Addon loaded: " .. ADDON_NAME)
    addon.say("Addon ready!")
end

function onFrame(frame, state)
end

function onDance(danceName)
    addon.log("Dancing: " .. danceName)
end

function onUnload()
    addon.log("Addon unloaded: " .. ADDON_NAME)
end
'''
        with open(addon_path / "main.lua", 'w', encoding='utf-8') as f:
            f.write(lua_code)
        
        self._scan_addons()
        logging.info(f"Created addon: {name}")
        return True
    
    def create_extension(self, name: str) -> bool:
        """Create a new extension template"""
        ext_path = self.config.BASE_PATH / "Extensions" / name
        ext_path.mkdir(parents=True, exist_ok=True)
        
        config = {
            "name": name,
            "version": "1.0",
            "author": "MEMEBOT User",
            "description": "A custom extension",
            "enabled": False,
            "type": "extension"
        }
        with open(ext_path / "extension.json", 'w') as f:
            json.dump(config, f, indent=2)
        
        py_code = '''"""
MEMEBOT Extension: ''' + name + '''
Custom Python extension for MEMEBOT
"""

import logging

EXTENSION_NAME = "''' + name + '''"
EXTENSION_VERSION = "1.0"

def setup(app, config):
    logging.info(f"Extension loaded: {EXTENSION_NAME}")
    app.character.say(f"Extension: {EXTENSION_NAME}")

def cleanup():
    logging.info(f"Extension unloaded: {EXTENSION_NAME}")
'''
        with open(ext_path / "main.py", 'w', encoding='utf-8') as f:
            f.write(py_code)
        
        self._scan_extensions()
        logging.info(f"Created extension: {name}")
        return True