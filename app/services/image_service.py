import io
from PIL import Image


class ImageService:
    @staticmethod
    def process_upload(file_bytes: bytes) -> Image.Image:
        """
        Converts raw bytes into a PIL Image and resizes it
        to optimize cloud transmission speeds and control costs.
        """
        image = Image.open(io.BytesIO(file_bytes))

        # Convert RGBA (like PNGs) to RGB to prevent JPEG conversion crashes
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        # Downscale image if it's too large, preserving aspect ratio
        max_size = (1024, 1024)
        image.thumbnail(max_size, Image.Resampling.LANCZOS)

        return image
