#!/usr/bin/env python3
"""
Channel Packer GUI

A graphical user interface for packing 3 grayscale images into RGB channels.
Features drag-and-drop functionality for easy image loading and output path selection.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinterdnd2 as tkdnd
from PIL import Image, ImageTk
import os
import threading
from channel_packer import pack_channels, load_grayscale_image


class DropZone(tk.Frame):
    """A drag-and-drop zone for image files."""
    
    def __init__(self, parent, channel_name, color, callback=None):
        super().__init__(parent, relief="raised", borderwidth=2)
        self.callback = callback
        self.channel_name = channel_name
        self.color = color
        self.image_path = None
        self.preview_image = None
        
        # Configure the drop zone
        self.configure(bg="lightgray", width=200, height=200)
        self.pack_propagate(False)
        
        # Create label for channel name
        self.channel_label = tk.Label(
            self, 
            text=f"{channel_name} Channel",
            font=("Arial", 12, "bold"),
            fg=color,
            bg="lightgray"
        )
        self.channel_label.pack(pady=5)
        
        # Create preview label
        self.preview_label = tk.Label(
            self,
            text="Drop image here\nor click to browse",
            font=("Arial", 9),
            fg="gray",
            bg="lightgray",
            wraplength=180
        )
        self.preview_label.pack(expand=True)
        
        # Create file path label
        self.path_label = tk.Label(
            self,
            text="No file selected",
            font=("Arial", 8),
            fg="darkgray",
            bg="lightgray",
            wraplength=190
        )
        self.path_label.pack(side="bottom", pady=2)
        
        # Enable drag and drop
        self.drop_target_register(tkdnd.DND_FILES)
        self.dnd_bind('<<Drop>>', self.on_drop)
        
        # Enable click to browse
        self.bind("<Button-1>", self.on_click)
        self.channel_label.bind("<Button-1>", self.on_click)
        self.preview_label.bind("<Button-1>", self.on_click)
        
        # Configure cursor
        self.configure(cursor="hand2")
    
    def on_drop(self, event):
        """Handle file drop event."""
        files = self.tk.splitlist(event.data)
        if files:
            self.load_image(files[0])
    
    def on_click(self, event):
        """Handle click to browse for file."""
        file_path = filedialog.askopenfilename(
            title=f"Select image for {self.channel_name} channel",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.gif"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.load_image(file_path)
    
    def load_image(self, file_path):
        """Load and preview an image."""
        try:
            # Validate file exists and is an image
            if not os.path.exists(file_path):
                messagebox.showerror("Error", f"File not found: {file_path}")
                return
            
            # Try to load the image
            test_image = load_grayscale_image(file_path)
            if test_image is None:
                messagebox.showerror("Error", f"Could not load image: {file_path}")
                return
            
            self.image_path = file_path
            
            # Create preview thumbnail
            thumbnail = test_image.copy()
            thumbnail.thumbnail((150, 150), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage for display
            self.preview_image = ImageTk.PhotoImage(thumbnail)
            
            # Update the preview
            self.preview_label.configure(image=self.preview_image, text="")
            
            # Update path label
            filename = os.path.basename(file_path)
            if len(filename) > 25:
                filename = filename[:22] + "..."
            self.path_label.configure(text=filename, fg="black")
            
            # Change background color to indicate loaded
            self.configure(bg="#e8f5e8")
            self.channel_label.configure(bg="#e8f5e8")
            self.preview_label.configure(bg="#e8f5e8")
            self.path_label.configure(bg="#e8f5e8")
            
            # Call callback if provided
            if self.callback:
                self.callback()
                
        except Exception as e:
            messagebox.showerror("Error", f"Error loading image: {str(e)}")
    
    def clear_image(self):
        """Clear the loaded image."""
        self.image_path = None
        self.preview_image = None
        
        # Reset preview
        self.preview_label.configure(
            image="",
            text="Drop image here\nor click to browse"
        )
        
        # Reset path label
        self.path_label.configure(text="No file selected", fg="darkgray")
        
        # Reset background color
        self.configure(bg="lightgray")
        self.channel_label.configure(bg="lightgray")
        self.preview_label.configure(bg="lightgray")
        self.path_label.configure(bg="lightgray")
    
    def get_image_path(self):
        """Get the currently loaded image path."""
        return self.image_path


class ChannelPackerGUI:
    """Main GUI application for channel packing."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Channel Packer - Pack 3 Images into RGB Channels")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Output path
        self.output_path = tk.StringVar(value="packed_output.png")
        
        # Create GUI components
        self.create_widgets()
        
        # Update pack button state
        self.update_pack_button()
    
    def create_widgets(self):
        """Create all GUI widgets."""
        
        # Title
        title_label = tk.Label(
            self.root,
            text="Channel Packer",
            font=("Arial", 18, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=10)
        
        # Subtitle
        subtitle_label = tk.Label(
            self.root,
            text="Drag and drop 1-3 grayscale images to pack them into RGB channels",
            font=("Arial", 11),
            fg="#7f8c8d"
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Drop zones frame
        drop_frame = tk.Frame(self.root)
        drop_frame.pack(pady=10, padx=20, fill="x")
        
        # Configure grid
        drop_frame.grid_columnconfigure(0, weight=1)
        drop_frame.grid_columnconfigure(1, weight=1)
        drop_frame.grid_columnconfigure(2, weight=1)
        
        # Create drop zones
        self.red_zone = DropZone(drop_frame, "Red", "#e74c3c", self.update_pack_button)
        self.red_zone.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.green_zone = DropZone(drop_frame, "Green", "#27ae60", self.update_pack_button)
        self.green_zone.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        self.blue_zone = DropZone(drop_frame, "Blue", "#3498db", self.update_pack_button)
        self.blue_zone.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        
        # Output path selection
        output_frame = tk.LabelFrame(self.root, text="Output Settings", font=("Arial", 10, "bold"))
        output_frame.pack(pady=20, padx=20, fill="x")
        
        path_frame = tk.Frame(output_frame)
        path_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(path_frame, text="Output file:", font=("Arial", 10)).pack(side="left")
        
        self.path_entry = tk.Entry(path_frame, textvariable=self.output_path, font=("Arial", 10))
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(10, 5))
        
        browse_button = tk.Button(
            path_frame,
            text="Browse...",
            command=self.browse_output_path,
            font=("Arial", 10)
        )
        browse_button.pack(side="right")
        
        # Control buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        self.pack_button = tk.Button(
            button_frame,
            text="Pack Images",
            command=self.pack_images,
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            state="disabled",
            width=15,
            height=2
        )
        self.pack_button.pack(side="left", padx=5)
        
        clear_button = tk.Button(
            button_frame,
            text="Clear All",
            command=self.clear_all,
            font=("Arial", 12),
            bg="#e74c3c",
            fg="white",
            width=15,
            height=2
        )
        clear_button.pack(side="left", padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.root,
            mode='indeterminate',
            length=300
        )
        self.progress.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Ready - Load at least 1 image to begin",
            font=("Arial", 10),
            fg="#7f8c8d"
        )
        self.status_label.pack(pady=5)
        
        # Instructions
        instructions = tk.Text(
            self.root,
            height=4,
            font=("Arial", 9),
            bg="#f8f9fa",
            fg="#2c3e50",
            wrap="word",
            relief="flat"
        )
        instructions.pack(pady=10, padx=20, fill="x")
        instructions.insert("1.0", 
            "Instructions:\n"
            "1. Drag and drop or click to select 1-3 grayscale images\n"
            "2. Choose output filename (will be saved as PNG)\n"
            "3. Click 'Pack Images' to combine them into RGB channels\n"
            "Note: Missing channels will be filled with black. Images will be automatically resized to match and converted to grayscale if needed."
        )
        instructions.configure(state="disabled")
    
    def update_pack_button(self):
        """Update the pack button state based on loaded images."""
        red_loaded = self.red_zone.get_image_path() is not None
        green_loaded = self.green_zone.get_image_path() is not None
        blue_loaded = self.blue_zone.get_image_path() is not None
        
        # Enable packing if at least one channel is loaded
        any_loaded = red_loaded or green_loaded or blue_loaded
        
        if any_loaded:
            self.pack_button.configure(state="normal")
            if red_loaded and green_loaded and blue_loaded:
                self.status_label.configure(text="Ready to pack all 3 channels!", fg="#27ae60")
            else:
                loaded_channels = []
                if red_loaded:
                    loaded_channels.append("Red")
                if green_loaded:
                    loaded_channels.append("Green")
                if blue_loaded:
                    loaded_channels.append("Blue")
                self.status_label.configure(
                    text=f"Ready to pack {len(loaded_channels)} channel(s): {', '.join(loaded_channels)} (missing channels will be black)",
                    fg="#f39c12"
                )
        else:
            self.pack_button.configure(state="disabled")
            self.status_label.configure(
                text="Load at least one image to begin",
                fg="#e74c3c"
            )
    
    def browse_output_path(self):
        """Browse for output file path."""
        file_path = filedialog.asksaveasfilename(
            title="Save packed image as...",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if file_path:
            self.output_path.set(file_path)
    
    def pack_images(self):
        """Pack the loaded images into channels."""
        try:
            # Validate output path
            output_file = self.output_path.get().strip()
            if not output_file:
                messagebox.showerror("Error", "Please specify an output filename.")
                return
            
            # Ensure .png extension
            if not output_file.lower().endswith('.png'):
                output_file += '.png'
                self.output_path.set(output_file)
            
            # Start progress bar
            self.progress.start()
            self.pack_button.configure(state="disabled")
            self.status_label.configure(text="Packing images...", fg="#3498db")
            
            # Run packing in a separate thread to avoid freezing GUI
            thread = threading.Thread(target=self._pack_images_thread, args=(output_file,))
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            self.progress.stop()
            self.pack_button.configure(state="normal")
            messagebox.showerror("Error", f"Error starting pack operation: {str(e)}")
    
    def _pack_images_thread(self, output_file):
        """Thread function for packing images."""
        try:
            # Load images or create black images for missing channels
            red_path = self.red_zone.get_image_path()
            green_path = self.green_zone.get_image_path()
            blue_path = self.blue_zone.get_image_path()
            
            # Load available images
            loaded_images = []
            if red_path:
                red_image = load_grayscale_image(red_path)
                if red_image:
                    loaded_images.append(red_image)
            if green_path:
                green_image = load_grayscale_image(green_path)
                if green_image:
                    loaded_images.append(green_image)
            if blue_path:
                blue_image = load_grayscale_image(blue_path)
                if blue_image:
                    loaded_images.append(blue_image)
            
            if not loaded_images:
                raise Exception("No valid images loaded")
            
            # Determine target dimensions from the largest loaded image
            max_width = max(img.width for img in loaded_images)
            max_height = max(img.height for img in loaded_images)
            
            # Create or load each channel
            if red_path and red_image:
                final_red = red_image
            else:
                final_red = Image.new('L', (max_width, max_height), 0)  # Black image
                
            if green_path and green_image:
                final_green = green_image
            else:
                final_green = Image.new('L', (max_width, max_height), 0)  # Black image
                
            if blue_path and blue_image:
                final_blue = blue_image
            else:
                final_blue = Image.new('L', (max_width, max_height), 0)  # Black image
            
            # Pack channels
            pack_channels(final_red, final_green, final_blue, output_file)
            
            # Update GUI in main thread
            self.root.after(0, self._pack_complete, output_file)
            
        except Exception as e:
            self.root.after(0, self._pack_error, str(e))
    
    def _pack_complete(self, output_file):
        """Called when packing is complete."""
        self.progress.stop()
        self.pack_button.configure(state="normal")
        self.status_label.configure(text=f"Success! Saved to {os.path.basename(output_file)}", fg="#27ae60")
        messagebox.showinfo("Success", f"Images successfully packed!\nSaved to: {output_file}")
    
    def _pack_error(self, error_message):
        """Called when packing fails."""
        self.progress.stop()
        self.pack_button.configure(state="normal")
        self.status_label.configure(text="Error occurred during packing", fg="#e74c3c")
        messagebox.showerror("Error", f"Failed to pack images:\n{error_message}")
        self.update_pack_button()
    
    def clear_all(self):
        """Clear all loaded images."""
        self.red_zone.clear_image()
        self.green_zone.clear_image()
        self.blue_zone.clear_image()
        self.update_pack_button()


def main():
    """Main function to run the GUI application."""
    try:
        root = tkdnd.TkinterDnD.Tk()
        app = ChannelPackerGUI(root)
        root.mainloop()
    except ImportError:
        # Fallback if tkinterdnd2 is not available
        print("Warning: tkinterdnd2 not found. Drag-and-drop will not be available.")
        print("Install it with: pip install tkinterdnd2")
        
        root = tk.Tk()
        app = ChannelPackerGUI(root)
        root.mainloop()


if __name__ == "__main__":
    main()
