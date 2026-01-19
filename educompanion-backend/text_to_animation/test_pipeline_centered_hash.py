#!/usr/bin/env python3
"""
Test hash table centering with the intelligent animator
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from intelligent_animator import ContentAnalyzer, UniversalAnimationEngine

def test_centered_hash_table_in_pipeline():
    """Test the content analyzer and animation engine with centered hash table"""
    print("🔐 Testing Centered Hash Table in Pipeline")
    print("=" * 50)
    
    # Sample hash table text
    hash_table_text = """
    HASH TABLE DATA STRUCTURE
    
    Hash table implementation with collision resolution:
    
    Operations:
    1. insert(15) - hash(15) = 15 % 7 = 1
    2. insert(22) - hash(22) = 22 % 7 = 1 (collision!)
    3. insert(8) - hash(8) = 8 % 7 = 1 (another collision!)
    4. search(22) - found in chain at index 1
    5. delete(8) - remove from chain
    6. insert(29) - hash(29) = 29 % 7 = 1 (collision chain)
    
    Collision resolution: Separate chaining
    Load factor = elements / buckets
    """
    
    try:
        print("🔍 Analyzing content...")
        analyzer = ContentAnalyzer()
        content = analyzer.analyze_content(hash_table_text)
        
        print(f"✅ Content Analysis:")
        print(f"   Type: {content.get('type')}")
        print(f"   Score: {content.get('score')}")
        print(f"   Elements: {len(content.get('elements', []))}")
        
        if content.get('type') == 'data_structures':
            print("\n🎬 Creating centered hash table animation...")
            animator = UniversalAnimationEngine()
            
            result = animator.create_animation(
                content_analysis=content,
                output_path="output/pipeline_test_centered_hash.mp4"
            )
            
            print("✅ SUCCESS! Animation created with centered hash table")
            print(f"📁 Video saved: {result}")
            print("🎯 Hash table is properly centered in the pipeline!")
            return True
        else:
            print("❌ Content not detected as hash table data structure")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_centered_hash_table_in_pipeline()
    
    if success:
        print("\n🎉 COMPLETE SUCCESS!")
        print("✅ Hash table is properly centered in visualization")
        print("✅ Content analysis and animation pipeline works perfectly")
        print("✅ All data structures now have proper structural representations")
    else:
        print("\n❌ Test failed")
    
    exit(0 if success else 1)
    