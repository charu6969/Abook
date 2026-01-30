"""
Text processing module for handwriting recognition and summarization
"""
import pygame
from PIL import Image
import sys
import os

class TextProcessor:
    """Handles OCR and text summarization"""
    
    def __init__(self):
        self._setup_tesseract()
        self.ocr_available = self._check_ocr_available()
    
    def _setup_tesseract(self):
        """Setup Tesseract path for Windows if needed"""
        try:
            import pytesseract
            
            # First check if user has set a custom path in config
            try:
                from tesseract_config import TESSERACT_PATH
                if TESSERACT_PATH and os.path.exists(TESSERACT_PATH):
                    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
                    print(f"✓ Tesseract configured from tesseract_config.py: {TESSERACT_PATH}")
                    return
            except ImportError:
                pass
            
            # For Windows: Auto-detect Tesseract in common locations
            if sys.platform == 'win32':
                possible_paths = [
                    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                    r'C:\Users\{}\AppData\Local\Tesseract-OCR\tesseract.exe'.format(os.getenv('USERNAME', ''))
                ]
                
                for path in possible_paths:
                    if os.path.exists(path):
                        pytesseract.pytesseract.tesseract_cmd = path
                        print(f"✓ Tesseract auto-detected at: {path}")
                        return
                
                print("⚠ Tesseract not found. Please set TESSERACT_PATH in tesseract_config.py")
                print("  Or install Tesseract to: C:\\Program Files\\Tesseract-OCR\\")
        except ImportError:
            print("⚠ pytesseract module not found. Run: pip install pytesseract")
    
    def _check_ocr_available(self):
        """Check if OCR libraries are available"""
        try:
            import pytesseract
            return True
        except ImportError:
            return False
    
    def extract_text_from_surface(self, surface):
        """
        Extract text from a pygame surface using OCR
        Returns: extracted text string
        """
        print(f"\n[OCR] Starting text extraction...")
        print(f"[OCR] Surface size: {surface.get_size()}")
        print(f"[OCR] OCR available: {self.ocr_available}")
        
        if not self.ocr_available:
            return self._simple_placeholder_extraction()
        
        try:
            import pytesseract
            from PIL import ImageEnhance, ImageOps, ImageFilter
            import numpy as np
            
            # Convert pygame surface to PIL Image
            size = surface.get_size()
            mode = 'RGBA'
            
            print(f"[OCR] Converting surface to PIL Image...")
            # Get raw string buffer from surface
            raw_str = pygame.image.tostring(surface, mode)
            pil_image = Image.frombytes(mode, size, raw_str)
            
            # IMPORTANT: Create a white background and paste the drawing on top
            print(f"[OCR] Creating white background for transparent image...")
            white_bg = Image.new('RGB', pil_image.size, 'white')
            
            # If image has transparency, composite it onto white background
            if pil_image.mode == 'RGBA':
                white_bg.paste(pil_image, mask=pil_image.split()[3])  # Use alpha channel as mask
            else:
                white_bg.paste(pil_image)
            
            pil_image = white_bg
            
            # Convert to grayscale
            print(f"[OCR] Converting to grayscale...")
            pil_image = pil_image.convert('L')
            
            # Enhance contrast to make text darker
            print(f"[OCR] Enhancing image for better OCR...")
            enhancer = ImageEnhance.Contrast(pil_image)
            pil_image = enhancer.enhance(3.0)  # Increased from 2.0 to 3.0
            
            # Sharpen the image
            pil_image = pil_image.filter(ImageFilter.SHARPEN)
            
            # Apply binary threshold to make text pure black and background pure white
            pil_array = np.array(pil_image)
            # More aggressive threshold
            threshold = 220  # Changed from 200
            pil_array = np.where(pil_array < threshold, 0, 255).astype(np.uint8)
            pil_image = Image.fromarray(pil_array)
            
            # Optionally invert if background is darker than foreground
            avg_brightness = np.mean(pil_array)
            print(f"[OCR] Average brightness: {avg_brightness:.1f}")
            
            if avg_brightness < 127:
                print(f"[OCR] Image appears inverted, flipping colors...")
                pil_image = ImageOps.invert(pil_image)
            
            # Crop to content area (remove large white margins)
            print(f"[OCR] Cropping to content area...")
            pil_array = np.array(pil_image)
            rows = np.any(pil_array < 250, axis=1)
            cols = np.any(pil_array < 250, axis=0)
            
            if rows.any() and cols.any():
                ymin, ymax = np.where(rows)[0][[0, -1]]
                xmin, xmax = np.where(cols)[0][[0, -1]]
                # Add some padding
                padding = 20
                ymin = max(0, ymin - padding)
                ymax = min(pil_array.shape[0], ymax + padding)
                xmin = max(0, xmin - padding)
                xmax = min(pil_array.shape[1], xmax + padding)
                pil_image = pil_image.crop((xmin, ymin, xmax, ymax))
                print(f"[OCR] Cropped to: {xmax-xmin}x{ymax-ymin}")
            
            # Resize if too small (make text bigger for better OCR)
            width, height = pil_image.size
            if width < 200 or height < 100:
                scale = max(200 / width, 100 / height, 2.0)
                new_width = int(width * scale)
                new_height = int(height * scale)
                pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                print(f"[OCR] Upscaled to: {new_width}x{new_height}")
            
            # Save debug image
            try:
                pil_image.save('debug_ocr_input.png')
                print(f"[OCR] ✓ Debug image saved as 'debug_ocr_input.png'")
                print(f"[OCR]   → Open this file to see what OCR is reading")
            except Exception as e:
                print(f"[OCR] Could not save debug image: {e}")
            
            # Try multiple OCR configurations
            print(f"[OCR] Running Tesseract OCR with multiple configs...")
            
            # Config 1: Standard
            config1 = r'--oem 3 --psm 7'  # PSM 7 = single text line
            text1 = pytesseract.image_to_string(pil_image, config=config1).strip()
            
            # Config 2: Single word
            config2 = r'--oem 3 --psm 8'  # PSM 8 = single word
            text2 = pytesseract.image_to_string(pil_image, config=config2).strip()
            
            # Config 3: Sparse text
            config3 = r'--oem 3 --psm 11'  # PSM 11 = sparse text
            text3 = pytesseract.image_to_string(pil_image, config=config3).strip()
            
            # Choose the longest result
            results = [text1, text2, text3]
            text = max(results, key=len) if any(results) else ""
            
            print(f"[OCR] Results from different configs:")
            print(f"[OCR]   Config 1 (line): '{text1}'")
            print(f"[OCR]   Config 2 (word): '{text2}'")
            print(f"[OCR]   Config 3 (sparse): '{text3}'")
            print(f"[OCR] Selected: '{text}'")
            
            if text:
                print(f"[OCR] ✓ SUCCESS! Text was detected: '{text}'")
            else:
                print(f"[OCR] ✗ No text detected (empty result)")
            
            if not text:
                return "[No text detected]\n\nTips:\n- Write in LARGE, clear CAPITAL letters\n- Write HORIZONTALLY (not diagonal)\n- Use very thick, dark strokes (pen size 10-15)\n- Ensure good spacing between words\n- Avoid cursive writing - use PRINT letters\n- Try writing 'HELLO' in big block letters"
            
            return text
            
        except Exception as e:
            print(f"[OCR] ✗ Error: {e}")
            import traceback
            traceback.print_exc()
            return f"[OCR processing error: {str(e)}]"
    
    def _simple_placeholder_extraction(self):
        """Placeholder when OCR is not available"""
        return "[Handwriting detected]\n\nTo convert handwriting to text, please install:\n\n1. pip install pytesseract pillow\n\n2. Download Tesseract OCR:\nhttps://github.com/UB-Mannheim/tesseract/wiki\n\n3. Install to: C:\\Program Files\\Tesseract-OCR\\"
    
    def summarize_text(self, text, max_sentences=3):
        """
        Summarize text using simple extractive summarization
        Returns: summarized text
        """
        if not text or len(text.strip()) < 50:
            return text
        
        # Simple sentence-based summarization
        sentences = [s.strip() for s in text.replace('\n', '. ').split('.') if s.strip()]
        
        if len(sentences) <= max_sentences:
            return text
        
        # Score sentences by length and position
        scored = []
        for i, sentence in enumerate(sentences):
            # Prefer longer sentences and earlier positions
            score = len(sentence.split()) - (i * 0.5)
            scored.append((score, sentence))
        
        # Sort by score and take top sentences
        scored.sort(reverse=True)
        top_sentences = sorted(scored[:max_sentences], key=lambda x: sentences.index(x[1]))
        
        summary = '. '.join([s for _, s in top_sentences])
        if summary and not summary.endswith('.'):
            summary += '.'
        
        return summary
    
    def advanced_summarize(self, text):
        """
        Advanced summarization using transformers (if available)
        """
        try:
            from transformers import pipeline
            
            # Use a summarization model
            summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
            
            # Limit input length for the model
            if len(text) > 1024:
                text = text[:1024]
            
            summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
            return summary[0]['summary_text']
            
        except ImportError:
            # Fall back to simple summarization
            return self.summarize_text(text)
        except Exception as e:
            print(f"Advanced summarization error: {e}")
            return self.summarize_text(text)