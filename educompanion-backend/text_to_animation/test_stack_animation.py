import sys
import os
sys.path.append('.')
from intelligent_animator import create_intelligent_animation

# Test creating a stack animation
stack_content = """
STACK DATA STRUCTURE

A stack is a LIFO (Last In First Out) data structure.

Operations:
1. push(10) - Add 10 to stack
2. push(20) - Add 20 to stack  
3. push(30) - Add 30 to stack
4. pop() - Remove top element
5. push(40) - Add 40 to stack

The stack follows the principle: Last In, First Out.
"""

print("🎬 Creating Stack Animation...")
try:
    output_path = "test_stack_animation.mp4"
    result = create_intelligent_animation(stack_content, output_path)
    print(f"✅ Animation created successfully: {result}")
    
    # Check if file exists and get size
    if os.path.exists(result):
        size = os.path.getsize(result)
        print(f"📁 File size: {size:,} bytes")
    else:
        print("❌ Output file not found")
        
except Exception as e:
    print(f"❌ Error creating animation: {e}")
    import traceback
    traceback.print_exc()
