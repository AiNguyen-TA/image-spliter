#!/usr/bin/env python3
"""
Image Utilities UI
A unified interface for image processing tools including image splitting and channel packing.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add the channels-packing directory to the path so we can import from it
sys.path.append(os.path.join(os.path.dirname(__file__), 'channels-packing'))

# Import the individual tool classes
from image_splitter import ImageSplitterGUI
try:
    from channel_packer_gui import ChannelPackerGUI
    import tkinterdnd2 as tkdnd
    DND_AVAILABLE = True
except ImportError:
    print("Warning: tkinterdnd2 not found. Channel packer drag-and-drop will not be available.")
    print("Install it with: pip install tkinterdnd2")
    DND_AVAILABLE = False


class ImageUtilitiesUI:
    """Main application class that provides a unified interface for image utilities."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Image Utilities - Unified Toolset")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Current active tool
        self.current_tool = None
        self.current_frame = None
        
        # Create the main UI
        self.create_main_ui()
        
        # Show welcome screen by default
        self.show_welcome()
    
    def create_main_ui(self):
        """Create the main UI with navigation buttons and content area."""
        
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Title bar
        title_frame = ttk.Frame(main_container)
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(
            title_frame,
            text="Image Utilities",
            font=("Arial", 24, "bold"),
            fg="#2c3e50"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Unified toolset for image processing tasks",
            font=("Arial", 12),
            fg="#7f8c8d"
        )
        subtitle_label.pack()
        
        # Navigation frame
        nav_frame = ttk.LabelFrame(main_container, text="Tools", padding="10")
        nav_frame.pack(fill='x', pady=(0, 10))
        
        # Create navigation buttons
        button_frame = ttk.Frame(nav_frame)
        button_frame.pack()
        
        # Welcome/Home button
        self.welcome_btn = ttk.Button(
            button_frame,
            text="🏠 Home",
            command=self.show_welcome,
            width=15
        )
        self.welcome_btn.pack(side='left', padx=5)
        
        # Image Splitter button
        self.splitter_btn = ttk.Button(
            button_frame,
            text="✂️ Image Splitter",
            command=self.show_image_splitter,
            width=20
        )
        self.splitter_btn.pack(side='left', padx=5)
        
        # Channel Packer button
        self.packer_btn = ttk.Button(
            button_frame,
            text="📦 Channel Packer",
            command=self.show_channel_packer,
            width=20
        )
        self.packer_btn.pack(side='left', padx=5)
        
        # Status indicator
        self.status_frame = ttk.Frame(nav_frame)
        self.status_frame.pack(fill='x', pady=(10, 0))
        
        self.current_tool_label = tk.Label(
            self.status_frame,
            text="Current Tool: Welcome",
            font=("Arial", 10, "italic"),
            fg="#27ae60"
        )
        self.current_tool_label.pack()
        
        # Content area
        self.content_frame = ttk.Frame(main_container)
        self.content_frame.pack(fill='both', expand=True)
    
    def clear_content(self):
        """Clear the current content area."""
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None
        self.current_tool = None
    
    def update_button_states(self, active_button):
        """Update button states to show which tool is active."""
        # Reset all buttons to normal state
        buttons = [self.welcome_btn, self.splitter_btn, self.packer_btn]
        for btn in buttons:
            btn.state(['!pressed'])
        
        # Set active button to pressed state
        if active_button:
            active_button.state(['pressed'])
    
    def show_welcome(self):
        """Show the welcome screen with tool descriptions."""
        self.clear_content()
        self.update_button_states(self.welcome_btn)
        self.current_tool_label.config(text="Current Tool: Welcome", fg="#27ae60")
        
        # Create welcome content
        welcome_frame = ttk.Frame(self.content_frame)
        welcome_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Welcome message
        welcome_label = tk.Label(
            welcome_frame,
            text="Welcome to Image Utilities!",
            font=("Arial", 18, "bold"),
            fg="#2c3e50"
        )
        welcome_label.pack(pady=(0, 20))
        
        # Tool descriptions
        tools_frame = ttk.Frame(welcome_frame)
        tools_frame.pack(fill='both', expand=True)
        
        # Configure grid
        tools_frame.grid_columnconfigure(0, weight=1)
        tools_frame.grid_columnconfigure(1, weight=1)
        
        # Image Splitter description
        splitter_frame = ttk.LabelFrame(tools_frame, text="Image Splitter", padding="15")
        splitter_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        
        splitter_icon = tk.Label(splitter_frame, text="✂️", font=("Arial", 48))
        splitter_icon.pack(pady=10)
        
        splitter_desc = tk.Label(
            splitter_frame,
            text="Split large images into smaller pieces based on a grid.\n\n"
                 "Features:\n"
                 "• Configurable grid size (rows × columns)\n"
                 "• Real-time preview with grid overlay\n"
                 "• Batch processing\n"
                 "• Progress tracking\n"
                 "• Automatic file naming",
            font=("Arial", 10),
            justify='left',
            wraplength=300
        )
        splitter_desc.pack(pady=10)
        
        splitter_launch_btn = ttk.Button(
            splitter_frame,
            text="Open Image Splitter",
            command=self.show_image_splitter,
            style='Accent.TButton'
        )
        splitter_launch_btn.pack(pady=10)
        
        # Channel Packer description
        packer_frame = ttk.LabelFrame(tools_frame, text="Channel Packer", padding="15")
        packer_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        
        packer_icon = tk.Label(packer_frame, text="📦", font=("Arial", 48))
        packer_icon.pack(pady=10)
        
        drag_drop_text = "\n• Drag-and-drop support" if DND_AVAILABLE else "\n• Click to browse (drag-drop not available)"
        
        packer_desc = tk.Label(
            packer_frame,
            text="Pack 1-3 grayscale images into RGB channels.\n\n"
                 "Features:\n"
                 "• Combine separate images into color channels\n"
                 "• Automatic image resizing and conversion" +
                 drag_drop_text + "\n"
                 "• Real-time preview\n"
                 "• Flexible channel assignment",
            font=("Arial", 10),
            justify='left',
            wraplength=300
        )
        packer_desc.pack(pady=10)
        
        packer_launch_btn = ttk.Button(
            packer_frame,
            text="Open Channel Packer",
            command=self.show_channel_packer,
            style='Accent.TButton'
        )
        packer_launch_btn.pack(pady=10)
        
        # Configure row weight for equal height
        tools_frame.grid_rowconfigure(0, weight=1)
        
        # Instructions
        instructions_frame = ttk.LabelFrame(welcome_frame, text="How to Use", padding="15")
        instructions_frame.pack(fill='x', pady=(20, 0))
        
        instructions_text = tk.Label(
            instructions_frame,
            text="1. Click on a tool button above or use the launch buttons below\n"
                 "2. Each tool opens in the same window with its own interface\n"
                 "3. Use the navigation buttons at the top to switch between tools\n"
                 "4. Return to this welcome screen anytime by clicking the Home button",
            font=("Arial", 11),
            justify='left'
        )
        instructions_text.pack()
        
        self.current_frame = welcome_frame
    
    def show_image_splitter(self):
        """Show the image splitter tool."""
        self.clear_content()
        self.update_button_states(self.splitter_btn)
        self.current_tool_label.config(text="Current Tool: Image Splitter", fg="#e74c3c")
        
        # Create a container for the image splitter
        splitter_container = ttk.Frame(self.content_frame)
        splitter_container.pack(fill='both', expand=True)
        
        # Create a wrapper that better mimics a Tkinter root
        class SplitterWrapper(tk.Frame):
            def __init__(self, parent):
                super().__init__(parent)
                self.pack(fill='both', expand=True)
                self.title_text = "Image Splitter"
                self.geometry_text = "800x600"
                
            def title(self, text):
                self.title_text = text
                
            def geometry(self, geom):
                self.geometry_text = geom
                
            def mainloop(self):
                pass  # Do nothing as we're embedded
        
        # Create the image splitter GUI
        wrapper = SplitterWrapper(splitter_container)
        self.current_tool = ImageSplitterGUI(wrapper)
        self.current_frame = splitter_container
    
    def show_channel_packer(self):
        """Show the channel packer tool."""
        if not DND_AVAILABLE:
            # Show a simplified version or message if drag-and-drop is not available
            messagebox.showwarning(
                "Feature Limited", 
                "Channel Packer is available but drag-and-drop functionality is limited.\n"
                "Install tkinterdnd2 for full functionality:\n\n"
                "pip install tkinterdnd2"
            )
        
        self.clear_content()
        self.update_button_states(self.packer_btn)
        self.current_tool_label.config(text="Current Tool: Channel Packer", fg="#3498db")
        
        # Create a container for the channel packer
        packer_container = ttk.Frame(self.content_frame)
        packer_container.pack(fill='both', expand=True)
        
        # Create a wrapper that better mimics a Tkinter root  
        class PackerWrapper(tk.Frame):
            def __init__(self, parent):
                super().__init__(parent)
                self.pack(fill='both', expand=True)
                self.title_text = "Channel Packer"
                self.geometry_text = "800x600"
                
            def title(self, text):
                self.title_text = text
                
            def geometry(self, geom):
                self.geometry_text = geom
                
            def resizable(self, *args):
                pass  # Do nothing as we're embedded
                
            def mainloop(self):
                pass  # Do nothing as we're embedded
        
        try:
            # Create the channel packer GUI
            if DND_AVAILABLE:
                wrapper = PackerWrapper(packer_container)
                from channel_packer_gui import ChannelPackerGUI
                self.current_tool = ChannelPackerGUI(wrapper)
            else:
                # Create a simplified version without drag-and-drop
                self.create_simplified_channel_packer(packer_container)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Channel Packer: {str(e)}")
            self.show_welcome()
            return
            
        self.current_frame = packer_container
    
    def create_simplified_channel_packer(self, parent):
        """Create a simplified channel packer without drag-and-drop."""
        # Simple message for now - could implement a basic version
        message_frame = ttk.Frame(parent)
        message_frame.pack(fill='both', expand=True, padx=50, pady=50)
        
        icon_label = tk.Label(message_frame, text="📦", font=("Arial", 64))
        icon_label.pack(pady=20)
        
        title_label = tk.Label(
            message_frame,
            text="Channel Packer",
            font=("Arial", 18, "bold"),
            fg="#2c3e50"
        )
        title_label.pack(pady=10)
        
        message_label = tk.Label(
            message_frame,
            text="Channel Packer requires tkinterdnd2 for full functionality.\n\n"
                 "To install the required dependency:\n"
                 "pip install tkinterdnd2\n\n"
                 "Then restart the application to use Channel Packer.",
            font=("Arial", 12),
            justify='center'
        )
        message_label.pack(pady=20)
        
        install_button = ttk.Button(
            message_frame,
            text="Open Installation Instructions",
            command=lambda: messagebox.showinfo(
                "Installation Instructions",
                "To install tkinterdnd2:\n\n"
                "1. Open a command prompt or terminal\n"
                "2. Run: pip install tkinterdnd2\n"
                "3. Restart this application\n\n"
                "After installation, Channel Packer will have full "
                "drag-and-drop functionality."
            )
        )
        install_button.pack(pady=10)


def main():
    """Main function to run the unified utilities application."""
    try:
        if DND_AVAILABLE:
            root = tkdnd.TkinterDnD.Tk()
        else:
            root = tk.Tk()
            
        app = ImageUtilitiesUI(root)
        root.mainloop()
        
    except Exception as e:
        print(f"Error starting application: {e}")
        # Fallback to basic Tkinter
        root = tk.Tk()
        app = ImageUtilitiesUI(root)
        root.mainloop()


if __name__ == "__main__":
    main()
