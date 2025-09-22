import os
import requests
from urllib.parse import urlparse, unquote
from pathlib import Path

def create_image_directory():
    """
    Creates 'Fetched_Images' directory if it doesn't exist
    Implements Ubuntu principle of organized sharing
    """
    directory = Path("Fetched_Images")
    try:
        directory.mkdir(exist_ok=True)
        print(f"✓ Directory '{directory}' created/verified")
        return directory
    except Exception as error:
        print(f"✗ Error creating directory: {error}")
        return None

def extract_filename(url):
    """
    Extracts filename from URL or generates one
    Implements Ubuntu principle of practicality
    """
    parsed_url = urlparse(url)
    path = unquote(parsed_url.path)
    filename = Path(path).name
    
    # Generate filename if none found
    if not filename or '.' not in filename:
        filename = f"downloaded_image_{hash(url) % 10000}.jpg"
    else:
        # Ensure valid image extension
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        if not any(filename.lower().endswith(ext) for ext in valid_extensions):
            filename += '.jpg'
    
    return filename

def download_image(url, directory):
    """
    Downloads image from URL with graceful error handling
    Implements Ubuntu principles of respect and community
    """
    if not directory:
        print("✗ No valid directory available")
        return False
    
    filename = extract_filename(url)
    filepath = directory / filename
    
    try:
        # Community: Connect to wider web
        print(f"🌐 Connecting to {urlparse(url).netloc}...")
        
        # Respect: Handle request with timeout
        response = requests.get(url, stream=True, timeout=15)
        response.raise_for_status()  # Check for HTTP errors
        
        # Practicality: Verify it's an image
        content_type = response.headers.get('content-type', '')
        if not content_type.startswith('image/'):
            print(f"⚠️  Warning: Content-Type is '{content_type}', not image")
            if not input("Continue anyway? (y/n): ").lower().startswith('y'):
                return False
        
        # Download image in binary mode
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        print(f"📥 Downloading: {filename}")
        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"📊 Progress: {percent:.1f}%", end='\r')
        
        # Sharing: Confirm successful save
        file_size = filepath.stat().st_size
        print(f"\n✅ Successfully saved: {filename} ({file_size:,} bytes)")
        print(f"📁 Location: {filepath.absolute()}")
        return True
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Please check your internet connection")
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: Connection took too long")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    return False

def main():
    """
    Main function embodying Ubuntu principles
    """
    print("=" * 60)
    print("UBUNTU IMAGE FETCHER")
    print("Community • Respect • Sharing • Practicality")
    print("=" * 60)
    
    # Create directory for organized sharing
    image_dir = create_image_directory()
    if not image_dir:
        return
    
    # Get URL from user
    url = input("\n🔗 Enter image URL: ").strip()
    
    if not url:
        print("❌ No URL provided")
        return
    
    # Validate URL format
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        print("❌ Invalid URL. Please include http:// or https://")
        return
    
    # Download the image
    success = download_image(url, image_dir)
    
    # Final feedback
    if success:
        print("\n🎉 Image fetched successfully! Ready for sharing.")
    else:
        print("\n💡 Download failed. Please check the URL and try again.")

if __name__ == "__main__":
    main()