import colorsys
import math
from typing import List, Tuple, Dict

def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[int, int, int]:
    """Convert RGB to HSL"""
    h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)
    return (int(h*360), int(s*100), int(l*100))

def rgb_to_cmyk(r: int, g: int, b: int) -> Tuple[int, int, int, int]:
    """Convert RGB to CMYK"""
    if r == 0 and g == 0 and b == 0:
        return (0, 0, 0, 100)
    
    r, g, b = r/255.0, g/255.0, b/255.0
    k = 1 - max(r, g, b)
    c = (1-r-k) / (1-k) if (1-k) != 0 else 0
    m = (1-g-k) / (1-k) if (1-k) != 0 else 0
    y = (1-b-k) / (1-k) if (1-k) != 0 else 0
    
    return (int(c*100), int(m*100), int(y*100), int(k*100))

def rgb_to_lab(r: int, g: int, b: int) -> Tuple[int, int, int]:
    """Convert RGB to LAB (simplified approximation)"""
    # Simplified LAB conversion for demonstration
    r, g, b = r/255.0, g/255.0, b/255.0
    
    # Convert to XYZ first (simplified)
    x = r * 0.4124 + g * 0.3576 + b * 0.1805
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = r * 0.0193 + g * 0.1192 + b * 0.9505
    
    # Convert to LAB (simplified)
    l = int(116 * (y ** (1/3)) - 16) if y > 0.008856 else int(903.3 * y)
    a = int(500 * ((x ** (1/3)) - (y ** (1/3))))
    b_lab = int(200 * ((y ** (1/3)) - (z ** (1/3))))
    
    return (max(0, min(100, l)), max(-128, min(127, a)), max(-128, min(127, b_lab)))

class GoetheFarbenlehre:
    """Goethe's Color Theory - psychological and aesthetic color analysis"""
    
    COLOR_EMOTIONS = {
        # Warme Farben - Goethe's active side
        'red': {'emotion': 'Kraft, Leidenschaft, Energie', 'character': 'Aktiv, Anregend', 'effect': 'Stimulierend'},
        'orange': {'emotion': 'Freude, Wärme, Optimismus', 'character': 'Lebhaft, Gesellig', 'effect': 'Belebend'},
        'yellow': {'emotion': 'Heiterkeit, Verstand, Erleuchtung', 'character': 'Heiter, Warm', 'effect': 'Erhebend'},
        
        # Kalte Farben - Goethe's passive side  
        'blue': {'emotion': 'Ruhe, Tiefe, Melancholie', 'character': 'Passiv, Beruhigend', 'effect': 'Besänftigend'},
        'violet': {'emotion': 'Mystik, Spiritualität, Würde', 'character': 'Unruhig, Sehnsüchtig', 'effect': 'Nachdenklich'},
        'green': {'emotion': 'Zufriedenheit, Ruhe, Natur', 'character': 'Neutral, Ausgleichend', 'effect': 'Beruhigend'},
    }
    
    @staticmethod
    def analyze_color_psychology(rgb: Tuple[int, int, int]) -> Dict[str, str]:
        """Analyze color according to Goethe's color psychology"""
        r, g, b = rgb
        h, s, l = rgb_to_hsl(r, g, b)
        
        # Determine dominant color category
        if h < 15 or h >= 345:  # Red
            base_color = 'red'
        elif h < 45:  # Orange
            base_color = 'orange'  
        elif h < 75:  # Yellow
            base_color = 'yellow'
        elif h < 150:  # Green
            base_color = 'green'
        elif h < 250:  # Blue
            base_color = 'blue'
        else:  # Violet
            base_color = 'violet'
            
        analysis = GoetheFarbenlehre.COLOR_EMOTIONS.get(base_color, {
            'emotion': 'Neutral', 'character': 'Ausgeglichen', 'effect': 'Harmonisch'
        })
        
        # Modify based on saturation and lightness
        if s < 30:
            analysis['character'] += ', Gedämpft'
        if l > 80:
            analysis['effect'] += ', Sanft'
        elif l < 20:
            analysis['effect'] += ', Intensiv'
            
        return analysis

class IttenFarbkreis:
    """Johannes Itten's Color Theory - systematic color relationships"""
    
    @staticmethod
    def get_complementary_color(rgb: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Get complementary color according to Itten's color wheel"""
        r, g, b = rgb
        h, s, l = rgb_to_hsl(r, g, b)
        
        # Complementary is 180° opposite
        comp_h = (h + 180) % 360
        comp_r, comp_g, comp_b = colorsys.hls_to_rgb(comp_h/360, l/100, s/100)
        
        return (int(comp_r*255), int(comp_g*255), int(comp_b*255))
    
    @staticmethod
    def get_triadic_colors(rgb: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
        """Get triadic colors (120° apart) according to Itten"""
        r, g, b = rgb
        h, s, l = rgb_to_hsl(r, g, b)
        
        triadic = []
        for offset in [120, 240]:
            new_h = (h + offset) % 360
            new_r, new_g, new_b = colorsys.hls_to_rgb(new_h/360, l/100, s/100)
            triadic.append((int(new_r*255), int(new_g*255), int(new_b*255)))
            
        return triadic
    
    @staticmethod
    def get_analogous_colors(rgb: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
        """Get analogous colors (30° adjacent) according to Itten"""
        r, g, b = rgb
        h, s, l = rgb_to_hsl(r, g, b)
        
        analogous = []
        for offset in [-30, 30]:
            new_h = (h + offset) % 360
            new_r, new_g, new_b = colorsys.hls_to_rgb(new_h/360, l/100, s/100)
            analogous.append((int(new_r*255), int(new_g*255), int(new_b*255)))
            
        return analogous

class ColorBlindnessSimulator:
    """Simulate different types of color blindness"""
    
    @staticmethod
    def simulate_protanopia(rgb: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Simulate red color blindness (Protanopia)"""
        r, g, b = rgb
        # Simplified protanopia simulation
        new_r = int(0.567 * r + 0.433 * g)
        new_g = int(0.558 * r + 0.442 * g) 
        new_b = int(0.242 * g + 0.758 * b)
        return (min(255, new_r), min(255, new_g), min(255, new_b))
    
    @staticmethod
    def simulate_deuteranopia(rgb: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Simulate green color blindness (Deuteranopia)"""
        r, g, b = rgb
        # Simplified deuteranopia simulation
        new_r = int(0.625 * r + 0.375 * g)
        new_g = int(0.7 * r + 0.3 * g)
        new_b = int(0.3 * g + 0.7 * b)
        return (min(255, new_r), min(255, new_g), min(255, new_b))
    
    @staticmethod
    def simulate_tritanopia(rgb: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Simulate blue color blindness (Tritanopia)"""
        r, g, b = rgb
        # Simplified tritanopia simulation  
        new_r = int(0.95 * r + 0.05 * g)
        new_g = int(0.433 * g + 0.567 * b)
        new_b = int(0.475 * g + 0.525 * b)
        return (min(255, new_r), min(255, new_g), min(255, new_b))

def get_comprehensive_color_analysis(rgb: Tuple[int, int, int]) -> Dict:
    """Get comprehensive color analysis combining all theories"""
    r, g, b = rgb
    
    analysis = {
        'basic': {
            'hex': f'#{r:02x}{g:02x}{b:02x}'.upper(),
            'rgb': f'RGB({r}, {g}, {b})',
            'hsl': f'HSL{rgb_to_hsl(r, g, b)}',
            'cmyk': f'CMYK{rgb_to_cmyk(r, g, b)}',
            'lab': f'LAB{rgb_to_lab(r, g, b)}'
        },
        'goethe': GoetheFarbenlehre.analyze_color_psychology(rgb),
        'itten': {
            'complementary': IttenFarbkreis.get_complementary_color(rgb),
            'triadic': IttenFarbkreis.get_triadic_colors(rgb),
            'analogous': IttenFarbkreis.get_analogous_colors(rgb)
        }
    }
    
    return analysis 