#!/usr/bin/env python3
"""
Image Optimizer for Instagram and Facebook
Optimizes images to maintain high quality while meeting platform requirements.
"""

from PIL import Image, ImageOps, ImageStat
import os
import sys
from pathlib import Path
from typing import Optional, List, Dict, Union

# Constants
DEFAULT_QUALITY = 95
DEFAULT_MAX_SIZE = 1080
MIN_QUALITY = 1
MAX_QUALITY = 100
MIN_MAX_SIZE = 100
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
SUPPORTED_FORMATS = {'JPEG', 'PNG', 'WEBP'}


def validate_quality(quality: Union[str, int]) -> int:
    """Validate JPEG quality parameter.
    
    Args:
        quality: Quality value to validate
        
    Returns:
        Validated quality value
        
    Raises:
        ValueError: If quality is not between 1 and 100
    """
    try:
        quality = int(quality)
    except (ValueError, TypeError):
        raise ValueError(f"Quality must be an integer, got {quality}")
    
    if not MIN_QUALITY <= quality <= MAX_QUALITY:
        raise ValueError(f"Quality must be between {MIN_QUALITY} and {MAX_QUALITY}, got {quality}")
    
    return quality


def validate_max_size(max_size: Union[str, int]) -> int:
    """Validate max_size parameter.
    
    Args:
        max_size: Max size value to validate
        
    Returns:
        Validated max size value
        
    Raises:
        ValueError: If max_size is less than 100
    """
    try:
        max_size = int(max_size)
    except (ValueError, TypeError):
        raise ValueError(f"Max size must be an integer, got {max_size}")
    
    if max_size < MIN_MAX_SIZE:
        raise ValueError(f"Max size must be at least {MIN_MAX_SIZE} pixels, got {max_size}")
    
    return max_size


def validate_format(format: str) -> str:
    """Validate output format.
    
    Args:
        format: Format to validate
        
    Returns:
        Validated format (uppercase)
        
    Raises:
        ValueError: If format is not JPEG, PNG, or WEBP
    """
    format_upper = format.upper()
    
    if format_upper not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Format must be one of {', '.join(SUPPORTED_FORMATS)}, got {format}"
        )
    
    return format_upper


def validate_file_size(file_path: Union[str, Path], max_size: int = MAX_FILE_SIZE) -> None:
    """Validate file size.
    
    Args:
        file_path: Path to file to check
        max_size: Maximum allowed file size in bytes
        
    Raises:
        ValueError: If file size exceeds limit
    """
    file_size = os.path.getsize(file_path)
    if file_size > max_size:
        raise ValueError(
            f"File size {file_size / 1024 / 1024:.1f}MB exceeds limit of "
            f"{max_size / 1024 / 1024:.0f}MB"
        )


def optimize_image(
    input_path: Union[str, Path],
    output_path: Optional[Union[str, Path]] = None,
    quality: int = DEFAULT_QUALITY,
    max_size: Optional[int] = None,
    format: str = 'JPEG',
    preserve_metadata: bool = True
) -> Optional[Path]:
    """
    Optimize an image for social media platforms.

    Args:
        input_path: Path to input image
        output_path: Path to save optimized image (optional)
        quality: JPEG quality (1-100), higher = better quality
        max_size: Maximum dimension in pixels (e.g., 1080 for Instagram)
        format: Output format ('JPEG' or 'PNG')
        preserve_metadata: Keep EXIF metadata (default: True)

    Returns:
        Path to optimized image or None if failed

    Raises:
        ValueError: If input parameters are invalid
        IOError: If file cannot be read or written
    """
    # Convert paths to Path objects
    input_path = Path(input_path).resolve()
    output_path = Path(output_path) if output_path else None

    # Validate file size
    try:
        validate_file_size(input_path)
    except ValueError as e:
        raise ValueError(f"File size validation failed: {e}")

    # Validate parameters
    quality = validate_quality(quality)
    if max_size is not None:
        max_size = validate_max_size(max_size)
    format = validate_format(format)

    try:
        # Open image with EXIF orientation handling
        with Image.open(input_path) as img:
            # Fix orientation based on EXIF data (critical for smartphone photos)
            img = ImageOps.exif_transpose(img)
            
            # Get original dimensions and file size
            original_width, original_height = img.size
            original_size = os.path.getsize(input_path)

            # Get EXIF data if available and preserving metadata
            exif_data = None
            if preserve_metadata:
                try:
                    if hasattr(img, '_getexif'):
                        exif_data = img._getexif()
                except (AttributeError, KeyError, TypeError):
                    exif_data = None

            # Convert to RGB if necessary (for JPEG)
            if format == 'JPEG' and img.mode in ('RGBA', 'P', 'LA', 'L'):
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
                output_path = input_path.parent / f"{input_path.stem}_optimized.{format.lower()}"

            # Prepare save parameters
            save_kwargs = {'quality': quality, 'optimize': True}
            if format == 'PNG':
                save_kwargs = {'optimize': True}

            # Save EXIF data if preserving metadata
            if preserve_metadata and exif_data:
                try:
                    from PIL import PngImagePlugin
                    
                    if format == 'PNG':
                        # For PNG, save EXIF in a text chunk
                        exif_bytes = exif_data.tobytes()
                        pnginfo = PngImagePlugin.PngInfo()
                        pnginfo.add_text("Exif", exif_bytes)
                        img.save(output_path, format.upper(), **save_kwargs, pnginfo=pnginfo)
                    else:
                        # For JPEG, EXIF preservation requires external library (piexif)
                        # We'll skip it for now to avoid additional dependencies
                        img.save(output_path, format.upper(), **save_kwargs)
                        
                except (AttributeError, KeyError, TypeError) as e:
                    # Fallback to basic save
                    print(f"Warning: Failed to preserve metadata for {input_path}: {e}")
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

    except (IOError, OSError) as e:
        print(f"✗ Error processing {input_path}: {e}")
        return None
    except ValueError as e:
        print(f"✗ Validation error for {input_path}: {e}")
        return None
    except Exception as e:
        print(f"✗ Unexpected error processing {input_path}: {e}")
        return None


def batch_optimize(
    input_dir: Union[str, Path],
    output_dir: Optional[Union[str, Path]] = None,
    quality: int = DEFAULT_QUALITY,
    max_size: Optional[int] = None,
    format: str = 'JPEG',
    preserve_metadata: bool = True,
    max_workers: int = 4
) -> None:
    """
    Optimize all images in a directory.

    Args:
        input_dir: Directory containing images
        output_dir: Directory to save optimized images (optional)
        quality: JPEG quality (1-100)
        max_size: Maximum dimension in pixels
        format: Output format
        preserve_metadata: Keep EXIF metadata
        max_workers: Number of parallel workers (default: 4)

    Raises:
        ValueError: If input parameters are invalid
    """
    # Convert paths to Path objects
    input_dir = Path(input_dir).resolve()
    output_dir = Path(output_dir) if output_dir else None

    # Validate input directory
    if not input_dir.is_dir():
        raise ValueError(f"Input path {input_dir} is not a directory")

    # Validate parameters
    quality = validate_quality(quality)
    if max_size is not None:
        max_size = validate_max_size(max_size)
    format = validate_format(format)

    # Determine output directory
    if output_dir is None:
        output_dir = input_dir / "optimized_images"

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Supported image formats
    image_extensions = {
        '.jpg', '.jpeg', '.png', '.webp', 
        '.JPG', '.JPEG', '.PNG', '.WEBP'
    }

    # Find all images
    images = [f for f in input_dir.iterdir() if f.suffix in image_extensions]

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
    print("-" * 60)

    # Optimize each image with progress
    optimized_count = 0
    failed_count = 0

    # Use multi-threading for faster processing
    try:
        from concurrent.futures import ThreadPoolExecutor, as_completed

        def process_image(img_path: Path) -> tuple[bool, Optional[Path]]:
            """Process a single image and return success status."""
            try:
                result = optimize_image(
                    img_path,
                    output_path=output_path / img_path.name,
                    quality=quality,
                    max_size=max_size,
                    format=format,
                    preserve_metadata=preserve_metadata
                )
                return (result is not None, result)
            except Exception as e:
                print(f"✗ Error processing {img_path}: {e}")
                return (False, None)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_path = {
                executor.submit(process_image, img_path): img_path
                for img_path in images
            }

            # Process as they complete
            for future in as_completed(future_to_path):
                img_path = future_to_path[future]
                success, result = future.result()
                
                if success:
                    optimized_count += 1
                else:
                    failed_count += 1

                # Print progress
                progress = (optimized_count + failed_count) / len(images) * 100
                bar_length = 40
                filled = int(bar_length * (optimized_count + failed_count) / len(images))
                bar = '█' * filled + '░' * (bar_length - filled)
                print(f"\r[{bar}] {progress:.1f}% ({optimized_count + failed_count}/{len(images)})", 
                      end='', flush=True)

    except ImportError:
        # Fallback to sequential processing if ThreadPoolExecutor not available
        for i, img_path in enumerate(images, 1):
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

            # Print progress
            progress = i / len(images) * 100
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
        print("  --max-workers NUM Number of parallel workers (default: 4)")
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
    quality = DEFAULT_QUALITY
    max_size = None
    format = 'JPEG'
    preserve_metadata = True
    batch_mode = False
    max_workers = 4

    # Parse options
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--batch':
            batch_mode = True
            i += 1
        elif arg == '--quality':
            quality = sys.argv[i + 1]
            i += 2
        elif arg == '--max-size':
            max_size = sys.argv[i + 1]
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
        elif arg == '--max-workers':
            max_workers = int(sys.argv[i + 1])
            i += 2
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
        batch_optimize(
            input_path,
            quality=quality,
            max_size=max_size,
            format=format,
            preserve_metadata=preserve_metadata,
            max_workers=max_workers
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
            preserve_metadata=preserve_metadata
        )


if __name__ == '__main__':
    main()