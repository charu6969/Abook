"""
Database Support for ABook
Save and load notebooks from SQLite database
"""
import sqlite3
import pickle
import pygame
from datetime import datetime


class NotebookDB:
    """SQLite database for notebooks"""
    
    def __init__(self, db_file="abook.db"):
        self.db_file = db_file
        self.conn = sqlite3.connect(db_file)
        self._create_tables()
        print(f"[DB] Connected to: {db_file}")
    
    def _create_tables(self):
        """Create database tables"""
        cursor = self.conn.cursor()
        
        # Notebooks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notebooks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                folder TEXT NOT NULL,
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        
        # Layers table  
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS layers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                notebook_id INTEGER,
                layer_num INTEGER,
                template_name TEXT,
                visible INTEGER,
                surface_data BLOB,
                FOREIGN KEY (notebook_id) REFERENCES notebooks(id) ON DELETE CASCADE
            )
        ''')
        
        self.conn.commit()
    
    def save_notebook(self, notebook):
        """Save notebook to database"""
        cursor = self.conn.cursor()
        now = datetime.now().isoformat()
        
        # Check if exists
        cursor.execute('SELECT id FROM notebooks WHERE name = ?', (notebook.name,))
        existing = cursor.fetchone()
        
        if existing:
            # Update
            nb_id = existing[0]
            cursor.execute('UPDATE notebooks SET folder=?, updated_at=? WHERE id=?',
                         (notebook.folder, now, nb_id))
            cursor.execute('DELETE FROM layers WHERE notebook_id=?', (nb_id,))
            print(f"[DB] Updated: {notebook.name}")
        else:
            # Insert new
            cursor.execute('INSERT INTO notebooks (name, folder, created_at, updated_at) VALUES (?, ?, ?, ?)',
                         (notebook.name, notebook.folder, now, now))
            nb_id = cursor.lastrowid
            print(f"[DB] Saved: {notebook.name} (ID: {nb_id})")
        
        # Save layers
        for i, layer in enumerate(notebook.layers):
            surface_bytes = self._surface_to_bytes(layer.surf)
            cursor.execute('''INSERT INTO layers 
                            (notebook_id, layer_num, template_name, visible, surface_data)
                            VALUES (?, ?, ?, ?, ?)''',
                         (nb_id, i, layer.template_name, int(layer.visible), surface_bytes))
        
        self.conn.commit()
        print(f"[DB] Saved {len(notebook.layers)} layers")
        return nb_id
    
    def load_notebook(self, notebook_id):
        """Load notebook from database"""
        cursor = self.conn.cursor()
        
        # Get notebook
        cursor.execute('SELECT name, folder FROM notebooks WHERE id=?', (notebook_id,))
        result = cursor.fetchone()
        
        if not result:
            print(f"[DB] Notebook {notebook_id} not found")
            return None
        
        name, folder = result
        
        # Create notebook
        from models import Notebook, Layer
        notebook = Notebook(name, folder)
        notebook.layers = []
        
        # Load layers
        cursor.execute('SELECT template_name, visible, surface_data FROM layers WHERE notebook_id=? ORDER BY layer_num',
                      (notebook_id,))
        
        for template_name, visible, surface_data in cursor.fetchall():
            layer = Layer(template_name)
            layer.visible = bool(visible)
            layer.surf = self._bytes_to_surface(surface_data)
            notebook.layers.append(layer)
        
        print(f"[DB] Loaded: {name} ({len(notebook.layers)} layers)")
        return notebook
    
    def list_notebooks(self):
        """List all notebooks"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, folder, updated_at FROM notebooks ORDER BY updated_at DESC')
        return cursor.fetchall()
    
    def delete_notebook(self, notebook_id):
        """Delete notebook"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM notebooks WHERE id=?', (notebook_id,))
        self.conn.commit()
        print(f"[DB] Deleted notebook {notebook_id}")
    
    def search(self, query):
        """Search notebooks by name"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, folder FROM notebooks WHERE name LIKE ?',
                      (f'%{query}%',))
        return cursor.fetchall()
    
    def get_stats(self):
        """Get database statistics"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM notebooks')
        total = cursor.fetchone()[0]
        cursor.execute('SELECT folder, COUNT(*) FROM notebooks GROUP BY folder')
        by_folder = dict(cursor.fetchall())
        return {'total': total, 'by_folder': by_folder}
    
    def _surface_to_bytes(self, surface):
        """Convert pygame surface to bytes"""
        size = surface.get_size()
        raw_str = pygame.image.tostring(surface, 'RGBA')
        data = {'size': size, 'data': raw_str}
        return pickle.dumps(data)
    
    def _bytes_to_surface(self, data_bytes):
        """Convert bytes to pygame surface"""
        from PIL import Image
        data = pickle.loads(data_bytes)
        size = data['size']
        raw_str = data['data']
        
        # Create surface
        surface = pygame.Surface(size, pygame.SRCALPHA)
        pil_img = Image.frombytes('RGBA', size, raw_str)
        
        # Convert to pygame
        py_img = pygame.image.fromstring(pil_img.tobytes(), size, 'RGBA')
        surface.blit(py_img, (0, 0))
        return surface
    
    def close(self):
        """Close database connection"""
        self.conn.close()
        print("[DB] Closed")