#!/usr/bin/env python3
"""
Channel Packer Script

This script takes 3-4 grayscale images and packs them into a single RGB/RGBA image,
where each grayscale image becomes one channel (R, G, B, or A) of the final image.
The output is saved as a PNG or TGA file.

Usage:
    python channel_packer.py <red_channel_image> <green_channel_image> <blue_channel_image> <output_image> [--alpha <alpha_channel_image>] [--resolution WIDTHxHEIGHT]

Example:
    python channel_packer.py image1.png image2.png image3.png packed_output.png
    python channel_packer.py r.png g.png b.png output.tga --alpha alpha.png
    python channel_packer.py r.png g.png b.png output.png --resolution 1024x768
"""

import sys
import os
from PIL import Image
import numpy as np


def extract_channels_from_image(image_path):
    """
    Extract individual channels from a multi-channel image.
    
    Args:
        image_path (str): Path to the input image
        
    Returns:
        dict: Dictionary with channel names as keys and PIL Images as values
    """
    try:
        image = Image.open(image_path)
        channels = {}
        
        if image.mode == 'RGB':
            r, g, b = image.split()
            channels['red'] = r
            channels['green'] = g
            channels['blue'] = b
            channels['alpha'] = None
        elif image.mode == 'RGBA':
            r, g, b, a = image.split()
            channels['red'] = r
            channels['green'] = g
            channels['blue'] = b
            channels['alpha'] = a
        elif image.mode == 'L':
            # Grayscale image
            channels['red'] = image
            channels['green'] = None
            channels['blue'] = None
            channels['alpha'] = None
        else:
            # Convert to RGB first
            rgb_image = image.convert('RGB')
            r, g, b = rgb_image.split()
            channels['red'] = r
            channels['green'] = g
            channels['blue'] = b
            channels['alpha'] = None
            
        return channels
        
    except Exception as e:
        print(f"Error extracting channels from {image_path}: {e}")
        return None


def save_channels_individually(channels, base_path):
    """
    Save each channel as a separate PNG file.
    
    Args:
        channels (dict): Dictionary with channel names and PIL Images
        base_path (str): Base path for output files (without extension)
    """
    try:
        saved_files = []
        for channel_name, channel_image in channels.items():
            if channel_image is not None:
                output_path = f"{base_path}_{channel_name}.png"
                channel_image.save(output_path, 'PNG')
                saved_files.append(output_path)
                print(f"Saved {channel_name} channel to {output_path}")
        return saved_files
    except Exception as e:
        print(f"Error saving individual channels: {e}")
        return []


def load_grayscale_image(image_path):
    """
    Load an image and convert it to grayscale.
    
    Args:
        image_path (str): Path to the input image
        
    Returns:
        PIL.Image: Grayscale image
    """
    try:
        image = Image.open(image_path)
        # Convert to grayscale if not already
        if image.mode != 'L':
            image = image.convert('L')
        return image
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return None


def resize_images_to_match(images):
    """
    Resize all images to match the dimensions of the largest image.
    
    Args:
        images (list): List of PIL Images
        
    Returns:
        list: List of resized PIL Images
    """
    # Find the maximum dimensions
    max_width = max(img.width for img in images)
    max_height = max(img.height for img in images)
    
    # Resize all images to match the maximum dimensions
    resized_images = []
    for img in images:
        if img.width != max_width or img.height != max_height:
            resized_img = img.resize((max_width, max_height), Image.Resampling.LANCZOS)
            resized_images.append(resized_img)
        else:
            resized_images.append(img)
    
    return resized_images


def pack_channels(red_image, green_image, blue_image, output_path, alpha_image=None, output_resolution=None):
    """
    Pack three or four grayscale images into RGB or RGBA channels and save.
    
    Args:
        red_image (PIL.Image): Image for red channel
        green_image (PIL.Image): Image for green channel
        blue_image (PIL.Image): Image for blue channel
        output_path (str): Path for the output file
        alpha_image (PIL.Image, optional): Image for alpha channel
        output_resolution (tuple, optional): Desired output resolution as (width, height)
    """
    try:
        # Collect valid images
        images_to_resize = []
        if red_image:
            images_to_resize.append(red_image)
        if green_image:
            images_to_resize.append(green_image)
        if blue_image:
            images_to_resize.append(blue_image)
        if alpha_image:
            images_to_resize.append(alpha_image)
            
        if not images_to_resize:
            raise Exception("No valid images provided")
            
        # Get dimensions from largest image
        max_width = max(img.width for img in images_to_resize)
        max_height = max(img.height for img in images_to_resize)
        
        # Resize images to match dimensions or create black images
        def resize_or_create_black(img):
            if img is None:
                return Image.new('L', (max_width, max_height), 0)
            elif img.width != max_width or img.height != max_height:
                return img.resize((max_width, max_height), Image.Resampling.LANCZOS)
            else:
                return img
        
        final_red = resize_or_create_black(red_image)
        final_green = resize_or_create_black(green_image)
        final_blue = resize_or_create_black(blue_image)
        
        # Convert images to numpy arrays
        red_array = np.array(final_red)
        green_array = np.array(final_green)
        blue_array = np.array(final_blue)
        
        # Handle alpha channel
        if alpha_image:
            final_alpha = resize_or_create_black(alpha_image)
            alpha_array = np.array(final_alpha)
            # Stack the arrays to create RGBA image
            rgba_array = np.stack([red_array, green_array, blue_array, alpha_array], axis=2)
            final_image = Image.fromarray(rgba_array, 'RGBA')
        else:
            # Stack the arrays to create RGB image
            rgb_array = np.stack([red_array, green_array, blue_array], axis=2)
            final_image = Image.fromarray(rgb_array, 'RGB')
        
        # Resize to the specified output resolution if provided
        if output_resolution:
            final_image = final_image.resize(output_resolution, Image.Resampling.LANCZOS)
            print(f"Resized to specified resolution: {output_resolution[0]}x{output_resolution[1]}")
            
        # Determine output format based on extension
        file_ext = os.path.splitext(output_path)[1].lower()
        if file_ext == '.tga':
            final_image.save(output_path, 'TGA')
        else:
            # Default to PNG
            if not output_path.lower().endswith('.png'):
                output_path = os.path.splitext(output_path)[0] + '.png'
            final_image.save(output_path, 'PNG')
        
        print(f"Successfully packed images into {output_path}")
        print(f"Output image dimensions: {final_image.width}x{final_image.height}")
        print(f"Output mode: {final_image.mode}")
        
    except Exception as e:
        print(f"Error packing channels: {e}")


def pack_channels_old(red_image, green_image, blue_image, output_path):
    """
    Pack three grayscale images into RGB channels and save as PNG.
    This is the old function kept for backward compatibility.
    """
    pack_channels(red_image, green_image, blue_image, output_path, None, None)


def main():
    """Main function to handle command line arguments and execute the packing."""
    # Parse arguments
    import argparse
    
    parser = argparse.ArgumentParser(description="Pack grayscale images into RGB/RGBA channels.")
    parser.add_argument("red_channel", help="Image to use for the red channel")
    parser.add_argument("green_channel", help="Image to use for the green channel")
    parser.add_argument("blue_channel", help="Image to use for the blue channel")
    parser.add_argument("output", help="Output filename")
    parser.add_argument("--alpha", "-a", help="Optional image to use for the alpha channel")
    parser.add_argument("--resolution", "-r", help="Output resolution in format WIDTHxHEIGHT (e.g., 1024x1024)")
    
    args = parser.parse_args()
    
    red_path = args.red_channel
    green_path = args.green_channel
    blue_path = args.blue_channel
    output_path = args.output
    alpha_path = args.alpha
    
    # Parse resolution if provided
    output_resolution = None
    if args.resolution:
        try:
            width, height = map(int, args.resolution.lower().split("x"))
            output_resolution = (width, height)
            print(f"Target output resolution: {width}x{height}")
        except ValueError:
            print(f"Error: Invalid resolution format '{args.resolution}'. Should be WIDTHxHEIGHT (e.g., 1024x1024)")
            sys.exit(1)
    
    # Verify input files exist
    for path in [red_path, green_path, blue_path]:
        if not os.path.exists(path):
            print(f"Error: Input file '{path}' does not exist.")
            sys.exit(1)
    
    if alpha_path and not os.path.exists(alpha_path):
        print(f"Error: Alpha channel file '{alpha_path}' does not exist.")
        sys.exit(1)
    
    # Load the grayscale images
    print("Loading images...")
    red_image = load_grayscale_image(red_path)
    green_image = load_grayscale_image(green_path)
    blue_image = load_grayscale_image(blue_path)
    alpha_image = load_grayscale_image(alpha_path) if alpha_path else None
    
    # Check if all images loaded successfully
    if not all([red_image, green_image, blue_image]):
        print("Error: Failed to load one or more input images.")
        sys.exit(1)
    
    print(f"Red channel: {red_image.width}x{red_image.height}")
    print(f"Green channel: {green_image.width}x{green_image.height}")
    print(f"Blue channel: {blue_image.width}x{blue_image.height}")
    if alpha_image:
        print(f"Alpha channel: {alpha_image.width}x{alpha_image.height}")
    
    # Pack the channels
    print("Packing channels...")
    pack_channels(red_image, green_image, blue_image, output_path, alpha_image, output_resolution)


if __name__ == "__main__":
    main()
