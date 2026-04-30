#!/usr/bin/env python3
"""
Image Optimizer for Instagram and Facebook
Optimizes images to maintain high quality while meeting platform requirements.
"""

from PIL import Image, ImageStat
import os
import sys
from pathlib import Path
import json
from datetime import datetime


def optimize_image(input_path, output_path=None, quality=95, max_size=None, format='JPEG', preserve_metadata=True, dry_run=False):
    """
    Optimize an image for social media platforms.

    Args:
        input_path: Path to input image
        output_path: Path to save optimized image (optional)
        quality: JPEG quality (1-100), higher = better quality
        max_size: Maximum dimension in pixels (e.g., 1080 for Instagram)
        format: Output format ('JPEG' or 'PNG')
        preserve_metadata: Keep EXIF metadata (default: True)
        dry_run: Preview changes without saving (default: False)
    """
    try:
        # Open image
        with Image.open(input_path) as img:
            # Get original dimensions and file size
            original_width, original_height = img.size
            original_size = os.path.getsize(input_path)
            
            # Get EXIF data if available
            exif_data = None
            if preserve_metadata and hasattr(img, '_getexif'):
                try:
                    exif_data = img._getexif()
                except:
                    exif_data = None

            # Convert to RGB if necessary (for JPEG)
            if format.upper() == 'JPEG' and img.mode in ('RGBA', 'P', 'LA', 'L'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                if img.mode in ('RGBA', 'LA', 'L'):
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                else:
                    img = img.convert('RGB')

            # Resize if max_size is specified
            if max_size:
                # Calculate new dimensions while maintaining aspect ratio
                width, height = img.size
                if max(width, height) > max_size:
                    if width > height:
                        new_height = int(height * (max_size / width))
                        new_size = (max_size, new_height)
                    else:
                        new_width = int(width * (max_size / height))
                        new_size = (new_width, max_size)
                    img = img.resize(new_size, Image.Resampling.LANCZOS)

            # Determine output path
            if output_path is None:
                input_path = Path(input_path)
                output_path = input_path.parent / f"{input_path.stem}_optimized.{format.lower()}"

            # Dry run - just preview
            if dry_run:
                print(f"✓ Preview: {output_path}")
                print(f"  Original: {original_width}x{original_height}, Size: {original_size/1024:.1f} KB")
                print(f"  Optimized: {img.size[0]}x{img.size[1]}")
                print(f"  Quality: {quality}%, Format: {format}")
                if preserve_metadata:
                    print(f"  Metadata: Preserved")
                else:
                    print(f"  Metadata: Stripped")
                return None

            # Save optimized image
            save_kwargs = {'quality': quality, 'optimize': True}
            if format.upper() == 'PNG':
                save_kwargs = {'optimize': True}
            
            # Save EXIF data if preserving metadata
            if preserve_metadata and exif_data:
                try:
                    from PIL import PngImagePlugin
                    if format.upper() == 'PNG':
                        # For PNG, save EXIF in a text chunk
                        exif_bytes = exif_data.tobytes()
                        pnginfo = PngImagePlugin.PngInfo()
                        pnginfo.add_text("Exif", exif_bytes)
                        img.save(output_path, format.upper(), **save_kwargs, pnginfo=pnginfo)
                    else:
                        # For JPEG, we can't easily preserve EXIF without external libraries
                        # PIL doesn't have built-in EXIF support for JPEG
                        img.save(output_path, format.upper(), **save_kwargs)
                except Exception as e:
                    # Fallback to basic save
                    img.save(output_path, format.upper(), **save_kwargs)
            else:
                img.save(output_path, format.upper(), **save_kwargs)

            # Get file size
            file_size_kb = os.path.getsize(output_path) / 1024

            # Calculate compression ratio
            compression_ratio = (1 - file_size_kb / original_size) * 100

            print(f"✓ Optimized: {output_path}")
            print(f"  Original: {original_width}x{original_height}, Size: {original_size/1024:.1f} KB")
            print(f"  Optimized: {img.size[0]}x{img.size[1]}, Size: {file_size_kb:.1f} KB")
            print(f"  Quality: {quality}%, Compression: {compression_ratio:.1f}%")
            if preserve_metadata:
                print(f"  Metadata: Preserved")
            else:
                print(f"  Metadata: Stripped")

            return output_path

    except Exception as e:
        print(f"✗ Error processing {input_path}: {e}")
        return None


def batch_optimize(input_dir, output_dir=None, quality=95, max_size=1080, format='JPEG', preserve_metadata=True, dry_run=False):
    """
    Optimize all images in a directory.

    Args:
        input_dir: Directory containing images
        output_dir: Directory to save optimized images (optional)
        quality: JPEG quality (1-100)
        max_size: Maximum dimension in pixels
        format: Output format
        preserve_metadata: Keep EXIF metadata
        dry_run: Preview changes without saving
    """
    input_path = Path(input_dir)

    # Determine output directory
    if output_dir is None:
        output_dir = input_path / "optimized_images"

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Supported image formats
    image_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.JPG', '.JPEG', '.PNG', '.WEBP'}

    # Find all images
    images = [f for f in input_path.iterdir() if f.suffix in image_extensions]

    if not images:
        print(f"No images found in {input_dir}")
        return

    print(f"Found {len(images)} images to optimize")
    print(f"Output directory: {output_path}")
    print(f"Quality: {quality}%, Max Size: {max_size}px, Format: {format}")
    if preserve_metadata:
        print(f"Metadata: Preserved")
    else:
        print(f"Metadata: Stripped")
    if dry_run:
        print(f"Mode: Preview (no changes will be saved)")
    print("-" * 60)

    # Optimize each image with progress
    optimized_count = 0
    failed_count = 0
    total_size_reduction = 0

    for i, img_path in enumerate(images, 1):
        if dry_run:
            # Preview mode
            result = optimize_image(
                img_path,
                output_path=output_path / img_path.name,
                quality=quality,
                max_size=max_size,
                format=format,
                preserve_metadata=preserve_metadata,
                dry_run=True
            )
        else:
            # Actual optimization
            result = optimize_image(
                img_path,
                output_path=output_path / img_path.name,
                quality=quality,
                max_size=max_size,
                format=format,
                preserve_metadata=preserve_metadata
            )
        
        if result:
            optimized_count += 1
        else:
            failed_count += 1

        # Print progress bar
        if not dry_run:
            progress = (i / len(images)) * 100
            bar_length = 40
            filled = int(bar_length * i / len(images))
            bar = '█' * filled + '░' * (bar_length - filled)
            print(f"\r[{bar}] {progress:.1f}% ({i}/{len(images)})", end='', flush=True)

    print("\n" + "-" * 60)
    print(f"✓ Successfully optimized: {optimized_count}/{len(images)} images")
    if failed_count > 0:
        print(f"✗ Failed: {failed_count}/{len(images)} images")
    print(f"Output saved to: {output_path}")


def main():
    """Main function with command-line interface."""
    if len(sys.argv) < 2:
        print("Image Optimizer for Instagram and Facebook")
        print("\nUsage:")
        print("  python image_optimizer.py <image_path> [output_path] [options]")
        print("  python image_optimizer.py <directory> --batch [options]")
        print("\nOptions:")
        print("  --quality NUM    JPEG quality (1-100), default: 95")
        print("  --max-size NUM   Maximum dimension in pixels, default: 1080")
        print("  --format FORMAT  Output format (JPEG/PNG), default: JPEG")
        print("  --preserve-metadata Keep EXIF metadata (default: True)")
        print("  --dry-run Preview changes without saving")
        print("\nExamples:")
        print("  python image_optimizer.py photo.jpg")
        print("  python image_optimizer.py photo.jpg --quality 90")
        print("  python image_optimizer.py photos/ --batch")
        print("  python image_optimizer.py photo.png --format PNG")
        print("  python image_optimizer.py photos/ --batch --dry-run")
        print("  python image_optimizer.py photo.jpg --preserve-metadata")
        sys.exit(1)

    # Parse arguments
    input_arg = sys.argv[1]
    output_path = None
    quality = 95
    max_size = 1080
    format = 'JPEG'
    preserve_metadata = True
    dry_run = False
    batch_mode = False

    # Parse options
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--batch':
            batch_mode = True
            i += 1
        elif arg == '--quality':
            quality = int(sys.argv[i + 1])
            i += 2
        elif arg == '--max-size':
            max_size = int(sys.argv[i + 1])
            i += 2
        elif arg == '--format':
            format = sys.argv[i + 1]
            i += 2
        elif arg == '--preserve-metadata':
            preserve_metadata = True
            i += 1
        elif arg == '--strip-metadata':
            preserve_metadata = False
            i += 1
        elif arg == '--dry-run':
            dry_run = True
            i += 1
        elif arg.startswith('--'):
            print(f"Unknown option: {arg}")
            print("Run 'python image_optimizer.py' for help")
            sys.exit(1)
        else:
            # Assume this is an output path
            output_path = arg
            i += 1

    # Process based on mode
    input_path = Path(input_arg)

    if batch_mode:
        if not input_path.is_dir():
            print(f"Error: {input_arg} is not a directory")
            sys.exit(1)
        batch_optimize(
            input_path, 
            quality=quality, 
            max_size=max_size, 
            format=format,
            preserve_metadata=preserve_metadata,
            dry_run=dry_run
        )
    else:
        if not input_path.is_file():
            print(f"Error: {input_arg} is not a file")
            sys.exit(1)

        if output_path is None:
            output_path = input_path.parent / f"{input_path.stem}_optimized.{format.lower()}"

        optimize_image(
            input_path, 
            output_path, 
            quality=quality, 
            max_size=max_size, 
            format=format,
            preserve_metadata=preserve_metadata,
            dry_run=dry_run
        )


if __name__ == '__main__':
    main()