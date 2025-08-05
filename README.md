# Image Splitter

A Python GUI application that splits images into smaller pieces based on grid specifications.

## Features

- **Easy-to-use GUI**: Simple interface built with tkinter
- **Flexible grid splitting**: Specify any number of rows and columns (e.g., 2×4 creates 8 pieces)
- **Live preview**: See how your image will be split with visual grid lines
- **Multiple image formats**: Supports PNG, JPG, JPEG, GIF, BMP, TIFF
- **PNG output**: All split pieces are saved as PNG files
- **Progress tracking**: Visual progress bar during splitting process
- **Smart naming**: Output files are named systematically (e.g., `image_piece_1_1.png`, `image_piece_1_2.png`, etc.)

## Requirements

- Python 3.6 or higher
- Pillow (PIL) library

## Installation

### Option 1: Using the provided batch files (Windows - Recommended)

1. Clone or download this repository
2. Double-click `setup.bat` to create a virtual environment and install dependencies
3. Double-click `run.bat` to start the application

### Option 2: Manual installation

1. Clone or download this repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Using batch files (Windows)
- Double-click `run.bat` to start the application

### Manual run
1. Activate the virtual environment (if using one):
   ```bash
   venv\Scripts\activate
   ```
2. Run the application:
   ```bash
   python image_splitter.py
   ```

2. **Select an image**: Click "Browse" next to "Select Image" to choose your input image

3. **Choose output directory**: Click "Browse" next to "Output Directory" to select where the split images will be saved

4. **Configure the split**:
   - Set the number of **Rows** (vertical divisions)
   - Set the number of **Columns** (horizontal divisions)
   - For example: 2 rows × 4 columns = 8 total pieces

5. **Preview**: Click "Preview" to see how your image will be split (red grid lines show the divisions)

6. **Split**: Click "Split Image" to create all the individual pieces

## Output

- All pieces are saved as PNG files
- Files are named: `[original_name]_piece_[row]_[column].png`
- Example: If your original image is `photo.jpg` and you split it 2×3, you'll get:
  - `photo_piece_1_1.png` (top-left)
  - `photo_piece_1_2.png` (top-center)
  - `photo_piece_1_3.png` (top-right)
  - `photo_piece_2_1.png` (bottom-left)
  - `photo_piece_2_2.png` (bottom-center)
  - `photo_piece_2_3.png` (bottom-right)

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
