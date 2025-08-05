#!/usr/bin/env python3
"""
Channel Packer Script

This script takes 3 grayscale images and packs them into a single RGB image,
where each grayscale image becomes one channel (R, G, or B) of the final image.
The output is saved as a PNG file.

Usage:
    python channel_packer.py <red_channel_image> <green_channel_image> <blue_channel_image> <output_image>

Example:
    python channel_packer.py image1.png image2.png image3.png packed_output.png
"""

import sys
import os
from PIL import Image
import numpy as np


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


def pack_channels(red_image, green_image, blue_image, output_path):
    """
    Pack three grayscale images into RGB channels and save as PNG.
    
    Args:
        red_image (PIL.Image): Image for red channel
        green_image (PIL.Image): Image for green channel
        blue_image (PIL.Image): Image for blue channel
        output_path (str): Path for the output PNG file
    """
    try:
        # Resize images to match dimensions
        images = resize_images_to_match([red_image, green_image, blue_image])
        red_resized, green_resized, blue_resized = images
        
        # Convert images to numpy arrays
        red_array = np.array(red_resized)
        green_array = np.array(green_resized)
        blue_array = np.array(blue_resized)
        
        # Stack the arrays to create RGB image
        rgb_array = np.stack([red_array, green_array, blue_array], axis=2)
        
        # Create PIL image from the RGB array
        rgb_image = Image.fromarray(rgb_array, 'RGB')
        
        # Save as PNG
        rgb_image.save(output_path, 'PNG')
        
        print(f"Successfully packed images into {output_path}")
        print(f"Output image dimensions: {rgb_image.width}x{rgb_image.height}")
        
    except Exception as e:
        print(f"Error packing channels: {e}")


def main():
    """Main function to handle command line arguments and execute the packing."""
    if len(sys.argv) != 5:
        print("Usage: python channel_packer.py <red_channel> <green_channel> <blue_channel> <output.png>")
        print("\nExample:")
        print("python channel_packer.py image1.png image2.png image3.png packed_output.png")
        print("\nDescription:")
        print("- red_channel: Image to use for the red channel")
        print("- green_channel: Image to use for the green channel")
        print("- blue_channel: Image to use for the blue channel")
        print("- output.png: Output filename (will be saved as PNG)")
        sys.exit(1)
    
    red_path = sys.argv[1]
    green_path = sys.argv[2]
    blue_path = sys.argv[3]
    output_path = sys.argv[4]
    
    # Verify input files exist
    for path in [red_path, green_path, blue_path]:
        if not os.path.exists(path):
            print(f"Error: Input file '{path}' does not exist.")
            sys.exit(1)
    
    # Ensure output filename has .png extension
    if not output_path.lower().endswith('.png'):
        output_path += '.png'
    
    # Load the grayscale images
    print("Loading images...")
    red_image = load_grayscale_image(red_path)
    green_image = load_grayscale_image(green_path)
    blue_image = load_grayscale_image(blue_path)
    
    # Check if all images loaded successfully
    if not all([red_image, green_image, blue_image]):
        print("Error: Failed to load one or more input images.")
        sys.exit(1)
    
    print(f"Red channel: {red_image.width}x{red_image.height}")
    print(f"Green channel: {green_image.width}x{green_image.height}")
    print(f"Blue channel: {blue_image.width}x{blue_image.height}")
    
    # Pack the channels
    print("Packing channels...")
    pack_channels(red_image, green_image, blue_image, output_path)


if __name__ == "__main__":
    main()
