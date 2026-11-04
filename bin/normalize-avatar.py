"""Decode uploaded images and save a 512px square PNG without metadata."""
import sys
import resource
import warnings
from pathlib import Path

sys.path.insert(0, str(Path.home() / '.local/share/ifoj-avatar/python'))
from PIL import Image, ImageOps

resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, 512 * 1024 * 1024))
resource.setrlimit(resource.RLIMIT_CPU, (5, 5))
Image.MAX_IMAGE_PIXELS = 16_000_000
warnings.simplefilter('error', Image.DecompressionBombWarning)
try:
    with Image.open(sys.argv[1]) as image:
        if image.format not in ('JPEG', 'PNG', 'WEBP'):
            raise ValueError('Unsupported format')
        if image.width > 4096 or image.height > 4096:
            raise ValueError('Image too large')
        image.seek(0)
        result = ImageOps.fit(ImageOps.exif_transpose(image).convert('RGBA'),
                              (512, 512), method=Image.Resampling.LANCZOS)
        result.save(sys.argv[2], format='PNG')
except Exception:
    print('Invalid image: JPG, PNG or WebP up to 4096px per side required.', file=sys.stderr)
    sys.exit(1)
