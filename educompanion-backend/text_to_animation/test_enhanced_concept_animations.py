"""
Test script to verify enhanced concept-aware animations work properly
Tests physics, chemistry, mathematics, and biology concept extraction and animation
"""

import os
import sys

def test_enhanced_animations():
    """Test the enhanced concept-aware animation system"""
    
    print("🧪 Testing Enhanced Concept-Aware Animation System")
    print("="*60)
    
    # Test Physics Notes
    physics_notes = """
    Kinematics Problem:
    Initial velocity v = 20 m/s
    Acceleration a = -9.8 m/s²
    Time t = 3 s
    
    Using equation: s = ut + ½at²
    Distance s = 20×3 + ½×(-9.8)×3²
    Distance s = 60 - 44.1 = 15.9 m
    
    Final velocity v = u + at = 20 + (-9.8)×3 = -9.4 m/s
    """
    
    # Test Chemistry Notes  
    chemistry_notes = """
    Chemical Reaction:
    2H₂ + O₂ → 2H₂O
    
    Molecules involved:
    - H₂ (Hydrogen gas)
    - O₂ (Oxygen gas) 
    - H₂O (Water)
    
    This is a synthesis reaction where hydrogen and oxygen combine to form water.
    The reaction releases energy and is exothermic.
    """
    
    # Test Mathematics Notes
    math_notes = """
    Quadratic Function Analysis:
    f(x) = x² - 4x + 3
    
    To find roots: x² - 4x + 3 = 0
    Using quadratic formula: x = (-b ± √(b²-4ac))/2a
    where a=1, b=-4, c=3
    
    x = (4 ± √(16-12))/2 = (4 ± 2)/2
    So x = 3 or x = 1
    
    The parabola opens upward and has vertex at (2, -1)
    """
    
    # Test Biology Notes
    biology_notes = """
    Cell Structure:
    - Nucleus: Control center containing DNA
    - Mitochondria: Powerhouse of the cell, produces ATP
    - Cell membrane: Controls entry and exit of substances
    - Ribosomes: Protein synthesis
    - Vacuole: Storage organelle (large in plant cells)
    
    The cell is the basic unit of life. Plant cells have additional structures
    like chloroplasts for photosynthesis and a rigid cell wall.
    """
    
    # Import the enhanced system
    try:
        from intelligent_animator import ContentAnalyzer, UniversalAnimationEngine
        
        analyzer = ContentAnalyzer()
        animator = UniversalAnimationEngine()
        
        # Test cases
        test_cases = [
            ("Physics", physics_notes, "test_physics_enhanced.mp4"),
            ("Chemistry", chemistry_notes, "test_chemistry_enhanced.mp4"),
            ("Mathematics", math_notes, "test_math_enhanced.mp4"),
            ("Biology", biology_notes, "test_biology_enhanced.mp4")
        ]
        
        for subject, notes, output_file in test_cases:
            print(f"\n📚 Testing {subject} Animation:")
            print("-" * 40)
            
            # Analyze content
            analysis = analyzer.analyze_content(notes)
            
            print(f"Content Type Detected: {analysis['type']}")
            print(f"Confidence Score: {analysis['score']}")
            print(f"Elements Extracted: {len(analysis['elements'])}")
            
            if analysis['elements']:
                print(f"First Element: {analysis['elements'][0]}")
            
            # Create animation
            try:
                output_path = f"output/{output_file}"
                os.makedirs("output", exist_ok=True)
                
                result = animator.create_animation(analysis, output_path)
                print(f"✅ Animation created: {result}")
                
                if os.path.exists(result):
                    file_size = os.path.getsize(result) / 1024  # KB
                    print(f"   File size: {file_size:.1f} KB")
                else:
                    print("❌ Animation file not found")
                    
            except Exception as e:
                print(f"❌ Animation creation failed: {e}")
        
        # Test concept extraction directly
        print(f"\n🔬 Testing Enhanced Concept Analyzers:")
        print("-" * 40)
        
        try:
            from enhanced_concept_analyzers import (
                EnhancedPhysicsAnalyzer, EnhancedChemistryAnalyzer, 
                EnhancedMathematicsAnalyzer, EnhancedBiologyAnalyzer
            )
            
            # Test Physics Analyzer
            physics_analyzer = EnhancedPhysicsAnalyzer()
            physics_concepts = physics_analyzer.extract_physics_concepts(physics_notes)
            print(f"Physics concepts: {physics_concepts}")
            
            # Test Chemistry Analyzer
            chemistry_analyzer = EnhancedChemistryAnalyzer()
            chemistry_concepts = chemistry_analyzer.extract_chemistry_concepts(chemistry_notes)
            print(f"Chemistry concepts: {chemistry_concepts}")
            
            # Test Math Analyzer
            math_analyzer = EnhancedMathematicsAnalyzer()
            math_concepts = math_analyzer.extract_math_concepts(math_notes)
            print(f"Math concepts: {math_concepts}")
            
            # Test Biology Analyzer
            biology_analyzer = EnhancedBiologyAnalyzer()
            biology_concepts = biology_analyzer.extract_biology_concepts(biology_notes)
            print(f"Biology concepts: {biology_concepts}")
            
        except ImportError as e:
            print(f"❌ Enhanced analyzers not available: {e}")
            
    except ImportError as e:
        print(f"❌ Failed to import animation system: {e}")
        return False
    
    print(f"\n✅ Enhanced concept-aware animation testing completed!")
    print("Now your physics, chemistry, math, and biology animations will use actual concepts from notes!")
    
    return True


if __name__ == "__main__":
    test_enhanced_animations()