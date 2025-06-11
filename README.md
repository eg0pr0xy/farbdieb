# FARBDIEB 🎨

**Professional Color Extraction & Analysis Tool**

A desktop application for extracting dominant colors from images and analyzing their psychological impact using **Goethe's Color Theory** and **Itten's Color Harmonies**.

![FARBDIEB Interface](Farbdieb-interface.png)

## 🔄 Workflow Overview

```mermaid
graph TB
    A["📸 Image Upload"] --> B["🔍 Color Extraction<br/>K-means Clustering"]
    B --> C["🎨 Multi-Theory Analysis"]
    
    C --> D["📊 Basic Formats<br/>HEX • RGB • HSL<br/>CMYK • LAB"]
    C --> E["🧠 Goethe Psychology<br/>Emotion • Character • Effect"]
    C --> F["🎯 Itten Harmonies<br/>Complementary • Triadic<br/>Analogous"]
    C --> G["🖌️ Oil Paint Matching<br/>Pigments • Mixing • Tips"]
    C --> H["🏷️ Pantone Mapping<br/>Professional Standards"]
    
    G --> I["🎨 Pure Pigments<br/>28+ Professional Colors"]
    G --> J["🧪 Mixing Recipes<br/>Traditional Formulas"]
    G --> K["💡 Painting Tips<br/>Technical Advice"]
    G --> L["🏭 Brand Database<br/>Schmincke • W&N • etc."]
    
    D --> M["📤 Professional Export"]
    E --> M
    F --> M
    G --> M
    H --> M
    
    M --> N["💾 7 Export Formats"]
    N --> O["📊 CSV • JSON • Adobe ASE"]
    N --> P["🌐 CSS • SCSS • Figma"]
    N --> Q["🎨 Oil Paint Palette"]
    
    style A fill:#e3f2fd
    style C fill:#fff3e0
    style G fill:#f3e5f5
    style I fill:#ffebee
    style J fill:#ffebee
    style K fill:#ffebee
    style L fill:#ffebee
    style M fill:#e8f5e8
    style Q fill:#fff8e1
```

## ✨ Features

### 🎯 **Core Functionality**
- **Smart Color Extraction** with K-means clustering
- **Multi-format Support** (JPG, PNG, BMP, GIF)
- **Responsive Swiss Design** interface
- **Real-time Image Analysis** with threading
- **Oil Paint Matching** - Digital-to-analog color translation

### 🧠 **Color Psychology & Theory**
- **Goethe's Color Psychology** - Emotion, Character, Effect analysis
- **Itten's Color Harmonies** - Complementary, Triadic, Analogous colors
- **Pantone Color Matching** for professional workflows
- **5 Color Space Analysis** (HEX, RGB, HSL, CMYK, LAB)

### 📤 **Professional Export Options**
- **CSV** - For Excel & spreadsheet applications
- **JSON** - Complete analysis data for developers
- **Adobe ASE** - Adobe Swatch Exchange for Creative Suite
- **CSS Variables** - For web development
- **SCSS Variables** - For preprocessor workflows  
- **Figma Design Tokens** - For design system integration
- **Oil Paint Palette** - Shopping lists with mixing recipes

### 🎛️ **User Experience**
- **Keyboard Shortcuts** (Ctrl+O, Ctrl+S, F1, F5)
- **Toast Notifications** for copy feedback
- **Hover Effects** and micro-interactions
- **High-DPI Support** for modern displays
- **Selectable & Copyable** color values

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- tkinter (usually included with Python)
- Required packages (see requirements.txt)

### Installation

```bash
# Clone the repository
git clone https://github.com/eg0pr0xy/farbdieb.git
cd farbdieb

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## 🎨 How to Use

1. **Launch FARBDIEB** - Run `python main.py`
2. **Select Image** - Click "SELECT IMAGE" or press `Ctrl+O`
3. **Analyze Colors** - Colors are automatically extracted and analyzed
4. **Explore Analysis** - View formats, Goethe psychology, Itten harmonies, and oil paints
5. **Copy Colors** - Click any color value to select, double-click to copy
6. **Export Results** - Press `Ctrl+S` or click "EXPORT" for professional formats

## 🏗️ Architecture

```
farbdieb/
├── main.py              # Application entry point
├── gui.py               # Main GUI interface with Swiss Design
├── color_utils.py       # Color extraction algorithms
├── color_theory.py      # Goethe & Itten analysis engine
├── oil_paint_data.py    # Oil paint database and matching algorithms
├── export_utils.py      # Professional export formats
├── pantone_data.py      # Pantone color matching database
├── requirements.txt     # Python dependencies
└── assets/              # Logo and preview images
```

## 🔬 Color Analysis Engine

### Goethe's Color Psychology
- **Emotion Analysis** - Warm/cool psychological impact
- **Character Assessment** - Color personality traits
- **Effect Evaluation** - Visual and emotional influence

### Itten's Color Harmonies
- **Complementary Colors** - 180° opposite on color wheel
- **Triadic Relationships** - 120° intervals for balance
- **Analogous Schemes** - 30° adjacent harmonious colors

### Oil Paint Matching 🎨
- **Pigment Database** - 28+ professional oil paints with accurate RGB values
- **Brand Information** - Schmincke, Winsor & Newton, and more
- **Paint Properties** - Opacity, drying time, lightfastness ratings
- **Mixing Recipes** - 10+ traditional color mixing formulas
- **Painting Tips** - Professional advice for each pigment
- **Cost Analysis** - Student vs. artist vs. professional grade recommendations

## 🎯 Use Cases

### 🎭 **Portrait Artists**
Extract skin tones from photos and get precise oil paint mixing recipes for realistic flesh tones.

### 🏞️ **Landscape Painters**
Analyze nature photos to create optimized plein air palettes with minimal tube count.

### 🎓 **Art Educators**
Generate material lists and mixing exercises for color theory courses.

### 🎨 **Digital Artists Transitioning to Traditional**
Bridge the gap between digital inspiration and physical painting materials.

## 🎛️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Open image |
| `Ctrl+S` | Export colors |
| `Ctrl+Q` | Quit application |
| `F1` | Show help |
| `F5` | Re-analyze current image |

## 📋 Export Formats

| Format | Use Case | File Extension |
|--------|----------|----------------|
| **CSV** | Excel, Numbers, Data Analysis | `.csv` |
| **JSON** | APIs, Web Development | `.json` |
| **Adobe ASE** | Photoshop, Illustrator | `.ase` |
| **CSS Variables** | Web Development | `.css` |
| **SCSS Variables** | Sass Preprocessing | `.scss` |
| **Figma Tokens** | Design Systems | `.json` |
| **Oil Paint Palette** | Traditional Painting, Art Supply Lists | `.csv` |

## 🛠️ Technical Stack

- **GUI Framework**: tkinter with Swiss Design principles
- **Image Processing**: PIL (Pillow)
- **Color Analysis**: scikit-learn K-means clustering
- **Data Visualization**: matplotlib
- **Color Space**: Advanced HSL, CMYK, LAB conversions
- **Export Engine**: Custom SwatchExporter class

## 🎨 Design Philosophy

FARBDIEB follows **Swiss Design principles**:
- **Minimalism** - Clean, functional interface
- **Typography** - Segoe UI font hierarchy
- **Grid System** - Responsive column layout
- **Color Palette** - Professional off-white (#FAFAFA) background
- **Micro-interactions** - Subtle hover effects and animations

## 🧪 Dependencies

```txt
pillow>=9.0.0
scikit-learn>=1.0.0
matplotlib>=3.5.0
numpy>=1.21.0
```

## 📈 Performance

- **Multi-threading** for non-blocking UI during analysis
- **Optimized K-means** clustering for dominant color extraction
- **Efficient color space** conversions
- **Memory management** for large image processing

## 🔧 Development

### Project Structure
- **Modular Design** - Separated concerns (GUI, analysis, export)
- **Swiss Design System** - Consistent visual hierarchy
- **Error Handling** - Graceful degradation and user feedback
- **Cross-platform** - Windows, macOS, Linux support

### Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Johann Wolfgang von Goethe** - Color psychology theory
- **Johannes Itten** - Color harmony principles  
- **Swiss Design Movement** - Visual design inspiration
- **Pantone Inc.** - Professional color matching

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/eg0pr0xy/farbdieb/issues)
- **Discussions**: [GitHub Discussions](https://github.com/eg0pr0xy/farbdieb/discussions)

---

**Made with 🎨 and Swiss precision**
