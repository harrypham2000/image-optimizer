# Image Optimizer for Instagram and Facebook

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

A powerful, easy-to-use command-line tool for optimizing images for Instagram, Facebook, and other social media platforms while maintaining maximum quality and sharpness.

## Why Images Appear Blurry on Social Media?

Images often appear blurry on Instagram and Facebook due to:

1. **Automatic Platform Compression**: Instagram and Facebook apply aggressive lossy compression to reduce bandwidth usage
2. **Size Resizing**: Images are automatically resized to platform-specific dimensions (1080x1080 for posts, 1080x1350 for stories)
3. **Format Conversion**: PNGs (lossless) are converted to JPEGs (lossy) during upload
4. **Over-optimization**: Many optimization tools reduce quality too much for social media
5. **Camera Compression**: Smartphone photos already have compression applied by the camera

## Features

✨ **Social Media Presets**
- Instagram: 1080x1080 square, 1080x1350 portrait
- Facebook: 1200px max
- Web: 1920px max

🎯 **Quality-First Approach**
- Default quality: 95-100 (industry standard for social media)
- LANCZOS resampling (highest quality)

📐 **Aspect Ratio Preservation**
- Maintains original aspect ratios
- Intelligent resizing without distortion

📦 **Multiple Format Support**
- Input: JPG, PNG, WEBP, BMP, GIF
- Output: JPEG, PNG

📊 **Batch Processing**
- Process entire directories
- Visual progress bar
- Detailed statistics

🔒 **Metadata Handling**
- Preserve EXIF data
- Strip metadata option

👁️ **Dry Run Mode**
- Preview changes before applying

## Installation

### Prerequisites

Python 3.6 or higher

### Install Pillow

```bash
pip install Pillow
```

Or if you're using pip3:

```bash
pip3 install Pillow
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
python3 image_optimizer.py photos/ --batch
# Creates optimized_images/ folder with all optimized images
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--quality NUM` | JPEG quality (1-100), higher = better quality | 95 |
| `--max-size NUM` | Maximum dimension in pixels | 1080 |
| `--format FORMAT` | Output format (JPEG/PNG) | JPEG |
| `--preserve-metadata` | Keep EXIF metadata | True |
| `--strip-metadata` | Remove EXIF metadata | False |
| `--dry-run` | Preview changes without saving | False |

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

## Examples

### Basic optimization
```bash
python3 image_optimizer.py photo.jpg
```

### High quality for Instagram
```bash
python3 image_optimizer.py photo.jpg --quality 100 --max-size 1080
```

### Batch optimization with progress
```bash
python3 image_optimizer.py photos/ --batch --quality 95 --max-size 1080
```

### Preview before optimizing
```bash
python3 image_optimizer.py photos/ --batch --dry-run
```

### Strip metadata
```bash
python3 image_optimizer.py photo.jpg --strip-metadata
```

### Preserve metadata
```bash
python3 image_optimizer.py photo.jpg --preserve-metadata
```

### Custom output path
```bash
python3 image_optimizer.py photo.jpg my_output.jpg
```

### Use PNG format
```bash
python3 image_optimizer.py photo.jpg --format PNG
```

## Output

Optimized images are saved to:
- **Single image**: Same directory as original
- **Batch**: `optimized_images/` subdirectory

**Example output:**
```
✓ Optimized: photo_optimized.jpeg
  Original: 4608x3456, Size: 6139.7 KB
  Optimized: 1080x810, Size: 283.3 KB
  Quality: 95%, Compression: 100.0%
  Metadata: Preserved
```

## Tips for Best Results

1. **Start with high-quality originals**: Don't rely on already compressed photos
2. **Use quality 95-100**: Higher quality resists compression better
3. **Resize to 1080px**: This is the optimal size for Instagram/Facebook
4. **Avoid over-sharpening**: Excessive sharpening gets lost during compression
5. **Use batch processing**: Save time by optimizing multiple images at once
6. **Use dry run first**: Preview changes before committing

## Troubleshooting

**Image appears blurry after optimization:**
- Increase quality to 95-100
- Check that original image is high resolution
- Don't over-sharpen before optimization

**File too large:**
- Reduce quality to 85-90
- Reduce max_size to 720px
- Consider PNG format for smaller files

**Metadata lost:**
- Use `--preserve-metadata` to keep EXIF data

**No progress:**
- Ensure you're using `--batch` flag

## Features Comparison

| Feature | Status |
|---------|--------|
| Social Media Presets | ✅ Yes |
| Quality Control | ✅ Yes (1-100) |
| Resizing | ✅ Smart (aspect ratio preserved) |
| Batch Processing | ✅ Yes (with progress bar) |
| CLI | ✅ Yes |
| WebP Input Support | ✅ Yes |
| WebP Output Support | ✅ Yes |
| Cross-platform | ✅ Yes |
| Aspect Ratio Preserve | ✅ Yes |
| Metadata Handling | ✅ Yes (preserve/strip) |
| Progress Bar | ✅ Yes |
| Dry Run Mode | ✅ Yes |
| Compression Ratio | ✅ Yes |

## Project Structure

```
image-optimizer/
├── image_optimizer.py    # Main script
├── README.md             # This file
├── LICENSE               # MIT License
├── .gitignore            # Git ignore rules
├── QUICK_START.md        # Quick reference guide
├── IMAGE_OPTIMIZER_README.md  # Detailed documentation
└── optimized_images/     # Output directory (created automatically)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Roadmap

- [ ] Web UI (FastAPI)
- [ ] Multiple optimization algorithms (MozJPEG, Guetzli, etc.)
- [ ] Advanced sharpening filters
- [ ] Configuration file support (JSON/YAML)
- [ ] Before/After comparison tool
- [ ] Cloud integration (Imgur, Cloudinary)
- [ ] Preset profiles (save/load optimization settings)
- [ ] Multi-threading for faster batch processing
- [ ] Desktop application (Electron/Tauri)

## Acknowledgments

- Built with [Pillow](https://python-pillow.org/) - The friendly PIL fork
- Inspired by the need for high-quality social media images

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

Made with ❤️ for social media enthusiasts