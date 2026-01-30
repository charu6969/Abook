# ABook - Modular Structure

## Project Structure

```
abook/
├── main.py              # Main application entry point
├── config.py            # Configuration constants and settings
├── boot.py              # Boot animation sequence
├── models.py            # Data models (Notebook, Layer)
├── ui_components.py     # Reusable UI components (Status bar, Keyboard)
├── home_view.py         # Home screen view
└── notepad_view.py      # Notepad/drawing view
```

## File Descriptions

### `main.py`

The main application file that ties everything together. Contains the `ABookApp` class which:

- Initializes pygame and creates the display
- Manages views and navigation
- Handles the main event loop
- Coordinates between different views

### `config.py`

Central configuration file containing:

- Display settings (width, height, FPS)
- Color definitions
- Boot animation timing settings
- Logo letter definitions

### `boot.py`

Boot animation sequence containing:

- `Particle` class for animation particles
- `generate_logo_positions()` function
- `run_boot_sequence()` function

### `models.py`

Data models for the application:

- `Layer` class - represents a drawing layer
- `Notebook` class - represents a notebook with layers

### `ui_components.py`

Reusable UI components:

- `draw_status_bar()` function - renders time, WiFi, battery
- `OnScreenKeyboard` class - virtual keyboard for text input

### `home_view.py`

Home screen view containing:

- `HomeView` class - manages the notebook list display
- Handles rendering and click events for home screen

### `notepad_view.py`

Notepad/drawing view containing:

- `NotepadView` class - manages the drawing interface
- Tool selection (pen/eraser)
- Size adjustment
- Drawing functionality

## How to Run

```bash
python main.py
```

## Benefits of This Structure

1. **Separation of Concerns**: Each file has a specific responsibility
2. **Easy Maintenance**: Changes to one feature don't affect others
3. **Reusability**: Components can be reused across views
4. **Testability**: Individual modules can be tested separately
5. **Scalability**: Easy to add new views or features
6. **Readability**: Smaller files are easier to understand

## Making Updates

- **Change colors/settings**: Edit `config.py`
- **Modify boot animation**: Edit `boot.py`
- **Update home screen**: Edit `home_view.py`
- **Update drawing features**: Edit `notepad_view.py`
- **Add new UI components**: Add to `ui_components.py`
- **Add new data models**: Add to `models.py`
- **Change app flow**: Edit `main.py`
