"""
Ölfarben-Datenbank für FARBDIEB
Pigment-basierte Farbmischungen und professionelle Malfarben-Informationen
"""

import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class OilPaint:
    """Repräsentiert eine spezifische Ölfarbe"""
    name: str
    pigment: str
    rgb: Tuple[int, int, int]
    opacity: str  # "transparent", "semi-opaque", "opaque"
    drying_time: str  # "fast", "medium", "slow"
    lightfastness: int  # 1-4 (4 = excellent)
    price_category: str  # "student", "artist", "professional"
    brand: str
    series: int  # Paint series number
    mixing_ratio: Optional[str] = None  # Für Mischungen

# Grundfarben-Palette - Traditionelle Künstlerpigmente
BASIC_OIL_PAINTS = {
    # Weiß
    (255, 255, 255): OilPaint(
        "Titanweiß", "PW6", (255, 255, 255), 
        "opaque", "medium", 4, "artist", "Schmincke", 1
    ),
    (252, 252, 250): OilPaint(
        "Zinkweiß", "PW4", (252, 252, 250), 
        "semi-opaque", "slow", 4, "artist", "Schmincke", 1
    ),
    
    # Schwarz
    (0, 0, 0): OilPaint(
        "Elfenbeinschwarz", "PBk9", (0, 0, 0), 
        "opaque", "slow", 4, "artist", "Schmincke", 1
    ),
    (25, 25, 28): OilPaint(
        "Paynesgrau", "PB15+PBk6", (25, 25, 28), 
        "transparent", "medium", 4, "artist", "Schmincke", 2
    ),
    
    # Rot
    (227, 18, 48): OilPaint(
        "Kadmiumrot dunkel", "PR108", (227, 18, 48), 
        "opaque", "medium", 4, "professional", "Schmincke", 3
    ),
    (238, 49, 36): OilPaint(
        "Kadmiumrot hell", "PR108", (238, 49, 36), 
        "opaque", "medium", 4, "professional", "Schmincke", 3
    ),
    (169, 17, 1): OilPaint(
        "Englischrot", "PR101", (169, 17, 1), 
        "opaque", "fast", 4, "artist", "Schmincke", 1
    ),
    (221, 65, 36): OilPaint(
        "Zinnoberrot", "PR108", (221, 65, 36), 
        "opaque", "medium", 3, "artist", "Schmincke", 2
    ),
    (178, 34, 52): OilPaint(
        "Alizarinkarmin", "PR83", (178, 34, 52), 
        "transparent", "slow", 3, "artist", "Schmincke", 2
    ),
    
    # Gelb
    (255, 237, 0): OilPaint(
        "Kadmiumgelb hell", "PY35", (255, 237, 0), 
        "opaque", "medium", 4, "professional", "Schmincke", 3
    ),
    (255, 205, 0): OilPaint(
        "Kadmiumgelb mittel", "PY35", (255, 205, 0), 
        "opaque", "medium", 4, "professional", "Schmincke", 3
    ),
    (227, 168, 87): OilPaint(
        "Neapelgelb", "PW4+PY42", (227, 168, 87), 
        "opaque", "medium", 4, "artist", "Schmincke", 2
    ),
    (252, 232, 131): OilPaint(
        "Hansagelb", "PY3", (252, 232, 131), 
        "transparent", "fast", 3, "artist", "Schmincke", 1
    ),
    (184, 134, 11): OilPaint(
        "Ockergelb", "PY43", (184, 134, 11), 
        "opaque", "fast", 4, "artist", "Schmincke", 1
    ),
    
    # Blau
    (0, 49, 83): OilPaint(
        "Preußischblau", "PB27", (0, 49, 83), 
        "transparent", "fast", 4, "artist", "Schmincke", 1
    ),
    (0, 56, 168): OilPaint(
        "Ultramarienblau", "PB29", (0, 56, 168), 
        "transparent", "slow", 4, "artist", "Schmincke", 1
    ),
    (91, 143, 175): OilPaint(
        "Coelinblau", "PB35", (91, 143, 175), 
        "semi-opaque", "medium", 4, "artist", "Schmincke", 2
    ),
    (41, 171, 226): OilPaint(
        "Phthaloblau", "PB15", (41, 171, 226), 
        "transparent", "medium", 4, "artist", "Schmincke", 2
    ),
    
    # Grün
    (18, 53, 36): OilPaint(
        "Viridian", "PG18", (18, 53, 36), 
        "transparent", "slow", 4, "artist", "Schmincke", 2
    ),
    (0, 158, 73): OilPaint(
        "Phthalogrün", "PG7", (0, 158, 73), 
        "transparent", "medium", 4, "artist", "Schmincke", 2
    ),
    (115, 147, 77): OilPaint(
        "Chromoxidgrün", "PG17", (115, 147, 77), 
        "opaque", "fast", 4, "artist", "Schmincke", 1
    ),
    
    # Erdfarben
    (121, 85, 72): OilPaint(
        "Umbra gebrannt", "PBr7", (121, 85, 72), 
        "transparent", "fast", 4, "artist", "Schmincke", 1
    ),
    (115, 74, 18): OilPaint(
        "Umbra natur", "PBr7", (115, 74, 18), 
        "transparent", "fast", 4, "artist", "Schmincke", 1
    ),
    (138, 54, 15): OilPaint(
        "Sienna gebrannt", "PBr7", (138, 54, 15), 
        "transparent", "fast", 4, "artist", "Schmincke", 1
    ),
    (160, 82, 45): OilPaint(
        "Sienna natur", "PBr7", (160, 82, 45), 
        "transparent", "fast", 4, "artist", "Schmincke", 1
    ),
    
    # Violett
    (92, 51, 23): OilPaint(
        "Vandyckbraun", "PBr8", (92, 51, 23), 
        "transparent", "fast", 4, "artist", "Schmincke", 1
    ),
    (128, 100, 162): OilPaint(
        "Ultramarinviolett", "PV15", (128, 100, 162), 
        "transparent", "slow", 4, "artist", "Schmincke", 2
    ),
    (146, 39, 143): OilPaint(
        "Dioxazinlila", "PV23", (146, 39, 143), 
        "transparent", "medium", 4, "artist", "Schmincke", 2
    )
}

# Mischungsrezepte für komplexe Farben
MIXING_RECIPES = {
    # Grau-Mischungen
    "Neutralgrau": {
        "components": ["Titanweiß", "Elfenbeinschwarz"],
        "ratios": [3, 1],
        "description": "Klassisches neutrales Grau"
    },
    "Warmgrau": {
        "components": ["Titanweiß", "Umbra gebrannt", "Elfenbeinschwarz"],
        "ratios": [4, 1, 1],
        "description": "Warmes Grau für Schatten"
    },
    "Kaltgrau": {
        "components": ["Titanweiß", "Preußischblau", "Elfenbeinschwarz"],
        "ratios": [4, 1, 1],
        "description": "Kühles Grau für Licht"
    },
    
    # Fleischfarben
    "Helle Haut": {
        "components": ["Titanweiß", "Kadmiumgelb hell", "Kadmiumrot hell", "Umbra gebrannt"],
        "ratios": [8, 1, 1, 0.5],
        "description": "Grundton für helle Hauttöne"
    },
    "Mittlere Haut": {
        "components": ["Titanweiß", "Neapelgelb", "Zinnoberrot", "Umbra natur"],
        "ratios": [4, 2, 1, 1],
        "description": "Grundton für mittlere Hauttöne"
    },
    "Dunkle Haut": {
        "components": ["Umbra gebrannt", "Zinnoberrot", "Neapelgelb", "Titanweiß"],
        "ratios": [3, 2, 1, 1],
        "description": "Grundton für dunkle Hauttöne"
    },
    
    # Natürliche Grüntöne
    "Laubgrün": {
        "components": ["Kadmiumgelb mittel", "Preußischblau", "Titanweiß"],
        "ratios": [2, 1, 1],
        "description": "Natürliches Blattgrün"
    },
    "Waldgrün": {
        "components": ["Viridian", "Umbra gebrannt", "Kadmiumgelb hell"],
        "ratios": [3, 1, 0.5],
        "description": "Dunkles Waldgrün"
    },
    
    # Himmel und Wasser
    "Himmelblau": {
        "components": ["Ultramarienblau", "Titanweiß", "Kadmiumgelb hell"],
        "ratios": [1, 4, 0.25],
        "description": "Warmes Himmelblau"
    },
    "Wasserblau": {
        "components": ["Phthaloblau", "Viridian", "Titanweiß"],
        "ratios": [2, 1, 3],
        "description": "Natürliches Wasserblau"
    }
}

def rgb_to_oil_paint_match(rgb: Tuple[int, int, int]) -> Dict:
    """
    Findet die beste Ölfarben-Entsprechung für einen RGB-Wert
    und schlägt Mischungsalternativen vor
    """
    def color_distance(c1: Tuple[int, int, int], c2: Tuple[int, int, int]) -> float:
        """Berechnet Euklidische Distanz zwischen zwei RGB-Farben"""
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))
    
    # Direkte Farbübereinstimmung suchen
    closest_paint = None
    min_distance = float('inf')
    
    for paint_rgb, paint in BASIC_OIL_PAINTS.items():
        distance = color_distance(rgb, paint_rgb)
        if distance < min_distance:
            min_distance = distance
            closest_paint = paint
    
    # Alternative Mischungen vorschlagen
    suggested_mixtures = []
    
    # Prüfe vordefinierte Mischungsrezepte
    for mixture_name, recipe in MIXING_RECIPES.items():
        # Berechne theoretische Mischfarbe (vereinfacht)
        if len(recipe["components"]) >= 2:
            # Einfache gewichtete Durchschnittsmischung
            total_ratio = sum(recipe["ratios"])
            mixed_r = mixed_g = mixed_b = 0
            
            for component, ratio in zip(recipe["components"], recipe["ratios"]):
                # Finde RGB-Werte der Komponente
                for paint_rgb, paint in BASIC_OIL_PAINTS.items():
                    if paint.name == component:
                        weight = ratio / total_ratio
                        mixed_r += paint_rgb[0] * weight
                        mixed_g += paint_rgb[1] * weight
                        mixed_b += paint_rgb[2] * weight
                        break
            
            mixed_color = (int(mixed_r), int(mixed_g), int(mixed_b))
            mixture_distance = color_distance(rgb, mixed_color)
            
            if mixture_distance < min_distance * 1.2:  # 20% Toleranz
                suggested_mixtures.append({
                    "name": mixture_name,
                    "recipe": recipe,
                    "distance": mixture_distance,
                    "resulting_color": mixed_color
                })
    
    # Sortiere Mischungen nach Genauigkeit
    suggested_mixtures.sort(key=lambda x: x["distance"])
    
    return {
        "closest_pure_paint": closest_paint,
        "distance": min_distance,
        "suggested_mixtures": suggested_mixtures[:3],  # Top 3 Vorschläge
        "painting_tips": get_painting_tips(rgb, closest_paint),
        "color_properties": analyze_oil_paint_properties(rgb)
    }

def get_painting_tips(rgb: Tuple[int, int, int], paint: OilPaint) -> List[str]:
    """Gibt praktische Maltipps für die spezifische Farbe"""
    tips = []
    
    # Allgemeine Tipps basierend auf Farbeigenschaften
    if paint.opacity == "transparent":
        tips.append("🎨 Transparente Farbe - ideal für Lasuren und Übergänge")
        tips.append("💡 Mit Medium verdünnen für gleichmäßige Schichten")
    elif paint.opacity == "opaque":
        tips.append("🎨 Deckende Farbe - perfekt für Grundierungen und Highlights")
        tips.append("💡 Sparsam verwenden, da sehr farbintensiv")
    
    if paint.drying_time == "slow":
        tips.append("⏰ Lange Trocknungszeit - mehr Zeit für Verblendung")
        tips.append("🌡️ Trockenbeschleuniger hinzufügen wenn nötig")
    elif paint.drying_time == "fast":
        tips.append("⏰ Schnelle Trocknung - zügig arbeiten")
        tips.append("💧 Mit Verzögerer mischen für mehr Arbeitszeit")
    
    if paint.lightfastness < 3:
        tips.append("☀️ Lichtempfindlich - für Studien verwenden")
        tips.append("🛡️ UV-Schutz beim Aufhängen beachten")
    
    # Spezielle Pigment-Tipps
    if "Kadmium" in paint.name:
        tips.append("⚠️ Kadmiumpigment - nicht mit schwefelhaltigen Farben mischen")
        tips.append("🧤 Vorsicht beim Umgang, giftig bei Einnahme")
    elif "Preußisch" in paint.name:
        tips.append("🔬 Reaktiv mit Alkali - pH-neutrale Grundierung verwenden")
    elif "Ultramarin" in paint.name:
        tips.append("🌊 Säureempfindlich - nicht mit sauren Medien mischen")
    
    return tips

def analyze_oil_paint_properties(rgb: Tuple[int, int, int]) -> Dict:
    """Analysiert die maltechnischen Eigenschaften einer Farbe"""
    r, g, b = rgb
    
    # Farbtemperatur bestimmen
    if r > b + 30:
        temperature = "warm"
        temp_description = "Warme Farbe - vorwärtsdrängend"
    elif b > r + 30:
        temperature = "cool" 
        temp_description = "Kühle Farbe - zurückweichend"
    else:
        temperature = "neutral"
        temp_description = "Neutrale Temperatur - ausgewogen"
    
    # Farbintensität
    intensity = max(r, g, b) - min(r, g, b)
    if intensity > 200:
        intensity_level = "high"
        intensity_desc = "Sehr intensive Farbe - sparsam dosieren"
    elif intensity > 100:
        intensity_level = "medium"
        intensity_desc = "Mittlere Intensität - vielseitig einsetzbar"
    else:
        intensity_level = "low"
        intensity_desc = "Gedeckte Farbe - gut für Schatten und Grundtöne"
    
    # Helligkeit
    brightness = (r + g + b) / 3
    if brightness > 200:
        brightness_level = "light"
        brightness_desc = "Helle Farbe - für Highlights und Lichteffekte"
    elif brightness > 100:
        brightness_level = "medium"
        brightness_desc = "Mittlere Helligkeit - für Mitteltöne"
    else:
        brightness_level = "dark"
        brightness_desc = "Dunkle Farbe - für Schatten und Konturen"
    
    return {
        "temperature": {
            "category": temperature,
            "description": temp_description
        },
        "intensity": {
            "level": intensity_level,
            "value": intensity,
            "description": intensity_desc
        },
        "brightness": {
            "level": brightness_level,
            "value": int(brightness),
            "description": brightness_desc
        },
        "mixing_behavior": get_mixing_behavior(rgb),
        "application_suggestions": get_application_suggestions(rgb)
    }

def get_mixing_behavior(rgb: Tuple[int, int, int]) -> Dict:
    """Gibt Informationen über das Mischverhalten der Farbe"""
    r, g, b = rgb
    
    # Primärfarben-Anteil analysieren
    is_warm = r > max(g, b)
    is_cool = b > max(r, g)
    has_yellow = g > b and (r + g) > b * 1.5
    
    behavior = {
        "dominant_primary": "",
        "mixing_warnings": [],
        "complementary_suggestions": [],
        "harmony_suggestions": []
    }
    
    if is_warm:
        behavior["dominant_primary"] = "Rot (warm)"
        behavior["mixing_warnings"].append("Kann andere Farben schnell überwältigen")
        behavior["complementary_suggestions"].append("Mit Grüntönen für Neutralisation")
    elif is_cool:
        behavior["dominant_primary"] = "Blau (kühl)"
        behavior["mixing_warnings"].append("Tendiert zu Schlammigkeit mit Erdfarben")
        behavior["complementary_suggestions"].append("Mit Orangetönen für Lebendigkeit")
    elif has_yellow:
        behavior["dominant_primary"] = "Gelb (hell)"
        behavior["mixing_warnings"].append("Verliert schnell an Leuchtkraft")
        behavior["complementary_suggestions"].append("Mit Violetttönen für Kontrast")
    
    return behavior

def get_application_suggestions(rgb: Tuple[int, int, int]) -> List[str]:
    """Schlägt Anwendungsbereiche für die Farbe vor"""
    r, g, b = rgb
    suggestions = []
    
    # Basierend auf Farbwerten
    brightness = (r + g + b) / 3
    saturation = max(r, g, b) - min(r, g, b)
    
    if brightness > 200:
        suggestions.extend([
            "Himmel und Wolken",
            "Highlights auf Haut",
            "Reflektionen auf Wasser",
            "Lichteffekte"
        ])
    elif brightness < 80:
        suggestions.extend([
            "Tiefe Schatten",
            "Nachtstimmungen", 
            "Konturen und Details",
            "Untermalung"
        ])
    
    if saturation > 150:
        suggestions.extend([
            "Blumenmalerei",
            "Stillleben-Akzente",
            "Expressionistische Werke",
            "Moderne Kompositionen"
        ])
    
    # Farbspezifische Vorschläge
    if r > g + b:  # Rottöne
        suggestions.extend(["Hauttöne", "Sonnenuntergänge", "Blüten"])
    elif g > r + b:  # Grüntöne
        suggestions.extend(["Landschaft", "Laub", "Natürliche Szenen"])
    elif b > r + g:  # Blautöne
        suggestions.extend(["Himmel", "Wasser", "Kühle Schatten"])
    
    return list(set(suggestions))  # Entferne Duplikate

def get_alternative_brands() -> Dict[str, List[str]]:
    """Alternative Marken für Ölfarben"""
    return {
        "Premium Professionell": [
            "Schmincke Mussini",
            "Old Holland Classic",
            "Michael Harding",
            "Williamsburg",
            "Gamblin 1980"
        ],
        "Künstlerqualität": [
            "Schmincke Norma",
            "Winsor & Newton Artists",
            "Rembrandt",
            "Daler Rowney Georgian",
            "Lukas 1862"
        ],
        "Studienqualität": [
            "Schmincke Akademie",
            "Winsor & Newton Winton",
            "Van Gogh",
            "Talens Art Creation",
            "Reeves"
        ]
    } 