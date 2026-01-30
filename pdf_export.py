"""
PDF Export for ABook Notebooks
"""
import pygame
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from PIL import Image
import io
import os
from datetime import datetime


class PDFExporter:
    """Export notebooks to PDF format"""
    
    def export_notebook(self, notebook, filepath=None):
        """Export notebook to PDF"""
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = "".join(c for c in notebook.name if c.isalnum() or c in (' ', '_')).strip()
            filepath = f"{safe_name}_{timestamp}.pdf"
        
        if not filepath.endswith('.pdf'):
            filepath += '.pdf'
        
        print(f"\n[PDF] Creating: {filepath}")
        
        # Create PDF
        c = canvas.Canvas(filepath, pagesize=A4)
        width, height = A4
        
        # Title page
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(width/2, height - 100, notebook.name)
        c.setFont("Helvetica", 12)
        c.drawCentredString(width/2, height - 150, datetime.now().strftime('%B %d, %Y'))
        c.showPage()
        
        # Export layers
        for i, layer in enumerate(notebook.layers):
            if layer.visible:
                print(f"[PDF] Layer {i+1}/{len(notebook.layers)}")
                self._add_layer(c, layer, width, height, i+1)
        
        c.save()
        print(f"[PDF] ✓ Saved: {filepath}")
        return filepath
    
    def _add_layer(self, c, layer, width, height, page_num):
        """Add layer to PDF"""
        # Convert surface to PIL
        surf_w, surf_h = layer.surf.get_size()
        raw_str = pygame.image.tostring(layer.surf, 'RGBA')
        pil_img = Image.frombytes('RGBA', (surf_w, surf_h), raw_str)
        
        # White background
        white_bg = Image.new('RGB', pil_img.size, 'white')
        white_bg.paste(pil_img, mask=pil_img.split()[3])
        
        # Scale to fit
        scale = min((width - 100) / surf_w, (height - 150) / surf_h)
        new_w = int(surf_w * scale)
        new_h = int(surf_h * scale)
        resized = white_bg.resize((new_w, new_h), Image.Resampling.LANCZOS)
        
        # Draw
        img_buf = io.BytesIO()
        resized.save(img_buf, format='PNG')
        img_buf.seek(0)
        
        x = (width - new_w) / 2
        y = (height - new_h) / 2
        c.drawImage(ImageReader(img_buf), x, y, new_w, new_h)
        c.drawRightString(width - 50, 30, f"Page {page_num}")
        c.showPage()