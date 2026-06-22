"""
MEMEBOT Bot Engagement System - Skin Analyzer
Analyzes MSK skin files for quality metrics and design elements
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List, Tuple
from datetime import datetime


class SkinAnalyzer:
    """Analyzes MSK skin files for various quality metrics"""
    
    # Scoring weights for different categories
    WEIGHTS = {
        'color_harmony': 0.15,
        'design_completeness': 0.20,
        'animation_readiness': 0.15,
        'customization_depth': 0.20,
        'accessory_variety': 0.10,
        'structural_quality': 0.20
    }
    
    # Color harmony reference palettes
    COMPLEMENTARY_PAIRS = [
        ((255, 0, 0), (0, 255, 255)),    # Red - Cyan
        ((0, 255, 0), (255, 0, 255)),    # Green - Magenta
        ((0, 0, 255), (255, 255, 0)),    # Blue - Yellow
        ((255, 128, 0), (0, 128, 255)),  # Orange - Blue
        ((128, 0, 255), (128, 255, 0)),  # Purple - Lime
    ]
    
    def __init__(self):
        self.analysis_results = {}
    
    def analyze_skin_file(self, skin_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform complete analysis of skin data"""
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'skin_name': skin_data.get('name', 'Unknown'),
            'author': skin_data.get('author', 'Unknown'),
            'version': skin_data.get('version', 'Unknown'),
            'scores': {},
            'metrics': {},
            'strengths': [],
            'weaknesses': [],
            'suggestions': [],
            'overall_score': 0.0
        }
        
        # Run all analysis passes
        color_score, color_metrics = self._analyze_colors(skin_data)
        design_score, design_metrics = self._analyze_design_completeness(skin_data)
        animation_score, animation_metrics = self._analyze_animation_readiness(skin_data)
        custom_score, custom_metrics = self._analyze_customization_depth(skin_data)
        accessory_score, accessory_metrics = self._analyze_accessories(skin_data)
        structural_score, structural_metrics = self._analyze_structure(skin_data)
        
        # Store scores
        analysis['scores'] = {
            'color_harmony': color_score,
            'design_completeness': design_score,
            'animation_readiness': animation_score,
            'customization_depth': custom_score,
            'accessory_variety': accessory_score,
            'structural_quality': structural_score
        }
        
        analysis['metrics'] = {
            'color': color_metrics,
            'design': design_metrics,
            'animation': animation_metrics,
            'customization': custom_metrics,
            'accessory': accessory_metrics,
            'structural': structural_metrics
        }
        
        # Calculate weighted overall score
        overall = sum(
            analysis['scores'][key] * self.WEIGHTS[key] 
            for key in self.WEIGHTS
        )
        analysis['overall_score'] = round(overall, 2)
        
        # Generate strengths and weaknesses
        analysis['strengths'] = self._identify_strengths(analysis['scores'], analysis['metrics'])
        analysis['weaknesses'] = self._identify_weaknesses(analysis['scores'], analysis['metrics'])
        analysis['suggestions'] = self._generate_suggestions(analysis['weaknesses'], skin_data)
        
        self.analysis_results = analysis
        return analysis
    
    def _analyze_colors(self, skin_data: Dict) -> Tuple[float, Dict]:
        """Analyze color palette for harmony and variety"""
        colors = skin_data.get('colors', {})
        metrics = {
            'total_colors_defined': len(colors),
            'unique_colors': 0,
            'harmony_score': 0,
            'contrast_score': 0,
            'palette_variety': 0
        }
        
        if not colors:
            return 0.0, metrics
        
        # Extract RGB values (ignore alpha for analysis)
        rgb_colors = []
        for key, value in colors.items():
            if isinstance(value, list) and len(value) >= 3:
                rgb = tuple(value[:3])
                rgb_colors.append(rgb)
        
        unique_colors = len(set(rgb_colors))
        metrics['unique_colors'] = unique_colors
        
        # Score color variety (5-15 unique colors is ideal)
        if unique_colors >= 8 and unique_colors <= 20:
            metrics['palette_variety'] = 1.0
        elif unique_colors >= 5:
            metrics['palette_variety'] = 0.7
        elif unique_colors >= 3:
            metrics['palette_variety'] = 0.4
        else:
            metrics['palette_variety'] = 0.2
        
        # Check for complementary color pairs
        harmony_count = 0
        for pair in self.COMPLEMENTARY_PAIRS:
            for color in rgb_colors:
                # Simple color distance check for complementary
                dist = sum((a - b) ** 2 for a, b in zip(color, pair[0]))
                if dist < 5000:  # Close to first color
                    # Check if complementary exists
                    for other in rgb_colors:
                        dist2 = sum((a - b) ** 2 for a, b in zip(other, pair[1]))
                        if dist2 < 5000:
                            harmony_count += 1
                            break
        
        metrics['harmony_score'] = min(1.0, harmony_count / 3.0)
        
        # Contrast analysis
        if rgb_colors:
            brightness_values = [
                0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2] 
                for c in rgb_colors
            ]
            if brightness_values:
                contrast_range = max(brightness_values) - min(brightness_values)
                metrics['contrast_score'] = min(1.0, contrast_range / 200.0)
        
        # Final color score
        color_score = (
            metrics['palette_variety'] * 0.4 +
            metrics['harmony_score'] * 0.35 +
            metrics['contrast_score'] * 0.25
        )
        
        return round(color_score * 10, 1), metrics
    
    def _analyze_design_completeness(self, skin_data: Dict) -> Tuple[float, Dict]:
        """Check if all design elements are properly defined"""
        required_sections = ['body_scale', 'body_shape', 'limbs', 'head', 'colors']
        optional_sections = ['hair', 'outfit', 'accessories', 'animations', 'particles', 'clothing']
        
        metrics = {
            'required_sections_present': 0,
            'total_required': len(required_sections),
            'optional_sections_present': 0,
            'total_optional': len(optional_sections),
            'has_lua_script': False,
            'has_sprite_data': False,
            'has_animation_frames': False,
            'completeness_percentage': 0
        }
        
        # Check required sections
        for section in required_sections:
            if section in skin_data and skin_data[section]:
                metrics['required_sections_present'] += 1
        
        # Check optional sections
        for section in optional_sections:
            if section in skin_data and skin_data[section]:
                metrics['optional_sections_present'] += 1
        
        # Check for advanced features
        metrics['has_lua_script'] = bool(skin_data.get('lua_script'))
        metrics['has_sprite_data'] = bool(skin_data.get('sprite_data'))
        metrics['has_animation_frames'] = bool(skin_data.get('animation_frames'))
        
        # Calculate completeness
        required_score = metrics['required_sections_present'] / metrics['total_required'] if metrics['total_required'] > 0 else 0
        optional_score = metrics['optional_sections_present'] / metrics['total_optional'] if metrics['total_optional'] > 0 else 0
        
        # Bonus for advanced features
        advanced_bonus = 0
        if metrics['has_lua_script']: advanced_bonus += 0.1
        if metrics['has_sprite_data']: advanced_bonus += 0.15
        if metrics['has_animation_frames']: advanced_bonus += 0.15
        
        metrics['completeness_percentage'] = round(
            (required_score * 0.6 + optional_score * 0.4 + advanced_bonus) * 100, 1
        )
        
        score = min(10.0, (required_score * 6 + optional_score * 2 + advanced_bonus * 2))
        
        return round(score, 1), metrics
    
    def _analyze_animation_readiness(self, skin_data: Dict) -> Tuple[float, Dict]:
        """Analyze if skin is ready for animations"""
        metrics = {
            'has_animations_config': False,
            'idle_speed_defined': False,
            'walk_speed_defined': False,
            'dance_speed_defined': False,
            'blink_rate_defined': False,
            'custom_animations_count': 0,
            'has_animation_frames_data': False,
            'frame_animations_count': 0
        }
        
        animations = skin_data.get('animations', {})
        if animations:
            metrics['has_animations_config'] = True
            metrics['idle_speed_defined'] = 'idle_speed' in animations
            metrics['walk_speed_defined'] = 'walk_speed' in animations
            metrics['dance_speed_defined'] = 'dance_speed' in animations
            metrics['blink_rate_defined'] = 'blink_rate' in animations
            
            custom_anims = animations.get('custom_animations', {})
            metrics['custom_animations_count'] = len(custom_anims)
        
        # Check animation frames
        animation_frames = skin_data.get('animation_frames', {})
        if animation_frames:
            metrics['has_animation_frames_data'] = True
            metrics['frame_animations_count'] = len(animation_frames)
        
        # Scoring
        score = 0.0
        
        # Base config score
        if metrics['has_animations_config']:
            score += 3.0
            config_details = sum([
                metrics['idle_speed_defined'],
                metrics['walk_speed_defined'],
                metrics['dance_speed_defined'],
                metrics['blink_rate_defined']
            ])
            score += config_details * 0.75
        
        # Custom animations bonus
        score += min(3.0, metrics['custom_animations_count'] * 1.0)
        
        # Frame animations bonus (high value)
        if metrics['has_animation_frames_data']:
            score += min(4.0, metrics['frame_animations_count'] * 1.5)
        
        return round(min(10.0, score), 1), metrics
    
    def _analyze_customization_depth(self, skin_data: Dict) -> Tuple[float, Dict]:
        """Analyze how customizable the skin is"""
        metrics = {
            'body_scale_options': 0,
            'body_shape_options': 0,
            'limb_customization': 0,
            'head_customization': 0,
            'hair_styles': 0,
            'outfit_options': 0,
            'accessory_slots': 0,
            'color_customization': 0,
            'total_customization_points': 0
        }
        
        # Body scale
        body_scale = skin_data.get('body_scale', {})
        metrics['body_scale_options'] = len([k for k, v in body_scale.items() if v != 1.0])
        
        # Body shape
        body_shape = skin_data.get('body_shape', {})
        metrics['body_shape_options'] = len(body_shape)
        
        # Limbs
        limbs = skin_data.get('limbs', {})
        metrics['limb_customization'] = len(limbs)
        
        # Head
        head = skin_data.get('head', {})
        metrics['head_customization'] = len(head)
        
        # Hair
        hair = skin_data.get('hair', {})
        metrics['hair_styles'] = 1 if hair else 0
        
        # Outfit
        outfit = skin_data.get('outfit', {})
        metrics['outfit_options'] = len(outfit)
        
        # Accessories
        accessories = skin_data.get('accessories', {})
        non_none = [k for k, v in accessories.items() if v is not None]
        metrics['accessory_slots'] = len(non_none)
        
        # Colors
        colors = skin_data.get('colors', {})
        metrics['color_customization'] = len(colors)
        
        # Total
        metrics['total_customization_points'] = sum([
            metrics['body_scale_options'],
            metrics['body_shape_options'],
            metrics['limb_customization'],
            metrics['head_customization'],
            metrics['hair_styles'],
            metrics['outfit_options'],
            metrics['accessory_slots'],
            metrics['color_customization']
        ])
        
        # Score based on total customization
        if metrics['total_customization_points'] >= 30:
            score = 10.0
        elif metrics['total_customization_points'] >= 20:
            score = 8.0
        elif metrics['total_customization_points'] >= 15:
            score = 6.0
        elif metrics['total_customization_points'] >= 10:
            score = 4.0
        else:
            score = 2.0
        
        return score, metrics
    
    def _analyze_accessories(self, skin_data: Dict) -> Tuple[float, Dict]:
        """Analyze accessory variety and quality"""
        accessories = skin_data.get('accessories', {})
        
        metrics = {
            'total_accessories': 0,
            'accessory_types': [],
            'has_hat': False,
            'has_glasses': False,
            'has_scarf': False,
            'has_shoes': False,
            'has_wings': False,
            'has_tail': False,
            'custom_accessories_count': 0
        }
        
        accessory_slots = ['hat', 'glasses', 'scarf', 'shoes', 'wings', 'tail_type']
        for slot in accessory_slots:
            value = accessories.get(slot)
            if value is not None and value != '':
                metrics['total_accessories'] += 1
                metrics['accessory_types'].append(slot)
                metrics[f'has_{slot}'] = True
        
        custom = accessories.get('custom_accessories', [])
        metrics['custom_accessories_count'] = len(custom)
        metrics['total_accessories'] += metrics['custom_accessories_count']
        
        # Score
        if metrics['total_accessories'] >= 5:
            score = 10.0
        elif metrics['total_accessories'] >= 3:
            score = 7.0
        elif metrics['total_accessories'] >= 2:
            score = 5.0
        elif metrics['total_accessories'] >= 1:
            score = 3.0
        else:
            score = 1.0
        
        return score, metrics
    
    def _analyze_structure(self, skin_data: Dict) -> Tuple[float, Dict]:
        """Analyze structural integrity of skin data"""
        metrics = {
            'has_name': False,
            'has_version': False,
            'has_author': False,
            'has_description': False,
            'has_lua_script': False,
            'lua_script_length': 0,
            'json_structure_valid': True,
            'total_keys': len(skin_data),
            'data_depth': 0
        }
        
        metrics['has_name'] = bool(skin_data.get('name'))
        metrics['has_version'] = bool(skin_data.get('version'))
        metrics['has_author'] = bool(skin_data.get('author'))
        metrics['has_description'] = bool(skin_data.get('description'))
        
        lua = skin_data.get('lua_script', '')
        metrics['has_lua_script'] = bool(lua)
        metrics['lua_script_length'] = len(lua)
        
        # Calculate data depth
        metrics['data_depth'] = self._calculate_depth(skin_data)
        
        # Score
        score = 0.0
        
        # Metadata score
        metadata_points = sum([
            metrics['has_name'],
            metrics['has_version'],
            metrics['has_author'],
            metrics['has_description']
        ])
        score += metadata_points * 1.5
        
        # Lua script score
        if metrics['has_lua_script']:
            if metrics['lua_script_length'] > 500:
                score += 3.0
            elif metrics['lua_script_length'] > 200:
                score += 2.0
            else:
                score += 1.0
        
        # Data complexity score
        if metrics['data_depth'] >= 4:
            score += 1.0
        
        return round(min(10.0, score), 1), metrics
    
    def _calculate_depth(self, data: Any, current_depth: int = 0) -> int:
        """Calculate maximum nesting depth of data structure"""
        if not isinstance(data, dict):
            return current_depth
        
        if not data:
            return current_depth
        
        max_depth = current_depth
        for value in data.values():
            if isinstance(value, dict):
                depth = self._calculate_depth(value, current_depth + 1)
                max_depth = max(max_depth, depth)
            elif isinstance(value, list) and value and isinstance(value[0], dict):
                depth = self._calculate_depth(value[0], current_depth + 2)
                max_depth = max(max_depth, depth)
        
        return max_depth
    
    def _identify_strengths(self, scores: Dict, metrics: Dict) -> List[str]:
        """Identify skin strengths based on analysis"""
        strengths = []
        
        if scores.get('color_harmony', 0) >= 7.0:
            strengths.append("Excellent color palette with good harmony and contrast")
        elif scores.get('color_harmony', 0) >= 5.0:
            strengths.append("Solid color choices that work well together")
        
        if scores.get('design_completeness', 0) >= 8.0:
            strengths.append("Highly complete design with all major sections filled out")
        elif scores.get('design_completeness', 0) >= 6.0:
            strengths.append("Good design foundation with most elements defined")
        
        if scores.get('animation_readiness', 0) >= 7.0:
            strengths.append("Well-prepared for animations with good configuration")
        
        if scores.get('customization_depth', 0) >= 7.0:
            strengths.append("Deep customization options allowing unique character creation")
        
        if scores.get('accessory_variety', 0) >= 6.0:
            strengths.append("Nice variety of accessories for character personalization")
        
        if scores.get('structural_quality', 0) >= 7.0:
            strengths.append("Well-structured skin data with good metadata")
        
        if not strengths:
            strengths.append("Functional skin with basic features implemented")
        
        return strengths
    
    def _identify_weaknesses(self, scores: Dict, metrics: Dict) -> List[str]:
        """Identify skin weaknesses based on analysis"""
        weaknesses = []
        
        if scores.get('color_harmony', 0) < 4.0:
            weaknesses.append("Color palette could use more variety and harmony")
        
        if scores.get('design_completeness', 0) < 5.0:
            weaknesses.append("Missing several important design sections")
        
        if scores.get('animation_readiness', 0) < 4.0:
            weaknesses.append("Limited animation configuration - animations may not work well")
        
        if scores.get('customization_depth', 0) < 5.0:
            weaknesses.append("Limited customization options for users")
        
        if scores.get('accessory_variety', 0) < 4.0:
            weaknesses.append("Few or no accessories defined")
        
        if scores.get('structural_quality', 0) < 5.0:
            weaknesses.append("Missing metadata (name, author, version) - harder to identify and manage")
        
        if not weaknesses:
            weaknesses.append("Minor refinements could elevate this skin further")
        
        return weaknesses
    
    def _generate_suggestions(self, weaknesses: List[str], skin_data: Dict) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        for weakness in weaknesses:
            if "color" in weakness.lower():
                suggestions.append("Try using complementary color pairs like blue-orange or purple-yellow")
                suggestions.append("Add more color variations for different body parts")
            elif "missing" in weakness.lower() or "design" in weakness.lower():
                suggestions.append("Fill out the head, hair, and outfit sections for a complete look")
                suggestions.append("Define animation speeds and blink rates")
            elif "animation" in weakness.lower():
                suggestions.append("Add custom animation frames for unique character movements")
                suggestions.append("Configure animation speeds for idle, walk, and dance states")
            elif "customization" in weakness.lower():
                suggestions.append("Add more body scale and shape options")
                suggestions.append("Include custom drawing modifications for uniqueness")
            elif "accessories" in weakness.lower():
                suggestions.append("Add hats, glasses, or wings to make the character stand out")
                suggestions.append("Define custom accessories for unique character features")
            elif "metadata" in weakness.lower():
                suggestions.append("Add skin name, version, author, and description")
        
        if not suggestions:
            suggestions.append("Consider adding a Lua script for custom behaviors")
            suggestions.append("Add particle effects for more visual appeal")
        
        return suggestions[:8]  # Limit to top 8 suggestions