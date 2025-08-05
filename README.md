# Image Utilities

A unified Python GUI application suite for image processing, including image splitting and channel packing tools.

## Features

### Image Splitter
- **Easy-to-use GUI**: Simple interface built with tkinter
- **Flexible grid splitting**: Specify any number of rows and columns (e.g., 2×4 creates 8 pieces)
- **Live preview**: See how your image will be split with visual grid lines
- **Multiple image formats**: Supports PNG, JPG, JPEG, GIF, BMP, TIFF
- **PNG output**: All split pieces are saved as PNG files
- **Progress tracking**: Visual progress bar during splitting process
- **Smart naming**: Output files are named systematically (e.g., `image_piece_1_1.png`, `image_piece_1_2.png`, etc.)

### Channel Packer
- **RGB Channel packing**: Combine 1-3 grayscale images into RGB channels
- **Drag-and-drop support**: Easy image loading with drag-and-drop functionality
- **Automatic resizing**: Images are automatically resized to match
- **Flexible assignment**: Choose which images go to which color channels
- **Real-time preview**: See the combined result before saving

### Unified Interface
- **Tabbed interface**: Switch between tools with easy navigation buttons
- **Consistent design**: Unified look and feel across all tools
- **Welcome screen**: Overview of available tools and features

## Requirements

- Python 3.7 or higher
- Pillow (PIL) library
- tkinterdnd2 (for drag-and-drop functionality)
- numpy (for channel packing operations)

## Installation

### Option 1: Using the provided batch files (Windows - Recommended)

1. Clone or download this repository
2. Double-click `setup_utils.bat` to create a virtual environment and install all dependencies
3. Choose your preferred launcher:
   - Double-click `run_utils.bat` to start the **unified interface** (recommended)
   - Double-click `run.bat` to start the **image splitter only**

### Option 2: Manual installation

1. Clone or download this repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements_utils.txt
   pip install -r channels-packing/requirements.txt
   ```

## Usage

### Using batch files (Windows)
- **Unified Interface**: Double-click `run_utils.bat` to start the unified image utilities
- **Image Splitter Only**: Double-click `run.bat` to start just the image splitter

### Manual run
1. Activate the virtual environment (if using one):
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```
2. Run the application:
   ```bash
   # Unified interface
   python utils_ui.py
   
   # Image splitter only
   python image_splitter.py
   ```

### Using the Unified Interface

1. **Launch**: Start the application using `run_utils.bat` or `python utils_ui.py`
2. **Navigate**: Use the tool buttons at the top to switch between features:
   - **🏠 Home**: Welcome screen with tool overview
   - **✂️ Image Splitter**: Split images into grid pieces
   - **📦 Channel Packer**: Combine images into RGB channels
3. **Work**: Each tool has its own interface and functionality

### Image Splitter Usage

1. **Select an image**: Click "Browse" next to "Select Image" to choose your input image

2. **Choose output directory**: Click "Browse" next to "Output Directory" to select where the split images will be saved

3. **Configure the split**:
   - Set the number of **Rows** (vertical divisions)
   - Set the number of **Columns** (horizontal divisions)
   - For example: 2 rows × 4 columns = 8 total pieces

4. **Preview**: Click "Preview" to see how your image will be split (red grid lines show the divisions)

5. **Split**: Click "Split Image" to create all the individual pieces

### Channel Packer Usage

1. **Load images**: Drag and drop or click to select 1-3 grayscale images for the RGB channels
2. **Assign channels**: Place images in the Red, Green, and/or Blue channel slots
3. **Set output**: Choose the output filename for the combined image
4. **Pack**: Click "Pack Images" to combine them into a single RGB image

## Output

### Image Splitter Output
- All pieces are saved as PNG files
- Files are named: `[original_name]_piece_[row]_[column].png`
- Example: If your original image is `photo.jpg` and you split it 2×3, you'll get:
  - `photo_piece_1_1.png` (top-left)
  - `photo_piece_1_2.png` (top-center)
  - `photo_piece_1_3.png` (top-right)
  - `photo_piece_2_1.png` (bottom-left)
  - `photo_piece_2_2.png` (bottom-center)
  - `photo_piece_2_3.png` (bottom-right)

### Channel Packer Output
- Combined image saved as PNG file
- Each input image becomes a color channel (Red, Green, Blue)
- Missing channels are filled with black
- Final image has the dimensions of the largest input image

## Examples

- **2×2 split**: Creates 4 equal pieces
- **1×4 split**: Creates 4 horizontal strips
- **3×1 split**: Creates 3 vertical strips
- **2×4 split**: Creates 8 pieces (as requested in your example)

## Notes

- The application handles edge cases where the image dimensions don't divide evenly
- Large images are automatically resized in the preview for better performance
- The original image quality is preserved in the output pieces
- Progress bar shows the splitting progress for large operations
