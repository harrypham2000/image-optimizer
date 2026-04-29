# Image Optimizer - Quick Start Guide

## New Features (Since Last Version)

### 1. Dry Run Mode 🎯
Preview changes without saving:
```bash
python3 image_optimizer.py photo.jpg --dry-run
python3 image_optimizer.py photos/ --batch --dry-run
```

### 2. Metadata Options 📸
**Preserve metadata** (keeps EXIF data):
```bash
python3 image_optimizer.py photo.jpg --preserve-metadata
```

**Strip metadata** (removes EXIF data):
```bash
python3 image_optimizer.py photo.jpg --strip-metadata
```

### 3. Progress Bar 📊
Batch processing now shows visual progress:
```bash
python3 image_optimizer.py photos/ --batch --quality 95 --max-size 1080
```

### 4. Compression Ratio 📉
See exact compression percentage:
```bash
python3 image_optimizer.py photo.jpg
```

Output includes:
```
✓ Optimized: photo_optimized.jpeg
  Original: 4608x3456, Size: 6139.7 KB
  Optimized: 1080x810, Size: 283.3 KB
  Quality: 95%, Compression: 100.0%
  Metadata: Preserved
```

---

## Recommended Instagram/Facebook Settings

### Instagram Square Posts (1080x1080)
```bash
python3 image_optimizer.py photo.jpg --quality 95 --max-size 1080
```

### Instagram Portrait Posts (1080x1350)
```bash
python3 image_optimizer.py photo.jpg --quality 95 --max-size 1080
# Then crop to 1080x1350 in your editor
```

### Facebook
```bash
python3 image_optimizer.py photo.jpg --quality 90 --max-size 1200
```

### Web Display
```bash
python3 image_optimizer.py photo.jpg --quality 85 --max-size 1920
```

---

## Complete Command Reference

### Single Image
```bash
python3 image_optimizer.py <image_path> [output_path] [options]
```

### Batch Processing
```bash
python3 image_optimizer.py <directory> --batch [options]
```

### Available Options
- `--quality NUM` - JPEG quality (1-100), default: 95
- `--max-size NUM` - Maximum dimension in pixels, default: 1080
- `--format FORMAT` - Output format (JPEG/PNG), default: JPEG
- `--preserve-metadata` - Keep EXIF metadata (default: True)
- `--strip-metadata` - Remove EXIF metadata
- `--dry-run` - Preview changes without saving

### Examples

**Basic optimization:**
```bash
python3 image_optimizer.py photo.jpg
```

**High quality for Instagram:**
```bash
python3 image_optimizer.py photo.jpg --quality 100 --max-size 1080
```

**Batch optimization with progress:**
```bash
python3 image_optimizer.py photos/ --batch --quality 95 --max-size 1080
```

**Preview before optimizing:**
```bash
python3 image_optimizer.py photos/ --batch --dry-run
```

**Strip metadata:**
```bash
python3 image_optimizer.py photo.jpg --strip-metadata
```

**Custom output path:**
```bash
python3 image_optimizer.py photo.jpg my_output.jpg
```

---

## Tips for Best Results

1. **Start with Dry Run**: Use `--dry-run` to preview changes first
2. **Preserve Metadata**: Use `--preserve-metadata` to keep EXIF data
3. **High Quality**: Use quality 95-100 for sharp images
4. **Check Compression**: Look at the compression ratio in output
5. **Use Progress Bar**: Watch the progress during batch processing
6. **Upload Optimized**: Use images from `optimized_images/` folder

---

## Output Location

Optimized images are saved to:
- Single image: Same directory as original
- Batch: `optimized_images/` subdirectory

Example:
```
/home/hungpg-t14/Downloads/
├── photo.jpg
├── photo_optimized.jpeg  # Single image output
└── optimized_images/      # Batch output directory
    ├── photo1_optimized.jpeg
    ├── photo2_optimized.jpeg
    └── ...
```

---

## Troubleshooting

**Image appears blurry:**
- Increase quality to 95-100
- Check original image resolution

**File too large:**
- Reduce quality to 85-90
- Reduce max_size to 720px

**Metadata lost:**
- Use `--preserve-metadata` to keep EXIF data

**No progress:**
- Ensure you're using `--batch` flag

---

## Updated Features Comparison

| Feature | Status |
|---------|--------|
| WebP Input Support | ✅ Yes |
| Metadata Preservation | ✅ Yes (default) |
| Metadata Stripping | ✅ Yes |
| Dry Run Mode | ✅ Yes |
| Progress Bar | ✅ Yes |
| Compression Ratio | ✅ Yes |
| EXIF Detection | ✅ Yes |

---

## Need Help?

Run:
```bash
python3 image_optimizer.py
```

See all options and examples.