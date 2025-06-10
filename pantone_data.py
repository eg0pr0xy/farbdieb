
pantone_colors = {
    (186, 12, 47): "Pantone 186 C",
    (0, 56, 168): "Pantone Reflex Blue C",
    (255, 209, 0): "Pantone Yellow C",
    (0, 158, 73): "Pantone Green C",
    (255, 103, 31): "Pantone 165 C",
    (140, 198, 63): "Pantone 368 C",
    (0, 133, 202): "Pantone 300 C",
    (237, 41, 57): "Pantone Warm Red C",
    (46, 49, 146): "Pantone 072 C",
    (255, 255, 255): "White",
    (0, 0, 0): "Black",
    (128, 128, 128): "Pantone Cool Gray 8 C"
}

def rgb_to_pantone_name(rgb):
    def distance(c1, c2):
        return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5

    closest = min(pantone_colors.keys(), key=lambda c: distance(rgb, c))
    return pantone_colors[closest]
