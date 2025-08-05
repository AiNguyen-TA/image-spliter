#!/usr/bin/env python3
"""
Image Splitter GUI Application
A tool to split images into smaller pieces based on grid specifications.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
import math

class ImageSplitterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Splitter")
        self.root.geometry("800x600")
        
        # Variables
        self.image_path = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.rows = tk.IntVar(value=2)
        self.cols = tk.IntVar(value=2)
        self.original_image = None
        self.preview_image = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        # File selection section
        ttk.Label(main_frame, text="Select Image:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.image_path, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_image).grid(row=0, column=2, padx=5)
        
        # Output directory selection
        ttk.Label(main_frame, text="Output Directory:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_dir, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_output_dir).grid(row=1, column=2, padx=5)
        
        # Grid configuration section
        grid_frame = ttk.LabelFrame(main_frame, text="Split Configuration", padding="10")
        grid_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        grid_frame.columnconfigure(1, weight=1)
        grid_frame.columnconfigure(3, weight=1)
        
        ttk.Label(grid_frame, text="Rows:").grid(row=0, column=0, sticky=tk.W, padx=5)
        ttk.Spinbox(grid_frame, from_=1, to=20, textvariable=self.rows, width=10, 
                   command=self.update_preview).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(grid_frame, text="Columns:").grid(row=0, column=2, sticky=tk.W, padx=5)
        ttk.Spinbox(grid_frame, from_=1, to=20, textvariable=self.cols, width=10,
                   command=self.update_preview).grid(row=0, column=3, sticky=tk.W, padx=5)
        
        # Info label
        self.info_label = ttk.Label(grid_frame, text="This will create 4 images (2×2)")
        self.info_label.grid(row=1, column=0, columnspan=4, pady=5)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="Preview", command=self.preview_split).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Split Image", command=self.split_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_all).pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Preview area
        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding="10")
        preview_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        
        # Canvas for preview with scrollbars
        canvas_frame = ttk.Frame(preview_frame)
        canvas_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        canvas_frame.columnconfigure(0, weight=1)
        canvas_frame.rowconfigure(0, weight=1)
        
        self.canvas = tk.Canvas(canvas_frame, bg='white')
        self.canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.canvas.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.canvas.configure(xscrollcommand=h_scrollbar.set)
        
        # Bind events
        self.rows.trace('w', self.update_info)
        self.cols.trace('w', self.update_info)
        
        # Initialize
        self.update_info()
        
    def browse_image(self):
        filename = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.image_path.set(filename)
            self.load_image()
            
    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir.set(directory)
            
    def load_image(self):
        try:
            self.original_image = Image.open(self.image_path.get())
            self.update_preview()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
            
    def update_info(self, *args):
        total_images = self.rows.get() * self.cols.get()
        self.info_label.config(text=f"This will create {total_images} images ({self.rows.get()}×{self.cols.get()})")
        
    def update_preview(self, *args):
        if self.original_image:
            self.preview_split()
            
    def preview_split(self):
        if not self.original_image:
            messagebox.showwarning("Warning", "Please select an image first.")
            return
            
        # Create preview with grid lines
        preview_img = self.original_image.copy()
        
        # Calculate dimensions
        img_width, img_height = preview_img.size
        piece_width = img_width // self.cols.get()
        piece_height = img_height // self.rows.get()
        
        # Resize for preview if too large
        max_preview_size = 400
        if img_width > max_preview_size or img_height > max_preview_size:
            ratio = min(max_preview_size / img_width, max_preview_size / img_height)
            new_width = int(img_width * ratio)
            new_height = int(img_height * ratio)
            preview_img = preview_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Recalculate piece dimensions for preview
            piece_width = new_width // self.cols.get()
            piece_height = new_height // self.rows.get()
        
        # Convert to PhotoImage for display
        self.preview_image = ImageTk.PhotoImage(preview_img)
        
        # Clear canvas and display image
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.preview_image)
        
        # Draw grid lines
        for i in range(1, self.cols.get()):
            x = i * piece_width
            self.canvas.create_line(x, 0, x, preview_img.height, fill="red", width=2)
            
        for i in range(1, self.rows.get()):
            y = i * piece_height
            self.canvas.create_line(0, y, preview_img.width, y, fill="red", width=2)
            
        # Update canvas scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def split_image(self):
        if not self.original_image:
            messagebox.showwarning("Warning", "Please select an image first.")
            return
            
        if not self.output_dir.get():
            messagebox.showwarning("Warning", "Please select an output directory.")
            return
            
        try:
            # Create output directory if it doesn't exist
            os.makedirs(self.output_dir.get(), exist_ok=True)
            
            # Get image dimensions
            img_width, img_height = self.original_image.size
            piece_width = img_width // self.cols.get()
            piece_height = img_height // self.rows.get()
            
            # Calculate total pieces for progress bar
            total_pieces = self.rows.get() * self.cols.get()
            self.progress['maximum'] = total_pieces
            self.progress['value'] = 0
            
            # Get base filename
            base_name = os.path.splitext(os.path.basename(self.image_path.get()))[0]
            
            piece_count = 0
            
            # Split the image
            for row in range(self.rows.get()):
                for col in range(self.cols.get()):
                    # Calculate crop box
                    left = col * piece_width
                    top = row * piece_height
                    right = left + piece_width
                    bottom = top + piece_height
                    
                    # Handle edge cases (last row/column might be slightly different)
                    if col == self.cols.get() - 1:
                        right = img_width
                    if row == self.rows.get() - 1:
                        bottom = img_height
                    
                    # Crop and save
                    piece = self.original_image.crop((left, top, right, bottom))
                    filename = f"{base_name}_piece_{row+1}_{col+1}.png"
                    filepath = os.path.join(self.output_dir.get(), filename)
                    piece.save(filepath, "PNG")
                    
                    # Update progress
                    piece_count += 1
                    self.progress['value'] = piece_count
                    self.root.update_idletasks()
            
            messagebox.showinfo("Success", f"Image split into {total_pieces} pieces successfully!\nSaved to: {self.output_dir.get()}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to split image: {str(e)}")
        finally:
            self.progress['value'] = 0
            
    def clear_all(self):
        self.image_path.set("")
        self.output_dir.set("")
        self.rows.set(2)
        self.cols.set(2)
        self.original_image = None
        self.preview_image = None
        self.canvas.delete("all")
        self.progress['value'] = 0

def main():
    root = tk.Tk()
    app = ImageSplitterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
