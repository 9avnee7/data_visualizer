# utils/s3_downloader.py
import boto3
import os
from botocore.exceptions import NoCredentialsError, ClientError
from dotenv import load_dotenv
load_dotenv() 

def download_from_s3(bucket_name, s3_key, local_path):
    """
    Downloads a file from S3 to local path
    
    Args:
        bucket_name (str): S3 bucket name
        s3_key (str): S3 object key (path)
        local_path (str): Local file path to save to
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('aws_access_key'),  # Standard AWS env var name
            aws_secret_access_key=os.getenv('aws_secret_access_key'),  # Standard AWS env var name
            region_name='ap-south-1'
        )
        
        s3.download_file(bucket_name, s3_key, local_path)
        print(f"Successfully downloaded {s3_key} to {local_path}")
        return True
        
    except NoCredentialsError:
        print("Error: AWS credentials not found")
        return False
    except ClientError as e:
        print(f"Error downloading file: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False




if __name__ == "__main__":
    success = download_from_s3(
        bucket_name='store-user-traced-code',
        s3_key='userCode/BFS.py',
        local_path='algorithms/bfs.py'
    )
    if success:
        print("Download completed successfully")
    else:
        print("Download failed")