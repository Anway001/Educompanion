"""
Intelligent Content-Aware Animation Generator
Analyzes uploaded notes and creates appropriate animations based on content type
Supports: Algorithms, Data Structures, Math Concepts, Science, Business Processes, etc.
"""

import os
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Arrow
import cv2
from PIL import Image, ImageDraw, ImageFont
from typing import List, Dict, Tuple, Any, Optional
import json
import math

class ContentAnalyzer:
    """Analyzes content and determines appropriate animation type"""
    
    def __init__(self):
        self.content_patterns = {
            'data_structures': {
                'keywords': ['stack', 'queue', 'array', 'linked list', 'tree', 'graph', 'hash', 'heap'],
                'operations': ['push', 'pop', 'enqueue', 'dequeue', 'insert', 'delete', 'search', 'traverse']
            },
            'algorithms': {
                'keywords': ['algorithm', 'sort', 'search', 'recursion', 'iteration', 'divide', 'conquer'],
                'patterns': ['bubble sort', 'merge sort', 'quick sort', 'binary search', 'linear search']
            },
            'mathematics': {
                'keywords': ['equation', 'formula', 'function', 'graph', 'derivative', 'integral', 'matrix'],
                'symbols': ['=', '+', '-', '*', '/', '^', '∫', '∂', 'Σ']
            },
            'physics': {
                'keywords': ['force', 'motion', 'energy', 'wave', 'velocity', 'acceleration', 'mass', 'kinematics', 'dynamics', 'momentum'],
                'concepts': ['newton', 'gravity', 'momentum', 'friction'],
                'patterns': ['m/s', 'm/s²', 'kg', 'N', 'J', 'W', 'Hz']
            },
            'chemistry': {
                'keywords': ['reaction', 'molecule', 'atom', 'bond', 'element', 'compound', 'chemical', 'formula'],
                'patterns': ['H2O', 'CO2', 'NaCl', 'chemical equation', 'pH', 'acid', 'base'],
                'concepts': ['equilibrium', 'catalyst', 'oxidation', 'reduction']
            },
            'biology': {
                'keywords': ['cell', 'dna', 'organism', 'evolution', 'gene', 'protein', 'enzyme'],
                'patterns': ['mitosis', 'meiosis', 'photosynthesis', 'respiration'],
                'concepts': ['nucleus', 'membrane', 'chromosome', 'inheritance', 'adaptation']
            },
            'business': {
                'keywords': ['process', 'workflow', 'strategy', 'analysis', 'diagram', 'flowchart'],
                'concepts': ['decision', 'approval', 'review', 'implementation']
            }
        }
    
    def analyze_content(self, text: str) -> Dict[str, Any]:
        """Analyze text content and determine animation type"""
        text_lower = text.lower()
        content_scores = {}
        
        # Score each content type with better specificity
        for content_type, patterns in self.content_patterns.items():
            score = 0
            
            # Check keywords with different weights based on specificity
            for keyword in patterns.get('keywords', []):
                count = text_lower.count(keyword.lower())
                if content_type == 'physics':
                    # Physics gets higher weight for specific physics terms
                    if keyword in ['kinematics', 'dynamics', 'momentum', 'velocity', 'acceleration']:
                        score += count * 5
                    else:
                        score += count * 2
                elif content_type == 'chemistry':
                    # Chemistry gets higher weight for specific chemistry terms
                    if keyword in ['reaction', 'molecule', 'chemical', 'formula']:
                        score += count * 5
                    else:
                        score += count * 2
                elif content_type == 'biology':
                    # Biology gets higher weight for specific biology terms
                    if keyword in ['cell', 'dna', 'organism', 'gene']:
                        score += count * 5
                    else:
                        score += count * 2
                elif content_type == 'mathematics':
                    # Mathematics gets higher weight for specific math terms
                    if keyword in ['equation', 'function', 'derivative', 'integral']:
                        score += count * 5
                    else:
                        score += count * 2
                else:
                    score += count * 2
            
            # Check operations/patterns
            for pattern in patterns.get('operations', []) + patterns.get('patterns', []):
                score += text_lower.count(pattern.lower()) * 3
            
            # Check symbols for math/science
            for symbol in patterns.get('symbols', []):
                score += text.count(symbol) * 1
            
            # Check concepts
            for concept in patterns.get('concepts', []):
                score += text_lower.count(concept.lower()) * 2
            
            content_scores[content_type] = score
        
        # Determine primary content type
        primary_type = max(content_scores, key=content_scores.get) if any(content_scores.values()) else 'general'
        
        # Extract specific elements based on content type
        elements = self._extract_elements(text, primary_type)
        
        return {
            'type': primary_type,
            'score': content_scores[primary_type],
            'elements': elements,
            'all_scores': content_scores
        }
    
    def _extract_elements(self, text: str, content_type: str) -> List[Dict]:
        """Extract specific elements for animation based on content type"""
        elements = []
        
        if content_type == 'data_structures':
            elements = self._extract_data_structure_operations(text)
        elif content_type == 'algorithms':
            elements = self._extract_algorithm_steps(text)
        elif content_type == 'mathematics':
            elements = self._extract_math_concepts(text)
        elif content_type == 'physics':
            elements = self._extract_physics_concepts(text)
        elif content_type == 'chemistry':
            elements = self._extract_chemistry_concepts(text)
        elif content_type == 'biology':
            elements = self._extract_biology_concepts(text)
        elif content_type == 'business':
            elements = self._extract_process_steps(text)
        else:
            elements = self._extract_general_concepts(text)
        
        return elements
    
    def _extract_data_structure_operations(self, text: str) -> List[Dict]:
        """Extract data structure operations from text with enhanced pattern matching"""
        operations = []
        text_lower = text.lower()
        
        # Stack operations with enhanced pattern matching
        if 'stack' in text_lower:
            # Enhanced patterns for push operations - only capture alphanumeric values
            push_patterns = [
                r'push\s*\(\s*["\']?([A-Za-z0-9]+)["\']?\s*\)',  # push(value) or push("value")
                r'\.push\s*\(\s*["\']?([A-Za-z0-9]+)["\']?\s*\)',  # obj.push(value)
                r'stack\.append\s*\(\s*["\']?([A-Za-z0-9]+)["\']?\s*\)',  # stack.append(value)
                r'add\s+([A-Za-z0-9]+)\s+to\s+stack',  # "add 10 to stack"
                r'push\s+([A-Za-z0-9]+)',  # "push 10"
                r'insert\s+([A-Za-z0-9]+)\s+into\s+stack',  # "insert 10 into stack"
            ]
            
            for pattern in push_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for value in matches:
                    clean_value = value.strip().strip('"\'()[]{}')
                    if clean_value:
                        operations.append({'type': 'stack_push', 'value': clean_value})
            
            # Enhanced patterns for pop operations
            pop_patterns = [
                r'pop\s*\(\s*\)',  # pop()
                r'\.pop\s*\(\s*\)',  # obj.pop()
                r'stack\.pop\s*\(\s*\)',  # stack.pop()
                r'remove\s+from\s+stack',  # "remove from stack"
                r'pop\s+element',  # "pop element"
            ]
            
            for pattern in pop_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for _ in matches:
                    operations.append({'type': 'stack_pop'})
        
        # Queue operations with enhanced pattern matching
        elif 'queue' in text_lower:
            # Enhanced patterns for enqueue operations - only capture alphanumeric values
            enqueue_patterns = [
                r'enqueue\s*\(\s*["\']?([A-Za-z0-9]+)["\']?\s*\)',  # enqueue(value)
                r'\.enqueue\s*\(\s*["\']?([A-Za-z0-9]+)["\']?\s*\)',  # obj.enqueue(value)
                r'queue\.append\s*\(\s*["\']?([A-Za-z0-9]+)["\']?\s*\)',  # queue.append(value)
                r'add\s+([A-Za-z0-9]+)\s+to\s+queue',  # "add 10 to queue"
                r'enqueue\s+([A-Za-z0-9]+)',  # "enqueue 10"
                r'insert\s+([A-Za-z0-9]+)\s+into\s+queue',  # "insert 10 into queue"
            ]
            
            for pattern in enqueue_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for value in matches:
                    clean_value = value.strip().strip('"\'()[]{}')
                    if clean_value:
                        operations.append({'type': 'queue_enqueue', 'value': clean_value})
            
            # Enhanced patterns for dequeue operations
            dequeue_patterns = [
                r'dequeue\s*\(\s*\)',  # dequeue()
                r'\.dequeue\s*\(\s*\)',  # obj.dequeue()
                r'queue\.popleft\s*\(\s*\)',  # queue.popleft()
                r'remove\s+from\s+queue',  # "remove from queue"
                r'dequeue\s+element',  # "dequeue element"
            ]
            
            for pattern in dequeue_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for _ in matches:
                    operations.append({'type': 'queue_dequeue'})
        
        # Binary Tree operations
        elif any(word in text_lower for word in ['tree', 'binary tree', 'bst', 'binary search tree', 'node', 'struct node']):
            # Look for insert operations with various patterns
            insert_matches = re.findall(r'insert\s*\(\s*(\d+)\s*\)', text, re.IGNORECASE)
            for value in insert_matches:
                operations.append({'type': 'tree_insert', 'value': value})
            
            # Look for createNode operations (common in C code)
            create_matches = re.findall(r'createNode\s*\(\s*(\d+)\s*\)', text, re.IGNORECASE)
            for value in create_matches:
                operations.append({'type': 'tree_insert', 'value': value})
            
            # Look for newNode assignments (common pattern)
            new_node_matches = re.findall(r'newNode.*?=.*?(\d+)', text, re.IGNORECASE)
            for value in new_node_matches:
                operations.append({'type': 'tree_insert', 'value': value})
            
            # Look for data assignments to nodes
            data_matches = re.findall(r'data\s*=\s*(\d+)', text, re.IGNORECASE)
            for value in data_matches:
                operations.append({'type': 'tree_insert', 'value': value})
            
            # Look for function calls with values (e.g., insert(root, 25))
            func_call_matches = re.findall(r'insert\s*\([^,]*,\s*(\d+)\s*\)', text, re.IGNORECASE)
            for value in func_call_matches:
                operations.append({'type': 'tree_insert', 'value': value})
            
            # If no specific operations found, create realistic tree operations based on code
            if not operations:
                # Check if it's a typical BST example
                if any(word in text_lower for word in ['50', '30', '70', '20', '40', '60', '80']):
                    # Use common BST example values
                    operations = [
                        {'type': 'tree_insert', 'value': '50'},
                        {'type': 'tree_insert', 'value': '30'},
                        {'type': 'tree_insert', 'value': '70'},
                        {'type': 'tree_insert', 'value': '20'},
                        {'type': 'tree_insert', 'value': '40'},
                        {'type': 'tree_insert', 'value': '60'},
                        {'type': 'tree_insert', 'value': '80'}
                    ]
                else:
                    # Generic tree operations
                    operations = [
                        {'type': 'tree_insert', 'value': '10'},
                        {'type': 'tree_insert', 'value': '5'},
                        {'type': 'tree_insert', 'value': '15'},
                        {'type': 'tree_insert', 'value': '3'},
                        {'type': 'tree_insert', 'value': '7'},
                        {'type': 'tree_insert', 'value': '12'},
                        {'type': 'tree_insert', 'value': '18'}
                    ]
        
        # Linked List operations
        elif any(word in text_lower for word in ['linked list', 'linkedlist', 'list']):
            insert_matches = re.findall(r'insert\s*\(?\s*(\w+)\s*\)?', text, re.IGNORECASE)
            for value in insert_matches:
                operations.append({'type': 'list_insert', 'value': value})
            
            append_matches = re.findall(r'append\s*\(?\s*(\w+)\s*\)?', text, re.IGNORECASE)
            for value in append_matches:
                operations.append({'type': 'list_append', 'value': value})
            
            delete_matches = re.findall(r'delete\s*\(\s*\)', text, re.IGNORECASE)
            for _ in delete_matches:
                operations.append({'type': 'list_delete'})
            
            # If no specific operations found, create sample list operations
            if not operations:
                operations = [
                    {'type': 'list_insert', 'value': '10'},
                    {'type': 'list_append', 'value': '20'},
                    {'type': 'list_insert', 'value': '5'},
                    {'type': 'list_delete'}
                ]
        
        # Graph operations
        elif 'graph' in text_lower:
            # Add node operations
            node_matches = re.findall(r'add.*node\s*\(?\s*(\w+)\s*\)?', text, re.IGNORECASE)
            for node in node_matches:
                operations.append({'type': 'graph_add_node', 'node': node})
            
            # Add edge operations
            edge_matches = re.findall(r'add.*edge\s*\(?\s*(\w+)\s*,\s*(\w+)\s*\)?', text, re.IGNORECASE)
            for match in edge_matches:
                operations.append({'type': 'graph_add_edge', 'from_node': match[0], 'to_node': match[1]})
            
            # DFS/BFS operations
            if 'dfs' in text_lower or 'depth.*first' in text_lower:
                operations.append({'type': 'graph_dfs', 'node': 'A'})
            elif 'bfs' in text_lower or 'breadth.*first' in text_lower:
                operations.append({'type': 'graph_bfs', 'node': 'A'})
            
            # If no specific operations found, create sample graph operations
            if not operations:
                operations = [
                    {'type': 'graph_add_node', 'node': 'A'},
                    {'type': 'graph_add_node', 'node': 'B'},
                    {'type': 'graph_add_node', 'node': 'C'},
                    {'type': 'graph_add_edge', 'from_node': 'A', 'to_node': 'B'},
                    {'type': 'graph_add_edge', 'from_node': 'B', 'to_node': 'C'},
                    {'type': 'graph_dfs', 'node': 'A'}
                ]
        
        # Hash Table operations
        elif any(word in text_lower for word in ['hash', 'hash table', 'hashtable']):
            insert_matches = re.findall(r'insert\s*\(?\s*(\w+)\s*\)?', text, re.IGNORECASE)
            for value in insert_matches:
                operations.append({'type': 'hash_insert', 'key': value})
            
            search_matches = re.findall(r'search\s*\(?\s*(\w+)\s*\)?', text, re.IGNORECASE)
            for value in search_matches:
                operations.append({'type': 'hash_search', 'key': value})
            
            delete_matches = re.findall(r'delete\s*\(?\s*(\w+)\s*\)?', text, re.IGNORECASE)
            for value in delete_matches:
                operations.append({'type': 'hash_delete', 'key': value})
            
            # If no specific operations found, create sample hash operations
            if not operations:
                operations = [
                    {'type': 'hash_insert', 'key': 'John'},
                    {'type': 'hash_insert', 'key': 'Jane'},
                    {'type': 'hash_search', 'key': 'John'},
                    {'type': 'hash_insert', 'key': 'Bob'},
                    {'type': 'hash_delete', 'key': 'Jane'}
                ]
        
        # Array operations
        elif 'array' in text_lower:
            insert_matches = re.findall(r'insert\s*\(\s*(\d+)\s*,?\s*(\d+)?\s*\)', text, re.IGNORECASE)
            for match in insert_matches:
                operations.append({'type': 'array_insert', 'value': match[0], 'index': match[1] or '0'})
            
            append_matches = re.findall(r'append\s*\(\s*(\d+)\s*\)', text, re.IGNORECASE)
            for value in append_matches:
                operations.append({'type': 'array_append', 'value': value})
            
            delete_matches = re.findall(r'delete\s*\(\s*(\d+)?\s*\)', text, re.IGNORECASE)
            for match in delete_matches:
                operations.append({'type': 'array_delete', 'index': match or '0'})
            
            # If no specific operations found, create sample array operations
            if not operations:
                operations = [
                    {'type': 'array_append', 'value': '10'},
                    {'type': 'array_append', 'value': '20'},
                    {'type': 'array_insert', 'value': '15', 'index': '1'},
                    {'type': 'array_delete', 'index': '0'}
                ]
        
        # Enhanced fallback: Look for numbered operations or sequences
        if not operations:
            # Try to extract from numbered lists like "1. push(10)" or "- Add 5"
            numbered_operations = re.findall(r'(?:^\d+\.|\-|\*)\s*(.+)', text, re.MULTILINE | re.IGNORECASE)
            
            for op_text in numbered_operations:
                if 'stack' in text_lower or any(word in op_text.lower() for word in ['push', 'pop']):
                    # Look for push operations in numbered lists
                    push_match = re.search(r'(?:push|add|insert).*?(\d+|[A-Za-z]+)', op_text, re.IGNORECASE)
                    if push_match:
                        operations.append({'type': 'stack_push', 'value': push_match.group(1)})
                    elif re.search(r'(?:pop|remove|delete)', op_text, re.IGNORECASE):
                        operations.append({'type': 'stack_pop'})
                
                elif 'queue' in text_lower or any(word in op_text.lower() for word in ['enqueue', 'dequeue']):
                    # Look for enqueue operations in numbered lists
                    enqueue_match = re.search(r'(?:enqueue|add|insert|put).*?(\d+|[A-Za-z]+)', op_text, re.IGNORECASE)
                    if enqueue_match:
                        operations.append({'type': 'queue_enqueue', 'value': enqueue_match.group(1)})
                    elif re.search(r'(?:dequeue|remove|take)', op_text, re.IGNORECASE):
                        operations.append({'type': 'queue_dequeue'})
        
        # If still no operations found, create operations with extracted values from text
        if not operations:
            # Try to extract any numbers or values from the text
            all_values = re.findall(r'\b(\d+|[A-Z])\b', text)
            unique_values = list(dict.fromkeys(all_values))  # Remove duplicates while preserving order
            
            if unique_values and len(unique_values) >= 2:
                # Determine if it's stack or queue based on keywords
                if 'stack' in text_lower or any(word in text_lower for word in ['push', 'pop', 'lifo']):
                    operations = []
                    for i, value in enumerate(unique_values[:4]):  # Use first 4 values
                        operations.append({'type': 'stack_push', 'value': value})
                        if i == 2:  # Add a pop in the middle
                            operations.append({'type': 'stack_pop'})
                    if len(operations) > 1:
                        operations.append({'type': 'stack_pop'})
                        
                elif 'queue' in text_lower or any(word in text_lower for word in ['enqueue', 'dequeue', 'fifo']):
                    operations = []
                    for i, value in enumerate(unique_values[:4]):
                        operations.append({'type': 'queue_enqueue', 'value': value})
                        if i == 2:  # Add a dequeue in the middle
                            operations.append({'type': 'queue_dequeue'})
                    if len(operations) > 1:
                        operations.append({'type': 'queue_dequeue'})
                else:
                    # Default to stack with extracted values
                    operations = []
                    for i, value in enumerate(unique_values[:3]):
                        operations.append({'type': 'stack_push', 'value': value})
                    operations.append({'type': 'stack_pop'})
            else:
                # Final fallback with default values only if no values found in text
                if 'stack' in text_lower or any(word in text_lower for word in ['push', 'pop', 'lifo']):
                    operations = [
                        {'type': 'stack_push', 'value': '10'},
                        {'type': 'stack_push', 'value': '20'},
                        {'type': 'stack_pop'},
                        {'type': 'stack_push', 'value': '30'}
                    ]
                elif 'queue' in text_lower or any(word in text_lower for word in ['enqueue', 'dequeue', 'fifo']):
                    operations = [
                        {'type': 'queue_enqueue', 'value': 'A'},
                        {'type': 'queue_enqueue', 'value': 'B'},
                        {'type': 'queue_dequeue'},
                        {'type': 'queue_enqueue', 'value': 'C'}
                    ]
                elif any(word in text_lower for word in ['data structure', 'push', 'pop', 'insert', 'delete']):
                    # Default to stack for general data structure content
                    operations = [
                        {'type': 'stack_push', 'value': '10'},
                        {'type': 'stack_push', 'value': '20'},
                        {'type': 'stack_pop'},
                        {'type': 'stack_push', 'value': '30'}
                    ]
        
        return operations
    
    def _extract_algorithm_steps(self, text: str) -> List[Dict]:
        """Extract algorithm steps for visualization"""
        steps = []
        
        # Look for sorting algorithms
        if any(word in text.lower() for word in ['sort', 'bubble', 'merge', 'quick']):
            # Extract array elements if present
            array_pattern = r'\[([^\]]+)\]'
            arrays = re.findall(array_pattern, text)
            
            if arrays:
                # Use first array found
                elements = [x.strip() for x in arrays[0].split(',')]
                steps = [{'type': 'sort_step', 'array': elements[:], 'step': i} for i in range(len(elements))]
            else:
                # Default sorting example
                elements = ['64', '34', '25', '12', '22', '11', '90']
                steps = [{'type': 'sort_step', 'array': elements[:], 'step': i} for i in range(len(elements))]
        
        return steps
    
    def _extract_math_concepts(self, text: str) -> List[Dict]:
        """Extract mathematical concepts for visualization using enhanced analyzer"""
        try:
            from .enhanced_concept_analyzers import EnhancedMathematicsAnalyzer
            math_analyzer = EnhancedMathematicsAnalyzer()
            return math_analyzer.extract_math_concepts(text)
        except ImportError:
            # Fallback to original method
            concepts = []
            
            # Look for equations
            equations = re.findall(r'([^=]+=[^=\n]+)', text)
            for eq in equations:
                concepts.append({'type': 'equation', 'expression': eq.strip()})
            
            # Look for functions
            functions = re.findall(r'f\(x\)\s*=\s*([^\n]+)', text)
            for func in functions:
                concepts.append({'type': 'function', 'expression': func.strip()})
            
            # Look for geometric shapes
            if any(word in text.lower() for word in ['circle', 'triangle', 'rectangle', 'square']):
                concepts.append({'type': 'geometry', 'shapes': ['circle', 'triangle', 'rectangle']})
            
            return concepts
    
    def _extract_physics_concepts(self, text: str) -> List[Dict]:
        """Extract physics concepts for visualization using enhanced analyzer"""
        try:
            from .enhanced_concept_analyzers import EnhancedPhysicsAnalyzer
            physics_analyzer = EnhancedPhysicsAnalyzer()
            return physics_analyzer.extract_physics_concepts(text)
        except ImportError:
            # Fallback to original method
            concepts = []
            
            # Motion concepts
            if any(word in text.lower() for word in ['motion', 'velocity', 'acceleration']):
                concepts.append({'type': 'motion', 'concept': 'kinematic'})
            
            # Force concepts
            if any(word in text.lower() for word in ['force', 'newton', 'gravity']):
                concepts.append({'type': 'force', 'concept': 'dynamics'})
            
            return concepts
    
    def _extract_chemistry_concepts(self, text: str) -> List[Dict]:
        """Extract chemistry concepts for visualization using enhanced analyzer""" 
        try:
            from .enhanced_concept_analyzers import EnhancedChemistryAnalyzer
            chemistry_analyzer = EnhancedChemistryAnalyzer()
            return chemistry_analyzer.extract_chemistry_concepts(text)
        except ImportError:
            # Fallback method
            concepts = []
            if any(word in text.lower() for word in ['reaction', 'molecule', 'atom', 'bond']):
                concepts.append({'type': 'chemical_reaction', 'concept': 'basic'})
            return concepts
    
    def _extract_biology_concepts(self, text: str) -> List[Dict]:
        """Extract biology concepts for visualization using enhanced analyzer"""
        try:
            from .enhanced_concept_analyzers import EnhancedBiologyAnalyzer
            biology_analyzer = EnhancedBiologyAnalyzer()
            return biology_analyzer.extract_biology_concepts(text)
        except ImportError:
            # Fallback method
            concepts = []
            if any(word in text.lower() for word in ['cell', 'dna', 'organism', 'evolution']):
                concepts.append({'type': 'biological_process', 'concept': 'basic'})
            return concepts
    
    def _extract_process_steps(self, text: str) -> List[Dict]:
        """Extract business process steps"""
        steps = []
        
        # Look for numbered steps
        numbered_steps = re.findall(r'(\d+\.?\s*[^\n]+)', text)
        for i, step in enumerate(numbered_steps):
            steps.append({'type': 'process_step', 'step': step.strip(), 'order': i})
        
        return steps
    
    def _extract_general_concepts(self, text: str) -> List[Dict]:
        """Extract general concepts for basic visualization"""
        # Split into sentences for slide-based animation
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        return [{'type': 'text_slide', 'content': sentence} for sentence in sentences]


class UniversalAnimationEngine:
    """Creates animations for any type of content"""
    
    def __init__(self, width=1280, height=720, fps=30):
        self.width = width
        self.height = height
        self.fps = fps
        self.frame_duration = 1.0 / fps
    
    def create_animation(self, content_analysis: Dict, output_path: str) -> str:
        """Create appropriate animation based on content analysis"""
        content_type = content_analysis['type']
        elements = content_analysis['elements']
        
        if content_type == 'data_structures':
            return self._create_data_structure_animation(elements, output_path)
        elif content_type == 'algorithms':
            return self._create_algorithm_animation(elements, output_path)
        elif content_type == 'mathematics':
            return self._create_math_animation(elements, output_path)
        elif content_type == 'physics':
            return self._create_physics_animation(elements, output_path)
        elif content_type == 'chemistry':
            return self._create_chemistry_animation(elements, output_path)
        elif content_type == 'biology':
            return self._create_biology_animation(elements, output_path)
        elif content_type == 'business':
            return self._create_process_animation(elements, output_path)
        else:
            return self._create_general_animation(elements, output_path)
    
    def _create_data_structure_animation(self, operations: List[Dict], output_path: str) -> str:
        """Create data structure animations"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Determine structure type from operations
        if any(op['type'].startswith('stack') for op in operations):
            return self._animate_stack(operations, output_path)
        elif any(op['type'].startswith('queue') for op in operations):
            return self._animate_queue(operations, output_path)
        elif any(op['type'].startswith('array') for op in operations):
            return self._animate_array(operations, output_path)
        elif any(op['type'].startswith('tree') for op in operations):
            return self._animate_tree(operations, output_path)
        elif any(op['type'].startswith('list') for op in operations):
            return self._animate_linked_list(operations, output_path)
        elif any(op['type'].startswith('graph') for op in operations):
            return self._animate_graph(operations, output_path)
        elif any(op['type'].startswith('hash') for op in operations):
            return self._animate_hash_table(operations, output_path)
        else:
            return self._create_general_animation([{'type': 'text_slide', 'content': 'Data Structure Operations'}], output_path)
    
    def _animate_stack(self, operations: List[Dict], output_path: str) -> str:
        """Animate stack operations"""
        fig, ax = plt.subplots(figsize=(12, 8))
        stack = []
        frames = []
        
        stack_x, stack_width, element_height = 0.4, 0.2, 0.08
        
        def draw_stack_frame(step_idx, operation=None):
            ax.clear()
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            
            # Draw stack container
            container = Rectangle((stack_x, 0.1), stack_width, 0.8, 
                                fill=False, edgecolor='black', linewidth=3)
            ax.add_patch(container)
            
            # Stack title
            ax.text(0.5, 0.95, 'STACK VISUALIZATION', ha='center', va='center', 
                   fontsize=20, fontweight='bold')
            ax.text(stack_x + stack_width/2, 0.05, 'STACK', ha='center', va='center', 
                   fontsize=16, fontweight='bold')
            
            # Draw stack elements
            for i, element in enumerate(stack):
                y_pos = 0.1 + i * element_height
                rect = Rectangle((stack_x + 0.01, y_pos), stack_width - 0.02, element_height - 0.01,
                               facecolor='lightblue', edgecolor='blue', linewidth=2)
                ax.add_patch(rect)
                ax.text(stack_x + stack_width/2, y_pos + element_height/2, str(element),
                       ha='center', va='center', fontsize=14, fontweight='bold')
            
            # Show operation
            if operation:
                op_text = f"Operation: {operation['type'].replace('stack_', '').upper()}"
                if 'value' in operation:
                    op_text += f"({operation['value']})"
                ax.text(0.1, 0.9, op_text, fontsize=16, fontweight='bold', 
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow"))
            
            # Show stack state
            stack_content = ' → '.join(map(str, stack)) if stack else 'Empty'
            ax.text(0.1, 0.85, f'Stack: [{stack_content}]', fontsize=14)
            ax.text(0.1, 0.8, f'Size: {len(stack)}', fontsize=14)
        
        # Generate animation frames
        frame_count = 0
        
        # Initial frame
        draw_stack_frame(0)
        plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
        frame_count += 1
        
        for i, operation in enumerate(operations):
            # Show operation about to happen
            draw_stack_frame(i, operation)
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
            frame_count += 1
            
            # Execute operation
            if operation['type'] == 'stack_push':
                stack.append(operation['value'])
            elif operation['type'] == 'stack_pop' and stack:
                stack.pop()
            
            # Show result
            draw_stack_frame(i)
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
            frame_count += 1
            
            # Hold frame
            for _ in range(60):  # 2 seconds at 30fps
                plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
                frame_count += 1
        
        plt.close()
        
        # Convert frames to video
        self._frames_to_video(frame_count, output_path)
        return output_path
    
    def _animate_queue(self, operations: List[Dict], output_path: str) -> str:
        """Animate queue operations"""
        fig, ax = plt.subplots(figsize=(12, 8))
        queue = []
        
        queue_y, queue_height, element_width = 0.4, 0.2, 0.08
        queue_start_x = 0.2
        
        def draw_queue_frame(operation=None):
            ax.clear()
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            
            # Title
            ax.text(0.5, 0.95, 'QUEUE VISUALIZATION', ha='center', va='center', 
                   fontsize=20, fontweight='bold')
            
            # Draw queue container
            container = Rectangle((queue_start_x, queue_y), 0.6, queue_height,
                                fill=False, edgecolor='black', linewidth=3)
            ax.add_patch(container)
            
            # Labels
            ax.text(queue_start_x - 0.05, queue_y + queue_height/2, 'REAR', 
                   ha='center', va='center', fontsize=12, fontweight='bold', rotation=90)
            ax.text(queue_start_x + 0.65, queue_y + queue_height/2, 'FRONT', 
                   ha='center', va='center', fontsize=12, fontweight='bold', rotation=90)
            
            # Draw elements
            for i, element in enumerate(queue):
                x_pos = queue_start_x + 0.01 + i * element_width
                rect = Rectangle((x_pos, queue_y + 0.01), element_width - 0.01, queue_height - 0.02,
                               facecolor='lightgreen', edgecolor='green', linewidth=2)
                ax.add_patch(rect)
                ax.text(x_pos + element_width/2, queue_y + queue_height/2, str(element),
                       ha='center', va='center', fontsize=12, fontweight='bold')
            
            # Show operation
            if operation:
                op_text = f"Operation: {operation['type'].replace('queue_', '').upper()}"
                if 'value' in operation:
                    op_text += f"({operation['value']})"
                ax.text(0.1, 0.9, op_text, fontsize=16, fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"))
            
            # Show queue state
            queue_content = ' → '.join(map(str, queue)) if queue else 'Empty'
            ax.text(0.1, 0.85, f'Queue: [{queue_content}]', fontsize=14)
            ax.text(0.1, 0.8, f'Size: {len(queue)}', fontsize=14)
        
        frame_count = 0
        
        # Initial frame
        draw_queue_frame()
        plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
        frame_count += 1
        
        for operation in operations:
            # Show operation
            draw_queue_frame(operation)
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
            frame_count += 1
            
            # Execute operation
            if operation['type'] == 'queue_enqueue':
                queue.append(operation['value'])
            elif operation['type'] == 'queue_dequeue' and queue:
                queue.pop(0)
            
            # Show result
            draw_queue_frame()
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
            frame_count += 1
            
            # Hold frame
            for _ in range(60):
                plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
                frame_count += 1
        
        plt.close()
        self._frames_to_video(frame_count, output_path)
        return output_path
    
    def _animate_array(self, operations: List[Dict], output_path: str) -> str:
        """Animate array operations"""
        fig, ax = plt.subplots(figsize=(12, 8))
        array = []
        max_size = 10
        
        def draw_array_frame(operation=None):
            ax.clear()
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            
            # Title
            ax.text(0.5, 0.95, 'ARRAY VISUALIZATION', ha='center', va='center', 
                   fontsize=20, fontweight='bold')
            
            # Draw array container
            array_y, array_height, element_width = 0.4, 0.2, 0.06
            array_start_x = 0.1
            
            # Draw array cells
            for i in range(max_size):
                x_pos = array_start_x + i * element_width
                rect = Rectangle((x_pos, array_y), element_width, array_height,
                               fill=False, edgecolor='black', linewidth=2)
                ax.add_patch(rect)
                
                # Index labels
                ax.text(x_pos + element_width/2, array_y - 0.05, str(i),
                       ha='center', va='center', fontsize=10)
                
                # Array elements
                if i < len(array):
                    # Filled cell
                    filled_rect = Rectangle((x_pos + 0.002, array_y + 0.002), 
                                          element_width - 0.004, array_height - 0.004,
                                          facecolor='lightblue', edgecolor='blue')
                    ax.add_patch(filled_rect)
                    ax.text(x_pos + element_width/2, array_y + array_height/2, str(array[i]),
                           ha='center', va='center', fontsize=12, fontweight='bold')
            
            # Show operation
            if operation:
                op_text = f"Operation: {operation['type'].replace('array_', '').upper()}"
                if 'value' in operation:
                    op_text += f"({operation['value']}"
                    if 'index' in operation:
                        op_text += f", {operation['index']}"
                    op_text += ")"
                ax.text(0.1, 0.9, op_text, fontsize=16, fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
            
            # Show array state
            array_content = ', '.join(map(str, array)) if array else 'Empty'
            ax.text(0.1, 0.85, f'Array: [{array_content}]', fontsize=14)
            ax.text(0.1, 0.8, f'Size: {len(array)}/{max_size}', fontsize=14)
        
        # Generate animation frames
        frame_count = 0
        
        # Initial frame
        draw_array_frame()
        plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
        frame_count += 1
        
        for i, operation in enumerate(operations):
            # Show operation about to happen
            draw_array_frame(operation)
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
            frame_count += 1
            
            # Execute operation
            if operation['type'] == 'array_insert':
                value = operation['value']
                index = int(operation.get('index', len(array)))
                if index <= len(array) and len(array) < max_size:
                    array.insert(index, value)
            elif operation['type'] == 'array_delete':
                index = int(operation.get('index', len(array) - 1))
                if 0 <= index < len(array):
                    array.pop(index)
            elif operation['type'] == 'array_append' and len(array) < max_size:
                array.append(operation['value'])
            
            # Show result
            draw_array_frame()
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
            frame_count += 1
            
            # Hold frame
            for _ in range(60):  # 2 seconds at 30fps
                plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
                frame_count += 1
        
        plt.close()
        self._frames_to_video(frame_count, output_path)
        return output_path
    
    def _animate_tree(self, operations: List[Dict], output_path: str) -> str:
        """Animate binary tree operations with proper tree structure visualization"""
        fig, ax = plt.subplots(figsize=(14, 10))
        
        class TreeNode:
            def __init__(self, value):
                self.value = value
                self.left = None
                self.right = None
                self.x = 0
                self.y = 0
                self.level = 0
        
        root = None
        
        def insert_node(root, value):
            if root is None:
                return TreeNode(value)
            if int(value) < int(root.value):
                root.left = insert_node(root.left, value)
            else:
                root.right = insert_node(root.right, value)
            return root
        
        def calculate_tree_layout(node, level=0):
            """Calculate proper tree layout with levels"""
            if node is None:
                return []
            
            nodes_at_level = []
            node.level = level
            nodes_at_level.append(node)
            
            # Get all nodes at each level
            if node.left:
                nodes_at_level.extend(calculate_tree_layout(node.left, level + 1))
            if node.right:
                nodes_at_level.extend(calculate_tree_layout(node.right, level + 1))
            
            return nodes_at_level
        
        def position_nodes(node, x_min, x_max, y):
            """Position nodes with proper spacing"""
            if node is None:
                return
            
            # Position current node at center of available space
            node.x = (x_min + x_max) / 2
            node.y = y
            
            # Calculate space for children
            mid = (x_min + x_max) / 2
            
            # Position left subtree
            if node.left:
                position_nodes(node.left, x_min, mid, y - 0.15)
            
            # Position right subtree  
            if node.right:
                position_nodes(node.right, mid, x_max, y - 0.15)
        
        def draw_tree_frame(operation=None, highlight_node=None, step_info=""):
            ax.clear()
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            
            # Title
            ax.text(0.5, 0.95, 'BINARY SEARCH TREE VISUALIZATION', ha='center', va='center', 
                   fontsize=18, fontweight='bold', color='darkblue')
            
            if root:
                # Position all nodes properly
                position_nodes(root, 0.1, 0.9, 0.8)
                
                # First draw all edges
                def draw_edges(node):
                    if node is None:
                        return
                    
                    if node.left:
                        # Draw edge to left child
                        ax.plot([node.x, node.left.x], [node.y, node.left.y], 
                               'darkblue', linewidth=3, alpha=0.7)
                        draw_edges(node.left)
                    
                    if node.right:
                        # Draw edge to right child
                        ax.plot([node.x, node.right.x], [node.y, node.right.y], 
                               'darkblue', linewidth=3, alpha=0.7)
                        draw_edges(node.right)
                
                # Then draw all nodes
                def draw_nodes(node):
                    if node is None:
                        return
                    
                    # Determine node color
                    if highlight_node == int(node.value):
                        color = 'gold'
                        edge_color = 'orange'
                        text_color = 'darkred'
                    else:
                        color = 'lightblue'
                        edge_color = 'darkblue'
                        text_color = 'darkblue'
                    
                    # Draw node circle
                    circle = Circle((node.x, node.y), 0.04, facecolor=color, 
                                  edgecolor=edge_color, linewidth=3)
                    ax.add_patch(circle)
                    
                    # Draw node value
                    ax.text(node.x, node.y, str(node.value), ha='center', va='center', 
                           fontsize=14, fontweight='bold', color=text_color)
                    
                    # Draw level indicator
                    ax.text(node.x, node.y - 0.07, f'L{node.level}', ha='center', va='center', 
                           fontsize=8, color='gray', style='italic')
                    
                    # Recursively draw children
                    draw_nodes(node.left)
                    draw_nodes(node.right)
                
                draw_edges(root)
                draw_nodes(root)
                
                # Show tree properties
                def count_nodes(node):
                    if node is None:
                        return 0
                    return 1 + count_nodes(node.left) + count_nodes(node.right)
                
                def tree_height(node):
                    if node is None:
                        return 0
                    return 1 + max(tree_height(node.left), tree_height(node.right))
                
                node_count = count_nodes(root)
                height = tree_height(root)
                
                # Display tree statistics
                ax.text(0.02, 0.15, 'Tree Properties:', fontsize=12, fontweight='bold')
                ax.text(0.02, 0.12, f'• Nodes: {node_count}', fontsize=10)
                ax.text(0.02, 0.09, f'• Height: {height}', fontsize=10)
                ax.text(0.02, 0.06, f'• Root: {root.value}', fontsize=10)
                
                # Show tree traversal info
                def inorder_traversal(node, result):
                    if node:
                        inorder_traversal(node.left, result)
                        result.append(node.value)
                        inorder_traversal(node.right, result)
                
                inorder_result = []
                inorder_traversal(root, inorder_result)
                
                ax.text(0.02, 0.02, f'Inorder: {" → ".join(str(x) for x in inorder_result)}', fontsize=9, 
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow"))
                
            else:
                # Empty tree visualization
                ax.text(0.5, 0.5, 'Empty Binary Tree', ha='center', va='center', 
                       fontsize=20, style='italic', color='gray')
                ax.text(0.5, 0.45, 'Ready for insertions...', ha='center', va='center', 
                       fontsize=14, color='gray')
            
            # Show current operation
            if operation:
                op_text = f"Operation: {operation['type'].replace('tree_', '').upper()}"
                if 'value' in operation:
                    op_text += f" ({operation['value']})"
                
                ax.text(0.5, 0.88, op_text, ha='center', va='center', fontsize=16, 
                       fontweight='bold', bbox=dict(boxstyle="round,pad=0.5", 
                       facecolor="lightgreen", edgecolor="green"))
            
            # Show step information
            if step_info:
                ax.text(0.98, 0.15, step_info, ha='right', va='top', fontsize=10,
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcyan"))
        
        # Generate animation frames
        frame_count = 0
        
        # Initial frame - empty tree
        draw_tree_frame(step_info="Starting with empty tree")
        plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=120, bbox_inches='tight')
        frame_count += 1
        
        # Hold initial frame
        for _ in range(30):  # 1 second at 30fps
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=120, bbox_inches='tight')
            frame_count += 1
        
        for i, operation in enumerate(operations):
            if operation['type'] == 'tree_insert':
                value = operation['value']
                
                # Show operation about to happen
                step_info = f"Step {i+1}: Inserting {value}"
                draw_tree_frame(operation, step_info=step_info)
                plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=120, bbox_inches='tight')
                frame_count += 1
                
                # Hold before insertion
                for _ in range(45):  # 1.5 seconds
                    plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=120, bbox_inches='tight')
                    frame_count += 1
                
                # Execute insertion
                root = insert_node(root, value)
                
                # Show result with highlighted new node
                step_info = f"✓ Inserted {value} successfully"
                draw_tree_frame(highlight_node=int(value), step_info=step_info)
                plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=120, bbox_inches='tight')
                frame_count += 1
                
                # Hold after insertion
                for _ in range(60):  # 2 seconds
                    plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=120, bbox_inches='tight')
                    frame_count += 1
        
        # Final frame showing complete tree
        draw_tree_frame(step_info="Binary Search Tree Complete!")
        for _ in range(90):  # 3 seconds final view
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=120, bbox_inches='tight')
            frame_count += 1
        
        plt.close()
        self._frames_to_video(frame_count, output_path)
        return output_path
    
    def _animate_linked_list(self, operations: List[Dict], output_path: str) -> str:
        """Animate linked list operations with enhanced node structure visualization"""
        fig, ax = plt.subplots(figsize=(14, 8))
        
        class ListNode:
            def __init__(self, value):
                self.value = value
                self.next = None
                self.x = 0
                self.y = 0
        
        head = None
        
        def draw_linked_list_frame(operation=None, highlight_value=None, step_info=""):
            ax.clear()
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            
            # Title
            ax.text(0.5, 0.95, 'LINKED LIST VISUALIZATION', ha='center', va='center', 
                   fontsize=18, fontweight='bold', color='darkgreen')
            
            # Draw linked list
            if head:
                current = head
                x_start = 0.05
                node_width = 0.12
                node_height = 0.08
                y_pos = 0.5
                pointer_width = 0.04
                
                x_pos = x_start
                node_count = 0
                
                # Count total nodes for positioning
                total_nodes = 0
                temp = head
                while temp and total_nodes < 8:  # Limit to 8 nodes for display
                    total_nodes += 1
                    temp = temp.next
                
                while current and node_count < total_nodes:
                    current.x = x_pos
                    current.y = y_pos
                    
                    # Draw node container with data and pointer sections
                    # Data section
                    data_rect = Rectangle((x_pos, y_pos), node_width * 0.7, node_height,
                                        facecolor='lightblue' if highlight_value != current.value else 'gold',
                                        edgecolor='darkblue', linewidth=2)
                    ax.add_patch(data_rect)
                    
                    # Pointer section
                    pointer_rect = Rectangle((x_pos + node_width * 0.7, y_pos), node_width * 0.3, node_height,
                                           facecolor='lightgray', edgecolor='darkblue', linewidth=2)
                    ax.add_patch(pointer_rect)
                    
                    # Node value in data section
                    ax.text(x_pos + node_width * 0.35, y_pos + node_height/2, str(current.value),
                           ha='center', va='center', fontsize=12, fontweight='bold', color='darkblue')
                    
                    # Node address label
                    ax.text(x_pos + node_width/2, y_pos - 0.03, f'Node{node_count+1}',
                           ha='center', va='center', fontsize=8, color='gray', style='italic')
                    
                    # Draw pointer arrow
                    if current.next:
                        # Pointer symbol in pointer section
                        ax.text(x_pos + node_width * 0.85, y_pos + node_height/2, '→',
                               ha='center', va='center', fontsize=14, fontweight='bold', color='red')
                        
                        # Arrow to next node
                        arrow_start_x = x_pos + node_width
                        arrow_end_x = x_pos + node_width + 0.02
                        ax.annotate('', xy=(arrow_end_x, y_pos + node_height/2),
                                  xytext=(arrow_start_x, y_pos + node_height/2),
                                  arrowprops=dict(arrowstyle='->', lw=3, color='red'))
                    else:
                        # NULL pointer
                        ax.text(x_pos + node_width * 0.85, y_pos + node_height/2, '∅',
                               ha='center', va='center', fontsize=14, fontweight='bold', color='red')
                        
                        # NULL label
                        ax.text(x_pos + node_width + 0.02, y_pos + node_height/2, 'NULL',
                               ha='left', va='center', fontsize=10, style='italic', color='red')
                    
                    current = current.next
                    x_pos += node_width + 0.03
                    node_count += 1
                
                # Draw HEAD pointer
                if head:
                    ax.text(0.02, 0.7, 'HEAD', ha='center', va='center', fontsize=14, 
                           fontweight='bold', color='darkgreen',
                           bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"))
                    ax.annotate('', xy=(head.x, head.y + node_height + 0.02),
                              xytext=(0.02, 0.65),
                              arrowprops=dict(arrowstyle='->', lw=2, color='darkgreen'))
                
                # Show list traversal info
                values = []
                temp = head
                while temp and len(values) < 8:
                    values.append(str(temp.value))
                    temp = temp.next
                
                traversal_text = " → ".join(values)
                if temp:  # More nodes exist
                    traversal_text += " → ..."
                
                ax.text(0.02, 0.15, 'Traversal:', fontsize=12, fontweight='bold')
                ax.text(0.02, 0.12, traversal_text, fontsize=10,
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow"))
                
            else:
                # Empty list visualization
                ax.text(0.5, 0.5, 'Empty Linked List', ha='center', va='center', 
                       fontsize=20, style='italic', color='gray')
                ax.text(0.5, 0.45, 'HEAD → NULL', ha='center', va='center', 
                       fontsize=16, color='gray')
                
                # Draw empty HEAD pointer
                ax.text(0.02, 0.7, 'HEAD', ha='center', va='center', fontsize=14, 
                       fontweight='bold', color='gray',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
                ax.text(0.02, 0.65, '↓', ha='center', va='center', fontsize=16, color='gray')
                ax.text(0.02, 0.6, 'NULL', ha='center', va='center', fontsize=12, 
                       style='italic', color='gray')
            
            # Show current operation
            if operation:
                op_text = f"Operation: {operation['type'].replace('list_', '').upper()}"
                if 'value' in operation:
                    op_text += f" ({operation['value']})"
                
                ax.text(0.5, 0.88, op_text, ha='center', va='center', fontsize=16, 
                       fontweight='bold', bbox=dict(boxstyle="round,pad=0.5", 
                       facecolor="lightcyan", edgecolor="darkblue"))
            
            # Show step information
            if step_info:
                ax.text(0.98, 0.15, step_info, ha='right', va='top', fontsize=10,
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"))
            
            # Show list properties
            size = 0
            current = head
            while current:
                size += 1
                current = current.next
            
            ax.text(0.02, 0.25, 'List Properties:', fontsize=12, fontweight='bold')
            ax.text(0.02, 0.22, f'• Size: {size} nodes', fontsize=10)
            ax.text(0.02, 0.19, f'• Type: Singly Linked', fontsize=10)
        
        # Generate animation frames
        frame_count = 0
        
        # Initial frame - empty list
        draw_linked_list_frame(step_info="Starting with empty list")
        plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=120, bbox_inches='tight')
        frame_count += 1
        
        # Hold initial frame
        for _ in range(30):  # 1 second
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=120, bbox_inches='tight')
            frame_count += 1
        
        for i, operation in enumerate(operations):
            # Show operation about to happen
            step_info = f"Step {i+1}: {operation['type'].replace('list_', '').title()}"
            if 'value' in operation:
                step_info += f" value {operation['value']}"
            
            draw_linked_list_frame(operation, step_info=step_info)
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=120, bbox_inches='tight')
            frame_count += 1
            
            # Hold before operation
            for _ in range(45):  # 1.5 seconds
                plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=120, bbox_inches='tight')
                frame_count += 1
            
            # Execute operation
            if operation['type'] == 'list_insert':
                value = operation['value']
                new_node = ListNode(value)
                
                if head is None:
                    head = new_node
                else:
                    # Insert at beginning for simplicity
                    new_node.next = head
                    head = new_node
                
                # Show result with highlighted node
                step_info = f"✓ Inserted {value} at head"
                draw_linked_list_frame(highlight_value=value, step_info=step_info)
                
            elif operation['type'] == 'list_delete' and head:
                deleted_value = head.value
                head = head.next
                step_info = f"✓ Deleted {deleted_value} from head"
                draw_linked_list_frame(step_info=step_info)
                
            elif operation['type'] == 'list_append':
                value = operation['value']
                new_node = ListNode(value)
                
                if head is None:
                    head = new_node
                else:
                    current = head
                    while current.next:
                        current = current.next
                    current.next = new_node
                
                step_info = f"✓ Appended {value} to tail"
                draw_linked_list_frame(highlight_value=value, step_info=step_info)
            else:
                draw_linked_list_frame()
                
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=120, bbox_inches='tight')
            frame_count += 1
            
            # Hold after operation
            for _ in range(60):  # 2 seconds
                plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=120, bbox_inches='tight')
                frame_count += 1
        
        # Final frame
        draw_linked_list_frame(step_info="Linked List Complete!")
        for _ in range(90):  # 3 seconds final view
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=120, bbox_inches='tight')
            frame_count += 1
        
        plt.close()
        self._frames_to_video(frame_count, output_path)
        return output_path
    
    def _animate_graph(self, operations: List[Dict], output_path: str) -> str:
        """Animate graph operations with enhanced network topology visualization"""
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Graph structure with adjacency list
        nodes = {}
        adjacency = {}
        edge_weights = {}
        visited_order = []
        
        def hash_string_to_color(s):
            """Generate consistent color from string"""
            hash_val = hash(s) % 7
            colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow', 
                     'lightpink', 'lightcyan', 'wheat']
            return colors[hash_val]
        
        def draw_graph_frame(operation=None, highlight_node=None, visited_nodes=None, step_info=""):
            ax.clear()
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            
            # Title
            ax.text(0.5, 0.95, 'GRAPH NETWORK VISUALIZATION', ha='center', va='center', 
                   fontsize=18, fontweight='bold', color='darkred')
            
            if not nodes:
                ax.text(0.5, 0.5, 'Empty Graph Network', ha='center', va='center', 
                       fontsize=20, style='italic', color='gray')
                ax.text(0.5, 0.45, 'No vertices or edges', ha='center', va='center', 
                       fontsize=14, color='gray')
                
                # Show graph properties for empty state
                ax.text(0.02, 0.2, 'Graph Properties:', fontsize=12, fontweight='bold')
                ax.text(0.02, 0.17, '• Vertices: 0', fontsize=10)
                ax.text(0.02, 0.14, '• Edges: 0', fontsize=10)
                ax.text(0.02, 0.11, '• Type: Undirected', fontsize=10)
                ax.text(0.02, 0.08, '• Connected: N/A', fontsize=10)
                return
            
            # Calculate better node positions using force-directed layout
            if len(nodes) == 1:
                # Single node at center
                for node in nodes:
                    nodes[node] = (0.5, 0.5)
            elif len(nodes) <= 6:
                # Arrange in circle for small graphs
                for i, node in enumerate(nodes.keys()):
                    angle = i * (2 * math.pi / len(nodes))
                    x = 0.5 + 0.25 * math.cos(angle)
                    y = 0.5 + 0.25 * math.sin(angle)
                    nodes[node] = (x, y)
            else:
                # Grid layout for larger graphs
                grid_size = math.ceil(math.sqrt(len(nodes)))
                for i, node in enumerate(nodes.keys()):
                    row = i // grid_size
                    col = i % grid_size
                    x = 0.2 + (col * 0.6 / (grid_size - 1)) if grid_size > 1 else 0.5
                    y = 0.3 + (row * 0.4 / (grid_size - 1)) if grid_size > 1 else 0.5
                    nodes[node] = (x, y)
            
            # Draw edges with weights and direction indicators
            total_edges = 0
            for node1 in adjacency:
                for node2 in adjacency[node1]:
                    if node1 in nodes and node2 in nodes:
                        x1, y1 = nodes[node1]
                        x2, y2 = nodes[node2]
                        
                        # Edge color based on whether it's being traversed
                        edge_color = 'red' if (visited_nodes and node1 in visited_nodes and 
                                             node2 in visited_nodes) else 'darkblue'
                        edge_width = 3 if edge_color == 'red' else 2
                        
                        # Draw edge line
                        ax.plot([x1, x2], [y1, y2], color=edge_color, 
                               linewidth=edge_width, alpha=0.8)
                        
                        # Draw directional arrow (for directed graphs)
                        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                        dx, dy = x2 - x1, y2 - y1
                        length = math.sqrt(dx*dx + dy*dy)
                        if length > 0:
                            # Normalize direction
                            dx_norm, dy_norm = dx/length, dy/length
                            arrow_x = mid_x + 0.01 * dx_norm
                            arrow_y = mid_y + 0.01 * dy_norm
                            
                            ax.annotate('', xy=(arrow_x, arrow_y),
                                      xytext=(mid_x, mid_y),
                                      arrowprops=dict(arrowstyle='->', 
                                                    lw=2, color=edge_color))
                        
                        # Show edge weight if available
                        edge_key = f"{node1}-{node2}"
                        if edge_key in edge_weights:
                            weight = edge_weights[edge_key]
                            ax.text(mid_x, mid_y + 0.02, str(weight), 
                                   ha='center', va='bottom', fontsize=9, 
                                   bbox=dict(boxstyle="round,pad=0.2", 
                                           facecolor="white", alpha=0.8))
                        
                        total_edges += 1
            
            # Draw nodes with enhanced styling
            for node, (x, y) in nodes.items():
                # Node color based on state
                if visited_nodes and node in visited_nodes:
                    if len(visited_order) > 0 and node == visited_order[-1]:
                        color = 'gold'  # Currently visiting
                    else:
                        color = 'lightgreen'  # Already visited
                elif highlight_node == node:
                    color = 'orange'  # About to visit
                else:
                    color = hash_string_to_color(str(node))
                
                # Draw node circle with border
                circle = Circle((x, y), 0.035, facecolor=color, 
                              edgecolor='darkblue', linewidth=3)
                ax.add_patch(circle)
                
                # Node label
                ax.text(x, y, str(node), ha='center', va='center', 
                       fontsize=11, fontweight='bold', color='darkblue')
                
                # Node degree (number of connections)
                degree = len(adjacency.get(node, []))
                ax.text(x, y - 0.06, f'deg:{degree}', ha='center', va='center', 
                       fontsize=8, style='italic', color='gray')
            
            # Show traversal path
            if len(visited_order) > 1:
                path_text = " → ".join(str(n) for n in visited_order[-8:])  # Last 8 nodes
                if len(visited_order) > 8:
                    path_text = "..." + path_text
                ax.text(0.5, 0.05, f'Traversal Path: {path_text}', 
                       ha='center', va='center', fontsize=10,
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow"))
            
            # Show current operation
            if operation:
                op_text = f"Operation: {operation['type'].replace('graph_', '').upper()}"
                if 'from_node' in operation and 'to_node' in operation:
                    op_text += f" ({operation['from_node']} → {operation['to_node']})"
                elif 'node' in operation:
                    op_text += f" (vertex {operation['node']})"
                if 'weight' in operation:
                    op_text += f" [weight: {operation['weight']}]"
                
                ax.text(0.5, 0.88, op_text, ha='center', va='center', fontsize=16, 
                       fontweight='bold', bbox=dict(boxstyle="round,pad=0.5", 
                       facecolor="lightcyan", edgecolor="darkblue"))
            
            # Show step information
            if step_info:
                ax.text(0.98, 0.88, step_info, ha='right', va='top', fontsize=10,
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"))
            
            # Show graph properties
            ax.text(0.02, 0.25, 'Graph Properties:', fontsize=12, fontweight='bold')
            ax.text(0.02, 0.22, f'• Vertices: {len(nodes)}', fontsize=10)
            ax.text(0.02, 0.19, f'• Edges: {total_edges}', fontsize=10)
            ax.text(0.02, 0.16, f'• Type: Directed', fontsize=10)
            
            # Check if graph is connected (simplified)
            is_connected = len(nodes) <= 1 or len(adjacency) == len(nodes)
            ax.text(0.02, 0.13, f'• Connected: {"Yes" if is_connected else "Unknown"}', fontsize=10)
            
            # Show adjacency list (partial)
            adj_text = "Adjacency List:"
            shown_nodes = 0
            for node in sorted(adjacency.keys()):
                if shown_nodes >= 4:  # Limit display
                    adj_text += "\n  ..."
                    break
                neighbors = sorted(adjacency[node])
                adj_text += f"\n  {node}: {neighbors}"
                shown_nodes += 1
            
            if adjacency:
                ax.text(0.98, 0.25, adj_text, ha='right', va='top', fontsize=9,
                       bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
        
        # Generate animation frames
        frame_count = 0
        
        # Initial frame - empty graph
        draw_graph_frame(step_info="Starting with empty graph")
        plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=120, bbox_inches='tight')
        frame_count += 1
        
        # Hold initial frame
        for _ in range(30):  # 1 second
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=120, bbox_inches='tight')
            frame_count += 1
        
        for i, operation in enumerate(operations):
            # Show operation about to happen
            step_info = f"Step {i+1}: {operation['type'].replace('graph_', '').title()}"
            
            draw_graph_frame(operation, step_info=step_info)
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=120, bbox_inches='tight')
            frame_count += 1
            
            # Hold before operation
            for _ in range(45):  # 1.5 seconds
                plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=120, bbox_inches='tight')
                frame_count += 1
            
            # Execute operation
            if operation['type'] == 'graph_add_node':
                node = operation['node']
                nodes[node] = (0.5, 0.5)  # Initial position, will be recalculated
                if node not in adjacency:
                    adjacency[node] = []
                
                step_info = f"✓ Added vertex {node}"
                draw_graph_frame(highlight_node=node, step_info=step_info)
                
            elif operation['type'] == 'graph_add_edge':
                from_node = operation['from_node']
                to_node = operation['to_node']
                weight = operation.get('weight', 1)
                
                # Add nodes if they don't exist
                for node in [from_node, to_node]:
                    if node not in nodes:
                        nodes[node] = (0.5, 0.5)
                    if node not in adjacency:
                        adjacency[node] = []
                
                # Add edge
                if to_node not in adjacency[from_node]:
                    adjacency[from_node].append(to_node)
                
                edge_key = f"{from_node}-{to_node}"
                edge_weights[edge_key] = weight
                
                step_info = f"✓ Added edge {from_node} → {to_node}"
                if weight != 1:
                    step_info += f" (weight: {weight})"
                draw_graph_frame(step_info=step_info)
                
            elif operation['type'] in ['graph_dfs', 'graph_bfs']:
                start_node = operation.get('node', list(nodes.keys())[0] if nodes else None)
                if start_node and start_node not in visited_order:
                    visited_order.append(start_node)
                    
                    # Simulate visiting connected nodes
                    if start_node in adjacency:
                        for neighbor in adjacency[start_node][:2]:  # Visit up to 2 neighbors
                            if neighbor not in visited_order:
                                visited_order.append(neighbor)
                
                step_info = f"✓ {operation['type'].replace('graph_', '').upper()} from {start_node}"
                draw_graph_frame(highlight_node=start_node, 
                               visited_nodes=set(visited_order), step_info=step_info)
            else:
                draw_graph_frame()
                
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=120, bbox_inches='tight')
            frame_count += 1
            
            # Hold after operation
            for _ in range(60):  # 2 seconds
                plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=120, bbox_inches='tight')
                frame_count += 1
        
        # Final frame
        draw_graph_frame(step_info="Graph Network Complete!")
        for _ in range(90):  # 3 seconds final view
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=120, bbox_inches='tight')
            frame_count += 1
        
        plt.close()
        self._frames_to_video(frame_count, output_path)
        return output_path
    
    def _animate_hash_table(self, operations: List[Dict], output_path: str) -> str:
        """Animate hash table operations with enhanced bucket visualization"""
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Hash table with chaining for collision resolution
        table_size = 7
        hash_table = [[] for _ in range(table_size)]  # Each slot is a list (chain)
        collision_count = 0
        
        def hash_function(key):
            """Enhanced hash function with visualization"""
            return hash(str(key)) % table_size
        
        def draw_hash_table_frame(operation=None, highlight_index=None, step_info=""):
            ax.clear()
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            
            # Title
            ax.text(0.5, 0.95, 'HASH TABLE VISUALIZATION', ha='center', va='center', 
                   fontsize=18, fontweight='bold', color='darkmagenta')
            
            # Draw hash table structure - CENTERED LAYOUT
            table_start_y = 0.72
            cell_height = 0.08
            cell_width = 0.18
            # Center the table horizontally
            total_table_width = 0.08 + cell_width  # index column + bucket column
            table_x = 0.5 - (total_table_width / 2) + 0.08  # Center and offset for index column
            
            # Hash table properties display
            total_elements = sum(len(chain) for chain in hash_table)
            load_factor = total_elements / table_size
            
            # Draw table header - CENTERED
            header_y = table_start_y + 0.06
            ax.text(table_x - 0.04, header_y, 'INDEX', ha='center', va='center', 
                   fontsize=14, fontweight='bold', color='darkblue',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcyan"))
            ax.text(table_x + cell_width/2, header_y, 'HASH BUCKET (CHAIN)', ha='center', va='center', 
                   fontsize=14, fontweight='bold', color='darkblue',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcyan"))
            
            # Draw each hash table slot with chaining - CENTERED
            for i in range(table_size):
                y_pos = table_start_y - (i * (cell_height + 0.015))
                
                # Index column - better spacing
                index_color = 'gold' if highlight_index == i else 'lightgray'
                rect_idx = Rectangle((table_x - 0.08, y_pos), 0.06, cell_height,
                                   facecolor=index_color, edgecolor='darkblue', linewidth=2)
                ax.add_patch(rect_idx)
                ax.text(table_x - 0.05, y_pos + cell_height/2, str(i),
                       ha='center', va='center', fontsize=14, fontweight='bold', color='darkblue')
                
                # Hash value indicator (hash bucket) - wider for better visibility
                bucket_color = 'yellow' if highlight_index == i else ('lightgreen' if hash_table[i] else 'white')
                rect_bucket = Rectangle((table_x, y_pos), cell_width, cell_height,
                                      facecolor=bucket_color, edgecolor='darkblue', linewidth=2)
                ax.add_patch(rect_bucket)
                
                # Draw chain elements with better formatting
                if hash_table[i]:
                    # Show chained elements
                    chain_text = " → ".join(str(elem) for elem in hash_table[i])
                    if len(chain_text) > 20:  # Adjust for wider cells
                        chain_text = chain_text[:17] + "..."
                    
                    ax.text(table_x + cell_width/2, y_pos + cell_height/2, chain_text,
                           ha='center', va='center', fontsize=11, fontweight='bold', color='darkgreen')
                    
                    # Show collision indicator if chain has multiple elements
                    if len(hash_table[i]) > 1:
                        ax.text(table_x + cell_width + 0.02, y_pos + cell_height/2, 
                               f'[{len(hash_table[i])} items]', ha='left', va='center', 
                               fontsize=10, color='red', fontweight='bold')
                else:
                    ax.text(table_x + cell_width/2, y_pos + cell_height/2, 'NULL',
                           ha='center', va='center', fontsize=11, style='italic', color='gray')
                
                # Show hash calculation for highlighted index - repositioned
                if operation and 'key' in operation and highlight_index == i:
                    key = operation['key']
                    hash_val = hash_function(key)
                    ax.text(table_x + cell_width + 0.08, y_pos + cell_height/2, 
                           f'hash({key}) = {hash_val}', ha='left', va='center', 
                           fontsize=10, bbox=dict(boxstyle="round,pad=0.2", facecolor="lightyellow"))
            
            # Show hash function details - LEFT SIDE
            ax.text(0.02, 0.40, 'Hash Function:', fontsize=12, fontweight='bold', color='darkred')
            ax.text(0.02, 0.37, 'h(key) = key % 7', fontsize=11, 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcyan"))
            ax.text(0.02, 0.33, 'Collision Resolution:', fontsize=12, fontweight='bold', color='darkred')
            ax.text(0.02, 0.30, 'Separate Chaining', fontsize=11,
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcyan"))
            
            # Show statistics - LEFT SIDE LOWER
            ax.text(0.02, 0.25, 'Hash Table Statistics:', fontsize=12, fontweight='bold', color='darkgreen')
            ax.text(0.02, 0.22, f'• Size: {table_size} buckets', fontsize=10)
            ax.text(0.02, 0.19, f'• Elements: {total_elements}', fontsize=10)
            ax.text(0.02, 0.16, f'• Load Factor: {load_factor:.2f}', fontsize=10)
            ax.text(0.02, 0.13, f'• Collisions: {collision_count}', fontsize=10)
            
            # Performance indicators - LEFT SIDE BOTTOM
            avg_chain_length = total_elements / table_size if table_size > 0 else 0
            max_chain_length = max(len(chain) for chain in hash_table) if hash_table else 0
            
            ax.text(0.02, 0.08, f'• Avg Chain Length: {avg_chain_length:.1f}', fontsize=10)
            ax.text(0.02, 0.05, f'• Max Chain Length: {max_chain_length}', fontsize=10)
            
            # Show current operation
            if operation:
                op_text = f"Operation: {operation['type'].replace('hash_', '').upper()}"
                if 'key' in operation:
                    key = operation['key']
                    index = hash_function(key)
                    op_text += f" (key: {key}, hash: {index})"
                
                ax.text(0.5, 0.88, op_text, ha='center', va='center', fontsize=16, 
                       fontweight='bold', bbox=dict(boxstyle="round,pad=0.5", 
                       facecolor="lightcyan", edgecolor="darkblue"))
            
            # Show step information - RIGHT SIDE TOP
            if step_info:
                ax.text(0.98, 0.85, step_info, ha='right', va='top', fontsize=11,
                       bbox=dict(boxstyle="round,pad=0.4", facecolor="lightgreen", alpha=0.8))
            
            # Draw hash function calculation demo - RIGHT SIDE MIDDLE
            if operation and 'key' in operation:
                key = operation['key']
                hash_val = hash_function(key)
                
                demo_text = f"Hash Calculation Demo:\n"
                demo_text += f"hash({key}) = {key} % {table_size} = {hash_val}\n"
                demo_text += f"→ Insert at bucket [{hash_val}]"
                
                ax.text(0.98, 0.45, demo_text, ha='right', va='top', fontsize=10,
                       bbox=dict(boxstyle="round,pad=0.4", facecolor="lightyellow", alpha=0.9))
            
            # Efficiency indicator - RIGHT SIDE BOTTOM
            efficiency = "Excellent" if load_factor < 0.5 else "Good" if load_factor < 0.75 else "Fair" if load_factor < 1.0 else "Poor"
            efficiency_colors = {"Excellent": "lightgreen", "Good": "lightblue", "Fair": "lightyellow", "Poor": "lightcoral"}
            efficiency_color = efficiency_colors.get(efficiency, "lightgray")
            
            ax.text(0.98, 0.20, f'Performance: {efficiency}', ha='right', va='center', fontsize=12,
                   fontweight='bold', bbox=dict(boxstyle="round,pad=0.4", facecolor=efficiency_color))
            
            # Hash table legend - RIGHT SIDE
            ax.text(0.98, 0.12, 'Legend:', ha='right', va='top', fontsize=10, fontweight='bold')
            ax.text(0.98, 0.09, '● Active Bucket (Yellow)', ha='right', va='top', fontsize=9)
            ax.text(0.98, 0.06, '● Occupied Bucket (Green)', ha='right', va='top', fontsize=9)
            ax.text(0.98, 0.03, '○ Empty Bucket (White)', ha='right', va='top', fontsize=9)
        
        # Generate animation frames
        frame_count = 0
        
        # Initial frame - empty hash table
        draw_hash_table_frame(step_info="Starting with empty hash table")
        plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=120, bbox_inches='tight')
        frame_count += 1
        
        # Hold initial frame
        for _ in range(30):  # 1 second
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=120, bbox_inches='tight')
            frame_count += 1
        
        for i, operation in enumerate(operations):
            # Show operation about to happen
            step_info = f"Step {i+1}: {operation['type'].replace('hash_', '').title()}"
            if 'key' in operation:
                step_info += f" key {operation['key']}"
            
            draw_hash_table_frame(operation, step_info=step_info)
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=120, bbox_inches='tight')
            frame_count += 1
            
            # Hold before operation
            for _ in range(45):  # 1.5 seconds
                plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=120, bbox_inches='tight')
                frame_count += 1
            
            # Execute operation
            if operation['type'] == 'hash_insert':
                key = operation['key']
                index = hash_function(key)
                
                # Check if this will cause a collision
                if hash_table[index]:
                    collision_count += 1
                
                # Insert into chain
                if key not in hash_table[index]:  # Avoid duplicates
                    hash_table[index].append(key)
                
                # Show result with highlighted index
                step_info = f"✓ Inserted {key} at index {index}"
                if len(hash_table[index]) > 1:
                    step_info += f" (collision resolved by chaining)"
                
                draw_hash_table_frame(operation, index, step_info)
                
            elif operation['type'] == 'hash_search':
                key = operation['key']
                index = hash_function(key)
                
                # Search in chain
                found = key in hash_table[index]
                
                step_info = f"✓ Search for {key}: {'Found' if found else 'Not found'} at index {index}"
                draw_hash_table_frame(operation, index, step_info)
                
            elif operation['type'] == 'hash_delete':
                key = operation['key']
                index = hash_function(key)
                
                # Remove from chain if exists
                if key in hash_table[index]:
                    hash_table[index].remove(key)
                    step_info = f"✓ Deleted {key} from index {index}"
                else:
                    step_info = f"✗ {key} not found for deletion"
                
                draw_hash_table_frame(operation, index, step_info)
            else:
                draw_hash_table_frame()
                
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=120, bbox_inches='tight')
            frame_count += 1
            
            # Hold after operation
            for _ in range(60):  # 2 seconds
                plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=120, bbox_inches='tight')
                frame_count += 1
        
        # Final frame
        draw_hash_table_frame(step_info="Hash Table Complete!")
        for _ in range(90):  # 3 seconds final view
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=120, bbox_inches='tight')
            frame_count += 1
        
        plt.close()
        self._frames_to_video(frame_count, output_path)
        return output_path
    
    def _create_algorithm_animation(self, elements: List[Dict], output_path: str) -> str:
        """Create algorithm animations (e.g., sorting)"""
        if not elements:
            return self._create_general_animation([{'type': 'text_slide', 'content': 'Algorithm Visualization'}], output_path)
        
        # Simple sorting animation
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Get array to sort
        array = elements[0].get('array', ['64', '34', '25', '12', '22', '11', '90'])
        array = [int(x) for x in array if x.isdigit()]
        
        def draw_sorting_frame(arr, comparing=None, swapping=None):
            ax.clear()
            ax.set_xlim(-0.5, len(arr) - 0.5)
            ax.set_ylim(0, max(arr) + 10)
            ax.set_title('BUBBLE SORT VISUALIZATION', fontsize=20, fontweight='bold')
            
            # Draw bars
            for i, val in enumerate(arr):
                color = 'red' if i in (comparing or []) else 'blue' if i in (swapping or []) else 'lightblue'
                ax.bar(i, val, color=color, edgecolor='black', linewidth=2)
                ax.text(i, val + 1, str(val), ha='center', va='bottom', fontsize=12, fontweight='bold')
        
        frame_count = 0
        
        # Bubble sort animation
        arr = array[:]
        n = len(arr)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                # Show comparison
                draw_sorting_frame(arr, comparing=[j, j + 1])
                plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
                frame_count += 1
                
                if arr[j] > arr[j + 1]:
                    # Show swap
                    draw_sorting_frame(arr, swapping=[j, j + 1])
                    plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
                    frame_count += 1
                    
                    # Perform swap
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    
                    # Show result
                    draw_sorting_frame(arr)
                    plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
                    frame_count += 1
                
                # Hold frame
                for _ in range(30):
                    plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
                    frame_count += 1
        
        # Final sorted array
        draw_sorting_frame(arr)
        ax.text(len(arr)/2, max(arr) + 5, 'SORTED!', ha='center', va='center', 
               fontsize=24, fontweight='bold', color='green')
        for _ in range(90):  # Hold final frame
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
            frame_count += 1
        
        plt.close()
        self._frames_to_video(frame_count, output_path)
        return output_path
    
    def _create_math_animation(self, elements: List[Dict], output_path: str) -> str:
        """Create enhanced mathematical animations based on actual note content"""
        try:
            from enhanced_concept_animators import EnhancedMathematicsAnimator
            if elements and len(elements) > 0:
                math_animator = EnhancedMathematicsAnimator()
                return math_animator.create_math_animation(elements[0], output_path)
        except ImportError:
            pass
        
        # Fallback to original math animation
        fig, ax = plt.subplots(figsize=(12, 8))
        
        def draw_math_frame(step):
            ax.clear()
            ax.set_xlim(-10, 10)
            ax.set_ylim(-10, 10)
            ax.grid(True, alpha=0.3)
            ax.set_title('MATHEMATICAL VISUALIZATION', fontsize=20, fontweight='bold')
            
            # Draw coordinate system
            ax.axhline(y=0, color='k', linewidth=0.5)
            ax.axvline(x=0, color='k', linewidth=0.5)
            
            # Draw a simple function (e.g., y = x^2)
            x = np.linspace(-3, 3, 100)
            y = x**2
            ax.plot(x, y, 'b-', linewidth=3, label='y = x²')
            
            # Animate a point moving along the curve
            t = step * 0.1
            if -3 <= t <= 3:
                point_y = t**2
                ax.plot(t, point_y, 'ro', markersize=10)
                ax.text(t, point_y + 1, f'({t:.1f}, {point_y:.1f})', 
                       ha='center', va='bottom', fontsize=12, fontweight='bold')
            
            ax.legend()
            ax.set_xlabel('x', fontsize=14)
            ax.set_ylabel('y', fontsize=14)
        
        frame_count = 0
        
        for step in range(60):  # 2 seconds of animation
            draw_math_frame(step)
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
            frame_count += 1
        
        plt.close()
        self._frames_to_video(frame_count, output_path)
        return output_path
    
    def _create_physics_animation(self, elements: List[Dict], output_path: str) -> str:
        """Create enhanced physics animations based on actual note content"""
        try:
            from enhanced_concept_animators import EnhancedPhysicsAnimator
            if elements and len(elements) > 0:
                physics_animator = EnhancedPhysicsAnimator()
                return physics_animator.create_physics_animation(elements[0], output_path)
        except ImportError:
            pass
        
        # Fallback to original physics animation
        fig, ax = plt.subplots(figsize=(12, 8))
        
        def draw_physics_frame(step):
            ax.clear()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 6)
            ax.set_title('PHYSICS SIMULATION - PROJECTILE MOTION', fontsize=20, fontweight='bold')
            
            # Projectile motion parameters
            v0 = 8  # initial velocity
            angle = 45  # launch angle
            g = 9.8  # gravity
            t = step * 0.1
            
            # Calculate position
            x = v0 * np.cos(np.radians(angle)) * t
            y = v0 * np.sin(np.radians(angle)) * t - 0.5 * g * t**2
            
            if y >= 0 and x <= 10:
                # Draw trajectory
                t_traj = np.linspace(0, t, 50)
                x_traj = v0 * np.cos(np.radians(angle)) * t_traj
                y_traj = v0 * np.sin(np.radians(angle)) * t_traj - 0.5 * g * t_traj**2
                
                valid_indices = y_traj >= 0
                ax.plot(x_traj[valid_indices], y_traj[valid_indices], 'b--', alpha=0.5)
                
                # Draw projectile
                ax.plot(x, y, 'ro', markersize=15)
                
                # Add velocity vector
                vx = v0 * np.cos(np.radians(angle))
                vy = v0 * np.sin(np.radians(angle)) - g * t
                ax.arrow(x, y, vx/10, vy/10, head_width=0.2, head_length=0.2, fc='red', ec='red')
                
                # Add text
                ax.text(1, 5, f'Time: {t:.1f}s', fontsize=14, fontweight='bold')
                ax.text(1, 4.5, f'Position: ({x:.1f}, {y:.1f})', fontsize=12)
            
            ax.set_xlabel('Distance (m)', fontsize=14)
            ax.set_ylabel('Height (m)', fontsize=14)
            ax.grid(True, alpha=0.3)
        
        frame_count = 0
        
        for step in range(80):
            draw_physics_frame(step)
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
            frame_count += 1
        
        plt.close()
        self._frames_to_video(frame_count, output_path)
        return output_path
    
    def _create_chemistry_animation(self, elements: List[Dict], output_path: str) -> str:
        """Create enhanced chemistry animations based on actual note content"""
        try:
            from enhanced_concept_animators import EnhancedChemistryAnimator
            if elements and len(elements) > 0:
                chemistry_animator = EnhancedChemistryAnimator()
                return chemistry_animator.create_chemistry_animation(elements[0], output_path)
        except ImportError:
            pass
        
        # Fallback to basic chemistry animation
        return self._create_general_animation([{'type': 'text_slide', 'content': 'Chemistry Concepts Visualization'}], output_path)
    
    def _create_biology_animation(self, elements: List[Dict], output_path: str) -> str:
        """Create enhanced biology animations based on actual note content"""
        try:
            from enhanced_concept_animators import EnhancedBiologyAnimator
            if elements and len(elements) > 0:
                biology_animator = EnhancedBiologyAnimator()
                return biology_animator.create_biology_animation(elements[0], output_path)
        except ImportError:
            pass
        
        # Fallback to basic biology animation
        return self._create_general_animation([{'type': 'text_slide', 'content': 'Biology Concepts Visualization'}], output_path)
    
    def _create_process_animation(self, elements: List[Dict], output_path: str) -> str:
        """Create business process animations"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        def draw_process_frame(current_step):
            ax.clear()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 8)
            ax.set_title('BUSINESS PROCESS FLOW', fontsize=20, fontweight='bold')
            
            # Draw process steps as boxes
            steps = ['Start', 'Analysis', 'Decision', 'Implementation', 'Review', 'End']
            positions = [(1, 4), (3, 4), (5, 4), (7, 4), (5, 2), (9, 4)]
            
            for i, (step, pos) in enumerate(zip(steps, positions)):
                color = 'lightgreen' if i == current_step else 'lightblue'
                rect = Rectangle((pos[0]-0.5, pos[1]-0.3), 1, 0.6, 
                               facecolor=color, edgecolor='black', linewidth=2)
                ax.add_patch(rect)
                ax.text(pos[0], pos[1], step, ha='center', va='center', 
                       fontsize=10, fontweight='bold')
            
            # Draw arrows
            arrow_paths = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (2, 4)]  # Decision branch
            for start_idx, end_idx in arrow_paths:
                if start_idx < len(positions) and end_idx < len(positions):
                    start_pos = positions[start_idx]
                    end_pos = positions[end_idx]
                    ax.annotate('', xy=end_pos, xytext=start_pos,
                               arrowprops=dict(arrowstyle='->', lw=2, color='blue'))
        
        frame_count = 0
        
        for step in range(6):
            for _ in range(60):  # Hold each step for 2 seconds
                draw_process_frame(step)
                plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
                frame_count += 1
        
        plt.close()
        self._frames_to_video(frame_count, output_path)
        return output_path
    
    def _create_general_animation(self, elements: List[Dict], output_path: str) -> str:
        """Create general text-based animation"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        def draw_text_frame(text, step):
            ax.clear()
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            
            # Animated text appearance
            visible_chars = min(len(text), step * 2)
            visible_text = text[:visible_chars]
            
            ax.text(0.5, 0.5, visible_text, ha='center', va='center', 
                   fontsize=20, fontweight='bold', wrap=True)
        
        frame_count = 0
        
        for element in elements:
            text = element.get('content', 'Content Visualization')
            
            # Animate text appearance
            for step in range(len(text) // 2 + 30):
                draw_text_frame(text, step)
                plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
                frame_count += 1
        
        plt.close()
        self._frames_to_video(frame_count, output_path)
        return output_path
    
    def _frames_to_video(self, frame_count: int, output_path: str):
        """Convert frame images to video using moviepy"""
        try:
            # Import MoviePy locally to avoid import conflicts
            from moviepy.editor import ImageSequenceClip
            
            # Create list of frame files
            frame_files = [f'temp_frame_{i:04d}.png' for i in range(frame_count)]
            
            # Filter only existing frames
            existing_frames = [f for f in frame_files if os.path.exists(f)]
            
            if not existing_frames:
                print("No frames found to create video")
                return
            
            # Create video clip
            clip = ImageSequenceClip(existing_frames, fps=self.fps)
            clip.write_videofile(output_path, codec='libx264', logger=None)
            clip.close()
            
            # Clean up temporary frames
            for frame_file in existing_frames:
                if os.path.exists(frame_file):
                    os.remove(frame_file)
                    
        except Exception as e:
            print(f"Error creating video: {e}")
            # Fallback: copy first frame as static image
            if os.path.exists('temp_frame_0000.png'):
                import shutil
                shutil.copy('temp_frame_0000.png', output_path.replace('.mp4', '.png'))


def create_intelligent_animation(text: str, output_path: str) -> str:
    """Main function to create intelligent animations from any text content"""
    
    # Analyze content
    analyzer = ContentAnalyzer()
    content_analysis = analyzer.analyze_content(text)
    
    print(f"🔍 Content Analysis:")
    print(f"   Type: {content_analysis['type']}")
    print(f"   Score: {content_analysis['score']}")
    print(f"   Elements: {len(content_analysis['elements'])}")
    
    # Create appropriate animation
    animator = UniversalAnimationEngine()
    result_path = animator.create_animation(content_analysis, output_path)
    
    # Add audio narration
    from text_to_animation_full_project import text_to_speech
    temp_audio = 'temp_narration.mp3'
    
    # Create context-appropriate narration
    narration_text = f"This is an animated explanation of {content_analysis['type'].replace('_', ' ')} concepts. "
    
    if content_analysis['type'] == 'data_structures':
        narration_text += "Watch how the data structure operations work step by step. "
    elif content_analysis['type'] == 'algorithms':
        narration_text += "Observe how the algorithm processes the data elements. "
    elif content_analysis['type'] == 'mathematics':
        narration_text += "See the mathematical concepts visualized graphically. "
    elif content_analysis['type'] == 'physics':
        narration_text += "Watch the physics simulation in action. "
    
    narration_text += text[:200] + "..."  # Add some original content
    
    try:
        # Import MoviePy locally to avoid conflicts
        from text_to_animation_full_project import text_to_speech
        text_to_speech(narration_text, temp_audio)
        
        # Combine video and audio
        from moviepy.editor import VideoFileClip, AudioFileClip
        
        video_clip = VideoFileClip(result_path)
        audio_clip = AudioFileClip(temp_audio)
        
        # Adjust durations
        if video_clip.duration < audio_clip.duration:
            video_clip = video_clip.loop(duration=audio_clip.duration)
        else:
            audio_clip = audio_clip.subclip(0, min(audio_clip.duration, video_clip.duration))
        
        final_video = video_clip.set_audio(audio_clip)
        final_output = output_path.replace('.mp4', '_with_audio.mp4')
        final_video.write_videofile(final_output, codec='libx264', audio_codec='aac', logger=None)
        
        # Clean up
        video_clip.close()
        audio_clip.close()
        final_video.close()
        
        if os.path.exists(temp_audio):
            os.remove(temp_audio)
        if os.path.exists(result_path):
            os.remove(result_path)
        
        return final_output
        
    except Exception as e:
        print(f"Audio processing failed: {e}, returning video only")
        return result_path


class IntelligentAnimator:
    """High-level interface for creating intelligent animations"""
    
    def __init__(self):
        self.engine = UniversalAnimationEngine()
        self.analyzer = ContentAnalyzer()
        
    def create_data_structure_animation(self, elements: List[Dict], output_path: str = None) -> str:
        """Create data structure animation"""
        if output_path is None:
            output_path = "data_structure_animation.mp4"
        
        return self.engine._create_data_structure_animation(elements, output_path)
    
    def _create_data_structure_animation(self, elements: List[Dict], output_path: str) -> str:
        """Delegate to engine for backward compatibility"""
        return self.engine._create_data_structure_animation(elements, output_path)
    
    def create_algorithm_animation(self, elements: List[Dict], output_path: str = None) -> str:
        """Create algorithm animation"""
        if output_path is None:
            output_path = "algorithm_animation.mp4"
        
        return self.engine._create_algorithm_animation(elements, output_path)
    
    def create_math_animation(self, elements: List[Dict], output_path: str = None) -> str:
        """Create mathematics animation"""
        if output_path is None:
            output_path = "math_animation.mp4"
        
        return self.engine._create_math_animation(elements, output_path)
    
    def create_general_animation(self, elements: List[Dict], output_path: str = None) -> str:
        """Create general animation"""
        if output_path is None:
            output_path = "general_animation.mp4"
        
        return self.engine._create_general_animation(elements, output_path)
    
    def analyze_and_animate(self, text: str, output_path: str = None) -> str:
        """Analyze content and create appropriate animation"""
        if output_path is None:
            output_path = "intelligent_animation.mp4"
            
        # Analyze content
        analysis = self.analyzer.analyze_content(text)
        
        # Create animation based on analysis
        return self.engine.create_animation(analysis, output_path)
