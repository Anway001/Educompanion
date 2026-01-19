"""
Enhanced concept-aware content analyzers for Physics, Chemistry, Mathematics, and Biology
These analyze actual note content and create relevant visualizations
"""

import re
import math
import numpy as np
from typing import List, Dict, Any, Tuple
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Arrow, Ellipse, Polygon
import matplotlib.patches as mpatches

class EnhancedPhysicsAnalyzer:
    """Enhanced physics concept analyzer that extracts actual physics concepts from notes"""
    
    def __init__(self):
        self.physics_patterns = {
            'kinematics': {
                'keywords': ['velocity', 'acceleration', 'displacement', 'speed', 'motion', 'distance', 'time'],
                'equations': [r'v\s*=\s*u\s*\+\s*at', r's\s*=\s*ut\s*\+\s*½at²', r'v²\s*=\s*u²\s*\+\s*2as'],
                'variables': ['v', 'u', 'a', 't', 's', 'distance', 'velocity', 'acceleration']
            },
            'forces': {
                'keywords': ['force', 'newton', 'mass', 'acceleration', 'weight', 'friction', 'tension'],
                'equations': [r'F\s*=\s*ma', r'W\s*=\s*mg', r'F\s*=\s*μN'],
                'variables': ['F', 'force', 'm', 'mass', 'a', 'g', 'weight', 'friction']
            },
            'energy': {
                'keywords': ['energy', 'kinetic', 'potential', 'work', 'power', 'joule'],
                'equations': [r'KE\s*=\s*½mv²', r'PE\s*=\s*mgh', r'W\s*=\s*Fd'],
                'variables': ['KE', 'PE', 'W', 'work', 'power', 'energy']
            },
            'waves': {
                'keywords': ['wave', 'frequency', 'wavelength', 'amplitude', 'period', 'oscillation'],
                'equations': [r'v\s*=\s*fλ', r'T\s*=\s*1/f'],
                'variables': ['f', 'λ', 'wavelength', 'frequency', 'amplitude', 'period']
            },
            'electricity': {
                'keywords': ['current', 'voltage', 'resistance', 'ohm', 'circuit', 'power'],
                'equations': [r'V\s*=\s*IR', r'P\s*=\s*IV', r'P\s*=\s*I²R'],
                'variables': ['V', 'I', 'R', 'P', 'voltage', 'current', 'resistance', 'power']
            }
        }
    
    def extract_physics_concepts(self, text: str) -> List[Dict]:
        """Extract specific physics concepts from text"""
        concepts = []
        text_lower = text.lower()
        
        # Identify physics topic
        topic_scores = {}
        for topic, patterns in self.physics_patterns.items():
            score = 0
            for keyword in patterns['keywords']:
                score += text_lower.count(keyword.lower())
            topic_scores[topic] = score
        
        primary_topic = max(topic_scores, key=topic_scores.get) if any(topic_scores.values()) else 'kinematics'
        
        # Extract numerical values and units
        values = self._extract_physics_values(text)
        equations = self._extract_equations(text, primary_topic)
        
        # Create concept based on topic
        concept = {
            'type': 'physics_simulation',
            'topic': primary_topic,
            'values': values,
            'equations': equations,
            'original_text': text[:200] + "..." if len(text) > 200 else text
        }
        
        concepts.append(concept)
        return concepts
    
    def _extract_physics_values(self, text: str) -> Dict[str, float]:
        """Extract numerical values with units from physics text"""
        values = {}
        
        # Common physics value patterns
        patterns = {
            'velocity': [r'v\s*=\s*(\d+(?:\.\d+)?)\s*m/s', r'velocity\s*=\s*(\d+(?:\.\d+)?)'],
            'acceleration': [r'a\s*=\s*(\d+(?:\.\d+)?)\s*m/s²', r'acceleration\s*=\s*(\d+(?:\.\d+)?)'],
            'mass': [r'm\s*=\s*(\d+(?:\.\d+)?)\s*kg', r'mass\s*=\s*(\d+(?:\.\d+)?)'],
            'force': [r'F\s*=\s*(\d+(?:\.\d+)?)\s*N', r'force\s*=\s*(\d+(?:\.\d+)?)'],
            'distance': [r's\s*=\s*(\d+(?:\.\d+)?)\s*m', r'distance\s*=\s*(\d+(?:\.\d+)?)'],
            'time': [r't\s*=\s*(\d+(?:\.\d+)?)\s*s', r'time\s*=\s*(\d+(?:\.\d+)?)'],
            'frequency': [r'f\s*=\s*(\d+(?:\.\d+)?)\s*Hz', r'frequency\s*=\s*(\d+(?:\.\d+)?)'],
            'voltage': [r'V\s*=\s*(\d+(?:\.\d+)?)\s*V', r'voltage\s*=\s*(\d+(?:\.\d+)?)'],
            'current': [r'I\s*=\s*(\d+(?:\.\d+)?)\s*A', r'current\s*=\s*(\d+(?:\.\d+)?)'],
            'resistance': [r'R\s*=\s*(\d+(?:\.\d+)?)\s*Ω', r'resistance\s*=\s*(\d+(?:\.\d+)?)']
        }
        
        for variable, pattern_list in patterns.items():
            for pattern in pattern_list:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    values[variable] = float(matches[0])
                    break
        
        return values
    
    def _extract_equations(self, text: str, topic: str) -> List[str]:
        """Extract physics equations from text"""
        equations = []
        
        if topic in self.physics_patterns:
            for eq_pattern in self.physics_patterns[topic]['equations']:
                matches = re.findall(eq_pattern, text, re.IGNORECASE)
                equations.extend(matches)
        
        # Also look for general equation patterns
        general_equations = re.findall(r'([A-Za-z]+\s*=\s*[^=\n]+)', text)
        equations.extend([eq.strip() for eq in general_equations])
        
        return equations[:3]  # Limit to first 3 equations


class EnhancedChemistryAnalyzer:
    """Enhanced chemistry concept analyzer"""
    
    def __init__(self):
        self.chemistry_patterns = {
            'reactions': {
                'keywords': ['reaction', 'reactant', 'product', 'catalyst', 'equilibrium'],
                'patterns': [r'[A-Z][a-z]?\d*\s*\+\s*[A-Z][a-z]?\d*\s*→\s*[A-Z][a-z]?\d*']
            },
            'acids_bases': {
                'keywords': ['acid', 'base', 'pH', 'neutral', 'hydroxide', 'hydrogen'],
                'patterns': [r'pH\s*=\s*\d+', r'H\+', r'OH-']
            },
            'organic': {
                'keywords': ['organic', 'carbon', 'hydrocarbon', 'alcohol', 'alkane', 'alkene'],
                'patterns': [r'C\d*H\d*', r'CH\d', r'OH']
            },
            'stoichiometry': {
                'keywords': ['mole', 'molecular', 'atomic', 'mass', 'coefficient'],
                'patterns': [r'\d+\s*mol', r'molar\s*mass']
            }
        }
    
    def extract_chemistry_concepts(self, text: str) -> List[Dict]:
        """Extract specific chemistry concepts from text"""
        concepts = []
        text_lower = text.lower()
        
        # Identify chemistry topic
        topic_scores = {}
        for topic, patterns in self.chemistry_patterns.items():
            score = 0
            for keyword in patterns['keywords']:
                score += text_lower.count(keyword.lower())
            topic_scores[topic] = score
        
        primary_topic = max(topic_scores, key=topic_scores.get) if any(topic_scores.values()) else 'reactions'
        
        # Extract chemical formulas and equations
        formulas = self._extract_chemical_formulas(text)
        reactions = self._extract_chemical_reactions(text)
        
        concept = {
            'type': 'chemistry_simulation',
            'topic': primary_topic,
            'formulas': formulas,
            'reactions': reactions,
            'original_text': text[:200] + "..." if len(text) > 200 else text
        }
        
        concepts.append(concept)
        return concepts
    
    def _extract_chemical_formulas(self, text: str) -> List[str]:
        """Extract chemical formulas from text"""
        formulas = []
        
        # Common chemical formulas - direct matches
        common_formulas = ['H2O', 'H₂O', 'CO2', 'CO₂', 'NaCl', 'HCl', 'NH3', 'NH₃', 'CH4', 'CH₄', 'O2', 'O₂', 'N2', 'N₂', 'H2', 'H₂']
        for formula in common_formulas:
            if formula in text:
                formulas.append(formula.replace('₂', '2').replace('₃', '3').replace('₄', '4'))
        
        # Pattern for chemical formulas like H2O, CO2, NaCl, etc.
        formula_pattern = r'\b[A-Z][a-z]?(?:\d+)?(?:[A-Z][a-z]?(?:\d+)?)*\b'
        
        matches = re.findall(formula_pattern, text)
        
        # Filter out non-chemical matches
        chemical_elements = {'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Fe', 'Cu', 'Zn', 'Br', 'I', 'Ba', 'Au', 'Hg', 'Pb'}
        
        for match in matches:
            # Check if starts with known chemical element and is likely a formula
            element = re.match(r'[A-Z][a-z]?', match).group()
            if element in chemical_elements and (len(match) <= 6 and any(c.isdigit() for c in match)):
                formulas.append(match)
        
        return list(set(formulas))  # Remove duplicates
    
    def _extract_chemical_reactions(self, text: str) -> List[str]:
        """Extract chemical reaction equations"""
        reactions = []
        
        # Look for reaction arrows first
        arrow_patterns = ['→', '->', '⟶', '-->', '=']
        
        for arrow in arrow_patterns:
            if arrow in text:
                # Split by lines and find lines with arrows
                lines = text.split('\n')
                for line in lines:
                    if arrow in line:
                        # Clean up the line
                        clean_line = line.strip()
                        if len(clean_line) > 5:  # Must be reasonably long
                            reactions.append(clean_line)
        
        # Pattern-based extraction for more complex cases
        reaction_patterns = [
            r'\d*[A-Z][a-z]?[₀-₉]*(?:\s*\+\s*\d*[A-Z][a-z]?[₀-₉]*)*\s*(?:→|->)\s*\d*[A-Z][a-z]?[₀-₉]*(?:\s*\+\s*\d*[A-Z][a-z]?[₀-₉]*)*',
            r'[A-Z][a-z]?\d*(?:\s*\+\s*[A-Z][a-z]?\d*)*\s*(?:→|->)\s*[A-Z][a-z]?\d*(?:\s*\+\s*[A-Z][a-z]?\d*)*'
        ]
        
        for pattern in reaction_patterns:
            matches = re.findall(pattern, text)
            reactions.extend(matches)
        
        return list(set(reactions))  # Remove duplicates


class EnhancedMathematicsAnalyzer:
    """Enhanced mathematics concept analyzer"""
    
    def __init__(self):
        self.math_patterns = {
            'algebra': {
                'keywords': ['equation', 'variable', 'solve', 'x', 'y', 'linear', 'quadratic'],
                'patterns': [r'[xy]\s*=\s*[^=\n]+', r'ax²\s*\+\s*bx\s*\+\s*c\s*=\s*0']
            },
            'calculus': {
                'keywords': ['derivative', 'integral', 'limit', 'differentiate', 'integrate'],
                'patterns': [r'd/dx', r'∫', r'lim', r'f\'']
            },
            'geometry': {
                'keywords': ['triangle', 'circle', 'rectangle', 'area', 'perimeter', 'angle'],
                'patterns': [r'area\s*=\s*[^=\n]+', r'perimeter\s*=\s*[^=\n]+']
            },
            'trigonometry': {
                'keywords': ['sin', 'cos', 'tan', 'sine', 'cosine', 'tangent', 'angle'],
                'patterns': [r'sin\([^)]+\)', r'cos\([^)]+\)', r'tan\([^)]+\)']
            },
            'functions': {
                'keywords': ['function', 'domain', 'range', 'graph', 'plot'],
                'patterns': [r'f\(x\)\s*=\s*[^=\n]+', r'y\s*=\s*[^=\n]+']
            }
        }
    
    def extract_math_concepts(self, text: str) -> List[Dict]:
        """Extract specific mathematical concepts from text"""
        concepts = []
        text_lower = text.lower()
        
        # Identify math topic
        topic_scores = {}
        for topic, patterns in self.math_patterns.items():
            score = 0
            for keyword in patterns['keywords']:
                score += text_lower.count(keyword.lower())
            topic_scores[topic] = score
        
        primary_topic = max(topic_scores, key=topic_scores.get) if any(topic_scores.values()) else 'algebra'
        
        # Extract mathematical expressions
        expressions = self._extract_mathematical_expressions(text)
        functions = self._extract_functions(text)
        geometric_shapes = self._extract_geometric_concepts(text)
        
        concept = {
            'type': 'mathematics_visualization',
            'topic': primary_topic,
            'expressions': expressions,
            'functions': functions,
            'geometric_shapes': geometric_shapes,
            'original_text': text[:200] + "..." if len(text) > 200 else text
        }
        
        concepts.append(concept)
        return concepts
    
    def _extract_mathematical_expressions(self, text: str) -> List[str]:
        """Extract mathematical expressions and equations"""
        expressions = []
        
        # Common mathematical expression patterns
        patterns = [
            r'[xy]\s*=\s*[^=\n]+',  # Variable equations
            r'\d+x\s*[\+\-]\s*\d+\s*=\s*\d+',  # Linear equations
            r'ax²\s*[\+\-]\s*bx\s*[\+\-]\s*c\s*=\s*0',  # Quadratic form
            r'f\(x\)\s*=\s*[^=\n]+',  # Function definitions
            r'[A-Za-z]+\s*=\s*\d+(?:\.\d+)?',  # Variable assignments
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            expressions.extend(matches)
        
        return expressions[:5]  # Limit to first 5 expressions
    
    def _extract_functions(self, text: str) -> List[Dict]:
        """Extract function definitions"""
        functions = []
        
        # Function patterns
        function_patterns = [
            r'f\(x\)\s*=\s*([^=\n]+)',
            r'y\s*=\s*([^=\n]+)',
            r'g\(x\)\s*=\s*([^=\n]+)'
        ]
        
        for pattern in function_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                functions.append({
                    'expression': match.strip(),
                    'type': 'function'
                })
        
        return functions
    
    def _extract_geometric_concepts(self, text: str) -> List[Dict]:
        """Extract geometric shapes and properties"""
        shapes = []
        text_lower = text.lower()
        
        shape_patterns = {
            'circle': ['circle', 'radius', 'diameter', 'circumference'],
            'triangle': ['triangle', 'angle', 'side', 'hypotenuse'],
            'rectangle': ['rectangle', 'length', 'width', 'area'],
            'square': ['square', 'side', 'area', 'perimeter']
        }
        
        for shape, keywords in shape_patterns.items():
            if any(keyword in text_lower for keyword in keywords):
                # Extract numerical values related to the shape
                values = re.findall(r'(\d+(?:\.\d+)?)', text)
                shapes.append({
                    'type': shape,
                    'values': [float(v) for v in values[:3]]  # First 3 values
                })
        
        return shapes


class EnhancedBiologyAnalyzer:
    """Enhanced biology concept analyzer"""
    
    def __init__(self):
        self.biology_patterns = {
            'cell_structure': {
                'keywords': ['cell', 'nucleus', 'membrane', 'cytoplasm', 'organelle', 'mitochondria'],
                'structures': ['nucleus', 'membrane', 'cytoplasm', 'ribosomes', 'vacuole']
            },
            'genetics': {
                'keywords': ['dna', 'rna', 'gene', 'chromosome', 'allele', 'inheritance'],
                'patterns': ['DNA', 'RNA', 'A-T', 'G-C', 'mRNA', 'tRNA']
            },
            'ecology': {
                'keywords': ['ecosystem', 'food chain', 'producer', 'consumer', 'decomposer'],
                'relationships': ['predator', 'prey', 'symbiosis', 'competition']
            },
            'human_body': {
                'keywords': ['heart', 'lung', 'brain', 'blood', 'organ', 'system'],
                'systems': ['circulatory', 'respiratory', 'nervous', 'digestive']
            },
            'evolution': {
                'keywords': ['evolution', 'natural selection', 'adaptation', 'species', 'darwin'],
                'concepts': ['mutation', 'fitness', 'variation', 'survival']
            }
        }
    
    def extract_biology_concepts(self, text: str) -> List[Dict]:
        """Extract specific biology concepts from text"""
        concepts = []
        text_lower = text.lower()
        
        # Identify biology topic
        topic_scores = {}
        for topic, patterns in self.biology_patterns.items():
            score = 0
            for keyword in patterns['keywords']:
                score += text_lower.count(keyword.lower())
            topic_scores[topic] = score
        
        primary_topic = max(topic_scores, key=topic_scores.get) if any(topic_scores.values()) else 'cell_structure'
        
        # Extract biological terms and processes
        terms = self._extract_biology_terms(text, primary_topic)
        processes = self._extract_biological_processes(text)
        
        concept = {
            'type': 'biology_visualization',
            'topic': primary_topic,
            'terms': terms,
            'processes': processes,
            'original_text': text[:200] + "..." if len(text) > 200 else text
        }
        
        concepts.append(concept)
        return concepts
    
    def _extract_biology_terms(self, text: str, topic: str) -> List[str]:
        """Extract biological terms from text"""
        terms = []
        text_lower = text.lower()
        
        if topic in self.biology_patterns:
            # Look for specific terms related to the topic
            topic_data = self.biology_patterns[topic]
            
            # Check all keyword categories
            for key in ['keywords', 'structures', 'patterns', 'relationships', 'systems', 'concepts']:
                if key in topic_data:
                    for term in topic_data[key]:
                        if term.lower() in text_lower:
                            terms.append(term)
        
        return list(set(terms))  # Remove duplicates
    
    def _extract_biological_processes(self, text: str) -> List[str]:
        """Extract biological processes from text"""
        processes = []
        
        # Common biological processes
        process_keywords = [
            'photosynthesis', 'respiration', 'mitosis', 'meiosis', 'fertilization',
            'digestion', 'circulation', 'reproduction', 'metabolism', 'homeostasis'
        ]
        
        text_lower = text.lower()
        for process in process_keywords:
            if process in text_lower:
                processes.append(process)
        
        return processes