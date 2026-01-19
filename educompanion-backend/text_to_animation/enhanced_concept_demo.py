"""
Enhanced Concept-Aware Animation Demo
Shows how physics, chemistry, math, and biology animations now use actual note content
"""

import streamlit as st
import os
from intelligent_animator import ContentAnalyzer, UniversalAnimationEngine

def main():
    st.title("🧪 Enhanced Concept-Aware Animation System")
    st.markdown("**Now generates animations that match actual concepts from your notes!**")
    
    st.markdown("---")
    
    # Sample notes for different subjects
    sample_notes = {
        "Physics": """
        Kinematics Problem:
        Initial velocity v = 15 m/s
        Acceleration a = -9.8 m/s²  
        Time t = 2 s
        
        Using equation: s = ut + ½at²
        Distance s = 15×2 + ½×(-9.8)×2²
        Distance s = 30 - 19.6 = 10.4 m
        """,
        
        "Chemistry": """
        Chemical Reaction:
        2H₂ + O₂ → 2H₂O
        
        This is a combustion reaction where:
        - H₂ (hydrogen gas) reacts with O₂ (oxygen gas)
        - Forms H₂O (water)
        - Releases energy (exothermic)
        """,
        
        "Mathematics": """
        Quadratic Function: f(x) = 2x² - 8x + 6
        
        To find vertex: x = -b/2a = -(-8)/2(2) = 2
        f(2) = 2(4) - 8(2) + 6 = -2
        
        Vertex: (2, -2)
        Opens upward since a > 0
        """,
        
        "Biology": """
        Plant Cell Structure:
        - Cell wall: Rigid outer layer for support
        - Chloroplasts: Site of photosynthesis  
        - Large vacuole: Maintains turgor pressure
        - Nucleus: Contains DNA, controls activities
        - Mitochondria: Cellular respiration
        """
    }
    
    # Create tabs for different subjects
    tab1, tab2, tab3, tab4 = st.tabs(["🔬 Physics", "⚗️ Chemistry", "📐 Mathematics", "🧬 Biology"])
    
    analyzer = ContentAnalyzer()
    
    for tab, subject in zip([tab1, tab2, tab3, tab4], ["Physics", "Chemistry", "Mathematics", "Biology"]):
        with tab:
            st.subheader(f"{subject} Notes Analysis")
            
            # Show sample notes
            notes_text = st.text_area(
                f"Enter your {subject.lower()} notes:",
                value=sample_notes[subject],
                height=150,
                key=f"{subject}_notes"
            )
            
            if st.button(f"Analyze {subject} Content", key=f"analyze_{subject}"):
                with st.spinner(f"Analyzing {subject.lower()} concepts..."):
                    
                    # Analyze content
                    analysis = analyzer.analyze_content(notes_text)
                    
                    # Display analysis results
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("Content Type Detected", analysis['type'].title())
                        st.metric("Confidence Score", analysis['score'])
                        
                    with col2:
                        st.metric("Elements Extracted", len(analysis['elements']))
                        
                        # Show content type scores
                        st.write("**All Scores:**")
                        for content_type, score in analysis['all_scores'].items():
                            st.write(f"- {content_type.title()}: {score}")
                    
                    # Show extracted elements
                    if analysis['elements']:
                        st.subheader("Extracted Concepts")
                        element = analysis['elements'][0]
                        
                        if subject == "Physics" and 'values' in element:
                            st.write("**Physics Values Found:**")
                            for key, value in element['values'].items():
                                st.write(f"- {key.title()}: {value}")
                                
                        elif subject == "Chemistry" and 'formulas' in element:
                            st.write("**Chemical Formulas:**")
                            formulas = element.get('formulas', [])
                            if formulas:
                                st.write(", ".join(formulas))
                            else:
                                st.write("None detected")
                                
                        elif subject == "Mathematics" and 'functions' in element:
                            st.write("**Mathematical Functions:**")
                            functions = element.get('functions', [])
                            for func in functions:
                                st.write(f"- {func['expression']}")
                                
                        elif subject == "Biology" and 'terms' in element:
                            st.write("**Biological Terms:**")
                            terms = element.get('terms', [])
                            st.write(", ".join(terms))
                    
                    # Success message
                    st.success(f"""
                    ✅ **Enhanced Analysis Complete!**
                    
                    The animation system now understands the actual {subject.lower()} concepts in your notes:
                    - **Physics**: Uses real velocity, acceleration, and time values
                    - **Chemistry**: Shows actual chemical formulas and reactions
                    - **Mathematics**: Plots your specific functions and equations  
                    - **Biology**: Highlights the biological terms you mentioned
                    
                    When you upload these notes in the main app, the generated video will visualize 
                    these specific concepts instead of generic examples!
                    """)
    
    st.markdown("---")
    st.markdown("### 🎯 Key Improvements")
    
    improvements = [
        "**Physics**: Extracts actual values (velocity=15 m/s, time=2s) and uses them in motion simulations",
        "**Chemistry**: Identifies real chemical formulas (H₂O, CO₂) and shows molecular structures", 
        "**Mathematics**: Finds specific functions (f(x)=2x²-8x+6) and plots them accurately",
        "**Biology**: Recognizes biological terms (nucleus, mitochondria) and shows relevant cell structures"
    ]
    
    for improvement in improvements:
        st.markdown(f"• {improvement}")
    
    st.info("💡 **Tip**: The more specific your notes are with values, formulas, and terms, the better the animations will be!")

if __name__ == "__main__":
    main()