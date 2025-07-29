import os
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image, ImageOps

INPUT_CSV = "generator.csv"
OUTPUT_DIR = "BARCODE"
DPI = 300
WIDTH_CM = 3
HEIGHT_CM = 1

width_px = int(WIDTH_CM / 2.54 * DPI)
height_px = int(HEIGHT_CM / 2.54 * DPI)

os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_barcodes():
    """Solusi paling sederhana - baca file baris per baris"""
    
    # Baca file secara manual
    with open(INPUT_CSV, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Skip header (baris pertama) dan proses data
    for i, line in enumerate(lines[1:], start=1):
        value = line.strip()
        
        # Skip baris kosong
        if not value:
            continue
        
        # Debug: tampilkan nilai yang dibaca
        print(f"Membaca nilai: '{value}' (panjang: {len(value)})")
        
        filename = os.path.join(OUTPUT_DIR, f"{value}")
        
        writer_options = {
            "module_width": 0.25,
            "module_height": 15,
            "quiet_zone": 0,
            "write_text": False,
        }
        
        try:
            barcode = Code128(value, writer=ImageWriter())
            tmp_filename = barcode.save(filename, options=writer_options)
            
            with Image.open(tmp_filename) as img:
                img = img.convert("RGB")
                img = ImageOps.fit(img, (width_px, height_px), Image.LANCZOS)
                img.save(tmp_filename, dpi=(DPI, DPI))
            
            print(f"[{i}] ✅ Barcode '{value}' berhasil disimpan di {tmp_filename}")
            
        except Exception as e:
            print(f"[{i}] ❌ Error untuk '{value}': {e}")

if __name__ == "__main__":
    print("🔄 Memulai generate barcode...")
    generate_barcodes()
    print("✅ Selesai!")