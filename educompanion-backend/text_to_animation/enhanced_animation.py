"""
Enhanced animation module for creating sophisticated animated videos
Includes advanced slide generation, transitions, visual effects, and scene management
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from moviepy.editor import (
    ImageClip, AudioFileClip, VideoFileClip, CompositeVideoClip,
    concatenate_videoclips, ColorClip, TextClip
)
from moviepy.video.fx import fadein, fadeout, resize
from moviepy.video.fx.accel_decel import accel_decel
from typing import List, Dict, Tuple, Optional
import logging
from dataclasses import dataclass
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import io

@dataclass
class SlideConfig:
    """Configuration for individual slides"""
    text: str
    duration: float
    background_color: Tuple[int, int, int]
    text_color: Tuple[int, int, int]
    font_size: int
    animation_type: str = "fade"
    highlight_keywords: List[str] = None

@dataclass
class VideoConfig:
    """Configuration for video generation"""
    resolution: Tuple[int, int]
    fps: int
    background_color: Tuple[int, int, int]
    transition_duration: float
    slide_duration: float

class AdvancedSlideGenerator:
    """Generate sophisticated animated slides"""
    
    def __init__(self, config: dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.resolution = (
            config.get('resolution', {}).get('width', 1280),
            config.get('resolution', {}).get('height', 720)
        )
        self.font_cache = {}
    
    def _load_font(self, font_path: Optional[str], size: int) -> ImageFont.FreeTypeFont:
        """Load and cache fonts"""
        cache_key = (font_path, size)
        if cache_key in self.font_cache:
            return self.font_cache[cache_key]
        
        try:
            if font_path and os.path.exists(font_path):
                font = ImageFont.truetype(font_path, size)
            else:
                # Try to load a system font
                try:
                    font = ImageFont.truetype("arial.ttf", size)
                except:
                    try:
                        font = ImageFont.truetype("DejaVuSans.ttf", size)
                    except:
                        font = ImageFont.load_default()
        except Exception as e:
            self.logger.warning(f"Could not load font: {e}")
            font = ImageFont.load_default()
        
        self.font_cache[cache_key] = font
        return font
    
    def _wrap_text(self, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> List[str]:
        """Wrap text to fit within specified width"""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = font.getbbox(test_line)
            text_width = bbox[2] - bbox[0]
            
            if text_width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    # Word is too long, split it
                    lines.append(word)
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
    def _highlight_keywords(self, text: str, keywords: List[str]) -> List[Tuple[str, bool]]:
        """Mark keywords in text for highlighting"""
        if not keywords:
            return [(text, False)]
        
        # Simple keyword highlighting
        result = []
        remaining_text = text
        
        for keyword in keywords:
            if keyword.lower() in remaining_text.lower():
                parts = remaining_text.lower().split(keyword.lower())
                if len(parts) > 1:
                    # Add text before keyword
                    if parts[0]:
                        result.append((remaining_text[:len(parts[0])], False))
                    
                    # Add keyword (highlighted)
                    keyword_start = len(parts[0])
                    keyword_end = keyword_start + len(keyword)
                    result.append((remaining_text[keyword_start:keyword_end], True))
                    
                    # Continue with remaining text
                    remaining_text = remaining_text[keyword_end:]
        
        if remaining_text:
            result.append((remaining_text, False))
        
        return result if result else [(text, False)]
    
    def create_gradient_background(self, size: Tuple[int, int], 
                                 color1: Tuple[int, int, int], 
                                 color2: Tuple[int, int, int]) -> Image.Image:
        """Create a gradient background"""
        width, height = size
        image = Image.new('RGB', size)
        
        for y in range(height):
            ratio = y / height
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            
            for x in range(width):
                image.putpixel((x, y), (r, g, b))
        
        return image
    
    def create_slide_with_effects(self, slide_config: SlideConfig, output_path: str) -> str:
        """Create an enhanced slide with visual effects"""
        width, height = self.resolution
        
        # Create background
        if self.config.get('use_gradient', False):
            bg_color2 = tuple(max(0, min(255, c + 20)) for c in slide_config.background_color)
            image = self.create_gradient_background((width, height), 
                                                  slide_config.background_color, bg_color2)
        else:
            image = Image.new('RGB', (width, height), slide_config.background_color)
        
        draw = ImageDraw.Draw(image)
        
        # Load font
        font_path = self.config.get('font', {}).get('family')
        font = self._load_font(font_path, slide_config.font_size)
        
        # Text wrapping
        margin = self.config.get('slides', {}).get('margin', 40)
        max_width = width - 2 * margin
        lines = self._wrap_text(slide_config.text, font, max_width)
        
        # Calculate text positioning
        line_height = slide_config.font_size + self.config.get('font', {}).get('line_spacing', 8)
        total_text_height = len(lines) * line_height
        start_y = (height - total_text_height) // 2
        
        # Highlight keywords if specified
        if slide_config.highlight_keywords:
            highlighted_text = self._highlight_keywords(slide_config.text, slide_config.highlight_keywords)
        else:
            highlighted_text = [(slide_config.text, False)]
        
        # Draw text with highlighting
        current_y = start_y
        for line in lines:
            # Simple approach: draw entire line, then highlight keywords
            line_bbox = font.getbbox(line)
            line_width = line_bbox[2] - line_bbox[0]
            x = (width - line_width) // 2  # Center align
            
            # Draw main text
            draw.text((x, current_y), line, fill=slide_config.text_color, font=font)
            
            # Add keyword highlighting (simple version)
            if slide_config.highlight_keywords:
                for keyword in slide_config.highlight_keywords:
                    if keyword.lower() in line.lower():
                        # Draw highlight background
                        keyword_bbox = font.getbbox(keyword)
                        keyword_width = keyword_bbox[2] - keyword_bbox[0]
                        keyword_x = x + line.lower().find(keyword.lower()) * (line_width // len(line))
                        
                        # Highlight background
                        highlight_color = (255, 255, 0, 128)  # Yellow with transparency
                        highlight_rect = Image.new('RGBA', (keyword_width + 4, line_height), highlight_color)
                        image.paste(highlight_rect, (keyword_x - 2, current_y - 2), highlight_rect)
            
            current_y += line_height
        
        # Add decorative elements
        if self.config.get('add_decorations', True):
            self._add_decorative_elements(draw, width, height)
        
        # Apply effects
        if self.config.get('apply_effects', True):
            image = self._apply_image_effects(image)
        
        image.save(output_path, quality=95)
        return output_path
    
    def _add_decorative_elements(self, draw: ImageDraw.Draw, width: int, height: int):
        """Add decorative elements to the slide"""
        # Add subtle border
        border_color = (200, 200, 200)
        border_width = 2
        draw.rectangle([border_width, border_width, 
                       width - border_width, height - border_width], 
                      outline=border_color, width=border_width)
        
        # Add corner elements
        corner_size = 20
        corner_color = (150, 150, 150)
        
        # Top-left corner
        draw.line([10, 10, 10 + corner_size, 10], fill=corner_color, width=3)
        draw.line([10, 10, 10, 10 + corner_size], fill=corner_color, width=3)
        
        # Top-right corner
        draw.line([width - 10 - corner_size, 10, width - 10, 10], fill=corner_color, width=3)
        draw.line([width - 10, 10, width - 10, 10 + corner_size], fill=corner_color, width=3)
        
        # Bottom-left corner
        draw.line([10, height - 10 - corner_size, 10, height - 10], fill=corner_color, width=3)
        draw.line([10, height - 10, 10 + corner_size, height - 10], fill=corner_color, width=3)
        
        # Bottom-right corner
        draw.line([width - 10 - corner_size, height - 10, width - 10, height - 10], fill=corner_color, width=3)
        draw.line([width - 10, height - 10 - corner_size, width - 10, height - 10], fill=corner_color, width=3)
    
    def _apply_image_effects(self, image: Image.Image) -> Image.Image:
        """Apply subtle visual effects to the image"""
        # Slight blur for smoothness
        image = image.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        # Enhance contrast slightly
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.1)
        
        return image

class AdvancedVideoGenerator:
    """Generate sophisticated animated videos with transitions"""
    
    def __init__(self, config: dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.slide_generator = AdvancedSlideGenerator(config)
    
    def create_transition_clip(self, duration: float, transition_type: str = "fade") -> VideoFileClip:
        """Create transition effects between slides"""
        width, height = (
            self.config.get('resolution', {}).get('width', 1280),
            self.config.get('resolution', {}).get('height', 720)
        )
        
        if transition_type == "fade":
            # Simple fade transition using ColorClip
            return ColorClip(size=(width, height), color=(0, 0, 0)).set_duration(duration)
        
        # Add more transition types as needed
        return ColorClip(size=(width, height), color=(0, 0, 0)).set_duration(duration)
    
    def create_animated_text_clip(self, text: str, duration: float, 
                                animation_type: str = "typewriter") -> VideoFileClip:
        """Create animated text clips"""
        if animation_type == "typewriter":
            # Create typewriter effect using TextClip
            clip = TextClip(text, fontsize=50, color='white', font='Arial')
            clip = clip.set_duration(duration)
            
            # Add typewriter animation (simplified)
            return clip.fx(fadein, 0.5).fx(fadeout, 0.5)
        
        # Default: simple text clip
        clip = TextClip(text, fontsize=50, color='white', font='Arial')
        return clip.set_duration(duration).fx(fadein, 0.5).fx(fadeout, 0.5)
    
    def split_text_into_slides(self, text: str, keywords: List[str] = None) -> List[SlideConfig]:
        """Split text into multiple slide configurations"""
        max_chars = self.config.get('slides', {}).get('max_chars_per_slide', 220)
        sentences = text.split('. ')
        
        slides = []
        current_slide_text = ""
        slide_duration = self.config.get('slide_duration', 4.0)
        
        # Default colors from config
        bg_color = tuple(self.config.get('background_color', [255, 255, 255]))
        text_color = tuple(self.config.get('text_color', [0, 0, 0]))
        font_size = self.config.get('font', {}).get('size', 36)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Add period back if it doesn't end with punctuation
            if not sentence.endswith(('.', '!', '?')):
                sentence += '.'
            
            if len(current_slide_text + ' ' + sentence) <= max_chars:
                current_slide_text += (' ' if current_slide_text else '') + sentence
            else:
                if current_slide_text:
                    slides.append(SlideConfig(
                        text=current_slide_text,
                        duration=slide_duration,
                        background_color=bg_color,
                        text_color=text_color,
                        font_size=font_size,
                        animation_type=self.config.get('animation_style', 'fade'),
                        highlight_keywords=keywords
                    ))
                current_slide_text = sentence
        
        # Add the last slide
        if current_slide_text:
            slides.append(SlideConfig(
                text=current_slide_text,
                duration=slide_duration,
                background_color=bg_color,
                text_color=text_color,
                font_size=font_size,
                animation_type=self.config.get('animation_style', 'fade'),
                highlight_keywords=keywords
            ))
        
        return slides
    
    def create_video_from_slides(self, slide_configs: List[SlideConfig], 
                               audio_path: Optional[str], output_path: str) -> str:
        """Create final video with advanced transitions and effects"""
        temp_dir = self.config.get('temp_directory', 'ttm_tmp')
        os.makedirs(temp_dir, exist_ok=True)
        
        # Generate slide images
        slide_paths = []
        for i, slide_config in enumerate(slide_configs):
            slide_path = os.path.join(temp_dir, f'enhanced_slide_{i}.png')
            self.slide_generator.create_slide_with_effects(slide_config, slide_path)
            slide_paths.append(slide_path)
        
        # Create video clips
        clips = []
        transition_duration = self.config.get('transition_duration', 0.5)
        
        for i, (slide_path, slide_config) in enumerate(zip(slide_paths, slide_configs)):
            # Create main slide clip
            clip = ImageClip(slide_path).set_duration(slide_config.duration)
            
            # Add animation effects based on type
            if slide_config.animation_type == "fade":
                clip = clip.fx(fadein, transition_duration).fx(fadeout, transition_duration)
            elif slide_config.animation_type == "slide":
                # Add slide-in effect
                clip = clip.fx(accel_decel)
            elif slide_config.animation_type == "zoom":
                # Add zoom effect
                clip = clip.fx(resize, lambda t: 1 + 0.1 * t)
            
            clips.append(clip)
            
            # Add transition between slides (except for the last one)
            if i < len(slide_paths) - 1 and self.config.get('scene_transitions', True):
                transition = self.create_transition_clip(transition_duration)
                clips.append(transition)
        
        # Concatenate all clips
        final_video = concatenate_videoclips(clips, method='compose')
        
        # Add audio if provided
        if audio_path and os.path.exists(audio_path):
            audio = AudioFileClip(audio_path)
            
            # Adjust video duration to match audio
            if final_video.duration < audio.duration:
                # Extend last slide
                last_slide = clips[-1]
                extension_duration = audio.duration - final_video.duration
                extended_last = last_slide.fx(lambda c: c).set_duration(
                    last_slide.duration + extension_duration
                )
                
                # Recreate video with extended last slide
                clips[-1] = extended_last
                final_video = concatenate_videoclips(clips, method='compose')
            
            final_video = final_video.set_audio(audio)
        
        # Write final video
        fps = self.config.get('fps', 24)
        codec = self.config.get('video_codec', 'libx264')
        audio_codec = self.config.get('audio_codec', 'aac')
        
        final_video.write_videofile(
            output_path,
            fps=fps,
            codec=codec,
            audio_codec=audio_codec,
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        return output_path

def create_animation_engine(config: dict) -> AdvancedVideoGenerator:
    """Factory function to create animation engine with configuration"""
    return AdvancedVideoGenerator(config)
