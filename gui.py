
import tkinter as tk
from tkinter import filedialog, IntVar, Checkbutton, messagebox, font, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import csv
import threading
import time
from PIL import Image, ImageTk
from color_utils import extract_dominant_colors
from color_theory import get_comprehensive_color_analysis
from export_utils import SwatchExporter
import sys
import os

# Set high DPI awareness for Windows
if sys.platform == "win32":
    import ctypes
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Per monitor DPI aware
    except:
        try:
            ctypes.windll.user32.SetProcessDPIAware()  # System DPI aware
        except:
            pass

stored_colors = []
stored_comprehensive_analysis = []
current_image_path = None
is_processing = False

def start_gui():
    # Toast notification system
    def show_toast(message, duration=2000):
        toast = tk.Toplevel(window)
        toast.overrideredirect(True)
        toast.attributes('-topmost', True)
        toast.configure(bg='#2D2D2D')
        
        # Position at bottom right
        toast.geometry("300x50")
        x = window.winfo_x() + window.winfo_width() - 320
        y = window.winfo_y() + window.winfo_height() - 70
        toast.geometry(f"+{x}+{y}")
        
        # Toast content
        toast_frame = tk.Frame(toast, bg='#2D2D2D', padx=15, pady=10)
        toast_frame.pack(fill='both', expand=True)
        
        toast_label = tk.Label(toast_frame, text=message, 
                              font=('Segoe UI', 11), 
                              bg='#2D2D2D', fg='#FFFFFF')
        toast_label.pack()
        
        # Auto-hide after duration
        toast.after(duration, toast.destroy)
        
        # Fade-in effect
        toast.attributes('-alpha', 0.0)
        for i in range(1, 11):
            toast.after(i * 10, lambda a=i/10: toast.attributes('-alpha', a))
        
        # Fade-out effect before destruction
        fade_start = duration - 300
        for i in range(10):
            toast.after(fade_start + i * 30, lambda a=1-(i/10): toast.attributes('-alpha', a))

    def open_file():
        global stored_colors, stored_comprehensive_analysis, current_image_path
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
        if file_path:
            process_image(file_path)
    
    def process_image(file_path):
        global stored_colors, stored_comprehensive_analysis, current_image_path, is_processing
        
        if is_processing:
            return
            
        current_image_path = file_path
        is_processing = True
        
        # Show loading state
        show_loading_state()
        
        def analyze_image():
            try:
                cluster = cluster_var.get() == 1
                hex_colors, rgb_colors, pantone_names = extract_dominant_colors(
                    file_path, num_colors=30 if cluster else 1000, cluster=cluster
                )
                
                # Store basic colors
                global stored_colors
                stored_colors = list(zip(hex_colors, rgb_colors, pantone_names))
                
                # Comprehensive analysis with Goethe & Itten
                comprehensive_data = []
                for rgb in rgb_colors:
                    analysis = get_comprehensive_color_analysis(rgb)
                    comprehensive_data.append(analysis)
                
                global stored_comprehensive_analysis
                stored_comprehensive_analysis = comprehensive_data
                
                # Update UI in main thread
                window.after(0, lambda: show_colors_with_analysis(hex_colors, rgb_colors, pantone_names, comprehensive_data))
                window.after(0, lambda: show_image_preview(file_path))
                
            except Exception as e:
                window.after(0, lambda: messagebox.showerror("Error", f"Failed to process image: {str(e)}"))
            finally:
                global is_processing
                is_processing = False
        
        # Run analysis in background thread
        threading.Thread(target=analyze_image, daemon=True).start()
    
    def show_loading_state():
        # Clear previous content
        for widget in inner_frame.winfo_children():
            widget.destroy()
            
        # Enhanced loading animation
        loading_frame = tk.Frame(inner_frame, bg='#FAFAFA')
        loading_frame.pack(expand=True, fill='both')
        
        # Loading icon
        loading_icon = tk.Label(loading_frame, text="🔄", font=('Segoe UI', 48), 
                               fg='#1A1A1A', bg='#FAFAFA')
        loading_icon.pack(pady=(100, 20))
        
        # Animated loading text
        loading_label = tk.Label(loading_frame, text="ANALYZING IMAGE", 
                                font=('Segoe UI', 20, 'bold'), 
                                fg='#1A1A1A', bg='#FAFAFA')
        loading_label.pack(pady=(0, 10))
        
        # Status text
        status_label = tk.Label(loading_frame, text="Extracting colors and analyzing psychology...", 
                               font=('Segoe UI', 12), 
                               fg='#666666', bg='#FAFAFA')
        status_label.pack(pady=(0, 30))
        
        # Styled progress bar
        style = ttk.Style()
        style.configure("Colorful.Horizontal.TProgressbar", 
                       background='#1A1A1A', 
                       troughcolor='#E0E0E0',
                       borderwidth=0, 
                       lightcolor='#1A1A1A', 
                       darkcolor='#1A1A1A')
        
        progress = ttk.Progressbar(loading_frame, mode='indeterminate', length=500,
                                  style="Colorful.Horizontal.TProgressbar")
        progress.pack(pady=(0, 20))
        progress.start(interval=50)  # Faster animation
        
        # Animate loading text
        def animate_text():
            current_text = loading_label.cget('text')
            if current_text.endswith('...'):
                loading_label.config(text="ANALYZING IMAGE")
            elif current_text.endswith('..'):
                loading_label.config(text="ANALYZING IMAGE...")
            elif current_text.endswith('.'):
                loading_label.config(text="ANALYZING IMAGE..")
            else:
                loading_label.config(text="ANALYZING IMAGE.")
            loading_frame.after(500, animate_text)
        
        animate_text()
        window.update()
    
    def show_image_preview(image_path):
        try:
            # Update preview in header
            img = Image.open(image_path)
            img.thumbnail((80, 80), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            # Remove old preview if exists
            for widget in header_frame.winfo_children():
                if hasattr(widget, '_preview_widget'):
                    widget.destroy()
            
            # Create new preview label
            preview_label = tk.Label(header_frame, image=photo, bg='#FAFAFA')
            preview_label.image = photo  # Keep reference
            preview_label._preview_widget = True  # Mark for removal
            preview_label.pack(side='right', padx=20)
                
        except Exception as e:
            print(f"Could not show image preview: {e}")
    
    # Simplified drag and drop using tkinter events
    def setup_drag_drop():
        # Basic drag and drop support for Windows
        try:
            def on_drop(event):
                files = event.data.split()
                if files:
                    file_path = files[0].strip('{}')  # Remove curly braces if present
                    if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                        process_image(file_path)
            
            # Enable drag and drop on the main window
            window.tk.call('wm', 'attributes', window, '-topmost', False)
            
            # Bind drop events (this is a simplified version)
            def handle_drop(event):
                # Get dropped files from clipboard or event
                try:
                    files = window.selection_get(selection='CLIPBOARD')
                    if files and any(files.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']):
                        process_image(files.strip())
                except:
                    pass
            
            # For now, we'll focus on the file dialog since cross-platform drag & drop is complex
            pass
            
        except Exception as e:
            print(f"Drag and drop not available: {e}")
            pass

    def show_colors_with_analysis(hex_colors, rgb_colors, pantone_names, comprehensive_data):
        # Clear previous widgets in inner_frame
        for widget in inner_frame.winfo_children():
            widget.destroy()
        
        # Calculate responsive columns based on window width - Swiss grid system
        def calculate_columns():
            window_width = window.winfo_width()
            color_card_width = 250  # Swiss card width including margins
            available_width = window_width - 120  # Account for margins
            max_cols = max(1, available_width // color_card_width)
            return min(max_cols, len(rgb_colors), 5)  # Max 5 columns for Swiss proportion
        
        # Initial column calculation
        cols = calculate_columns() if window.winfo_width() > 1 else 4
        
        # Create responsive grid
        def create_color_grid():
            current_cols = calculate_columns() if window.winfo_width() > 1 else cols
            
            # Clear and recreate grid
            for widget in inner_frame.winfo_children():
                widget.destroy()
            
            # Create comprehensive color cards with all analysis
            for i, (hex_color, rgb_color, pantone_name, analysis) in enumerate(zip(hex_colors, rgb_colors, pantone_names, comprehensive_data)):
                row = i // current_cols
                col = i % current_cols
                
                # Enhanced Swiss-style card frame with hover effects
                card_frame = tk.Frame(inner_frame, bg='#FFFFFF', relief='flat', bd=1, 
                                    highlightbackground='#E0E0E0', highlightthickness=1)
                card_frame.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
                
                # Add hover effects
                def on_card_enter(event):
                    card_frame.configure(highlightbackground='#CCCCCC', highlightthickness=2)
                    card_frame.configure(bg='#FAFAFA')
                
                def on_card_leave(event):
                    card_frame.configure(highlightbackground='#E0E0E0', highlightthickness=1)
                    card_frame.configure(bg='#FFFFFF')
                
                card_frame.bind('<Enter>', on_card_enter)
                card_frame.bind('<Leave>', on_card_leave)
                
                # Bind hover to all child elements too
                def bind_hover_to_children(widget):
                    widget.bind('<Enter>', on_card_enter)
                    widget.bind('<Leave>', on_card_leave)
                    for child in widget.winfo_children():
                        bind_hover_to_children(child)
                
                # Add subtle shadow effect
                shadow_frame = tk.Frame(card_frame, bg='#E8E8E8', height=2)
                shadow_frame.pack(fill='x', side='bottom')
                
                # Color display with harmonies
                color_frame = tk.Frame(card_frame, bg='#FFFFFF')
                color_frame.pack(fill='x', pady=(15, 10))
                
                # Main color (centered)
                main_color_canvas = tk.Canvas(color_frame, width=180, height=120, 
                                            bg=hex_color, highlightthickness=0,
                                            relief='flat', bd=0)
                main_color_canvas.pack()
                
                # Color harmony preview (centered under main color)
                harmony_frame = tk.Frame(color_frame, bg='#FFFFFF')
                harmony_frame.pack(pady=(8, 0))  # More space above harmonies
                
                # Create horizontal layout for harmonies - centered
                harmony_container = tk.Frame(harmony_frame, bg='#FFFFFF')
                harmony_container.pack()
                
                # Complementary color
                comp_rgb = analysis['itten']['complementary']
                comp_hex = f'#{comp_rgb[0]:02x}{comp_rgb[1]:02x}{comp_rgb[2]:02x}'
                comp_canvas = tk.Canvas(harmony_container, width=35, height=25, bg=comp_hex, 
                                      highlightthickness=1, highlightbackground='#CCCCCC')
                comp_canvas.pack(side='left', padx=3)
                
                # Triadic colors
                for triadic_rgb in analysis['itten']['triadic']:
                    tri_hex = f'#{triadic_rgb[0]:02x}{triadic_rgb[1]:02x}{triadic_rgb[2]:02x}'
                    tri_canvas = tk.Canvas(harmony_container, width=35, height=25, bg=tri_hex, 
                                         highlightthickness=1, highlightbackground='#CCCCCC')
                    tri_canvas.pack(side='left', padx=3)
                
                # Small label for harmonies
                harmony_label = tk.Label(harmony_frame, text="Itten Harmonies", 
                                       font=('Segoe UI', 8), fg='#999999', bg='#FFFFFF')
                harmony_label.pack(pady=(3, 0))
                
                # Typography section with expanded formats
                text_frame = tk.Frame(card_frame, bg='#FFFFFF')
                text_frame.pack(fill='x', padx=15, pady=(0, 15))
                
                # Create notebook for tabbed content
                notebook = ttk.Notebook(text_frame)
                notebook.pack(fill='both', expand=True)
                
                                # Basic formats tab
                basic_frame = tk.Frame(notebook, bg='#FFFFFF')
                notebook.add(basic_frame, text='Formats')
                
                # Create entry fields with copy functionality
                entries = [
                    (analysis['basic']['hex'], swiss_font_mono, '#FFFFFF', '#1A1A1A'),
                    (analysis['basic']['rgb'], swiss_font_mono_small, '#F8F8F8', '#666666'),
                    (analysis['basic']['hsl'], swiss_font_mono_small, '#F8F8F8', '#666666'),
                    (analysis['basic']['cmyk'], swiss_font_mono_small, '#F8F8F8', '#666666'),
                    (analysis['basic']['lab'], swiss_font_mono_small, '#F8F8F8', '#666666'),
                    (pantone_name, swiss_font_small, '#F0F0F0', '#000000'),  # Add Pantone name
                ]
                
                for value, font_style, bg_color, fg_color in entries:
                    var = tk.StringVar(value=value)
                    entry = tk.Entry(basic_frame, textvariable=var,
                                   font=font_style, justify='center',
                                   relief='flat', bd=0, readonlybackground=bg_color,
                                   state='readonly', selectbackground=fg_color,
                                   selectforeground='#FFFFFF', fg=fg_color)
                    entry.pack(fill='x', pady=2)
                    
                    # Add selection and copy functionality
                    def make_selectable(entry_widget):
                        def select_all(event):
                            entry_widget.select_range(0, tk.END)
                            entry_widget.focus()
                        
                        def copy_to_clipboard(event):
                            window.clipboard_clear()
                            window.clipboard_append(entry_widget.get())
                            # Toast notification feedback
                            show_toast(f"✓ {entry_widget.get()} copied!")
                            # Visual feedback
                            original_bg = entry_widget.cget('readonlybackground')
                            entry_widget.config(readonlybackground='#E8E8E8')
                            window.after(200, lambda: entry_widget.config(readonlybackground=original_bg))
                        
                        entry_widget.bind('<Button-1>', select_all)
                        entry_widget.bind('<FocusIn>', select_all)
                        entry_widget.bind('<Double-Button-1>', copy_to_clipboard)
                        entry_widget.bind('<Control-c>', copy_to_clipboard)
                    
                    make_selectable(entry)
                
                # Goethe analysis tab
                goethe_frame = tk.Frame(notebook, bg='#FFFFFF')
                notebook.add(goethe_frame, text='Goethe')
                
                goethe_emotion = tk.Label(goethe_frame, text=f"Emotion: {analysis['goethe']['emotion']}", 
                                        font=swiss_font_small, fg='#333333', bg='#FFFFFF', wraplength=180)
                goethe_emotion.pack(fill='x', pady=2)
                
                goethe_character = tk.Label(goethe_frame, text=f"Character: {analysis['goethe']['character']}", 
                                          font=swiss_font_small, fg='#333333', bg='#FFFFFF', wraplength=180)
                goethe_character.pack(fill='x', pady=2)
                
                goethe_effect = tk.Label(goethe_frame, text=f"Effect: {analysis['goethe']['effect']}", 
                                       font=swiss_font_small, fg='#333333', bg='#FFFFFF', wraplength=180)
                goethe_effect.pack(fill='x', pady=2)
                
                # Oil Paint analysis tab (if available)
                if 'oil_paints' in analysis:
                    oil_frame = tk.Frame(notebook, bg='#FFFFFF')
                    notebook.add(oil_frame, text='Ölfarben')
                    
                    oil_data = analysis['oil_paints']
                    
                    # Closest pure paint
                    if oil_data['closest_pure_paint']:
                        paint = oil_data['closest_pure_paint']
                        
                        # Paint name and pigment
                        paint_name = tk.Label(oil_frame, text=f"🎨 {paint.name}", 
                                            font=('Segoe UI', 9, 'bold'), fg='#1A1A1A', bg='#FFFFFF')
                        paint_name.pack(fill='x', pady=(5, 2))
                        
                        pigment_label = tk.Label(oil_frame, text=f"Pigment: {paint.pigment}", 
                                               font=swiss_font_small, fg='#666666', bg='#FFFFFF')
                        pigment_label.pack(fill='x', pady=1)
                        
                        # Properties in compact format
                        properties_text = f"⚫ {paint.opacity} • ⏱️ {paint.drying_time} • ☀️ {paint.lightfastness}/4"
                        properties_label = tk.Label(oil_frame, text=properties_text, 
                                                   font=('Segoe UI', 7), fg='#888888', bg='#FFFFFF')
                        properties_label.pack(fill='x', pady=1)
                        
                        # Brand and series
                        brand_text = f"{paint.brand} • Serie {paint.series} • {paint.price_category}"
                        brand_label = tk.Label(oil_frame, text=brand_text, 
                                             font=('Segoe UI', 7), fg='#999999', bg='#FFFFFF')
                        brand_label.pack(fill='x', pady=(1, 5))
                        
                        # Separator
                        separator = tk.Frame(oil_frame, height=1, bg='#E0E0E0')
                        separator.pack(fill='x', pady=3)
                    
                    # Mixing suggestions (if available)
                    if oil_data['suggested_mixtures']:
                        mix_label = tk.Label(oil_frame, text="💫 Mischungsvorschläge:", 
                                           font=('Segoe UI', 8, 'bold'), fg='#1A1A1A', bg='#FFFFFF')
                        mix_label.pack(fill='x', pady=(5, 2))
                        
                        for mixture in oil_data['suggested_mixtures'][:2]:  # Show top 2
                            mix_name = tk.Label(oil_frame, text=f"• {mixture['name']}", 
                                              font=('Segoe UI', 7, 'bold'), fg='#333333', bg='#FFFFFF')
                            mix_name.pack(fill='x', pady=1)
                            
                            # Mixing components
                            components = mixture['recipe']['components']
                            ratios = mixture['recipe']['ratios']
                            mix_recipe = " + ".join([f"{comp} ({ratio})" for comp, ratio in zip(components, ratios)])
                            
                            recipe_label = tk.Label(oil_frame, text=mix_recipe, 
                                                  font=('Segoe UI', 6), fg='#666666', bg='#FFFFFF', wraplength=170)
                            recipe_label.pack(fill='x', pady=(0, 3))
                    
                    # Quick painting tips
                    if oil_data['painting_tips']:
                        tips_label = tk.Label(oil_frame, text="💡 Maltipps:", 
                                            font=('Segoe UI', 8, 'bold'), fg='#1A1A1A', bg='#FFFFFF')
                        tips_label.pack(fill='x', pady=(5, 2))
                        
                        # Show first 2 most important tips
                        for tip in oil_data['painting_tips'][:2]:
                            tip_text = tip.replace("🎨 ", "").replace("💡 ", "").replace("⏰ ", "").replace("☀️ ", "")
                            tip_label = tk.Label(oil_frame, text=f"• {tip_text}", 
                                                font=('Segoe UI', 6), fg='#555555', bg='#FFFFFF', wraplength=170)
                            tip_label.pack(fill='x', pady=1)
                

                

            
            # Configure grid weights for responsive behavior
            for i in range(current_cols):
                inner_frame.columnconfigure(i, weight=1)
            
            # Update scroll region
            inner_frame.update_idletasks()
            scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
        
        # Create initial grid
        create_color_grid()
        
        # Make window responsive by binding resize events
        def on_window_resize(event):
            if event.widget == window and window.winfo_width() > 1:
                # Delay the grid recreation to avoid too many updates
                if hasattr(on_window_resize, 'resize_job'):
                    window.after_cancel(on_window_resize.resize_job)
                on_window_resize.resize_job = window.after(300, create_color_grid)
        
        # Bind resize event to window
        window.bind('<Configure>', on_window_resize)
        
        # Configure window grid weights for proper resizing
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)

    def export_colors():
        if not stored_colors or not stored_comprehensive_analysis:
            messagebox.showwarning("No Data", "Please analyze an image first.")
            return
            
        # Simple export options dialog
        export_window = tk.Toplevel(window)
        export_window.title("Export Colors")
        export_window.configure(bg='#FAFAFA')
        export_window.transient(window)
        export_window.grab_set()
        export_window.resizable(False, False)
        
        # Export format selection
        tk.Label(export_window, text="SELECT EXPORT FORMAT", 
                font=('Segoe UI', 14, 'bold'), bg='#FAFAFA', fg='#1A1A1A').pack(pady=20)
        
        export_var = tk.StringVar(value="csv")
        
        # Check if oil paint data is available
        has_oil_paints = any('oil_paints' in analysis for analysis in stored_comprehensive_analysis) if stored_comprehensive_analysis else False
        
        formats = [
            ("CSV - Basic colors", "csv"),
            ("JSON - Complete analysis", "json"),
            ("Adobe Swatch (.ASE)", "ase"),
            ("CSS Variables", "css"),
            ("SCSS Variables", "scss"),
            ("Figma Design Tokens", "figma")
        ]
        
        # Add oil paint export option if data is available
        if has_oil_paints:
            formats.append(("Ölfarben-Palette (CSV)", "oil_paint_csv"))
        
        for text, value in formats:
            tk.Radiobutton(export_window, text=text, variable=export_var, value=value,
                          font=swiss_font_small, bg='#FAFAFA', fg='#1A1A1A').pack(anchor='w', padx=40, pady=5)
        
        def do_export():
            format_type = export_var.get()
            
            file_types = {
                "csv": [("CSV files", "*.csv")],
                "json": [("JSON files", "*.json")],
                "ase": [("Adobe Swatch files", "*.ase")],
                "css": [("CSS files", "*.css")],
                "scss": [("SCSS files", "*.scss")],
                "figma": [("JSON files", "*.json")],
                "oil_paint_csv": [("CSV files", "*.csv")]
            }
            
            file_path = filedialog.asksaveasfilename(
                defaultextension=f".{format_type}",
                filetypes=file_types[format_type]
            )
            
            if file_path:
                success = False
                
                if format_type == "csv":
                    # Basic CSV export
                    with open(file_path, "w", newline="", encoding='utf-8') as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(["HEX", "RGB", "HSL", "CMYK", "Pantone", "Goethe_Emotion"])
                        for i, (hex_val, rgb, pantone) in enumerate(stored_colors):
                            analysis = stored_comprehensive_analysis[i]
                            writer.writerow([
                                analysis['basic']['hex'],
                                analysis['basic']['rgb'],
                                analysis['basic']['hsl'],
                                analysis['basic']['cmyk'],
                                pantone,
                                analysis['goethe']['emotion']
                            ])
                    success = True
                    
                elif format_type == "json":
                    success = SwatchExporter.export_json(stored_comprehensive_analysis, file_path)
                    
                elif format_type == "ase":
                    success = SwatchExporter.export_adobe_ase(stored_colors, file_path)
                    
                elif format_type == "css":
                    success = SwatchExporter.export_css_variables(stored_colors, file_path)
                    
                elif format_type == "scss":
                    success = SwatchExporter.export_scss_variables(stored_colors, file_path)
                    
                elif format_type == "figma":
                    success = SwatchExporter.export_figma_tokens(stored_colors, file_path)
                    
                elif format_type == "oil_paint_csv":
                    success = SwatchExporter.export_oil_paint_palette(stored_comprehensive_analysis, file_path)
                
                if success:
                    messagebox.showinfo("Export Successful", f"File saved: {file_path}")
                    export_window.destroy()
                else:
                    messagebox.showerror("Export Failed", "Could not export file.")
        
        tk.Button(export_window, text="EXPORT", command=do_export,
                 font=swiss_font_medium, bg='#1A1A1A', fg='#FFFFFF', 
                 relief='flat', bd=0, padx=25, pady=12).pack(pady=20)
    
    # Keyboard shortcuts
    def setup_keyboard_shortcuts():
        window.bind('<Control-o>', lambda e: open_file())
        window.bind('<Control-s>', lambda e: export_colors())
        window.bind('<Control-q>', lambda e: window.quit())
        window.bind('<F1>', lambda e: show_help())
        window.bind('<F5>', lambda e: process_image(current_image_path) if current_image_path else None)
    
    def show_help():
        help_text = """
FARBDIEB - Professional Color Extraction Tool

KEYBOARD SHORTCUTS:
Ctrl+O - Open image
Ctrl+S - Export colors  
Ctrl+Q - Quit application
F1 - Show this help
F5 - Re-analyze current image

FEATURES:
• Advanced color analysis with 5 color spaces
• Goethe's color psychology (emotion, character, effect)
• Itten's color harmony theory (complementary, triadic, analogous)
• 6 export formats (CSS, SCSS, Adobe ASE, JSON, Figma)
• Swiss Design Interface

COLOR CARD TABS:
• Formats: HEX, RGB, HSL, CMYK, LAB + Pantone
• Goethe: Emotional and psychological color effects

COLOR HARMONIES:
Each color card shows small previews of harmonies:
- Complementary color (180° opposite)
- Triadic colors (120° intervals)
- Analogous colors (30° adjacent)
        """
        
        help_window = tk.Toplevel(window)
        help_window.title("Help - FARBDIEB")
        help_window.geometry("500x400")
        help_window.configure(bg='#FAFAFA')
        
        help_label = tk.Label(help_window, text=help_text, 
                             font=swiss_font_small, bg='#FAFAFA', fg='#1A1A1A',
                             justify='left', wraplength=450)
        help_label.pack(padx=20, pady=20)

    window = tk.Tk()
    window.title("FARBDIEB — Color Extraction Tool")
    
    # Calculate optimal window size for exactly 5 color cards
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # Card width calculation based on actual card dimensions:
    # Main color canvas: 180px + card padding + grid padx
    # Each card: 180px (canvas) + 20px (internal padding) + 30px (grid padx) = 230px
    # 5 cards = 5 * 230 = 1150px + container margins (80px) = 1230px
    card_width = 180  # Canvas width
    card_internal_padding = 20  # Card internal padding
    card_grid_padding = 30  # Grid padx (15px * 2)
    cards_count = 5
    container_margins = 80  # Main container margins
    
    optimal_width = cards_count * (card_width + card_internal_padding + card_grid_padding) + container_margins
    optimal_height = 900  # Fixed height for good proportions
    
    # Center the window
    x = (screen_width - optimal_width) // 2
    y = (screen_height - optimal_height) // 2
    
    window.geometry(f"{optimal_width}x{optimal_height}+{x}+{y}")
    window.minsize(1000, 700)  # Minimum window size to see everything
    window.configure(bg='#FAFAFA')  # Swiss design: off-white background
    
    # Configure window to be resizable
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
    
    # Configure high-DPI fonts
    default_font = font.nametofont("TkDefaultFont")
    default_font.configure(size=11)
    
    # Swiss Design Typography - Helvetica-like fonts
    swiss_font_large = ('Segoe UI', 16, 'normal')
    swiss_font_medium = ('Segoe UI', 12, 'normal') 
    swiss_font_small = ('Segoe UI', 10, 'normal')
    swiss_font_mono = ('Consolas', 14, 'normal')
    swiss_font_mono_small = ('Consolas', 11, 'normal')

    # Main container with grid layout for responsiveness
    main_container = tk.Frame(window, bg='#FAFAFA')
    main_container.pack(fill='both', expand=True)
    
    # Header frame - Swiss minimal design
    header_frame = tk.Frame(main_container, bg='#FAFAFA', height=120)
    header_frame.pack(fill='x', padx=40, pady=(30, 0))
    header_frame.pack_propagate(False)

    # Left side of header - title and subtitle
    title_frame = tk.Frame(header_frame, bg='#FAFAFA')
    title_frame.pack(side='left', fill='both', expand=True)
    
    # App title - Swiss typography
    title_label = tk.Label(title_frame, text="FARBDIEB", 
                          font=('Segoe UI', 32, 'bold'), 
                          bg='#FAFAFA', fg='#1A1A1A')
    title_label.pack(anchor='w', pady=(10, 0))
    
    subtitle_label = tk.Label(title_frame, text="Professional Color Extraction & Analysis", 
                             font=swiss_font_medium, 
                             bg='#FAFAFA', fg='#666666')
    subtitle_label.pack(anchor='w')

    # Control panel - minimal Swiss design
    control_panel = tk.Frame(main_container, bg='#FFFFFF', relief='flat', bd=1)
    control_panel.pack(fill='x', padx=40, pady=20)

    # Inner control frame for proper spacing
    inner_control = tk.Frame(control_panel, bg='#FFFFFF')
    inner_control.pack(fill='x', padx=30, pady=20)

    # Buttons with Swiss design principles
    button_frame = tk.Frame(inner_control, bg='#FFFFFF')
    button_frame.pack(side='left')

    # Swiss-style buttons - minimal, functional
    select_btn = tk.Button(button_frame, text="SELECT IMAGE", command=open_file, 
                          font=swiss_font_medium, bg='#1A1A1A', fg='#FFFFFF', 
                          relief='flat', bd=0, padx=25, pady=12,
                          activebackground='#333333', activeforeground='#FFFFFF',
                          cursor='hand2')
    select_btn.pack(side='left', padx=(0, 20))
    
    cluster_var = IntVar(value=1)
    cluster_check = Checkbutton(inner_control, text="Extract dominant colors only", 
                               variable=cluster_var, font=swiss_font_small, 
                               bg='#FFFFFF', fg='#1A1A1A', 
                               selectcolor='#FFFFFF', relief='flat',
                               activebackground='#FFFFFF', activeforeground='#1A1A1A')
    cluster_check.pack(side='left', padx=(0, 30))
    
    export_btn = tk.Button(button_frame, text="EXPORT", command=export_colors,
                          font=swiss_font_medium, bg='#FFFFFF', fg='#1A1A1A', 
                          relief='solid', bd=1, padx=25, pady=12,
                          activebackground='#F0F0F0', activeforeground='#1A1A1A',
                          cursor='hand2')
    export_btn.pack(side='left')

    # Main content area - Swiss grid system
    content_frame = tk.Frame(main_container, bg='#FAFAFA')
    content_frame.pack(fill='both', expand=True, padx=40, pady=(0, 30))
    
    # Colors section header
    colors_header = tk.Label(content_frame, text="EXTRACTED COLORS", 
                            font=('Segoe UI', 18, 'bold'), 
                            bg='#FAFAFA', fg='#1A1A1A')
    colors_header.pack(anchor='w', pady=(0, 20))
    
    # Scrollable content area
    canvas_frame = tk.Frame(content_frame, bg='#FAFAFA')
    canvas_frame.pack(fill='both', expand=True)
    
    # Swiss-style minimal scrollbars
    v_scrollbar = tk.Scrollbar(canvas_frame, orient='vertical', bg='#E0E0E0', 
                              troughcolor='#F5F5F5', activebackground='#CCCCCC')
    h_scrollbar = tk.Scrollbar(canvas_frame, orient='horizontal', bg='#E0E0E0',
                              troughcolor='#F5F5F5', activebackground='#CCCCCC')
    
    # Create canvas for scrolling
    scroll_canvas = tk.Canvas(canvas_frame, bg='#FAFAFA',
                             yscrollcommand=v_scrollbar.set,
                             xscrollcommand=h_scrollbar.set,
                             highlightthickness=0)
    
    v_scrollbar.config(command=scroll_canvas.yview)
    h_scrollbar.config(command=scroll_canvas.xview)
    
    v_scrollbar.pack(side='right', fill='y')
    h_scrollbar.pack(side='bottom', fill='x')
    scroll_canvas.pack(side='left', fill='both', expand=True)
    
    # Frame inside canvas for content
    inner_frame = tk.Frame(scroll_canvas, bg='#FAFAFA')
    scroll_canvas.create_window((0, 0), window=inner_frame, anchor='nw')
    
    # Define show_drop_zone function first
    def show_drop_zone():
        # Clear content and show simple instruction
        for widget in inner_frame.winfo_children():
            widget.destroy()
            
        drop_frame = tk.Frame(inner_frame, bg='#FAFAFA')
        drop_frame.pack(expand=True, fill='both', pady=100)
        
        # Simple dashed border effect
        border_frame = tk.Frame(drop_frame, bg='#CCCCCC', height=200)
        border_frame.pack(fill='x', padx=100, pady=50)
        
        inner_drop = tk.Frame(border_frame, bg='#FAFAFA')
        inner_drop.pack(fill='both', expand=True, padx=3, pady=3)
        
        tk.Label(inner_drop, text="SELECT IMAGE TO ANALYZE", 
                font=('Segoe UI', 24, 'bold'), 
                fg='#CCCCCC', bg='#FAFAFA').pack(expand=True)
        
        tk.Label(inner_drop, text="Click 'SELECT IMAGE' button to start", 
                font=swiss_font_medium, 
                fg='#999999', bg='#FAFAFA').pack()
        
        # Update scroll region
        inner_frame.update_idletasks()
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
    
    # Setup all functionality
    setup_keyboard_shortcuts()
    try:
        setup_drag_drop()
    except:
        pass  # Drag and drop might not be available on all systems
    
    # Show initial drop zone
    show_drop_zone()

    window.mainloop()
