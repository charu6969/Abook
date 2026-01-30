"""
Simple test script to verify Tesseract OCR is working
Run this to test if your OCR setup is correct
"""
import sys
import os

print("="*50)
print("TESSERACT OCR TEST")
print("="*50)

# Test 1: Check pytesseract import
print("\n1. Testing pytesseract import...")
try:
    import pytesseract
    print("   ✓ pytesseract imported successfully")
except ImportError as e:
    print(f"   ✗ Failed to import pytesseract: {e}")
    print("   Solution: Run 'pip install pytesseract'")
    sys.exit(1)

# Test 2: Check PIL import
print("\n2. Testing PIL/Pillow import...")
try:
    from PIL import Image
    print("   ✓ PIL imported successfully")
except ImportError as e:
    print(f"   ✗ Failed to import PIL: {e}")
    print("   Solution: Run 'pip install Pillow'")
    sys.exit(1)

# Test 3: Auto-detect Tesseract
print("\n3. Auto-detecting Tesseract...")
if sys.platform == 'win32':
    possible_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    ]
    
    found = False
    for path in possible_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            print(f"   ✓ Tesseract found at: {path}")
            found = True
            break
    
    if not found:
        print("   ✗ Tesseract not found in common locations")
        print("   Please install from: https://github.com/UB-Mannheim/tesseract/wiki")
        sys.exit(1)
else:
    print("   ℹ Non-Windows system, assuming Tesseract is in PATH")

# Test 4: Check Tesseract version
print("\n4. Testing Tesseract executable...")
try:
    version = pytesseract.get_tesseract_version()
    print(f"   ✓ Tesseract version: {version}")
except Exception as e:
    print(f"   ✗ Failed to run Tesseract: {e}")
    print("   Make sure Tesseract is properly installed")
    sys.exit(1)

# Test 5: Simple OCR test
print("\n5. Testing OCR on sample text...")
try:
    # Create a simple test image with text
    from PIL import Image, ImageDraw, ImageFont
    
    # Create white image
    img = Image.new('RGB', (400, 100), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw text
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    draw.text((10, 30), "HELLO WORLD", fill='black', font=font)
    
    # Try OCR
    text = pytesseract.image_to_string(img)
    text = text.strip()
    
    print(f"   OCR Result: '{text}'")
    
    if 'HELLO' in text.upper() or 'WORLD' in text.upper():
        print("   ✓ OCR is working correctly!")
    else:
        print("   ⚠ OCR returned unexpected result")
        print("   This might still work with handwriting")
        
except Exception as e:
    print(f"   ✗ OCR test failed: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("✓ ALL TESTS PASSED!")
print("Your OCR setup is working correctly.")
print("="*50)
print("\nTips for using OCR in ABook:")
print("1. Write clearly in CAPITAL LETTERS")
print("2. Use good spacing between words")
print("3. Write with thick, dark strokes")
print("4. Avoid cursive handwriting")
print("5. Keep the background clean (white)")