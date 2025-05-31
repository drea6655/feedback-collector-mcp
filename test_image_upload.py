#!/usr/bin/env python3
"""
Test script for image upload functionality in feedback UI
"""
import os
import sys
import tempfile
import json
import base64

# Add the current directory to the path so we can import feedback_ui
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from feedback_ui import feedback_ui

def create_test_image(filename: str) -> str:
    """Create a simple test image (1x1 PNG) and return its path"""
    # Create a minimal 1x1 PNG image (base64 encoded)
    # This is a 1x1 red pixel PNG
    png_data = base64.b64decode(
        'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=='
    )

    # Save to temporary file
    temp_dir = tempfile.gettempdir()
    filepath = os.path.join(temp_dir, filename)
    with open(filepath, 'wb') as f:
        f.write(png_data)

    return filepath

def test_image_upload():
    """Test the image upload functionality"""
    print("Creating test images...")
    
    # Create test images
    red_image = create_test_image("test_red.png")
    blue_image = create_test_image("test_blue.png")
    green_image = create_test_image("test_green.png")
    
    print(f"Created test images:")
    print(f"  - {red_image}")
    print(f"  - {blue_image}")
    print(f"  - {green_image}")
    
    print("\nTo test the image upload functionality:")
    print("1. Run the feedback UI")
    print("2. Click 'Add Images' button")
    print("3. Select the test images created above")
    print("4. Verify they appear in the preview area")
    print("5. Submit feedback and check the JSON output includes image data")
    
    # Test the feedback UI with a simple prompt
    print("\nLaunching feedback UI for testing...")
    print("(Close the UI window to continue)")
    
    try:
        result = feedback_ui(
            project_directory=os.getcwd(),
            prompt="Testing image upload functionality. Please upload some test images and provide feedback."
        )
        
        if result:
            print("\n" + "="*50)
            print("FEEDBACK RESULT:")
            print("="*50)
            print(f"Command logs: {result['command_logs']}")
            print(f"Interactive feedback: {result['interactive_feedback']}")
            print(f"Number of images: {len(result['images'])}")
            
            for i, img in enumerate(result['images']):
                print(f"\nImage {i+1}:")
                print(f"  Filename: {img['filename']}")
                print(f"  MIME type: {img['mime_type']}")
                print(f"  Data size: {len(img['data'])} characters (base64)")
                
                # Verify the image data is valid base64
                try:
                    decoded = base64.b64decode(img['data'])
                    print(f"  Decoded size: {len(decoded)} bytes")
                    print("  ✓ Valid base64 data")
                except Exception as e:
                    print(f"  ✗ Invalid base64 data: {e}")
        else:
            print("No result returned (user closed without submitting)")
            
    except Exception as e:
        print(f"Error testing feedback UI: {e}")
    
    # Cleanup test images
    print("\nCleaning up test images...")
    for img_path in [red_image, blue_image, green_image]:
        try:
            os.remove(img_path)
            print(f"  Removed: {img_path}")
        except Exception as e:
            print(f"  Failed to remove {img_path}: {e}")

if __name__ == "__main__":
    test_image_upload()
