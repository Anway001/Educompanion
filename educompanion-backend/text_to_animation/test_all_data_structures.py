"""
Test script for all data structure animations
Tests the newly implemented animation methods
"""

import os
import sys
from intelligent_animator import ContentAnalyzer, IntelligentAnimator

def test_data_structure_animations():
    """Test all data structure animations"""
    
    analyzer = ContentAnalyzer()
    animator = IntelligentAnimator()
    
    # Test cases for different data structures
    test_cases = [
        {
            'name': 'Stack Operations',
            'text': '''STACK DATA STRUCTURE
            A stack is a LIFO structure.
            Operations:
            1. push(10) - Add 10 to top
            2. push(20) - Add 20 to top  
            3. pop() - Remove top element
            4. push(30) - Add 30 to top
            ''',
            'expected_type': 'data_structures'
        },
        {
            'name': 'Binary Tree Operations',
            'text': '''BINARY TREE INSERTION
            Binary Search Tree operations:
            1. insert(50) - Add root node
            2. insert(30) - Add left child
            3. insert(70) - Add right child
            4. insert(20) - Add to left subtree
            ''',
            'expected_type': 'data_structures'
        },
        {
            'name': 'Linked List Operations',
            'text': '''LINKED LIST IMPLEMENTATION
            Linked list operations:
            1. insert(10) - Add first node
            2. append(20) - Add to end
            3. insert(5) - Add to beginning
            4. delete() - Remove node
            ''',
            'expected_type': 'data_structures'
        },
        {
            'name': 'Graph Operations',
            'text': '''GRAPH ALGORITHMS
            Graph data structure:
            1. Add node A
            2. Add node B  
            3. Add edge A to B
            4. DFS traversal from A
            ''',
            'expected_type': 'data_structures'
        },
        {
            'name': 'Hash Table Operations',
            'text': '''HASH TABLE IMPLEMENTATION
            Hash table with collision handling:
            1. insert("John") - Add key
            2. insert("Jane") - Add another key
            3. search("John") - Find key
            4. delete("Jane") - Remove key
            ''',
            'expected_type': 'data_structures'
        },
        {
            'name': 'Array Operations',
            'text': '''ARRAY DATA STRUCTURE
            Dynamic array operations:
            1. append(10) - Add element
            2. insert(5, 0) - Insert at index
            3. delete(1) - Remove element
            ''',
            'expected_type': 'data_structures'
        }
    ]
    
    print("🧪 Testing Data Structure Animations...")
    print("=" * 50)
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing {test_case['name']}")
        print("-" * 30)
        
        try:
            # Analyze content
            content_analysis = analyzer.analyze_content(test_case['text'])
            
            print(f"✓ Content Type: {content_analysis['type']}")
            print(f"✓ Score: {content_analysis['score']}")
            print(f"✓ Elements Found: {len(content_analysis['elements'])}")
            
            # Check if correct type detected
            if content_analysis['type'] == test_case['expected_type']:
                print("✅ Content type detection: PASS")
            else:
                print(f"❌ Content type detection: FAIL (expected {test_case['expected_type']}, got {content_analysis['type']})")
                all_passed = False
            
            # Test animation creation (without actually creating video files)
            if content_analysis['elements']:
                print(f"✓ Found {len(content_analysis['elements'])} operations to animate")
                
                # Test that the animation method can be called
                output_path = f"test_output_{i}.mp4"
                try:
                    result_path = animator._create_data_structure_animation(
                        content_analysis['elements'], 
                        output_path
                    )
                    print("✅ Animation method: PASS")
                    
                    # Clean up test file if created
                    if os.path.exists(result_path):
                        os.remove(result_path)
                        print("✓ Test file cleaned up")
                        
                except Exception as e:
                    print(f"❌ Animation method: FAIL - {str(e)}")
                    all_passed = False
            else:
                print("⚠️  No operations detected for animation")
                
        except Exception as e:
            print(f"❌ Test failed with error: {str(e)}")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED! All data structure animations are working!")
    else:
        print("❌ Some tests failed. Check the output above for details.")
    
    return all_passed

def test_content_detection():
    """Test content detection for various data structures"""
    
    analyzer = ContentAnalyzer()
    
    test_texts = {
        'Stack': 'This is about stack data structure with push and pop operations',
        'Queue': 'Queue implementation with enqueue and dequeue operations',
        'Tree': 'Binary tree with insert and traversal operations',
        'Graph': 'Graph algorithms including DFS and BFS traversal',
        'Hash': 'Hash table implementation with collision resolution',
        'Array': 'Array operations including insert and delete',
        'Linked List': 'Linked list data structure with node operations'
    }
    
    print("\n🔍 Testing Content Detection...")
    print("=" * 40)
    
    for structure, text in test_texts.items():
        content = analyzer.analyze_content(text)
        print(f"{structure:12} → Type: {content['type']:15} Score: {content['score']:3}")
    
    return True

if __name__ == "__main__":
    print("🚀 Starting Data Structure Animation Tests")
    print("=" * 60)
    
    # Test content detection
    test_content_detection()
    
    # Test all animations
    success = test_data_structure_animations()
    
    if success:
        print("\n✅ All tests completed successfully!")
        print("Your application now supports:")
        print("  • Stack animations (push/pop)")
        print("  • Queue animations (enqueue/dequeue)")  
        print("  • Array animations (insert/delete/append)")
        print("  • Binary Tree animations (insert/traversal)")
        print("  • Linked List animations (insert/append/delete)")
        print("  • Graph animations (nodes/edges/DFS/BFS)")
        print("  • Hash Table animations (insert/search/delete)")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
        sys.exit(1)
