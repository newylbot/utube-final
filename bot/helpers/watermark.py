import os
import subprocess
import logging
from ..config import Config

log = logging.getLogger(__name__)

class Watermark:
    def __init__(self, input_video: str, watermark_image: str):
        self.input_video = input_video
        self.watermark_image = watermark_image
        self.output_video = self._get_output_path()
    
    def _get_output_path(self) -> str:
        """Generate the output filename with `_watermarked` suffix."""
        file_name, ext = os.path.splitext(self.input_video)
        return f"{file_name}_watermarked{ext}"

    def _ffmpeg_exists(self) -> bool:
        """Check if FFmpeg is installed."""
        try:
            subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except FileNotFoundError:
            log.error("FFmpeg is not installed or not found in PATH.")
            return False

    def apply(self) -> str:
        """Applies watermark and returns the path to the new video."""
        
        if not self._ffmpeg_exists():
            log.error("FFmpeg is required but not found! Uploading original video.")
            return self.input_video  # Return original video if FFmpeg is missing

        if not os.path.exists(self.watermark_image):
            log.error("Watermark image not found! Uploading original video.")
            return self.input_video  # Return original video if watermark is missing

        # Define watermark positions
        positions = {
            "topleft": "10:10",
            "topright": "W-w-10:10",
            "bottomleft": "10:H-h-10",
            "bottomright": "W-w-10:H-h-10"
        }
        position = positions.get(Config.WATERMARK_POSITION, "bottomright")

        # Set watermark size (resize to 10% of video width, smaller than before)
        scale_filter = "scale=iw*0.1:-1"  # Watermark is now 10% of video width

        # Set transparency (opacity 50% using "format=rgba, colorchannelmixer")
        transparency_filter = "format=rgba,colorchannelmixer=aa=0.5"

        # FFmpeg command to overlay watermark
        command = [
            "ffmpeg", "-i", self.input_video, "-i", self.watermark_image, 
            "-filter_complex", f"[1:v] {scale_filter}, {transparency_filter} [wm]; [0:v][wm] overlay={position}",
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k",
            self.output_video, "-y"
        ]

        try:
            log.info("Applying watermark, this may take a moment...")
            subprocess.run(command, check=True)
            log.info(f"Watermark added successfully: {self.output_video}")
            return self.output_video
        except subprocess.CalledProcessError as e:
            log.error(f"FFmpeg error: {e}. Uploading original video instead.")
            return self.input_video  # Return original video if error occurs
