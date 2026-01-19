#!/usr/bin/env python3
"""
Test Clean Value Extraction
Tests if brackets and other symbols are properly filtered out
"""

import sys
sys.path.append('.')
from dynamic_code_visualizer import CodePatternDetector
from intelligent_animator import ContentAnalyzer

def test_clean_value_extraction():
    """Test that only clean alphanumeric values are extracted (no brackets, quotes, etc.)"""
    
    # Initialize detectors
    code_detector = CodePatternDetector()
    content_analyzer = ContentAnalyzer()
    
    # Test cases that might include brackets or unwanted symbols
    test_cases = {
        'Queue with brackets': """
        Queue Operations:
        1. enqueue(10) - Add 10 to queue
        2. enqueue("A") - Add A to queue  
        3. enqueue([20]) - Add 20 to queue
        4. dequeue() - Remove from queue
        5. enqueue({30}) - Add 30 to queue
        """,
        
        'Stack with mixed formatting': """
        Stack Operations:
        - push(100);
        - push("hello");
        - push([200]);
        - pop();
        - push({300});
        """,
        
        'Code with quotes and brackets': """
        queue.append("value1");
        queue.append([value2]);
        queue.append({value3});
        stack.push("data1");
        stack.push([data2]);
        """,
        
        'Natural language with parentheses': """
        Add (50) to the queue
        Insert (60) into stack
        Put (70) in queue
        Push (80) to stack
        """
    }
    
    print("🧪 TESTING CLEAN VALUE EXTRACTION")
    print("=" * 60)
    
    for test_name, test_text in test_cases.items():
        print(f"\n--- {test_name} ---")
        print(f"Input text: {test_text.strip()[:80]}...")
        
        # Test with CodePatternDetector
        data_structure = code_detector.detect_data_structure(test_text)
        operations = code_detector.extract_operations(test_text, data_structure)
        
        print(f"🔍 Detected structure: {data_structure}")
        print(f"📝 Extracted operations (CodePatternDetector):")
        for i, op in enumerate(operations, 1):
            if 'value' in op:
                value = op['value']
                # Check if value contains unwanted characters
                has_brackets = any(char in value for char in '()[]{}"\'')
                status = "❌ HAS BRACKETS/QUOTES" if has_brackets else "✅ CLEAN"
                print(f"   {i}. {op['type']} -> VALUE: '{value}' {status}")
            else:
                print(f"   {i}. {op['type']} ✅")
        
        # Test with ContentAnalyzer
        content_analysis = content_analyzer.analyze_content(test_text)
        if content_analysis['elements']:
            print(f"🔧 Content analyzer operations:")
            for i, op in enumerate(content_analysis['elements'][:5], 1):
                if 'value' in op:
                    value = op['value']
                    has_brackets = any(char in value for char in '()[]{}"\'')
                    status = "❌ HAS BRACKETS/QUOTES" if has_brackets else "✅ CLEAN"
                    print(f"   {i}. {op['type']} -> VALUE: '{value}' {status}")
                else:
                    print(f"   {i}. {op['type']} ✅")
    
    print(f"\n✅ Clean value extraction test completed!")

if __name__ == "__main__":
    test_clean_value_extraction()