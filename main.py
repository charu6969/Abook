"""
ABook - Digital Notebook Application
Main application file
"""
import pygame
import sys
from config import *
from boot import run_boot_sequence
from ui_components import OnScreenKeyboard
from models import Notebook
from home_view import HomeView
from notepad_view import NotepadView
from text_view import TextView
from text_processor import TextProcessor


class ABookApp:
    """Main application class"""
    def __init__(self):
        pygame.init()
        
        # Display setup - LANDSCAPE WINDOW with PORTRAIT CONTENT
        # Physical window is 1024x600 (landscape)
        self.screen = pygame.display.set_mode((1024, 600))
        
        # Virtual portrait surface (600x1024) that we'll rotate and display
        self.portrait_surface = pygame.Surface((600, 1024))
        
        pygame.display.set_caption("ABook")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font_s = pygame.font.SysFont('Arial', 16)
        self.font_m = pygame.font.SysFont('Arial', 20)
        self.font_l = pygame.font.SysFont('Arial', 32, bold=True)
        fonts = (self.font_s, self.font_m, self.font_l)
        
        # Views
        self.home_view = HomeView(fonts)
        self.notepad_view = NotepadView(fonts)
        self.text_view = TextView(fonts)
        self.current_view = 'home'
        
        # Text processor
        self.text_processor = TextProcessor()
        
        # Data - Create sample notebooks in different folders
        self.notebooks = [
            Notebook("My First Note", folder='notes'),
        ]
        
        # Add Atomic Habits study notebook with chapter structure
        atomic_habits = self._create_atomic_habits_book()
        self.notebooks.append(atomic_habits)
        
        # Add a story book for reading and highlighting
        story_book = self._create_story_book()
        self.notebooks.append(story_book)
        
        # Add 50-page sample book
        sample_book = self._create_sample_book()
        self.notebooks.append(sample_book)
        
        self.active_notebook_idx = 0
        self.active_layer_idx = 0
        
        # UI components
        self.keyboard = OnScreenKeyboard(self.font_s)
        self.renaming_idx = None
        self.temp_name = ""
        
        # Processing state
        self.processing = False
    
    def _create_atomic_habits_book(self):
        """Create Atomic Habits study notebook with chapter structure"""
        from models import Layer
        
        print("[Setup] Creating Atomic Habits study notebook...")
        
        book = Notebook("Atomic Habits", "books")
        book.layers = []
        
        # Chapter structure and key concepts
        # User can add their own notes and highlights from the actual book
        chapter_pages = [
            ["ATOMIC HABITS", "", "by James Clear", "", "", "", "A study notebook"],
            ["", "INTRODUCTION", "", "The Surprising Power", "of Atomic Habits", "", "", "Notes:"],
            
            # THE FUNDAMENTALS
            ["", "PART I", "THE FUNDAMENTALS", "", "Why Tiny Changes", "Make a Big Difference"],
            ["", "Chapter 1", "The Surprising Power", "of Atomic Habits", "", "", "Key Points:", ""],
            ["", "Chapter 2", "How Your Habits", "Shape Your Identity", "(and Vice Versa)", "", "Key Points:", ""],
            ["", "Chapter 3", "How to Build", "Better Habits", "in 4 Simple Steps", "", "Key Points:", ""],
            
            # THE 1ST LAW: MAKE IT OBVIOUS
            ["", "PART II", "THE 1ST LAW", "Make It Obvious", "", "", ""],
            ["", "Chapter 4", "The Man Who Didn't", "Look Right", "", "Implementation", "Intentions", ""],
            ["", "Chapter 5", "The Best Way to", "Start a New Habit", "", "Habit Stacking", "", ""],
            ["", "Chapter 6", "Motivation Is", "Overrated;", "Environment Often", "Matters More", "", ""],
            ["", "Chapter 7", "The Secret to", "Self-Control", "", "Make Bad Habits", "Invisible", ""],
            
            # THE 2ND LAW: MAKE IT ATTRACTIVE
            ["", "PART III", "THE 2ND LAW", "Make It Attractive", "", "", ""],
            ["", "Chapter 8", "How to Make a", "Habit Irresistible", "", "Temptation", "Bundling", ""],
            ["", "Chapter 9", "The Role of Family", "and Friends in", "Shaping Your Habits", "", "", ""],
            ["", "Chapter 10", "How to Find and", "Fix the Causes", "of Your Bad Habits", "", "", ""],
            
            # THE 3RD LAW: MAKE IT EASY
            ["", "PART IV", "THE 3RD LAW", "Make It Easy", "", "", ""],
            ["", "Chapter 11", "Walk Slowly, but", "Never Backward", "", "Two-Minute Rule", "", ""],
            ["", "Chapter 12", "The Law of", "Least Effort", "", "Prime Your", "Environment", ""],
            ["", "Chapter 13", "How to Stop", "Procrastinating by", "Using the", "Two-Minute Rule", "", ""],
            ["", "Chapter 14", "How to Make Good", "Habits Inevitable", "and Bad Habits", "Impossible", "", ""],
            
            # THE 4TH LAW: MAKE IT SATISFYING
            ["", "PART V", "THE 4TH LAW", "Make It Satisfying", "", "", ""],
            ["", "Chapter 15", "The Cardinal Rule", "of Behavior Change", "", "What Is Immediately", "Rewarded Is Repeated", ""],
            ["", "Chapter 16", "How to Stick with", "Good Habits", "Every Day", "", "Habit Tracking", ""],
            ["", "Chapter 17", "How an", "Accountability Partner", "Can Change", "Everything", "", ""],
            
            # ADVANCED TACTICS
            ["", "PART VI", "ADVANCED TACTICS", "", "How to Go from", "Being Merely Good", "to Being Truly Great"],
            ["", "Chapter 18", "The Truth About", "Talent", "(When Genes Matter", "and When They Don't)", "", ""],
            ["", "Chapter 19", "The Goldilocks Rule:", "How to Stay", "Motivated in Life", "and Work", "", ""],
            ["", "Chapter 20", "The Downside of", "Creating Good Habits", "", "Keep Your Identity", "Small", ""],
            
            # CONCLUSION
            ["", "CONCLUSION", "", "The Secret to", "Results That Last", "", "", ""],
            
            # Personal Notes Pages
            ["", "MY HABITS", "TO BUILD", "", "", "", "", ""],
            ["", "MY HABITS", "TO BREAK", "", "", "", "", ""],
            ["", "HABIT TRACKER", "", "Month: _______", "", "", "", ""],
            ["", "IDENTITY", "STATEMENT", "", "I am someone who...", "", "", ""],
            ["", "KEY TAKEAWAYS", "", "", "", "", "", ""],
            ["", "ACTION PLAN", "", "", "", "", "", ""],
            ["", "PROGRESS NOTES", "", "", "", "", "", ""],
            ["", "REFLECTIONS", "", "", "", "", "", ""],
        ]
        
        # Create pages with proper formatting
        for page_lines in chapter_pages:
            layer = Layer("Blank")
            layer.surf.fill((255, 255, 255))  # White background
            
            # Draw the text
            font_title = pygame.font.SysFont('Arial', 26, bold=True)
            font_content = pygame.font.SysFont('Arial', 22)
            
            y = 50
            line_spacing = 45
            
            for line in page_lines:
                if line:
                    # Detect if it's a title (all caps or specific keywords)
                    if line.isupper() or line in ["PART I", "PART II", "PART III", "PART IV", "PART V", "PART VI"]:
                        text_surf = font_title.render(line, True, (0, 0, 0))
                        x = (layer.surf.get_width() - text_surf.get_width()) // 2
                    else:
                        text_surf = font_content.render(line, True, (0, 0, 0))
                        x = 40  # Left aligned for regular text
                    
                    layer.surf.blit(text_surf, (x, y))
                
                y += line_spacing
                
                # Handle overflow (shouldn't happen with our content)
                if y > layer.surf.get_height() - 100:
                    break
            
            book.layers.append(layer)
        
        print(f"[Setup] Created Atomic Habits book with {len(book.layers)} pages")
        return book
    
    
    def _create_story_book(self):
        """Create a short story for reading and highlighting"""
        from models import Layer
        
        print("[Setup] Creating storybook 'The Little Star'...")
        
        book = Notebook("The Little Star", "books")
        book.layers = []
        
        # Simple story - each page is one layer
        story_pages = [
            # Title page
            "THE LITTLE STAR\n\n\nA Tale of Dreams\nand Discovery",
            
            # Chapter 1
            "CHAPTER 1\nThe Lonely Sky\n\nHigh above the Earth, in the vast\nexpanse of space, there lived a little\nstar named Stella.\n\nUnlike the other stars who shone\nbrightly and confidently, Stella felt\nsmall and insignificant.",
            
            "Every night, she watched the Moon\nglow softly, admired by everyone below.\n\nShe saw planets with their rings and\nmoons, celebrated for their beauty.\n\n\"What am I here for?\" Stella wondered,\nher light flickering softly. \"I'm just one\ntiny star among billions.\"",
            
            # Chapter 2
            "CHAPTER 2\nThe Wish\n\nOne clear night, a child named Luna sat\nby her window, gazing at the sky.\n\nShe had moved to a new city and felt\nlonely, far from her old friends.\n\n\"I wish I had someone to talk to,\"\nLuna whispered to the darkness.",
            
            "Stella heard the wish. It traveled\nthrough space like a gentle melody,\nreaching her heart.\n\nFor the first time in her long existence,\nsomeone had noticed her light.\n\n\"Maybe I can be her friend,\" thought\nStella. She began to shine a little\nbrighter, sending her light toward Luna.",
            
            "Luna noticed a star that seemed to\ntwinkle just for her.\n\nIt wasn't the brightest star, but there\nwas something special about it.\nSomething warm.\n\n\"Hello, little star,\" Luna said softly.\n\"Are you saying hello back?\"",
            
            # Chapter 3
            "CHAPTER 3\nThe Connection\n\nNight after night, Luna returned to her\nwindow. She would tell Stella about her\nday, her worries, her dreams.\n\nAnd Stella would listen, her light\nsteady and true.",
            
            "Stella realized something wonderful:\nshe didn't need to be the biggest or\nbrightest.\n\nShe just needed to be there, constant\nand caring.\n\nHer purpose wasn't to outshine others,\nbut to provide comfort to one lonely girl.",
            
            "\"You're my favorite star,\" Luna told her\none night. \"Not because you're the\nbrightest, but because you're mine.\"\n\nStella glowed with happiness.\n\nShe understood now that every star, no\nmatter how small, can light up someone's\ndarkness.",
            
            # Chapter 4
            "CHAPTER 4\nNew Friends\n\nAs weeks passed, Luna made friends at\nher new school.\n\nShe was less lonely now, but she never\nforgot to check on Stella each night.\n\n\"I have friends now,\" Luna told the star.\n\"But you're still special to me.\"",
            
            "Stella noticed something else too.\nOther children had started looking at\nthe sky, following Luna's gaze.\n\nSoon, many people were looking up,\nfinding their own stars, making their\nown wishes.\n\nStella had inspired others simply by\nbeing herself.",
            
            # Chapter 5  
            "CHAPTER 5\nThe Truth\n\nYears passed. Luna grew up, but she\nnever stopped looking for her special\nstar.\n\nEven when life got busy, even when\nclouds covered the sky, she knew\nStella was there.",
            
            "On Luna's eighteenth birthday, she sat\nby the same window, now with her own\ndaughter.\n\n\"See that star?\" Luna pointed. \"That's\nmy friend Stella. She taught me that\nI'm never alone.\"\n\nThe little girl's eyes widened.",
            
            "\"Just look up and find one that speaks\nto your heart,\" Luna smiled.\n\nStella watched the scene, her light\nwarm with contentment.\n\nShe had found her purpose: to remind\nothers that they matter, that they're\nseen, that they're loved.",
            
            # Epilogue
            "EPILOGUE\n\n\nEvery star has a story.\n\nEvery heart has a light.\n\nAnd somewhere in the universe,\nthey find each other.\n\n\nTHE END",
        ]
        
        # Create each page as a layer
        font_text = pygame.font.SysFont('Georgia', 22)
        
        for page_text in story_pages:
            layer = Layer("Blank")
            layer.surf.fill((255, 255, 255))  # White background
            
            # Draw text lines
            lines = page_text.split('\n')
            y = 60
            
            for line in lines:
                if line.strip():
                    text_surf = font_text.render(line, True, (20, 20, 20))
                    x = 50  # Left margin
                    layer.surf.blit(text_surf, (x, y))
                y += 32  # Line spacing
            
            book.layers.append(layer)
        
        print(f"[Setup] Created 'The Little Star' with {len(book.layers)} pages")
        return book
    
    def _create_sample_book(self):
        """Create a 50-page sample storybook"""
        from models import Layer
        
        print("[Setup] Creating sample storybook...")
        
        book = Notebook("The Digital Adventure", "books")
        book.layers = []
        
        # Story content - A simple adventure story
        story_pages = [
            # Page 1-5: Introduction
            ["THE DIGITAL ADVENTURE", "", "By ABook", "", "", "A tale of technology", "and creativity"],
            ["Chapter 1", "The Beginning", "", "Once upon a time,", "in a small town,", "there lived a student", "named Alex."],
            ["Alex loved to take", "notes and draw,", "but traditional notebooks", "were getting expensive.", "", "One day, Alex discovered", "ABook!"],
            ["It was perfect!", "Alex could write, draw,", "and organize everything", "in one place.", "", "This was the beginning", "of an amazing journey."],
            ["Chapter 2", "Discovery", "", "Alex explored every", "feature.", "", "The pen tool felt natural,", "like real paper."],
            
            # Page 6-10
            ["Templates were amazing!", "Grid paper for math,", "lined paper for essays,", "blank pages for art.", "", "Each template made", "work easier."],
            ["The layer system was", "brilliant.", "", "Alex could separate", "notes from diagrams,", "text from drawings.", "", "Very organized!"],
            ["Chapter 3", "Creating", "", "Alex started creating", "more and more.", "", "Book reports,", "study guides,", "and sketches."],
            ["The OCR feature was", "magical!", "", "Handwritten notes became", "searchable text", "instantly.", "", "No more retyping!"],
            ["Templates helped Alex", "work faster.", "", "Math on graph paper,", "essays on lined paper,", "sketches on blank.", "", "Perfect every time."],
            
            # Continue with more readable pages
            ["Chapter 4", "Sharing", "", "Alex wanted to share", "work with classmates.", "", "The PDF export was", "perfect for this."],
            ["Teachers were impressed.", "Clean, organized", "submissions.", "", "Easy to read", "and grade.", "", "Classmates asked", "for tips!"],
            ["The database feature", "was genius.", "", "Automatic backups meant", "never losing work.", "", "Everything saved", "safely."],
            ["Chapter 5", "Organization", "", "Alex organized notebooks", "into folders.", "", "Notes for daily work,", "Books for projects."],
            ["Each notebook could", "have multiple layers.", "", "Rough drafts on one,", "final work on another.", "", "Perfect separation!"],
            
            # More pages
            ["The word search helped", "with vocabulary.", "", "Look up any word,", "see definitions and", "synonyms instantly.", "", "Learning was easier."],
            ["Chapter 6", "Creativity", "", "Alex started drawing", "more.", "", "Sketches, diagrams,", "and comics."],
            ["Different pen sizes", "for different effects.", "", "Thin lines for details,", "thick lines for bold.", "", "Every drawing looked", "great!"],
            ["Colors stayed clean.", "Black ink on white,", "just like a real", "notebook.", "", "Simple, professional,", "beautiful."],
            ["Templates inspired", "creativity.", "", "Graph paper for", "geometric art,", "blank pages for", "freeform drawing."],
            
            # Pages 21-30
            ["Chapter 7", "Advanced Features", "", "Alex discovered more.", "", "Layer merging,", "reordering,", "visibility controls."],
            ["Moving layers changed", "the composition.", "", "Hide and show parts,", "perfect for", "presentations.", "", "So much control!"],
            ["The search feature", "found anything", "instantly.", "", "Notes from months ago,", "specific topics.", "", "Everything findable."],
            ["Chapter 8", "Productivity", "", "Alex became more", "productive.", "", "Work finished faster,", "quality improved."],
            ["No more lost papers.", "No more messy erasures.", "No more running out", "of pages.", "", "Everything digital,", "everything perfect."],
            ["Homework took less", "time.", "", "Notes were clearer.", "Studies were more", "effective.", "", "Grades improved!"],
            ["Teachers noticed", "the change.", "", "Better organization,", "clearer submissions,", "more creativity.", "", "Alex was thriving."],
            ["Chapter 9", "Helping Others", "", "Alex taught friends", "to use ABook.", "", "Showed them all", "the features."],
            ["Study groups became", "better.", "", "Everyone had", "organized notes.", "Sharing was easier.", "", "Teams improved."],
            ["The whole class", "improved.", "", "Better grades,", "better organization,", "better creativity.", "", "ABook helped everyone."],
            
            # Pages 31-40
            ["Chapter 10", "Achievement", "", "At the end of the year,", "Alex looked back.", "", "Hundreds of pages,", "dozens of projects."],
            ["All in one place.", "All organized.", "All accessible.", "", "This was the power", "of digital notebooks.", "", "Truly amazing!"],
            ["The science fair", "project was entirely", "in ABook.", "", "Research, diagrams,", "calculations,", "sketches."],
            ["Alex won first place!", "", "The judges were", "impressed by the", "organization.", "", "ABook made it", "possible."],
            ["Chapter 11", "The Future", "", "Alex planned to use", "ABook forever.", "", "High school, college,", "career."],
            ["New features were", "coming.", "", "Cloud sync,", "collaboration tools,", "more templates.", "", "The future was bright."],
            ["Mobile apps would", "arrive.", "", "Take notes anywhere,", "on phone or tablet.", "", "Perfect for", "on-the-go!"],
            ["Alex dreamed of", "becoming a developer.", "", "Creating tools", "like ABook,", "helping others learn.", "", "Technology for good."],
            ["Chapter 12", "Reflection", "", "What made ABook", "special?", "", "The freedom it gave", "to create and learn."],
            ["Digital didn't mean", "impersonal.", "", "It meant powerful,", "flexible, accessible.", "", "Best of both worlds."],
            
            # Pages 41-50
            ["Alex wrote in ABook", "daily.", "", "Thoughts, ideas,", "dreams.", "", "Everything preserved,", "organized."],
            ["Friends and family", "saw the transformation.", "", "More organized,", "more creative,", "more successful.", "", "Thanks to ABook."],
            ["Chapter 13", "Gratitude", "", "Alex was grateful", "for discovering ABook.", "", "It changed", "everything."],
            ["Every notebook told", "a story.", "", "Math problems solved,", "essays written,", "art created.", "", "All preserved forever."],
            ["The journey continued.", "", "New notebooks,", "new layers,", "new pages every day.", "", "Always growing,", "always learning."],
            ["Chapter 14", "Inspiration", "", "Alex inspired others.", "", "Teachers, students,", "artists.", "", "Everyone could benefit."],
            ["ABook became", "essential.", "", "Not just for school,", "but for life.", "", "Planning, creating,", "organizing, dreaming."],
            ["The Digital Adventure", "continued every day.", "", "New challenges,", "new projects,", "new achievements.", "", "All in ABook."],
            ["Epilogue", "", "And so the story", "continues.", "", "With ABook,", "anything is possible.", "", "Your adventure awaits!"],
            ["THE END", "", "", "Thank you for reading!", "", "", "Start your own", "Digital Adventure", "today!", "", "- ABook Team"]
        ]
        
        # Create pages with better rendering
        for page_num, content in enumerate(story_pages, 1):
            layer = Layer("Blank")
            
            # Fill with white to ensure clean background
            layer.surf.fill((255, 255, 255))
            
            # Page number - smaller, top right
            try:
                page_font = pygame.font.SysFont("Arial", 14)
                page_text = page_font.render(f"Page {page_num}", True, (150, 150, 150))
                layer.surf.blit(page_text, (layer.surf.get_width() - 100, 25))
            except:
                pass
            
            # Content - PROPER SPACING
            try:
                content_font = pygame.font.SysFont("Arial", 22)
                title_font = pygame.font.SysFont("Arial", 26, bold=True)
            except:
                content_font = pygame.font.SysFont(None, 22)
                title_font = pygame.font.SysFont(None, 26)
            
            y = 90
            line_spacing = 32  # Fixed spacing between lines
            
            for line in content:
                if not line:  # Empty line
                    y += line_spacing
                    continue
                
                # Choose font
                if line.startswith("Chapter") or line == "THE DIGITAL ADVENTURE" or line == "THE END" or line == "Epilogue":
                    font = title_font
                    color = (0, 0, 0)
                else:
                    font = content_font
                    color = (60, 60, 60)
                
                # Render with anti-aliasing
                text_surface = font.render(line, True, color)
                layer.surf.blit(text_surface, (50, y))
                y += line_spacing
                
                # Don't overflow page
                if y > layer.surf.get_height() - 50:
                    break
            
            book.layers.append(layer)
        
        print(f"[Setup] ✓ Storybook created with {len(book.layers)} pages")
        return book
    
    def run(self):
        """Main application loop"""
        # Show boot animation (on landscape screen)
        run_boot_sequence(self.screen, self.clock)
        
        # Main loop
        while True:
            # Get mouse position in landscape window coordinates
            landscape_mouse_pos = pygame.mouse.get_pos()
            
            # Transform to portrait coordinates for 90° counter-clockwise rotation
            # Portrait is 600 wide x 1024 tall
            # After 90° CCW: portrait (0,0) -> landscape (0, 600)
            # Formula: portrait_x = 600 - landscape_y
            #          portrait_y = landscape_x
            portrait_mouse_pos = (
                600 - landscape_mouse_pos[1],    # Portrait X = 600 - landscape Y
                landscape_mouse_pos[0]            # Portrait Y = landscape X
            )
            mouse_pos = portrait_mouse_pos
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_down(mouse_pos)
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.current_view == 'notepad':
                        self.notepad_view.stop_drawing()
                
                elif event.type == pygame.MOUSEMOTION:
                    if self.current_view == 'notepad' and self.notepad_view.drawing:
                        notebook = self.notebooks[self.active_notebook_idx]
                        layer = notebook.layers[self.active_layer_idx]
                        # Update the surface with the new stroke
                        self.notepad_view.draw_stroke(layer.surf, mouse_pos)
                        # Make sure the surface is marked as modified
                        layer.modified = True
                
                elif event.type == pygame.MOUSEWHEEL:
                    # Handle scrolling in notepad and text views
                    if self.current_view == 'notepad':
                        self.notepad_view.handle_scroll(event.y)
                    elif self.current_view == 'text':
                        self.text_view.handle_scroll(event.y)
            
            # Render current view to PORTRAIT surface (600x1024)
            if self.current_view == 'home':
                self.home_view.draw(
                    self.portrait_surface,
                    self.notebooks,
                    self.keyboard,
                    self.renaming_idx,
                    self.temp_name
                )
            elif self.current_view == 'notepad':
                notebook = self.notebooks[self.active_notebook_idx]
                self.notepad_view.draw(self.portrait_surface, notebook)
            elif self.current_view == 'text':
                self.text_view.draw(self.portrait_surface)
                
                # Show processing indicator
                if self.processing:
                    overlay = pygame.Surface((600, 1024), pygame.SRCALPHA)
                    overlay.fill((0, 0, 0, 128))
                    self.portrait_surface.blit(overlay, (0, 0))
                    msg = self.font_l.render("Processing...", True, COLOR_WHITE)
                    self.portrait_surface.blit(msg, (300 - 100, 512))
            
            # Rotate portrait surface 90° counter-clockwise - buttons on LEFT side
            rotated = pygame.transform.rotate(self.portrait_surface, 90)
            
            # After 90° rotation: 1024 wide × 600 tall - perfect fit!
            self.screen.fill((0, 0, 0))  # Black background
            self.screen.blit(rotated, (0, 0))
            
            pygame.display.flip()
            self.clock.tick(FPS)
    
    def handle_mouse_down(self, pos):
        """Handle mouse down events"""
        if self.current_view == 'home':
            self.handle_home_click(pos)
        elif self.current_view == 'notepad':
            self.handle_notepad_click(pos)
        elif self.current_view == 'text':
            self.handle_text_click(pos)
    
    def handle_home_click(self, pos):
        """Handle clicks on home view"""
        action, data = self.home_view.handle_click(
            pos,
            self.notebooks,
            self.keyboard,
            self.renaming_idx,
            self.temp_name
        )
        
        if action == 'switch_folder':
            # Folder tab clicked
            pass  # Already handled in modern_home
        
        elif action == 'open_notebook':
            self.active_notebook_idx = data
            self.active_layer_idx = 0
            self.current_view = 'notepad'
        
        elif action == 'add_notebook':
            # Add new notebook to the current folder
            folder = data
            if folder:
                count = sum(1 for nb in self.notebooks if nb.folder == folder)
                folder_names = {'notes': 'Note', 'books': 'Book'}
                new_name = f"{folder_names.get(folder, 'Note')} {count + 1}"
                self.notebooks.append(Notebook(new_name, folder=folder))
        
        elif action == 'delete_notebook':
            # Delete notebook at index
            if 0 <= data < len(self.notebooks):
                del self.notebooks[data]
        
        # Legacy actions for compatibility
        elif action == 'open_folder':
            self.home_view.set_folder(data)
        
        elif action == 'back_to_folders':
            if hasattr(self.home_view, 'back_to_main'):
                self.home_view.back_to_main()
            self.keyboard.visible = False
            self.renaming_idx = None
        
        elif action == 'new_notebook':
            folder = data
            count = sum(1 for nb in self.notebooks if nb.folder == folder)
            folder_names = {'notes': 'Note', 'books': 'Book'}
            new_name = f"{folder_names[folder]} {count + 1}"
            self.notebooks.append(Notebook(new_name, folder=folder))
        
        elif action == 'start_rename':
            self.renaming_idx = data
            self.temp_name = self.notebooks[data].name
            self.keyboard.visible = True
        
        elif action == 'rename_done':
            self.notebooks[self.renaming_idx].name = data
            self.keyboard.visible = False
            self.renaming_idx = None
        
        elif action == 'add_char':
            self.temp_name += data
        
        elif action == 'backspace':
            self.temp_name = self.temp_name[:-1]
    
    def handle_notepad_click(self, pos):
        """Handle clicks on notepad view"""
        action, data = self.notepad_view.handle_click(pos)
        
        if action == 'back':
            self.current_view = 'home'
        
        elif action == 'select_pen':
            self.notepad_view.select_tool('pen')
        
        elif action == 'select_highlighter':
            self.notepad_view.select_tool('highlighter')
        
        elif action == 'select_eraser':
            self.notepad_view.select_tool('eraser')
        
        elif action == 'increase_size':
            self.notepad_view.adjust_size(True)
        
        elif action == 'decrease_size':
            self.notepad_view.adjust_size(False)
        
        elif action == 'convert_to_text':
            self.convert_handwriting_to_text()
        
        elif action == 'check_spelling':
            self.check_spelling()
        
        elif action == 'close_suggestions':
            self.notepad_view.show_suggestions = False
            self.notepad_view.current_suggestions = []
        
        elif action == 'ignore_all_spelling':
            self.notepad_view.show_suggestions = False
            self.notepad_view.current_suggestions = []
        
        elif action == 'recheck_spelling':
            self.check_spelling()
        
        elif action == 'accept_suggestion':
            original_word, suggestion, error_idx = data
            # TODO: Replace word in layer (requires text layer support)
            print(f"[Spell Check] Accepting: '{original_word}' → '{suggestion}'")
            # For now, just remove this error from suggestions
            if error_idx < len(self.notepad_view.current_suggestions):
                self.notepad_view.current_suggestions.pop(error_idx)
            if not self.notepad_view.current_suggestions:
                self.notepad_view.show_suggestions = False
        
        elif action == 'toggle_template_menu':
            self.notepad_view.show_template_menu = not self.notepad_view.show_template_menu
            self.notepad_view.show_layer_menu = False
            self.notepad_view.show_search_panel = False
        
        elif action == 'toggle_layer_menu':
            self.notepad_view.show_layer_menu = not self.notepad_view.show_layer_menu
            self.notepad_view.show_template_menu = False
            self.notepad_view.show_search_panel = False
        
        elif action == 'toggle_search':
            print(f"[DEBUG] Toggle search action received")
            print(f"[DEBUG] Current view: {self.current_view}")
            # Toggle the search panel
            was_showing = self.notepad_view.show_search_panel
            self.notepad_view.show_search_panel = not was_showing
            print(f"[DEBUG] Search panel now: {self.notepad_view.show_search_panel}")
            self.notepad_view.show_template_menu = False
            self.notepad_view.show_layer_menu = False
            self.notepad_view.show_definition = False
            
            # Extract words from notebook when opening search (only if opening)
            if self.notepad_view.show_search_panel and not was_showing:
                print("[DEBUG] Starting word extraction...")
                # Set empty list first so UI shows loading state
                self.notepad_view.extracted_words = []
                # Force a display update
                pygame.display.flip()
                # Now extract words
                self.extract_words_from_notebook()
                print("[DEBUG] Word extraction complete")
        
        elif action == 'close_search':
            self.notepad_view.show_search_panel = False
            self.notepad_view.show_definition = False
        
        elif action == 'search_word':
            self.search_word_definition(data)
        
        elif action == 'back_to_word_list':
            self.notepad_view.show_definition = False
        
        elif action == 'export_pdf':
            self.export_to_pdf()
        
        elif action == 'save_to_db':
            self.save_to_database()
        
        elif action == 'select_template':
            self.apply_template(data)
            self.notepad_view.show_template_menu = False
        
        elif action == 'add_layer':
            notebook = self.notebooks[self.active_notebook_idx]
            from models import Layer
            notebook.layers.append(Layer())
            self.active_layer_idx = len(notebook.layers) - 1
        
        elif action == 'select_layer':
            self.active_layer_idx = data
        
        elif action == 'toggle_layer_visibility':
            notebook = self.notebooks[self.active_notebook_idx]
            notebook.layers[data].visible = not notebook.layers[data].visible
        
        elif action == 'move_layer_up':
            notebook = self.notebooks[self.active_notebook_idx]
            if data > 0:
                # Swap layers
                notebook.layers[data], notebook.layers[data-1] = notebook.layers[data-1], notebook.layers[data]
        
        elif action == 'move_layer_down':
            notebook = self.notebooks[self.active_notebook_idx]
            if data < len(notebook.layers) - 1:
                # Swap layers
                notebook.layers[data], notebook.layers[data+1] = notebook.layers[data+1], notebook.layers[data]
        
        elif action == 'merge_all_layers':
            self.merge_all_visible_layers()
        
        elif action == 'close_search':
            self.notepad_view.show_search_panel = False
        
        elif action == 'start_drawing':
            self.notepad_view.start_drawing(data)
    
    def apply_template(self, template_name):
        """Apply a template to the current layer"""
        from templates import get_template_by_name
        
        notebook = self.notebooks[self.active_notebook_idx]
        layer = notebook.layers[self.active_layer_idx]
        
        # Get the template
        template = get_template_by_name(template_name)
        
        # Draw template on layer surface
        template.draw(layer.surf)
        
        # Update layer template name
        layer.template_name = template_name
        
        print(f"Applied template: {template_name}")
    
    def handle_text_click(self, pos):
        """Handle clicks on text view"""
        action, data = self.text_view.handle_click(pos)
        
        if action == 'back':
            self.current_view = 'notepad'
        
        elif action == 'change_font':
            self.text_view.change_font()
        
        elif action == 'size_up':
            self.text_view.change_size(True)
        
        elif action == 'size_down':
            self.text_view.change_size(False)
        
        elif action == 'toggle_summary':
            self.text_view.toggle_summary()
    
    
    def check_spelling(self):
        """Run spell check on current notebook layer"""
        try:
            # Try to import writing assistant
            try:
                from writing_assistant import get_writing_assistant
            except ImportError:
                print("[Error] Writing assistant not available")
                print("[Info] Install: pip install pyspellchecker language-tool-python")
                return
            
            notebook = self.notebooks[self.active_notebook_idx]
            layer = notebook.layers[self.active_layer_idx]
            
            # First, run OCR to get text
            print("[Spell Check] Running OCR on layer...")
            text = self.text_processor.extract_text_from_surface(layer.surf)
            
            if not text.strip():
                print("[Spell Check] No text found in layer")
                self.notepad_view.show_suggestions = False
                return
            
            print(f"[Spell Check] Extracted text: {text[:100]}...")
            
            # Get writing assistant
            assistant = get_writing_assistant()
            
            # Check spelling
            errors = assistant.check_spelling(text)
            
            if errors:
                print(f"[Spell Check] Found {len(errors)} spelling errors")
                self.notepad_view.current_suggestions = errors
                self.notepad_view.show_suggestions = True
                # Close other panels
                self.notepad_view.show_template_menu = False
                self.notepad_view.show_layer_menu = False
                self.notepad_view.show_search_panel = False
            else:
                print("[Spell Check] No spelling errors found!")
                self.notepad_view.show_suggestions = False
                self.notepad_view.current_suggestions = []
                
        except Exception as e:
            print(f"[Error] Spell check failed: {e}")
            import traceback
            traceback.print_exc()
    
    def convert_handwriting_to_text(self):
        """Convert current notebook page to text"""
        print("\n" + "="*50)
        print("STARTING HANDWRITING CONVERSION")
        print("="*50)
        
        self.processing = True
        pygame.display.flip()
        
        # Get current layer surface
        notebook = self.notebooks[self.active_notebook_idx]
        layer = notebook.layers[self.active_layer_idx]
        surface = layer.surf
        
        print(f"Layer surface size: {surface.get_size()}")
        print(f"Layer modified flag: {layer.modified}")
        print(f"Surface format: {surface.get_flags()}")
        
        # Check if there's actually anything drawn
        # Get a small sample area to check
        try:
            pixel_data = pygame.surfarray.array3d(surface)
            import numpy as np
            
            # Check if all pixels are the same (likely blank)
            unique_colors = len(np.unique(pixel_data.reshape(-1, 3), axis=0))
            print(f"Unique colors in surface: {unique_colors}")
            
            if unique_colors <= 2:
                print("⚠ WARNING: Surface appears to be blank or nearly blank!")
                print("  Make sure you're drawing on the canvas before converting.")
        except Exception as e:
            print(f"Could not analyze surface: {e}")
        
        # Save a preview of what we're sending to OCR
        try:
            pygame.image.save(surface, 'debug_layer_surface.png')
            print("✓ Saved layer surface as 'debug_layer_surface.png'")
            print("  Open this file to see what OCR is receiving")
        except Exception as e:
            print(f"✗ Could not save debug image: {e}")
        
        # Extract text
        print("\nCalling OCR...")
        text = self.text_processor.extract_text_from_surface(surface)
        
        # Auto-correct spelling if writing assistant available
        corrections_made = []
        try:
            from writing_assistant import get_writing_assistant
            assistant = get_writing_assistant()
            
            print("\n[Auto-Correct] Checking spelling...")
            original_text = text
            
            # Get errors before correcting
            errors = assistant.check_spelling(original_text)
            
            # Apply corrections
            corrected_text = assistant.auto_correct(text, aggressive=False)
            
            # Track what was corrected
            if original_text != corrected_text and errors:
                print("[Auto-Correct] ✓ Fixed spelling errors:")
                for error in errors[:10]:  # Show first 10
                    if error.get('suggestions'):
                        correction = (error['word'], error['suggestions'][0])
                        corrections_made.append(correction)
                        print(f"  • '{error['word']}' → '{error['suggestions'][0]}'")
                text = corrected_text
            else:
                print("[Auto-Correct] ✓ No errors found")
                
        except Exception as e:
            print(f"[Auto-Correct] Skipped: {e}")
        
        self.text_view.set_text(text)
        self.text_view.corrections_made = corrections_made
        self.text_view.show_corrections_info = len(corrections_made) > 0
        
        print(f"\nOCR returned {len(text)} characters")
        if text:
            print(f"Preview: {text[:200]}...")
        else:
            print("Preview: (empty)")
        
        # Generate summary if text is long enough
        if len(text) > 100 and not text.startswith("[No text detected]"):
            print("\nGenerating summary...")
            summary = self.text_processor.summarize_text(text)
            self.text_view.set_summary(summary)
            print(f"Summary: {summary[:100]}...")
        
        self.processing = False
        self.current_view = 'text'
        
        print("\n" + "="*50)
        print("CONVERSION COMPLETE")
        print("="*50 + "\n")



    def extract_words_from_notebook(self):
        """Extract words from current notebook page using OCR"""
        print("\n[Word Search] Extracting words from notebook...")
        
        # Get current layer surface
        notebook = self.notebooks[self.active_notebook_idx]
        surface = notebook.layers[self.active_layer_idx].surf
        
        # Extract text using OCR
        text = self.text_processor.extract_text_from_surface(surface)
        
        if text and not text.startswith("[No text detected]"):
            # Split into words and clean
            import re
            words = re.findall(r'\b[a-zA-Z]+\b', text)
            # Remove duplicates and sort
            unique_words = sorted(list(set(words)), key=str.lower)
            self.notepad_view.extracted_words = unique_words[:15]  # Limit to 15 words
            print(f"[Word Search] Found {len(unique_words)} unique words")
        else:
            self.notepad_view.extracted_words = []
            print("[Word Search] No text found in notebook")
    
    def search_word_definition(self, word):
        """Search for word definition"""
        print(f"\n[Word Search] Looking up: {word}")
        
        from word_search import WordSearcher
        searcher = WordSearcher()
        
        # Get definition
        result = searcher.search_definition(word)
        result['word'] = word
        
        # Show definition
        self.notepad_view.current_word_definition = result
        self.notepad_view.show_definition = True
        
        if result.get('found'):
            print(f"[Word Search] ✓ Found definition for '{word}'")
        else:
            print(f"[Word Search] ✗ '{word}' not found in dictionary")
    
    def export_to_pdf(self):
        """Export current notebook to PDF"""
        notebook = self.notebooks[self.active_notebook_idx]
        
        try:
            from pdf_export import PDFExporter
            exporter = PDFExporter()
            filepath = exporter.export_notebook(notebook)
            
            print(f"\n✓ PDF Exported!")
            print(f"  File: {filepath}")
            print(f"  You can find it in the ABook folder")
            
        except ImportError as e:
            print(f"\n✗ Cannot export PDF: Missing library")
            print(f"  Install with: pip install reportlab")
        except Exception as e:
            print(f"\n✗ PDF Export Error: {e}")
    
    def save_to_database(self):
        """Save current notebook to database"""
        notebook = self.notebooks[self.active_notebook_idx]
        
        try:
            from database import NotebookDB
            
            # Initialize or get existing DB connection
            if not hasattr(self, 'db'):
                self.db = NotebookDB()
            
            notebook_id = self.db.save_notebook(notebook)
            
            print(f"\n✓ Saved to Database!")
            print(f"  Notebook: {notebook.name}")
            print(f"  ID: {notebook_id}")
            
            # Show stats
            stats = self.db.get_stats()
            print(f"  Total notebooks in DB: {stats['total']}")
            
        except Exception as e:
            print(f"\n✗ Database Save Error: {e}")
            import traceback
            traceback.print_exc()
    
    def merge_all_visible_layers(self):
        """Merge all visible layers into one"""
        notebook = self.notebooks[self.active_notebook_idx]
        
        # Get all visible layers
        visible_layers = [l for l in notebook.layers if l.visible]
        
        if len(visible_layers) <= 1:
            print("[Layers] Need at least 2 visible layers to merge")
            return
        
        # Create new merged surface
        from models import Layer
        merged = Layer("Blank")
        
        # Draw all visible layers onto merged layer
        for layer in visible_layers:
            merged.surf.blit(layer.surf, (0, 0))
        
        # Replace all layers with just the merged one
        notebook.layers = [merged]
        self.active_layer_idx = 0
        
        print(f"[Layers] Merged {len(visible_layers)} layers into 1")


if __name__ == "__main__":
    app = ABookApp()
    app.run()