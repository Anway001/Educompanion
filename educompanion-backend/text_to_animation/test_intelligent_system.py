"""
Test the Intelligent Animation System
Creates sample content for different types and generates appropriate animations
"""

import os
import sys
sys.path.append('.')

from intelligent_animator import create_intelligent_animation, ContentAnalyzer
from PIL import Image, ImageDraw, ImageFont

def create_test_content_samples():
    """Create various test content images to demonstrate intelligent animation"""
    
    test_contents = {
        'data_structures': '''
        STACK DATA STRUCTURE OPERATIONS
        
        A stack is a Last In First Out (LIFO) data structure.
        
        Key Operations:
        1. push(10) - Add element 10 to stack
        2. push(20) - Add element 20 to stack  
        3. push(30) - Add element 30 to stack
        4. pop() - Remove top element (returns 30)
        5. push(40) - Add element 40 to stack
        6. pop() - Remove top element (returns 40)
        7. pop() - Remove top element (returns 20)
        
        Final stack contains: [10]
        ''',
        
        'algorithms': '''
        BUBBLE SORT ALGORITHM
        
        Bubble sort is a simple sorting algorithm that repeatedly 
        steps through the list, compares adjacent elements and 
        swaps them if they are in the wrong order.
        
        Example array: [64, 34, 25, 12, 22, 11, 90]
        
        Algorithm steps:
        1. Compare adjacent elements
        2. Swap if left > right
        3. Repeat until no more swaps needed
        
        Time complexity: O(n²)
        Space complexity: O(1)
        ''',
        
        'mathematics': '''
        QUADRATIC FUNCTIONS
        
        A quadratic function has the form:
        f(x) = ax² + bx + c
        
        Where a ≠ 0
        
        Example: f(x) = x² - 4x + 3
        
        Key properties:
        - Vertex form: f(x) = a(x-h)² + k
        - Roots found using quadratic formula
        - Graph is a parabola
        
        The derivative is: f'(x) = 2ax + b
        ''',
        
        'physics': '''
        PROJECTILE MOTION
        
        When an object is thrown at an angle, it follows a parabolic path.
        
        Key equations:
        x = v₀ cos(θ) × t
        y = v₀ sin(θ) × t - ½gt²
        
        Where:
        - v₀ = initial velocity
        - θ = launch angle  
        - g = 9.8 m/s² (acceleration due to gravity)
        - t = time
        
        Maximum range occurs at 45° angle.
        ''',
        
        'business': '''
        PROJECT MANAGEMENT WORKFLOW
        
        Standard project management process:
        
        1. Project Initiation
           - Define scope and objectives
           - Identify stakeholders
        
        2. Planning Phase
           - Create work breakdown structure
           - Estimate resources and timeline
        
        3. Execution
           - Implement project plan
           - Monitor progress
        
        4. Review and Closure
           - Evaluate outcomes
           - Document lessons learned
        ''',
        
        'chemistry': '''
        CHEMICAL REACTIONS
        
        Types of chemical reactions:
        
        1. Synthesis: A + B → AB
           Example: 2H₂ + O₂ → 2H₂O
        
        2. Decomposition: AB → A + B
           Example: 2H₂O → 2H₂ + O₂
        
        3. Single displacement: A + BC → AC + B
           Example: Zn + CuSO₄ → ZnSO₄ + Cu
        
        4. Double displacement: AB + CD → AD + CB
           Example: AgNO₃ + NaCl → AgCl + NaNO₃
        '''
    }
    
    return test_contents

def create_test_images(test_contents):
    """Create test images from content"""
    os.makedirs('test_samples', exist_ok=True)
    
    for content_type, text in test_contents.items():
        # Create image with text
        img = Image.new('RGB', (1000, 800), 'white')
        draw = ImageDraw.Draw(img)
        
        try:
            # Try to use a decent font
            font = ImageFont.truetype("arial.ttf", 24)
            title_font = ImageFont.truetype("arial.ttf", 32)
        except:
            font = ImageFont.load_default()
            title_font = font
        
        # Draw title
        title = content_type.replace('_', ' ').title()
        draw.text((50, 30), title, fill='black', font=title_font)
        
        # Draw content
        lines = text.strip().split('\n')
        y_pos = 100
        for line in lines:
            if line.strip():
                draw.text((50, y_pos), line, fill='black', font=font)
                y_pos += 35
        
        # Save image
        image_path = f'test_samples/{content_type}_notes.jpg'
        img.save(image_path)
        print(f"✅ Created test image: {image_path}")
    
    return test_contents

def test_content_analysis():
    """Test the content analyzer"""
    print("🔍 Testing Content Analysis System...\n")
    
    test_contents = create_test_content_samples()
    analyzer = ContentAnalyzer()
    
    for content_type, text in test_contents.items():
        print(f"--- {content_type.upper()} ---")
        analysis = analyzer.analyze_content(text)
        print(f"Detected Type: {analysis['type']}")
        print(f"Confidence Score: {analysis['score']}")
        print(f"Elements Found: {len(analysis['elements'])}")
        print(f"All Scores: {analysis['all_scores']}")
        print()

def test_intelligent_animations():
    """Test creating animations for different content types"""
    print("🎬 Testing Intelligent Animation Generation...\n")
    
    test_contents = create_test_content_samples()
    
    # Create output directory
    os.makedirs('test_outputs', exist_ok=True)
    
    for content_type, text in test_contents.items():
        print(f"Creating animation for {content_type}...")
        
        try:
            output_path = f'test_outputs/{content_type}_animation.mp4'
            result = create_intelligent_animation(text, output_path)
            print(f"✅ Animation created: {result}")
        except Exception as e:
            print(f"❌ Failed to create {content_type} animation: {e}")
        
        print()

def run_comprehensive_test():
    """Run comprehensive test of the intelligent animation system"""
    print("🚀 INTELLIGENT ANIMATION SYSTEM - COMPREHENSIVE TEST\n")
    print("="*60)
    
    # Test 1: Content Analysis
    test_content_analysis()
    
    print("="*60)
    
    # Test 2: Create test images
    print("📄 Creating Test Images...\n")
    test_contents = create_test_images(create_test_content_samples())
    
    print("="*60)
    
    # Test 3: Generate animations
    test_intelligent_animations()
    
    print("="*60)
    print("🎉 COMPREHENSIVE TEST COMPLETED!")
    print("\nCheck the following directories:")
    print("- test_samples/ : Sample note images")
    print("- test_outputs/ : Generated animation videos")
    print("\nYou can now upload any of the test images to the Streamlit app!")

if __name__ == "__main__":
    run_comprehensive_test()
