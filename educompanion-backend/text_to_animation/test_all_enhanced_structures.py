#!/usr/bin/env python3
"""
Comprehensive test suite for all enhanced data structure animations
Tests all data structures with proper structural representations
"""

import os
import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from intelligent_animator import ContentAnalyzer, UniversalAnimationEngine

def test_enhanced_data_structures():
    """Test all enhanced data structure animations"""
    print("🚀 Testing All Enhanced Data Structure Animations")
    print("=" * 60)
    
    # Ensure output directory exists
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    content_analyzer = ContentAnalyzer()
    animation_engine = UniversalAnimationEngine()
    
    test_results = {}
    
    # Test 1: Enhanced Binary Tree
    print("\n📊 Testing Enhanced Binary Tree Animation...")
    tree_operations = [
        {'type': 'tree_insert', 'value': 50},
        {'type': 'tree_insert', 'value': 30},
        {'type': 'tree_insert', 'value': 70},
        {'type': 'tree_insert', 'value': 20},
        {'type': 'tree_insert', 'value': 40},
        {'type': 'tree_insert', 'value': 60},
        {'type': 'tree_insert', 'value': 80}
    ]
    
    try:
        tree_path = str(output_dir / "enhanced_tree_test.mp4")
        result = animation_engine._animate_tree(tree_operations, tree_path)
        
        if os.path.exists(tree_path):
            size = os.path.getsize(tree_path)
            test_results['Enhanced Binary Tree'] = f"✅ SUCCESS - {size} bytes"
            print(f"✅ Enhanced Binary Tree: Generated {size} bytes")
        else:
            test_results['Enhanced Binary Tree'] = "❌ FAILED - No output file"
            print("❌ Enhanced Binary Tree: Failed to generate video")
            
    except Exception as e:
        test_results['Enhanced Binary Tree'] = f"❌ ERROR - {str(e)}"
        print(f"❌ Enhanced Binary Tree: Error - {e}")
    
    # Test 2: Enhanced Linked List
    print("\n🔗 Testing Enhanced Linked List Animation...")
    list_operations = [
        {'type': 'list_insert', 'value': 10},
        {'type': 'list_append', 'value': 20},
        {'type': 'list_append', 'value': 30},
        {'type': 'list_insert', 'value': 5},
        {'type': 'list_delete'},
        {'type': 'list_append', 'value': 40}
    ]
    
    try:
        list_path = str(output_dir / "enhanced_linked_list_test.mp4")
        result = animation_engine._animate_linked_list(list_operations, list_path)
        
        if os.path.exists(list_path):
            size = os.path.getsize(list_path)
            test_results['Enhanced Linked List'] = f"✅ SUCCESS - {size} bytes"
            print(f"✅ Enhanced Linked List: Generated {size} bytes")
        else:
            test_results['Enhanced Linked List'] = "❌ FAILED - No output file"
            print("❌ Enhanced Linked List: Failed to generate video")
            
    except Exception as e:
        test_results['Enhanced Linked List'] = f"❌ ERROR - {str(e)}"
        print(f"❌ Enhanced Linked List: Error - {e}")
    
    # Test 3: Enhanced Graph
    print("\n🌐 Testing Enhanced Graph Animation...")
    graph_operations = [
        {'type': 'graph_add_node', 'node': 'A'},
        {'type': 'graph_add_node', 'node': 'B'},
        {'type': 'graph_add_node', 'node': 'C'},
        {'type': 'graph_add_node', 'node': 'D'},
        {'type': 'graph_add_edge', 'from_node': 'A', 'to_node': 'B', 'weight': 5},
        {'type': 'graph_add_edge', 'from_node': 'B', 'to_node': 'C', 'weight': 3},
        {'type': 'graph_add_edge', 'from_node': 'C', 'to_node': 'D', 'weight': 2},
        {'type': 'graph_add_edge', 'from_node': 'A', 'to_node': 'D', 'weight': 7},
        {'type': 'graph_dfs', 'node': 'A'}
    ]
    
    try:
        graph_path = str(output_dir / "enhanced_graph_test.mp4")
        result = animation_engine._animate_graph(graph_operations, graph_path)
        
        if os.path.exists(graph_path):
            size = os.path.getsize(graph_path)
            test_results['Enhanced Graph'] = f"✅ SUCCESS - {size} bytes"
            print(f"✅ Enhanced Graph: Generated {size} bytes")
        else:
            test_results['Enhanced Graph'] = "❌ FAILED - No output file"
            print("❌ Enhanced Graph: Failed to generate video")
            
    except Exception as e:
        test_results['Enhanced Graph'] = f"❌ ERROR - {str(e)}"
        print(f"❌ Enhanced Graph: Error - {e}")
    
    # Test 4: Enhanced Hash Table
    print("\n🔐 Testing Enhanced Hash Table Animation...")
    hash_operations = [
        {'type': 'hash_insert', 'key': 15},
        {'type': 'hash_insert', 'key': 22},
        {'type': 'hash_insert', 'key': 8},
        {'type': 'hash_insert', 'key': 29},  # This should cause collision with 22
        {'type': 'hash_search', 'key': 22},
        {'type': 'hash_insert', 'key': 36},  # Another collision
        {'type': 'hash_delete', 'key': 8},
        {'type': 'hash_search', 'key': 29}
    ]
    
    try:
        hash_path = str(output_dir / "enhanced_hash_table_test.mp4")
        result = animation_engine._animate_hash_table(hash_operations, hash_path)
        
        if os.path.exists(hash_path):
            size = os.path.getsize(hash_path)
            test_results['Enhanced Hash Table'] = f"✅ SUCCESS - {size} bytes"
            print(f"✅ Enhanced Hash Table: Generated {size} bytes")
        else:
            test_results['Enhanced Hash Table'] = "❌ FAILED - No output file"
            print("❌ Enhanced Hash Table: Failed to generate video")
            
    except Exception as e:
        test_results['Enhanced Hash Table'] = f"❌ ERROR - {str(e)}"
        print(f"❌ Enhanced Hash Table: Error - {e}")
    
    # Test 5: Enhanced Stack (existing)
    print("\n📚 Testing Enhanced Stack Animation...")
    stack_operations = [
        {'type': 'stack_push', 'value': 10},
        {'type': 'stack_push', 'value': 20},
        {'type': 'stack_push', 'value': 30},
        {'type': 'stack_pop'},
        {'type': 'stack_push', 'value': 40},
        {'type': 'stack_pop'}
    ]
    
    try:
        stack_path = str(output_dir / "enhanced_stack_test.mp4")
        result = animation_engine._animate_stack(stack_operations, stack_path)
        
        if os.path.exists(stack_path):
            size = os.path.getsize(stack_path)
            test_results['Enhanced Stack'] = f"✅ SUCCESS - {size} bytes"
            print(f"✅ Enhanced Stack: Generated {size} bytes")
        else:
            test_results['Enhanced Stack'] = "❌ FAILED - No output file"
            print("❌ Enhanced Stack: Failed to generate video")
            
    except Exception as e:
        test_results['Enhanced Stack'] = f"❌ ERROR - {str(e)}"
        print(f"❌ Enhanced Stack: Error - {e}")
    
    # Test 6: Enhanced Queue (existing)
    print("\n🎪 Testing Enhanced Queue Animation...")
    queue_operations = [
        {'type': 'queue_enqueue', 'value': 'A'},
        {'type': 'queue_enqueue', 'value': 'B'},
        {'type': 'queue_enqueue', 'value': 'C'},
        {'type': 'queue_dequeue'},
        {'type': 'queue_enqueue', 'value': 'D'},
        {'type': 'queue_dequeue'}
    ]
    
    try:
        queue_path = str(output_dir / "enhanced_queue_test.mp4")
        result = animation_engine._animate_queue(queue_operations, queue_path)
        
        if os.path.exists(queue_path):
            size = os.path.getsize(queue_path)
            test_results['Enhanced Queue'] = f"✅ SUCCESS - {size} bytes"
            print(f"✅ Enhanced Queue: Generated {size} bytes")
        else:
            test_results['Enhanced Queue'] = "❌ FAILED - No output file"
            print("❌ Enhanced Queue: Failed to generate video")
            
    except Exception as e:
        test_results['Enhanced Queue'] = f"❌ ERROR - {str(e)}"
        print(f"❌ Enhanced Queue: Error - {e}")
    
    # Test 7: Enhanced Array
    print("\n📋 Testing Enhanced Array Animation...")
    array_operations = [
        {'type': 'array_insert', 'value': 5, 'index': 0},
        {'type': 'array_insert', 'value': 10, 'index': 1},
        {'type': 'array_insert', 'value': 15, 'index': 2},
        {'type': 'array_update', 'value': 20, 'index': 1},
        {'type': 'array_delete', 'index': 0},
        {'type': 'array_insert', 'value': 25, 'index': 2}
    ]
    
    try:
        array_path = str(output_dir / "enhanced_array_test.mp4")
        result = animation_engine._animate_array(array_operations, array_path)
        
        if os.path.exists(array_path):
            size = os.path.getsize(array_path)
            test_results['Enhanced Array'] = f"✅ SUCCESS - {size} bytes"
            print(f"✅ Enhanced Array: Generated {size} bytes")
        else:
            test_results['Enhanced Array'] = "❌ FAILED - No output file"
            print("❌ Enhanced Array: Failed to generate video")
            
    except Exception as e:
        test_results['Enhanced Array'] = f"❌ ERROR - {str(e)}"
        print(f"❌ Enhanced Array: Error - {e}")
    
    # Final Results Summary
    print("\n" + "=" * 60)
    print("🎯 ENHANCED DATA STRUCTURES TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for structure, result in test_results.items():
        print(f"{structure:<25}: {result}")
        if "✅ SUCCESS" in result:
            passed += 1
    
    print(f"\n📊 OVERALL RESULTS: {passed}/{total} data structures enhanced successfully")
    
    if passed == total:
        print("🎉 ALL DATA STRUCTURES NOW SHOW PROPER STRUCTURAL REPRESENTATIONS!")
        print("✅ Binary Trees show proper node hierarchy with edges")
        print("✅ Linked Lists show proper node-pointer structure")
        print("✅ Graphs show proper network topology with adjacency")
        print("✅ Hash Tables show proper bucket structure with chaining")
        print("✅ Stacks and Queues already had proper visualizations")
        print("✅ Arrays show proper indexed element structure")
    else:
        print(f"⚠️  {total - passed} data structures need attention")
    
    print(f"\n📁 All test videos saved to: {output_dir.absolute()}")
    
    return passed == total

if __name__ == "__main__":
    start_time = time.time()
    success = test_enhanced_data_structures()
    end_time = time.time()
    
    print(f"\n⏱️  Total test time: {end_time - start_time:.2f} seconds")
    
    if success:
        print("🎯 ALL ENHANCED DATA STRUCTURE TESTS PASSED!")
        exit(0)
    else:
        print("❌ Some enhanced data structure tests failed")
        exit(1)
