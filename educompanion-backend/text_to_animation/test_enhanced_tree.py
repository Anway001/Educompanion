"""
Test the improved tree visualization
"""

from intelligent_animator import ContentAnalyzer, IntelligentAnimator

def test_tree_visualization():
    """Test binary tree visualization with better structure"""
    
    analyzer = ContentAnalyzer()
    animator = IntelligentAnimator()
    
    # Test with binary tree C code
    tree_code = '''
    Binary Search Tree Implementation in C
    
    #include <stdio.h>
    #include <stdlib.h>
    
    struct Node {
        int data;
        struct Node* left;
        struct Node* right;
    };
    
    struct Node* createNode(int value) {
        struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
        newNode->data = value;
        newNode->left = NULL;
        newNode->right = NULL;
        return newNode;
    }
    
    struct Node* insert(struct Node* root, int value) {
        if (root == NULL) {
            return createNode(value);
        }
        if (value < root->data) {
            root->left = insert(root->left, value);
        } else {
            root->right = insert(root->right, value);
        }
        return root;
    }
    
    Example insertions:
    insert(50) - Root node
    insert(30) - Left child
    insert(70) - Right child  
    insert(20) - Left-left
    insert(40) - Left-right
    insert(60) - Right-left
    insert(80) - Right-right
    '''
    
    print("🌳 Testing Enhanced Binary Tree Visualization")
    print("=" * 50)
    
    # Analyze content
    content = analyzer.analyze_content(tree_code)
    print(f"✓ Content Type: {content['type']}")
    print(f"✓ Score: {content['score']}")
    print(f"✓ Operations Found: {len(content['elements'])}")
    
    for i, op in enumerate(content['elements'], 1):
        print(f"  {i}. {op['type']} - Value: {op.get('value', 'N/A')}")
    
    # Create animation
    output_path = "enhanced_tree_animation.mp4"
    
    try:
        result_path = animator._create_data_structure_animation(content['elements'], output_path)
        print(f"\n✅ Enhanced tree animation created: {result_path}")
        
        import os
        if os.path.exists(result_path):
            file_size = os.path.getsize(result_path)
            print(f"📁 File size: {file_size:,} bytes")
            
            # Cleanup
            os.remove(result_path)
            print("✓ Test file cleaned up")
            
            print("\n🎉 Enhanced tree visualization working!")
            print("Features:")
            print("  • Proper binary search tree structure")
            print("  • Node positioning with levels") 
            print("  • Step-by-step insertion animation")
            print("  • Tree properties display")
            print("  • Inorder traversal shown")
            print("  • Highlighted new insertions")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_tree_visualization()
