#!/usr/bin/env python3
"""
Enhanced Channel Packer GUI

A graphical user interface for packing/unpacking 4 channel images (RGBA).
Features:
- Load multi-channel images (.png, .tga) and extract channels
- Drag-and-drop functionality for easy image loading
- Support for Red, Green, Blue, and Alpha channels
- Export individual channels to separate PNG files
- Pack channels into RGB or RGBA output
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import tkinterdnd2 as tkdnd
from PIL import Image, ImageTk
import os
import threading
from channel_packer import pack_channels, load_grayscale_image, extract_channels_from_image, save_channels_individually


class DropZone(tk.Frame):
    """A drag-and-drop zone for image files."""
    
    def __init__(self, parent, channel_name, color, callback=None):
        super().__init__(parent, relief="raised", borderwidth=2)
        self.callback = callback
        self.channel_name = channel_name
        self.color = color
        self.image_path = None
        self.preview_image = None
        self.channel_image = None  # Store the actual PIL image
        
        # Configure the drop zone
        self.configure(bg="lightgray", width=180, height=180)
        self.pack_propagate(False)
        
        # Create label for channel name
        self.channel_label = tk.Label(
            self, 
            text=f"{channel_name} Channel",
            font=("Arial", 10, "bold"),
            fg=color,
            bg="lightgray"
        )
        self.channel_label.pack(pady=3)
        
        # Create preview label
        self.preview_label = tk.Label(
            self,
            text="Drop image here\nor click to browse",
            font=("Arial", 8),
            fg="gray",
            bg="lightgray",
            wraplength=160
        )
        self.preview_label.pack(expand=True)
        
        # Create file path label
        self.path_label = tk.Label(
            self,
            text="No file selected",
            font=("Arial", 7),
            fg="darkgray",
            bg="lightgray",
            wraplength=170
        )
        self.path_label.pack(side="bottom", pady=1)
        
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
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.gif *.tga"),
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
            self.channel_image = test_image
            
            # Create preview thumbnail
            thumbnail = test_image.copy()
            thumbnail.thumbnail((130, 130), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage for display
            self.preview_image = ImageTk.PhotoImage(thumbnail)
            
            # Update the preview
            self.preview_label.configure(image=self.preview_image, text="")
            
            # Update path label
            filename = os.path.basename(file_path)
            if len(filename) > 22:
                filename = filename[:19] + "..."
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
    
    def set_channel_image(self, channel_image, source_info=""):
        """Set the channel image directly from a PIL Image."""
        if channel_image is None:
            self.clear_image()
            return
            
        try:
            self.channel_image = channel_image
            self.image_path = None  # No file path since it's extracted
            
            # Create preview thumbnail
            thumbnail = channel_image.copy()
            thumbnail.thumbnail((130, 130), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage for display
            self.preview_image = ImageTk.PhotoImage(thumbnail)
            
            # Update the preview
            self.preview_label.configure(image=self.preview_image, text="")
            
            # Update path label
            self.path_label.configure(text=f"From: {source_info}", fg="blue")
            
            # Change background color to indicate loaded
            self.configure(bg="#e8f5e8")
            self.channel_label.configure(bg="#e8f5e8")
            self.preview_label.configure(bg="#e8f5e8")
            self.path_label.configure(bg="#e8f5e8")
            
            # Call callback if provided
            if self.callback:
                self.callback()
                
        except Exception as e:
            messagebox.showerror("Error", f"Error setting channel image: {str(e)}")
    
    def clear_image(self):
        """Clear the loaded image."""
        self.image_path = None
        self.preview_image = None
        self.channel_image = None
        
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
    
    def get_channel_image(self):
        """Get the currently loaded channel image."""
        return self.channel_image
    
    def get_image_path(self):
        """Get the currently loaded image path."""
        return self.image_path


class ChannelPackerGUI:
    """Main GUI application for enhanced channel packing."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Channel Packer - RGBA Channel Editor")
        self.root.geometry("950x750")
        self.root.resizable(True, True)
        
        # Output path
        self.output_path = tk.StringVar(value="packed_output.png")
        
        # Create GUI components
        self.create_widgets()
        
        # Update button states
        self.update_button_states()
    
    def create_widgets(self):
        """Create all GUI widgets."""
        
        # Title
        title_label = tk.Label(
            self.root,
            text="Enhanced Channel Packer",
            font=("Arial", 18, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=10)
        
        # Subtitle
        subtitle_label = tk.Label(
            self.root,
            text="Load multi-channel images or individual channel images • Support for PNG and TGA files",
            font=("Arial", 11),
            fg="#7f8c8d"
        )
        subtitle_label.pack(pady=(0, 10))
        
        # Multi-channel image loader section
        loader_frame = tk.LabelFrame(self.root, text="Load Multi-Channel Image", font=("Arial", 10, "bold"))
        loader_frame.pack(pady=10, padx=20, fill="x")
        
        load_controls_frame = tk.Frame(loader_frame)
        load_controls_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(load_controls_frame, text="Select image file:", font=("Arial", 10)).pack(side="left")
        
        self.source_path = tk.StringVar()
        source_entry = tk.Entry(load_controls_frame, textvariable=self.source_path, font=("Arial", 10), state="readonly")
        source_entry.pack(side="left", fill="x", expand=True, padx=(10, 5))
        
        browse_source_button = tk.Button(
            load_controls_frame,
            text="Browse...",
            command=self.browse_source_image,
            font=("Arial", 10)
        )
        browse_source_button.pack(side="right", padx=(0, 5))
        
        extract_button = tk.Button(
            load_controls_frame,
            text="Extract Channels",
            command=self.extract_channels,
            font=("Arial", 10),
            bg="#3498db",
            fg="white"
        )
        extract_button.pack(side="right")
        
        # Drop zones frame
        drop_frame = tk.LabelFrame(self.root, text="Individual Channels", font=("Arial", 10, "bold"))
        drop_frame.pack(pady=10, padx=20, fill="x")
        
        zones_container = tk.Frame(drop_frame)
        zones_container.pack(pady=10, padx=10, fill="x")
        
        # Configure grid
        zones_container.grid_columnconfigure(0, weight=1)
        zones_container.grid_columnconfigure(1, weight=1)
        zones_container.grid_columnconfigure(2, weight=1)
        zones_container.grid_columnconfigure(3, weight=1)
        
        # Create drop zones
        self.red_zone = DropZone(zones_container, "Red", "#e74c3c", self.update_button_states)
        self.red_zone.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        self.green_zone = DropZone(zones_container, "Green", "#27ae60", self.update_button_states)
        self.green_zone.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        self.blue_zone = DropZone(zones_container, "Blue", "#3498db", self.update_button_states)
        self.blue_zone.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        self.alpha_zone = DropZone(zones_container, "Alpha", "#9b59b6", self.update_button_states)
        self.alpha_zone.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        
        # Export individual channels section
        export_frame = tk.LabelFrame(self.root, text="Export Individual Channels", font=("Arial", 10, "bold"))
        export_frame.pack(pady=10, padx=20, fill="x")
        
        export_controls_frame = tk.Frame(export_frame)
        export_controls_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(export_controls_frame, text="Base filename:", font=("Arial", 10)).pack(side="left")
        
        self.export_base_path = tk.StringVar(value="channels")
        export_entry = tk.Entry(export_controls_frame, textvariable=self.export_base_path, font=("Arial", 10))
        export_entry.pack(side="left", fill="x", expand=True, padx=(10, 5))
        
        export_browse_button = tk.Button(
            export_controls_frame,
            text="Browse...",
            command=self.browse_export_path,
            font=("Arial", 10)
        )
        export_browse_button.pack(side="right", padx=(0, 5))
        
        self.export_channels_button = tk.Button(
            export_controls_frame,
            text="Export All Channels",
            command=self.export_channels,
            font=("Arial", 10),
            bg="#f39c12",
            fg="white",
            state="disabled"
        )
        self.export_channels_button.pack(side="right")
        
        # Output path selection
        output_frame = tk.LabelFrame(self.root, text="Pack Channels Output", font=("Arial", 10, "bold"))
        output_frame.pack(pady=10, padx=20, fill="x")
        
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
        button_frame.pack(pady=15)
        
        self.pack_button = tk.Button(
            button_frame,
            text="Pack Channels",
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
            text="Clear All Channels",
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
            length=400
        )
        self.progress.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Ready - Load channels individually or extract from multi-channel image",
            font=("Arial", 10),
            fg="#7f8c8d"
        )
        self.status_label.pack(pady=5)
        
        # Instructions
        instructions = tk.Text(
            self.root,
            height=5,
            font=("Arial", 9),
            bg="#f8f9fa",
            fg="#2c3e50",
            wrap="word",
            relief="flat"
        )
        instructions.pack(pady=10, padx=20, fill="x")
        instructions.insert("1.0", 
            "Instructions:\n"
            "1. Load a multi-channel image (.png/.tga) and click 'Extract Channels' to auto-fill all channels\n"
            "2. Or drag/drop individual images to each channel manually\n"
            "3. Use 'Export All Channels' to save individual channel images as separate PNG files\n"
            "4. Use 'Pack Channels' to combine channels into a single RGB/RGBA image\n"
            "5. Alpha channel is supported for .tga and .png output formats"
        )
        instructions.configure(state="disabled")
    
    def browse_source_image(self):
        """Browse for source multi-channel image."""
        file_path = filedialog.askopenfilename(
            title="Select multi-channel image to extract channels from",
            filetypes=[
                ("Image files", "*.png *.tga"),
                ("PNG files", "*.png"),
                ("TGA files", "*.tga"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            self.source_path.set(file_path)
    
    def extract_channels(self):
        """Extract channels from the selected multi-channel image."""
        source_file = self.source_path.get().strip()
        if not source_file:
            messagebox.showerror("Error", "Please select a source image file first.")
            return
        
        if not os.path.exists(source_file):
            messagebox.showerror("Error", "Source file does not exist.")
            return
        
        try:
            # Extract channels
            channels = extract_channels_from_image(source_file)
            if channels is None:
                messagebox.showerror("Error", "Failed to extract channels from the image.")
                return
            
            # Get filename for display
            source_filename = os.path.basename(source_file)
            
            # Set the extracted channels to the drop zones
            self.red_zone.set_channel_image(channels.get('red'), source_filename)
            self.green_zone.set_channel_image(channels.get('green'), source_filename)
            self.blue_zone.set_channel_image(channels.get('blue'), source_filename)
            self.alpha_zone.set_channel_image(channels.get('alpha'), source_filename)
            
            self.update_button_states()
            
            # Show success message
            channels_found = [name for name, img in channels.items() if img is not None]
            messagebox.showinfo("Success", f"Successfully extracted channels: {', '.join(channels_found)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error extracting channels: {str(e)}")
    
    def browse_export_path(self):
        """Browse for export base path."""
        file_path = filedialog.asksaveasfilename(
            title="Choose base name for exported channel files",
            defaultextension="",
            filetypes=[("All files", "*.*")]
        )
        if file_path:
            # Remove any extension to use as base
            base_path = os.path.splitext(file_path)[0]
            self.export_base_path.set(base_path)
    
    def export_channels(self):
        """Export all loaded channels as individual PNG files."""
        base_path = self.export_base_path.get().strip()
        if not base_path:
            messagebox.showerror("Error", "Please specify a base filename for export.")
            return
        
        try:
            # Collect loaded channels
            channels = {}
            if self.red_zone.get_channel_image():
                channels['red'] = self.red_zone.get_channel_image()
            if self.green_zone.get_channel_image():
                channels['green'] = self.green_zone.get_channel_image()
            if self.blue_zone.get_channel_image():
                channels['blue'] = self.blue_zone.get_channel_image()
            if self.alpha_zone.get_channel_image():
                channels['alpha'] = self.alpha_zone.get_channel_image()
            
            if not channels:
                messagebox.showerror("Error", "No channels loaded to export.")
                return
            
            # Start progress bar
            self.progress.start()
            self.export_channels_button.configure(state="disabled")
            self.status_label.configure(text="Exporting channels...", fg="#3498db")
            
            # Run export in a separate thread
            thread = threading.Thread(target=self._export_channels_thread, args=(channels, base_path))
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error starting export: {str(e)}")
    
    def _export_channels_thread(self, channels, base_path):
        """Thread function for exporting channels."""
        try:
            saved_files = save_channels_individually(channels, base_path)
            self.root.after(0, self._export_complete, saved_files)
        except Exception as e:
            self.root.after(0, self._export_error, str(e))
    
    def _export_complete(self, saved_files):
        """Called when export is complete."""
        self.progress.stop()
        self.export_channels_button.configure(state="normal")
        self.status_label.configure(text=f"Exported {len(saved_files)} channel(s) successfully!", fg="#27ae60")
        messagebox.showinfo("Success", f"Successfully exported {len(saved_files)} channels:\n" + "\n".join(saved_files))
        self.update_button_states()
    
    def _export_error(self, error_message):
        """Called when export fails."""
        self.progress.stop()
        self.export_channels_button.configure(state="normal")
        self.status_label.configure(text="Error occurred during export", fg="#e74c3c")
        messagebox.showerror("Error", f"Failed to export channels:\n{error_message}")
        self.update_button_states()
    
    def update_button_states(self):
        """Update button states based on loaded channels."""
        red_loaded = self.red_zone.get_channel_image() is not None
        green_loaded = self.green_zone.get_channel_image() is not None
        blue_loaded = self.blue_zone.get_channel_image() is not None
        alpha_loaded = self.alpha_zone.get_channel_image() is not None
        
        # Enable packing if at least one channel is loaded
        any_loaded = red_loaded or green_loaded or blue_loaded or alpha_loaded
        
        # Enable export if any channels are loaded
        self.export_channels_button.configure(state="normal" if any_loaded else "disabled")
        
        if any_loaded:
            self.pack_button.configure(state="normal")
            loaded_channels = []
            if red_loaded:
                loaded_channels.append("Red")
            if green_loaded:
                loaded_channels.append("Green")
            if blue_loaded:
                loaded_channels.append("Blue")
            if alpha_loaded:
                loaded_channels.append("Alpha")
                
            channels_text = f"{len(loaded_channels)} channel(s): {', '.join(loaded_channels)}"
            if alpha_loaded:
                self.status_label.configure(
                    text=f"Ready to pack {channels_text} (RGBA output)",
                    fg="#27ae60"
                )
            else:
                self.status_label.configure(
                    text=f"Ready to pack {channels_text} (RGB output)",
                    fg="#27ae60"
                )
        else:
            self.pack_button.configure(state="disabled")
            self.status_label.configure(
                text="Load at least one channel to begin",
                fg="#e74c3c"
            )
    
    def browse_output_path(self):
        """Browse for output file path."""
        file_path = filedialog.asksaveasfilename(
            title="Save packed image as...",
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("TGA files", "*.tga"),
                ("All files", "*.*")
            ]
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
            
            # Ensure proper extension
            file_ext = os.path.splitext(output_file)[1].lower()
            if file_ext not in ['.png', '.tga']:
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
            # Get channel images
            red_image = self.red_zone.get_channel_image()
            green_image = self.green_zone.get_channel_image()
            blue_image = self.blue_zone.get_channel_image()
            alpha_image = self.alpha_zone.get_channel_image()
            
            # Pack channels
            pack_channels(red_image, green_image, blue_image, output_file, alpha_image)
            
            # Update GUI in main thread
            self.root.after(0, self._pack_complete, output_file)
            
        except Exception as e:
            self.root.after(0, self._pack_error, str(e))
    
    def _pack_complete(self, output_file):
        """Called when packing is complete."""
        self.progress.stop()
        self.pack_button.configure(state="normal")
        self.status_label.configure(text=f"Success! Saved to {os.path.basename(output_file)}", fg="#27ae60")
        messagebox.showinfo("Success", f"Channels successfully packed!\nSaved to: {output_file}")
        self.update_button_states()
    
    def _pack_error(self, error_message):
        """Called when packing fails."""
        self.progress.stop()
        self.pack_button.configure(state="normal")
        self.status_label.configure(text="Error occurred during packing", fg="#e74c3c")
        messagebox.showerror("Error", f"Failed to pack channels:\n{error_message}")
        self.update_button_states()
    
    def clear_all(self):
        """Clear all loaded channels."""
        self.red_zone.clear_image()
        self.green_zone.clear_image()
        self.blue_zone.clear_image()
        self.alpha_zone.clear_image()
        self.source_path.set("")
        self.update_button_states()


def main():
    """Main function to run the enhanced GUI application."""
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
