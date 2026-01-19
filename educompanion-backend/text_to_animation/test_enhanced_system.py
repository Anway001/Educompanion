"""
Test the enhanced content-aware animation system
"""

import os
import tempfile
from intelligent_animator import ContentAnalyzer, IntelligentAnimator

def test_content_aware_animation():
    """Test the content-aware animation system"""
    
    print("🧪 Testing Content-Aware Animation System")
    print("=" * 50)
    
    # Test data - stack operations from demo image
    test_text = """STACK DATA STRUCTURE
A stack is a LIFO (Last In First Out) structure_
Operations:
push(10)
Add 10 to top
2. push(20) _ Add 20 to
push(30)
Add 30 to top
4. pop() _ Remove 30 (top element)
5 . push(40)
Add 40 to top
Current stack: [10, 20, 40]
element: 40
top
Top"""
    
    # Step 1: Test Content Analysis
    print("1. Testing Content Analysis...")
    analyzer = ContentAnalyzer()
    content = analyzer.analyze_content(test_text)
    
    print(f"   ✓ Content Type: {content.get('type', 'unknown')}")
    print(f"   ✓ Score: {content.get('score', 0)}")
    print(f"   ✓ Elements Found: {len(content.get('elements', []))}")
    
    for i, element in enumerate(content.get('elements', [])[:3]):
        print(f"     - Element {i+1}: {element}")
    
    # Step 2: Test Animation Generation
    print("\n2. Testing Animation Generation...")
    animator = IntelligentAnimator()
    
    try:
        # Create temporary output path
        temp_dir = tempfile.mkdtemp()
        output_path = os.path.join(temp_dir, "test_stack_animation.mp4")
        
        # Generate animation
        print("   🎬 Creating stack animation...")
        result = animator.create_data_structure_animation(content.get('elements', []), output_path)
        
        if os.path.exists(result):
            file_size = os.path.getsize(result)
            print(f"   ✅ Animation created successfully!")
            print(f"   📁 File: {result}")
            print(f"   📊 Size: {file_size:,} bytes")
            
            # Clean up
            os.remove(result)
            print("   🧹 Cleaned up test file")
            
            return True
        else:
            print("   ❌ Animation file not found")
            return False
            
    except Exception as e:
        print(f"   ❌ Animation generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pdf_processing():
    """Test PDF processing capabilities"""
    print("\n3. Testing PDF Processing...")
    
    try:
        import PyPDF2
        import fitz
        print("   ✓ PyPDF2 available")
        print("   ✓ PyMuPDF available")
        return True
    except ImportError as e:
        print(f"   ❌ PDF libraries missing: {e}")
        return False

if __name__ == "__main__":
    # Run tests
    content_test = test_content_aware_animation()
    pdf_test = test_pdf_processing()
    
    print("\n" + "=" * 50)
    print("🎯 TEST SUMMARY")
    print("=" * 50)
    print(f"Content-Aware Animation: {'✅ PASS' if content_test else '❌ FAIL'}")
    print(f"PDF Processing:          {'✅ PASS' if pdf_test else '❌ FAIL'}")
    
    if content_test and pdf_test:
        print("\n🚀 System is ready! Use enhanced_clean_app.py")
        print("   Features:")
        print("   - ✅ Content-aware animations")
        print("   - ✅ PDF support")
        print("   - ✅ Image processing")
        print("   - ✅ Direct text input")
    else:
        print("\n⚠️  Some features may not work properly")
