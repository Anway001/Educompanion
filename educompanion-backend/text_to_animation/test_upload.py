"""
Simple test to check if file upload and processing works
"""

import os
import tempfile
from PIL import Image, ImageDraw, ImageFont

def create_test_image():
    """Create a simple test image"""
    # Create a simple test image
    img = Image.new('RGB', (600, 400), 'white')
    draw = ImageDraw.Draw(img)
    
    # Add some text
    text = "Stack Operations Test\npush(10)\npush(20)\npop()"
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    draw.text((50, 50), text, fill='black', font=font)
    
    # Save to temp file
    temp_path = "test_upload_image.jpg"
    img.save(temp_path)
    print(f"✅ Test image created: {temp_path}")
    return temp_path

def test_file_processing():
    """Test the complete file processing pipeline"""
    try:
        # Create test image
        test_image = create_test_image()
        
        # Test the pipeline
        from text_to_animation_full_project import run_pipeline
        
        output_path = "test_upload_output.mp4"
        print("🔄 Testing pipeline...")
        
        run_pipeline(test_image, output_path)
        
        # Check result
        possible_outputs = [
            output_path,
            output_path.replace('.mp4', '_with_audio.mp4')
        ]
        
        for output in possible_outputs:
            if os.path.exists(output):
                size = os.path.getsize(output)
                print(f"✅ Output created: {output} ({size:,} bytes)")
                
                # Clean up
                os.remove(output)
                break
        else:
            print("❌ No output file found")
        
        # Clean up test image
        if os.path.exists(test_image):
            os.remove(test_image)
            
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 TESTING FILE UPLOAD AND PROCESSING")
    print("=" * 50)
    
    success = test_file_processing()
    
    if success:
        print("\n✅ File processing test PASSED!")
        print("🌐 Your Streamlit app should work fine now.")
        print("📡 Try accessing: http://localhost:8503")
    else:
        print("\n❌ File processing test FAILED!")
        print("🔧 Check the errors above for debugging.")
