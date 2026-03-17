import fontforge
import os

font_map = [
    ("Black", "SFProDisplay-Black.ttf", "SFProDisplay-BlackItalic.ttf"),
    ("Bold", "SFProDisplay-Bold.ttf", "SFProDisplay-BoldItalic.ttf"),
    ("Heavy", "SFProDisplay-Heavy.ttf", "SFProDisplay-HeavyItalic.ttf"),
    ("Light", "SFProDisplay-Light.ttf", "SFProDisplay-LightItalic.ttf"),
    ("Medium", "SFProDisplay-Medium.ttf", "SFProDisplay-MediumItalic.ttf"),
    ("Regular", "SFProDisplay-Regular.ttf", "SFProDisplay-RegularItalic.ttf"), 
    ("Semibold", "SFProDisplay-Semibold.ttf", "SFProDisplay-SemiboldItalic.ttf"),
    ("Thin", "SFProDisplay-Thin.ttf", "SFProDisplay-ThinItalic.ttf"),
    ("Ultralight", "SFProDisplay-Ultralight.ttf", "SFProDisplay-UltralightItalic.ttf")
]

def merge_fonts(arabic_path, latin_path, output_path, weight, is_italic):
    if not os.path.exists(arabic_path) or not os.path.exists(latin_path):
        print(f"  --> Skipped: Missing {arabic_path} or {latin_path}")
        return

    base_font = fontforge.open(arabic_path)
    latin_font = fontforge.open(latin_path)
    
    # Merge glyphs
    base_font.mergeFonts(latin_path)
    
    # 1. WIPE Apple's problematic metadata completely
    base_font.sfnt_names = ()
    
    # 2. Construct bulletproof Windows names
    base_family_name = "SyrianFrancisco"
    
    # Windows Grouping Logic
    if weight in ["Regular", "Bold"]:
        family_name = base_family_name
        if weight == "Regular":
            style_name = "Italic" if is_italic else "Regular"
        else: # Bold
            style_name = "Bold Italic" if is_italic else "Bold"
    else:
        # Separate families for Black, Light, etc.
        family_name = f"{base_family_name} {weight}"
        style_name = "Italic" if is_italic else "Regular"
        
    postscript_name = f"{family_name.replace(' ', '')}-{style_name.replace(' ', '')}"
    full_name = f"{family_name} {style_name}".replace(" Regular", "") # "Regular" is omitted in full names
    
    # Apply standard metadata
    base_font.familyname = family_name
    base_font.fontname = postscript_name
    base_font.fullname = full_name
    base_font.weight = weight
    base_font.copyright = latin_font.copyright
    base_font.version = "1.0"
    
    # 3. Set strict OS/2 and Mac style flags for Word/Windows recognition
    if style_name == "Regular":
        base_font.macstyle = 0
        base_font.os2_stylemap = 64
        base_font.italicangle = 0
    elif style_name == "Italic":
        base_font.macstyle = 2
        base_font.os2_stylemap = 1
        base_font.italicangle = -15
    elif style_name == "Bold":
        base_font.macstyle = 1
        base_font.os2_stylemap = 32
        base_font.italicangle = 0
    elif style_name == "Bold Italic":
        base_font.macstyle = 3
        base_font.os2_stylemap = 33
        base_font.italicangle = -15

    # Generate and close
    base_font.generate(output_path)
    base_font.close()
    latin_font.close()
    print(f"  --> Saved {output_path}")

print("Starting clean Windows metadata font merge...\n")

for weight, latin_upright, latin_italic in font_map:
    arabic_file = f"SFArabic-{weight}.ttf"
    
    # 1. Process Upright
    print(f"Processing {weight} (Upright)...")
    output_upright = f"SyrianFrancisco-{weight}.ttf"
    merge_fonts(arabic_file, latin_upright, output_upright, weight, is_italic=False)
    
    # 2. Process Italic
    print(f"Processing {weight} (Italic)...")
    output_italic = f"SyrianFrancisco-{weight}Italic.ttf"
    merge_fonts(arabic_file, latin_italic, output_italic, weight, is_italic=True)
    print("-" * 40)

print("\nAll done! The fonts are ready for Windows installation.")