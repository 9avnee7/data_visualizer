import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Load environment variables from .env file
load_dotenv()

# Configure Cloudinary with environment variables
cloudinary.config(
    cloud_name=os.getenv('cloud_name'),
    api_key=os.getenv('api_key'),
    api_secret=os.getenv('api_secret'),
    secure=True
)

def upload_video_to_cloudinary(video_path):
    try:
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        response = cloudinary.uploader.upload(
            video_path,
            resource_type="video",
            folder="algorithm_visualizations"
        )

        hls_url = response.get("playback_url")
        secure_url = response.get("secure_url")

        if not hls_url:
            raise ValueError("Upload did not return a hls URL.")
        if not secure_url:
            raise ValueError("Upload did not return a secure URL.")

        print("Upload successful.")
        print("secure URL:", secure_url)
        print("hls URL:", hls_url)

       

        # print(f"Video URL saved to {js_file_path}")
        return hls_url,secure_url

    except Exception as e:
        print("Upload failed:", str(e))
        return None


video_path = "/Users/navneet/Documents/Internshiptasks/algorithmVisualizer/backend/visualization/execution/final_output.mp4"
upload_video_to_cloudinary(video_path)
