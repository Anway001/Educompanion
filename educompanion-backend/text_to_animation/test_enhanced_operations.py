#!/usr/bin/env python3
"""
Test Enhanced Operations Extraction
Tests if the improved pattern matching correctly extracts actual values from code/text
"""

import sys
sys.path.append('.')
from dynamic_code_visualizer import CodePatternDetector
from intelligent_animator import ContentAnalyzer

def test_enhanced_pattern_matching():
    """Test the enhanced pattern matching for data structure operations"""
    
    # Initialize detectors
    code_detector = CodePatternDetector()
    content_analyzer = ContentAnalyzer()
    
    # Test cases with actual values that should be extracted
    test_cases = {
        'Stack with numbered list': """
        Stack Operations:
        1. push(10) - Add 10 to stack
        2. push(20) - Add 20 to stack  
        3. push(30) - Add 30 to stack
        4. pop() - Remove top element
        5. push(40) - Add 40 to stack
        """,
        
        'Queue with natural language': """
        Queue Operations:
        - Add A to queue
        - Add B to queue
        - Add C to queue
        - Remove from queue
        - Put D in queue
        """,
        
        'Stack with code-like syntax': """
        stack.push(100);
        stack.push(200);
        stack.pop();
        stack.push(300);
        """,
        
        'Mixed values': """
        Data Structure Operations:
        Insert 5, 15, 25, 35 into the structure
        Remove one element
        Add 45 to the structure
        """
    }
    
    print("🧪 TESTING ENHANCED OPERATIONS EXTRACTION")
    print("=" * 60)
    
    for test_name, test_text in test_cases.items():
        print(f"\n--- {test_name} ---")
        print(f"Input text: {test_text.strip()[:100]}...")
        
        # Test with CodePatternDetector
        data_structure = code_detector.detect_data_structure(test_text)
        operations = code_detector.extract_operations(test_text, data_structure)
        
        print(f"🔍 Detected structure: {data_structure}")
        print(f"📝 Extracted operations:")
        for i, op in enumerate(operations, 1):
            if 'value' in op:
                print(f"   {i}. {op['type']} -> VALUE: {op['value']}")
            else:
                print(f"   {i}. {op['type']}")
        
        # Test with ContentAnalyzer
        content_analysis = content_analyzer.analyze_content(test_text)
        print(f"🎯 Content type: {content_analysis['type']}")
        if content_analysis['elements']:
            print(f"🔧 Content analyzer operations:")
            for i, op in enumerate(content_analysis['elements'][:5], 1):
                if 'value' in op:
                    print(f"   {i}. {op['type']} -> VALUE: {op['value']}")
                else:
                    print(f"   {i}. {op['type']}")
    
    print(f"\n✅ Enhanced pattern matching test completed!")

if __name__ == "__main__":
    test_enhanced_pattern_matching()