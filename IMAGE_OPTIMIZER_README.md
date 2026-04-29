# Image Optimizer for Instagram and Facebook

A Python script to optimize images for social media platforms while maintaining maximum quality and clarity.

## Why Images Appear Blurry on Instagram/Facebook

1. **Automatic Compression**: Platforms apply aggressive lossy compression to reduce bandwidth usage
2. **Size Resizing**: Images are automatically resized to platform-specific dimensions
3. **Format Conversion**: PNGs (lossless) are converted to JPEGs (lossy) during upload
4. **Over-optimization**: Many optimization tools reduce quality too much for social media
5. **Camera Compression**: Smartphone photos already have compression applied by the camera

## Solution

This script:
- Resizes images to optimal dimensions (1080x1080 for square posts)
- Converts to high-quality JPEG with minimal compression (90-95%)
- Preserves original aspect ratios where appropriate
- Can be run on batches of images

## Installation

Pillow (PIL) is required. It's already installed on this system.

If not installed:
```bash
pip install Pillow
```

## Usage

### Single Image Optimization

```bash
python3 image_optimizer.py <image_path> [output_path] [options]
```

**Example:**
```bash
python3 image_optimizer.py photo.jpg
# Creates: photo_optimized.jpeg
```

### Batch Processing

```bash
python3 image_optimizer.py <directory> --batch [options]
```

**Example:**
```bash
python3 image_optimizer.py /path/to/photos --batch
# Creates optimized_images/ folder with all optimized images
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--quality NUM` | JPEG quality (1-100), higher = better quality | 95 |
| `--max-size NUM` | Maximum dimension in pixels | 1080 |
| `--format FORMAT` | Output format (JPEG/PNG) | JPEG |

## Recommended Settings

### For Instagram Square Posts (1080x1080)
```bash
python3 image_optimizer.py photo.jpg --quality 95 --max-size 1080
```

### For Instagram Portrait Posts (1080x1350)
```bash
python3 image_optimizer.py photo.jpg --quality 95 --max-size 1080
# Then crop to 1080x1350 in your editor
```

### For Facebook
```bash
python3 image_optimizer.py photo.jpg --quality 90 --max-size 1200
```

### For Web Display
```bash
python3 image_optimizer.py photo.jpg --quality 85 --max-size 1920
```

## Quality vs File Size

- **Quality 95-100**: Best quality, larger file size (recommended for Instagram)
- **Quality 85-90**: Good quality, smaller file size (good for Facebook)
- **Quality 70-85**: Acceptable quality, smallest file size (not recommended for social media)

## Supported Input Formats

- JPG/JPEG
- PNG
- WEBP
- BMP
- GIF

## Output Format

- JPEG (default) - Best compatibility
- PNG - Lossless, larger files

## Example Output

```
✓ Optimized: _GHO2562_optimized.jpeg
  Original: 4608x3456, Size: 6139.7 KB
  Optimized: 1080x810, Size: 283.3 KB
  Quality: 95%
```

## Tips for Best Results

1. **Start with high-quality originals**: Don't rely on already compressed photos
2. **Use quality 95-100**: Higher quality resists compression better
3. **Resize to 1080px**: This is the optimal size for Instagram/Facebook
4. **Avoid over-sharpening**: Excessive sharpening gets lost during compression
5. **Use batch processing**: Save time by optimizing multiple images at once

## Troubleshooting

**Image appears blurry after optimization:**
- Increase quality to 95-100
- Check that original image is high resolution
- Don't over-sharpen before optimization

**File too large:**
- Reduce quality to 85-90
- Reduce max_size to 720px
- Consider PNG format for smaller files

**Unsupported format error:**
- Convert unsupported formats (like PDF) before running the script
- Use an image converter like ImageMagick or online tools

## License

Free to use for personal and commercial purposes.