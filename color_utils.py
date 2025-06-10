
from PIL import Image
from collections import Counter
from pantone_data import pantone_colors, rgb_to_pantone_name
import numpy as np
from sklearn.cluster import KMeans

def extract_dominant_colors(image_path, num_colors=20, cluster=True):
    img = Image.open(image_path).convert("RGB")
    img_small = img.resize((200, 200))
    pixels = np.array(img_small).reshape(-1, 3)

    if cluster:
        kmeans = KMeans(n_clusters=num_colors, random_state=0)
        kmeans.fit(pixels)
        colors = kmeans.cluster_centers_.astype(int)
    else:
        counts = Counter([tuple(px) for px in pixels])
        colors = [np.array(color) for color, _ in counts.most_common(num_colors)]

    hex_colors = ['#{:02x}{:02x}{:02x}'.format(*color) for color in colors]
    pantone_names = [rgb_to_pantone_name(tuple(color)) for color in colors]
    rgb_colors = [tuple(map(int, color)) for color in colors]

    return hex_colors, rgb_colors, pantone_names
