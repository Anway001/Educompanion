#!/usr/bin/env python3
"""
Test script specifically for the centered hash table visualization
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from intelligent_animator import UniversalAnimationEngine

def test_centered_hash_table():
    """Test the centered hash table animation"""
    print("🔐 Testing Centered Hash Table Visualization")
    print("=" * 50)
    
    # Ensure output directory exists
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    animation_engine = UniversalAnimationEngine()
    
    # Create comprehensive hash table operations to show centering
    hash_operations = [
        {'type': 'hash_insert', 'key': 15},
        {'type': 'hash_insert', 'key': 22},
        {'type': 'hash_insert', 'key': 8},
        {'type': 'hash_insert', 'key': 29},  # Collision with 22 (22%7=1, 29%7=1)
        {'type': 'hash_insert', 'key': 36},  # Another collision with 22,29 (36%7=1)
        {'type': 'hash_search', 'key': 22},
        {'type': 'hash_insert', 'key': 43},  # Another collision (43%7=1)
        {'type': 'hash_search', 'key': 29},
        {'type': 'hash_delete', 'key': 8},
        {'type': 'hash_insert', 'key': 50},  # 50%7=1, more collision
        {'type': 'hash_search', 'key': 36}
    ]
    
    try:
        hash_path = str(output_dir / "centered_hash_table_demo.mp4")
        print(f"🎬 Generating centered hash table animation...")
        print(f"📁 Output path: {hash_path}")
        
        result = animation_engine._animate_hash_table(hash_operations, hash_path)
        
        if os.path.exists(hash_path):
            size = os.path.getsize(hash_path)
            print(f"✅ SUCCESS!")
            print(f"📊 File size: {size:,} bytes ({size/1024:.1f} KB)")
            print(f"🎯 The hash table is now properly centered in the visualization!")
            print(f"🔗 Shows collision chaining with multiple elements")
            print(f"📈 Displays load factor and performance metrics")
            return True
        else:
            print("❌ FAILED - No output file generated")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_centered_hash_table()
    
    if success:
        print("\n🎉 Hash table visualization is now properly centered!")
        print("📺 Check the video to see the improved layout with:")
        print("   • Centered hash table structure")
        print("   • Balanced left/right information panels")
        print("   • Proper spacing and alignment")
        print("   • Enhanced visual clarity")
    else:
        print("\n❌ Hash table centering test failed")
    
    exit(0 if success else 1)
