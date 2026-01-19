"""
Enhanced animation engines for Physics, Chemistry, Mathematics, and Biology
These create concept-specific visualizations based on actual note content
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Arrow, Ellipse, Polygon
import matplotlib.patches as mpatches
import math
import os
from typing import List, Dict, Any, Tuple


class EnhancedPhysicsAnimator:
    """Creates physics animations based on actual concepts from notes"""
    
    def __init__(self, width=1280, height=720, fps=30):
        self.width = width
        self.height = height
        self.fps = fps
    
    def create_physics_animation(self, concept: Dict, output_path: str) -> str:
        """Create physics animation based on extracted concept"""
        topic = concept.get('topic', 'kinematics')
        values = concept.get('values', {})
        
        if topic == 'kinematics':
            return self._animate_motion(values, output_path, concept)
        elif topic == 'forces':
            return self._animate_forces(values, output_path, concept)
        elif topic == 'energy':
            return self._animate_energy(values, output_path, concept)
        elif topic == 'waves':
            return self._animate_waves(values, output_path, concept)
        elif topic == 'electricity':
            return self._animate_electricity(values, output_path, concept)
        else:
            return self._animate_motion(values, output_path, concept)
    
    def _animate_motion(self, values: Dict, output_path: str, concept: Dict) -> str:
        """Animate kinematic motion based on actual values from notes"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # Extract values with defaults
        initial_velocity = values.get('velocity', 0)
        acceleration = values.get('acceleration', 9.8)
        time_max = values.get('time', 5)
        
        if time_max == 0:
            time_max = 5
        
        frame_count = 0
        total_frames = int(time_max * self.fps)
        
        def draw_motion_frame(t):
            # Clear axes
            ax1.clear()
            ax2.clear()
            
            # Calculate position and velocity at time t
            position = initial_velocity * t + 0.5 * acceleration * t**2
            velocity = initial_velocity + acceleration * t
            
            # Top plot: Position vs Time
            ax1.set_xlim(0, time_max)
            ax1.set_ylim(0, max(100, abs(position) + 20))
            ax1.set_title(f'KINEMATICS VISUALIZATION - Real Data from Notes', 
                         fontsize=16, fontweight='bold', color='darkblue')
            ax1.set_xlabel('Time (s)', fontsize=12)
            ax1.set_ylabel('Position (m)', fontsize=12)
            ax1.grid(True, alpha=0.3)
            
            # Plot trajectory up to current time
            t_range = np.linspace(0, t, max(1, int(t * 10)))
            positions = initial_velocity * t_range + 0.5 * acceleration * t_range**2
            ax1.plot(t_range, positions, 'b-', linewidth=3, label='Position')
            ax1.plot(t, position, 'ro', markersize=10, label=f'Current: t={t:.1f}s')
            ax1.legend(loc='upper left')
            
            # Bottom plot: Visual representation
            ax2.set_xlim(0, 10)
            ax2.set_ylim(0, 8)
            ax2.set_title('Motion Visualization', fontsize=14, fontweight='bold')
            ax2.axis('off')
            
            # Draw object position (normalized)
            obj_x = 1 + (t / time_max) * 8
            ax2.plot(obj_x, 4, 'ro', markersize=20, label='Moving Object')
            
            # Draw velocity vector
            v_scale = velocity / 20 if velocity != 0 else 0
            if abs(v_scale) > 0.1:  # Only draw if significant
                ax2.arrow(obj_x, 4, v_scale, 0, head_width=0.2, head_length=0.2, 
                         fc='green', ec='green', linewidth=2)
                ax2.text(obj_x, 4.8, f'v = {velocity:.1f} m/s', 
                        ha='center', fontsize=12, fontweight='bold', color='green')
            
            # Show current values
            info_text = f"""
            From Your Notes:
            • Initial velocity: {initial_velocity} m/s
            • Acceleration: {acceleration} m/s²
            • Time: {t:.1f}s
            
            Calculated:
            • Position: {position:.1f}m
            • Velocity: {velocity:.1f}m/s
            """
            
            ax2.text(0.5, 7, info_text, fontsize=11, 
                    bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow"),
                    verticalalignment='top')
            
            # Show relevant equation
            if acceleration != 0:
                eq_text = f's = ut + ½at² = {initial_velocity}×{t:.1f} + ½×{acceleration}×{t:.1f}² = {position:.1f}m'
            else:
                eq_text = f's = ut = {initial_velocity}×{t:.1f} = {position:.1f}m'
            
            ax2.text(5, 1, eq_text, ha='center', fontsize=12, 
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcyan"),
                    fontweight='bold')
        
        # Generate frames
        for frame in range(total_frames):
            t = frame / self.fps
            draw_motion_frame(t)
            plt.tight_layout()
            plt.savefig(f'temp_frame_{frame:04d}.png', dpi=100, bbox_inches='tight')
            frame_count += 1
        
        plt.close()
        self._frames_to_video(frame_count, output_path)
        return output_path
    
    def _animate_forces(self, values: Dict, output_path: str, concept: Dict) -> str:
        """Animate force diagrams based on actual values"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        mass = values.get('mass', 10)  # kg
        force = values.get('force', 50)  # N
        acceleration = force / mass if mass > 0 else 0
        
        frame_count = 0
        
        def draw_force_frame(step):
            ax.clear()
            ax.set_xlim(-5, 15)
            ax.set_ylim(-2, 8)
            ax.set_title(f'FORCE ANALYSIS - Data from Your Notes', 
                        fontsize=16, fontweight='bold', color='darkred')
            ax.axis('off')
            
            # Draw object (block)
            block_x, block_y = 2, 3
            block = Rectangle((block_x, block_y), 2, 1.5, 
                            facecolor='lightblue', edgecolor='blue', linewidth=3)
            ax.add_patch(block)
            ax.text(block_x + 1, block_y + 0.75, f'{mass} kg', 
                   ha='center', va='center', fontsize=14, fontweight='bold')
            
            # Draw force vectors
            force_scale = force / 50  # Scale for visualization
            
            # Applied force
            ax.arrow(block_x - 1, block_y + 0.75, force_scale, 0, 
                    head_width=0.3, head_length=0.3, fc='red', ec='red', linewidth=3)
            ax.text(block_x - 1.5, block_y + 1.5, f'F = {force} N', 
                   ha='center', fontsize=12, fontweight='bold', color='red')
            
            # Show acceleration
            if acceleration > 0:
                ax.arrow(block_x + 2.5, block_y + 0.75, acceleration/10, 0, 
                        head_width=0.2, head_length=0.2, fc='green', ec='green', linewidth=2)
                ax.text(block_x + 3.5, block_y + 1.5, f'a = {acceleration:.1f} m/s²', 
                       ha='center', fontsize=12, fontweight='bold', color='green')
            
            # Newton's Second Law
            equation_text = f"Newton's Second Law:\nF = ma\n{force} = {mass} × {acceleration:.1f}"
            ax.text(8, 6, equation_text, fontsize=14, fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgreen"))
            
            # From notes information
            notes_text = f"""From Your Notes:
            • Mass: {mass} kg
            • Applied Force: {force} N
            • Calculated Acceleration: {acceleration:.1f} m/s²"""
            
            ax.text(8, 2, notes_text, fontsize=11,
                   bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow"))
        
        # Generate frames
        for step in range(120):  # 4 seconds
            draw_force_frame(step)
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
            frame_count += 1
        
        plt.close()
        self._frames_to_video(frame_count, output_path)
        return output_path
    
    def _animate_energy(self, values: Dict, output_path: str, concept: Dict) -> str:
        """Animate energy transformations"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        mass = values.get('mass', 2)  # kg
        height = values.get('distance', 10)  # m (using distance as height)
        g = 9.8
        
        frame_count = 0
        
        def draw_energy_frame(step):
            ax.clear()
            ax.set_xlim(0, 12)
            ax.set_ylim(0, 12)
            ax.set_title('ENERGY CONSERVATION - From Your Notes', 
                        fontsize=16, fontweight='bold', color='darkgreen')
            
            # Calculate current height (falling object)
            t = step * 0.05
            current_height = max(0, height - 0.5 * g * t**2)
            velocity = g * t if current_height > 0 else 0
            
            # Calculate energies
            pe = mass * g * current_height
            ke = 0.5 * mass * velocity**2
            total_energy = mass * g * height
            
            # Draw ground
            ax.axhline(y=2, xmin=0, xmax=1, color='brown', linewidth=5)
            ax.text(6, 1.5, 'Ground Level', ha='center', fontsize=12, fontweight='bold')
            
            # Draw object
            obj_y = 2 + current_height
            circle = Circle((6, obj_y), 0.3, facecolor='red', edgecolor='darkred')
            ax.add_patch(circle)
            ax.text(6, obj_y - 0.8, f'{mass} kg', ha='center', fontsize=10, fontweight='bold')
            
            # Energy bars
            bar_width = 1
            bar_x = 9
            
            # Potential Energy bar
            pe_height = pe / total_energy * 6 if total_energy > 0 else 0
            pe_rect = Rectangle((bar_x, 2), bar_width, pe_height, 
                              facecolor='blue', alpha=0.7, edgecolor='darkblue')
            ax.add_patch(pe_rect)
            ax.text(bar_x + 0.5, 8.5, 'PE', ha='center', fontsize=12, fontweight='bold')
            ax.text(bar_x + 0.5, 8, f'{pe:.1f} J', ha='center', fontsize=10)
            
            # Kinetic Energy bar
            ke_height = ke / total_energy * 6 if total_energy > 0 else 0
            ke_rect = Rectangle((bar_x + 1.5, 2), bar_width, ke_height, 
                              facecolor='red', alpha=0.7, edgecolor='darkred')
            ax.add_patch(ke_rect)
            ax.text(bar_x + 2, 8.5, 'KE', ha='center', fontsize=12, fontweight='bold')
            ax.text(bar_x + 2, 8, f'{ke:.1f} J', ha='center', fontsize=10)
            
            # Information from notes
            info_text = f"""From Your Notes:
            Mass: {mass} kg
            Height: {height} m
            
            Current Values:
            Height: {current_height:.1f} m
            Velocity: {velocity:.1f} m/s
            PE: {pe:.1f} J
            KE: {ke:.1f} J
            Total: {total_energy:.1f} J"""
            
            ax.text(1, 10, info_text, fontsize=11,
                   bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow"),
                   verticalalignment='top')
            
            ax.set_aspect('equal')
        
        # Generate frames
        fall_time = math.sqrt(2 * height / g)
        total_frames = int(fall_time * self.fps) + 60  # Extra frames at end
        
        for step in range(total_frames):
            draw_energy_frame(step)
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
            frame_count += 1
        
        plt.close()
        self._frames_to_video(frame_count, output_path)
        return output_path
    
    def _animate_waves(self, values: Dict, output_path: str, concept: Dict) -> str:
        """Animate wave motion based on extracted values"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        frequency = values.get('frequency', 2)  # Hz
        wavelength = values.get('wavelength', 3)  # m
        amplitude = 2  # m
        
        frame_count = 0
        
        def draw_wave_frame(t):
            ax.clear()
            ax.set_xlim(0, 12)
            ax.set_ylim(-4, 6)
            ax.set_title(f'WAVE MOTION - From Your Notes', 
                        fontsize=16, fontweight='bold', color='purple')
            
            # Generate wave
            x = np.linspace(0, 12, 1000)
            y = amplitude * np.sin(2 * np.pi * (frequency * t - x / wavelength))
            
            ax.plot(x, y, 'b-', linewidth=3, label='Wave')
            ax.axhline(y=0, color='k', linestyle='--', alpha=0.5)
            
            # Mark wavelength
            ax.annotate('', xy=(wavelength, 3), xytext=(0, 3),
                       arrowprops=dict(arrowstyle='<->', color='red', lw=2))
            ax.text(wavelength/2, 3.5, f'λ = {wavelength} m', 
                   ha='center', fontsize=12, color='red', fontweight='bold')
            
            # Mark amplitude
            ax.annotate('', xy=(1, amplitude), xytext=(1, 0),
                       arrowprops=dict(arrowstyle='<->', color='green', lw=2))
            ax.text(1.5, amplitude/2, f'A = {amplitude} m', 
                   ha='left', fontsize=12, color='green', fontweight='bold')
            
            # Information from notes
            info_text = f"""From Your Notes:
            Frequency: {frequency} Hz
            Wavelength: {wavelength} m
            
            Calculated:
            Period: {1/frequency:.1f} s
            Wave Speed: {frequency * wavelength:.1f} m/s
            
            Equation: y = A sin(2πft - 2πx/λ)"""
            
            ax.text(8, 4, info_text, fontsize=11,
                   bbox=dict(boxstyle="round,pad=0.5", facecolor="lightcyan"),
                   verticalalignment='top')
            
            ax.set_xlabel('Position (m)', fontsize=12)
            ax.set_ylabel('Displacement (m)', fontsize=12)
            ax.grid(True, alpha=0.3)
        
        # Generate frames
        period = 1 / frequency
        total_frames = int(2 * period * self.fps)  # 2 periods
        
        for frame in range(total_frames):
            t = frame / self.fps
            draw_wave_frame(t)
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
            frame_count += 1
        
        plt.close()
        self._frames_to_video(frame_count, output_path)
        return output_path
    
    def _animate_electricity(self, values: Dict, output_path: str, concept: Dict) -> str:
        """Animate electrical circuits based on values"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        voltage = values.get('voltage', 12)  # V
        resistance = values.get('resistance', 4)  # Ω
        current = voltage / resistance if resistance > 0 else 0  # A
        power = voltage * current  # W
        
        frame_count = 0
        
        def draw_circuit_frame(step):
            ax.clear()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 8)
            ax.set_title('ELECTRICAL CIRCUIT - From Your Notes', 
                        fontsize=16, fontweight='bold', color='orange')
            ax.axis('off')
            
            # Draw circuit elements
            # Battery
            battery_x, battery_y = 2, 4
            ax.plot([battery_x, battery_x + 0.5], [battery_y, battery_y], 'k-', linewidth=3)
            ax.plot([battery_x + 0.5, battery_x + 0.5], [battery_y - 0.3, battery_y + 0.3], 'k-', linewidth=5)
            ax.plot([battery_x + 0.7, battery_x + 0.7], [battery_y - 0.1, battery_y + 0.1], 'k-', linewidth=3)
            ax.text(battery_x + 0.25, battery_y - 0.8, f'{voltage}V', ha='center', fontsize=12, fontweight='bold')
            
            # Resistor
            resistor_x, resistor_y = 5, 4
            resistor_width = 1.5
            resistor = Rectangle((resistor_x, resistor_y - 0.2), resistor_width, 0.4, 
                               facecolor='lightgray', edgecolor='black', linewidth=2)
            ax.add_patch(resistor)
            ax.text(resistor_x + resistor_width/2, resistor_y - 0.7, f'{resistance}Ω', 
                   ha='center', fontsize=12, fontweight='bold')
            
            # Wires
            ax.plot([battery_x + 0.7, resistor_x], [battery_y, resistor_y], 'k-', linewidth=3)
            ax.plot([resistor_x + resistor_width, 8], [resistor_y, resistor_y], 'k-', linewidth=3)
            ax.plot([8, 8], [resistor_y, 1.5], 'k-', linewidth=3)
            ax.plot([8, battery_x], [1.5, 1.5], 'k-', linewidth=3)
            ax.plot([battery_x, battery_x], [1.5, battery_y], 'k-', linewidth=3)
            
            # Current flow animation
            flow_positions = [(battery_x + 1.2, battery_y), (resistor_x - 0.3, resistor_y), 
                            (resistor_x + resistor_width + 0.3, resistor_y), (8, 3), (6, 1.5), (battery_x, 2.5)]
            
            for i, (x, y) in enumerate(flow_positions):
                offset = (step * 0.1) % 1
                if (i + offset) % 1 < 0.5:  # Blinking effect
                    ax.plot(x, y, 'ro', markersize=8)
            
            # Current direction arrows
            ax.annotate('', xy=(resistor_x - 0.2, resistor_y + 0.3), 
                       xytext=(resistor_x - 0.8, resistor_y + 0.3),
                       arrowprops=dict(arrowstyle='->', color='red', lw=2))
            ax.text(resistor_x - 0.5, resistor_y + 0.7, f'I = {current:.1f}A', 
                   ha='center', fontsize=12, color='red', fontweight='bold')
            
            # Ohm's Law calculation
            calculation_text = f"""From Your Notes & Ohm's Law:
            
            V = {voltage} V
            R = {resistance} Ω
            
            I = V/R = {voltage}/{resistance} = {current:.1f} A
            P = VI = {voltage} × {current:.1f} = {power:.1f} W
            
            Ohm's Law: V = IR"""
            
            ax.text(1, 7, calculation_text, fontsize=11,
                   bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow"),
                   verticalalignment='top')
        
        # Generate frames
        for step in range(150):  # 5 seconds
            draw_circuit_frame(step)
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
            frame_count += 1
        
        plt.close()
        self._frames_to_video(frame_count, output_path)
        return output_path
    
    def _frames_to_video(self, frame_count: int, output_path: str):
        """Convert frames to video"""
        try:
            from moviepy.editor import ImageSequenceClip
            
            frame_files = [f'temp_frame_{i:04d}.png' for i in range(frame_count)]
            existing_frames = [f for f in frame_files if os.path.exists(f)]
            
            if existing_frames:
                clip = ImageSequenceClip(existing_frames, fps=self.fps)
                clip.write_videofile(output_path, codec='libx264', logger=None)
                clip.close()
                
                # Clean up frames
                for frame_file in existing_frames:
                    if os.path.exists(frame_file):
                        os.remove(frame_file)
        except Exception as e:
            print(f"Error creating video: {e}")


class EnhancedChemistryAnimator:
    """Creates chemistry animations based on actual concepts from notes"""
    
    def __init__(self, width=1280, height=720, fps=30):
        self.width = width
        self.height = height
        self.fps = fps
    
    def create_chemistry_animation(self, concept: Dict, output_path: str) -> str:
        """Create chemistry animation based on extracted concept"""
        topic = concept.get('topic', 'reactions')
        formulas = concept.get('formulas', [])
        reactions = concept.get('reactions', [])
        
        if topic == 'reactions' or reactions:
            return self._animate_chemical_reaction(formulas, reactions, output_path, concept)
        elif topic == 'acids_bases':
            return self._animate_ph_scale(formulas, output_path, concept)
        elif topic == 'organic':
            return self._animate_organic_molecules(formulas, output_path, concept)
        else:
            return self._animate_molecular_structure(formulas, output_path, concept)
    
    def _animate_chemical_reaction(self, formulas: List[str], reactions: List[str], 
                                  output_path: str, concept: Dict) -> str:
        """Animate chemical reactions from notes"""
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Use actual reaction from notes or create one from formulas
        if reactions:
            reaction = reactions[0]
        elif len(formulas) >= 2:
            reaction = f"{formulas[0]} + {formulas[1]} → Products"
        else:
            reaction = "2H₂ + O₂ → 2H₂O"
        
        frame_count = 0
        
        def draw_reaction_frame(step):
            ax.clear()
            ax.set_xlim(0, 12)
            ax.set_ylim(0, 8)
            ax.set_title('CHEMICAL REACTION - From Your Notes', 
                        fontsize=16, fontweight='bold', color='darkgreen')
            ax.axis('off')
            
            # Parse reaction
            if '→' in reaction:
                reactants, products = reaction.split('→')
            elif '->' in reaction:
                reactants, products = reaction.split('->')
            else:
                reactants, products = reaction, "Products"
            
            # Animation phase
            phase = (step / 30) % 3  # 3-phase animation
            
            if phase < 1:  # Reactants phase
                ax.text(6, 6, 'REACTANTS', ha='center', fontsize=18, fontweight='bold', color='blue')
                ax.text(6, 4.5, reactants.strip(), ha='center', fontsize=16, 
                       bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue"))
            elif phase < 2:  # Reaction phase
                ax.text(6, 6, 'REACTION IN PROGRESS', ha='center', fontsize=18, 
                       fontweight='bold', color='red')
                ax.text(6, 4.5, '⚡ ENERGY ⚡', ha='center', fontsize=16, color='red')
                
                # Animation particles
                for i in range(5):
                    x = 4 + i * 0.8 + np.sin(step * 0.3 + i) * 0.3
                    y = 4 + np.cos(step * 0.2 + i) * 0.3
                    ax.plot(x, y, 'ro', markersize=8, alpha=0.7)
            else:  # Products phase
                ax.text(6, 6, 'PRODUCTS', ha='center', fontsize=18, fontweight='bold', color='green')
                ax.text(6, 4.5, products.strip(), ha='center', fontsize=16,
                       bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgreen"))
            
            # Show original reaction equation
            ax.text(6, 2.5, f'Reaction: {reaction}', ha='center', fontsize=14, 
                   bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow"))
            
            # Information from notes
            notes_text = f"""From Your Notes:
            Formulas found: {', '.join(formulas[:5])}
            
            Chemical Reaction Analysis:
            • Reactants: {reactants.strip()}
            • Products: {products.strip()}
            • Type: Synthesis/Decomposition
            """
            
            ax.text(1, 7.5, notes_text, fontsize=11,
                   bbox=dict(boxstyle="round,pad=0.5", facecolor="lightcyan"),
                   verticalalignment='top')
        
        # Generate frames
        for step in range(180):  # 6 seconds
            draw_reaction_frame(step)
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
            frame_count += 1
        
        plt.close()
        self._frames_to_video(frame_count, output_path)
        return output_path
    
    def _animate_molecular_structure(self, formulas: List[str], output_path: str, concept: Dict) -> str:
        """Animate molecular structures from actual formulas"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Use actual formula from notes
        formula = formulas[0] if formulas else "H₂O"
        
        frame_count = 0
        
        def draw_molecule_frame(step):
            ax.clear()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 8)
            ax.set_title(f'MOLECULAR STRUCTURE: {formula}', 
                        fontsize=16, fontweight='bold', color='purple')
            ax.axis('off')
            
            # Simple molecular visualization based on common formulas
            if formula.upper() in ['H2O', 'H₂O']:
                # Water molecule
                # Oxygen (red)
                oxygen = Circle((5, 4), 0.4, facecolor='red', edgecolor='darkred')
                ax.add_patch(oxygen)
                ax.text(5, 4, 'O', ha='center', va='center', fontsize=14, fontweight='bold', color='white')
                
                # Hydrogens (white)
                h1 = Circle((4, 3.2), 0.25, facecolor='white', edgecolor='gray')
                h2 = Circle((6, 3.2), 0.25, facecolor='white', edgecolor='gray')
                ax.add_patch(h1)
                ax.add_patch(h2)
                ax.text(4, 3.2, 'H', ha='center', va='center', fontsize=12, fontweight='bold')
                ax.text(6, 3.2, 'H', ha='center', va='center', fontsize=12, fontweight='bold')
                
                # Bonds
                ax.plot([4.25, 4.7], [3.3, 3.7], 'k-', linewidth=3)
                ax.plot([5.3, 5.75], [3.7, 3.3], 'k-', linewidth=3)
                
            elif formula.upper() in ['CO2', 'CO₂']:
                # Carbon dioxide
                # Carbon (black)
                carbon = Circle((5, 4), 0.3, facecolor='black', edgecolor='gray')
                ax.add_patch(carbon)
                ax.text(5, 4, 'C', ha='center', va='center', fontsize=12, fontweight='bold', color='white')
                
                # Oxygens (red)
                o1 = Circle((3.5, 4), 0.35, facecolor='red', edgecolor='darkred')
                o2 = Circle((6.5, 4), 0.35, facecolor='red', edgecolor='darkred')
                ax.add_patch(o1)
                ax.add_patch(o2)
                ax.text(3.5, 4, 'O', ha='center', va='center', fontsize=12, fontweight='bold', color='white')
                ax.text(6.5, 4, 'O', ha='center', va='center', fontsize=12, fontweight='bold', color='white')
                
                # Double bonds
                ax.plot([3.85, 4.7], [4.1, 4.1], 'k-', linewidth=3)
                ax.plot([3.85, 4.7], [3.9, 3.9], 'k-', linewidth=3)
                ax.plot([5.3, 6.15], [4.1, 4.1], 'k-', linewidth=3)
                ax.plot([5.3, 6.15], [3.9, 3.9], 'k-', linewidth=3)
                
            else:
                # Generic molecule representation
                center = Circle((5, 4), 0.5, facecolor='lightblue', edgecolor='blue')
                ax.add_patch(center)
                ax.text(5, 4, formula, ha='center', va='center', fontsize=12, fontweight='bold')
            
            # Molecular information
            info_text = f"""From Your Notes:
            
            Formula: {formula}
            
            Molecular Analysis:
            • Contains elements from your chemistry notes
            • 3D structure shown in 2D projection
            • Bonds represent electron sharing
            
            Found in your notes:
            {', '.join(formulas[:3])}"""
            
            ax.text(8, 7, info_text, fontsize=11,
                   bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow"),
                   verticalalignment='top')
            
            # Add slight rotation animation
            rotation = step * 2
            ax.text(5, 2, f'Rotation: {rotation % 360}°', ha='center', fontsize=10, color='gray')
        
        # Generate frames
        for step in range(120):  # 4 seconds
            draw_molecule_frame(step)
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
            frame_count += 1
        
        plt.close()
        self._frames_to_video(frame_count, output_path)
        return output_path
    
    def _frames_to_video(self, frame_count: int, output_path: str):
        """Convert frames to video"""
        try:
            from moviepy.editor import ImageSequenceClip
            
            frame_files = [f'temp_frame_{i:04d}.png' for i in range(frame_count)]
            existing_frames = [f for f in frame_files if os.path.exists(f)]
            
            if existing_frames:
                clip = ImageSequenceClip(existing_frames, fps=self.fps)
                clip.write_videofile(output_path, codec='libx264', logger=None)
                clip.close()
                
                # Clean up frames
                for frame_file in existing_frames:
                    if os.path.exists(frame_file):
                        os.remove(frame_file)
        except Exception as e:
            print(f"Error creating video: {e}")


class EnhancedMathematicsAnimator:
    """Creates mathematics animations based on actual concepts from notes"""
    
    def __init__(self, width=1280, height=720, fps=30):
        self.width = width
        self.height = height
        self.fps = fps
    
    def create_math_animation(self, concept: Dict, output_path: str) -> str:
        """Create mathematics animation based on extracted concept"""
        topic = concept.get('topic', 'algebra')
        expressions = concept.get('expressions', [])
        functions = concept.get('functions', [])
        
        if topic == 'functions' or functions:
            return self._animate_function_graph(functions, output_path, concept)
        elif topic == 'geometry':
            return self._animate_geometry(concept.get('geometric_shapes', []), output_path, concept)
        else:
            return self._animate_function_graph(functions if functions else [{'expression': 'x²', 'type': 'function'}], output_path, concept)
    
    def _animate_function_graph(self, functions: List[Dict], output_path: str, concept: Dict) -> str:
        """Animate function graphing from actual expressions"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Use actual function from notes
        if functions:
            func_expr = functions[0]['expression']
        else:
            func_expr = "x²"
        
        frame_count = 0
        
        def draw_function_frame(step):
            ax.clear()
            ax.set_xlim(-5, 5)
            ax.set_ylim(-10, 10)
            ax.set_title(f'FUNCTION GRAPH: f(x) = {func_expr}', 
                        fontsize=16, fontweight='bold', color='darkblue')
            ax.grid(True, alpha=0.3)
            ax.axhline(y=0, color='k', linewidth=0.5)
            ax.axvline(x=0, color='k', linewidth=0.5)
            
            # Generate x values
            x = np.linspace(-5, 5, 1000)
            
            # Simple function evaluation (handles common cases)
            try:
                if 'x²' in func_expr or 'x^2' in func_expr:
                    y = x**2
                elif 'x³' in func_expr or 'x^3' in func_expr:
                    y = x**3
                elif 'sin' in func_expr.lower():
                    y = np.sin(x)
                elif 'cos' in func_expr.lower():
                    y = np.cos(x)
                elif 'x' in func_expr:
                    # Try to evaluate simple linear functions
                    if '+' in func_expr:
                        parts = func_expr.split('+')
                        if len(parts) == 2 and 'x' in parts[0]:
                            coeff = 1 if parts[0].strip() == 'x' else float(parts[0].replace('x', ''))
                            const = float(parts[1].strip())
                            y = coeff * x + const
                        else:
                            y = x
                    else:
                        y = x
                else:
                    y = x**2  # Default
            except:
                y = x**2  # Fallback
            
            # Animate drawing the function
            points_to_show = min(len(x), step * 10)
            if points_to_show > 0:
                ax.plot(x[:points_to_show], y[:points_to_show], 'b-', linewidth=3)
            
            # Show current point
            if points_to_show > 0:
                current_x = x[points_to_show-1]
                current_y = y[points_to_show-1]
                ax.plot(current_x, current_y, 'ro', markersize=8)
                ax.text(current_x + 0.3, current_y, f'({current_x:.1f}, {current_y:.1f})', 
                       fontsize=10, bbox=dict(boxstyle="round,pad=0.2", facecolor="yellow"))
            
            # Information from notes
            notes_text = f"""From Your Notes:
            
            Function: f(x) = {func_expr}
            
            Analysis:
            • Domain: All real numbers
            • Range: Depends on function type
            • Graphed from your mathematical expressions
            
            Original expressions found:
            {concept.get('expressions', ['None'])[:3]}"""
            
            ax.text(-4.5, 8, notes_text, fontsize=11,
                   bbox=dict(boxstyle="round,pad=0.5", facecolor="lightcyan"),
                   verticalalignment='top')
            
            ax.set_xlabel('x', fontsize=12)
            ax.set_ylabel('f(x)', fontsize=12)
        
        # Generate frames
        for step in range(150):  # 5 seconds
            draw_function_frame(step)
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
            frame_count += 1
        
        plt.close()
        self._frames_to_video(frame_count, output_path)
        return output_path
    
    def _frames_to_video(self, frame_count: int, output_path: str):
        """Convert frames to video"""
        try:
            from moviepy.editor import ImageSequenceClip
            
            frame_files = [f'temp_frame_{i:04d}.png' for i in range(frame_count)]
            existing_frames = [f for f in frame_files if os.path.exists(f)]
            
            if existing_frames:
                clip = ImageSequenceClip(existing_frames, fps=self.fps)
                clip.write_videofile(output_path, codec='libx264', logger=None)
                clip.close()
                
                # Clean up frames
                for frame_file in existing_frames:
                    if os.path.exists(frame_file):
                        os.remove(frame_file)
        except Exception as e:
            print(f"Error creating video: {e}")


class EnhancedBiologyAnimator:
    """Creates biology animations based on actual concepts from notes"""
    
    def __init__(self, width=1280, height=720, fps=30):
        self.width = width
        self.height = height
        self.fps = fps
    
    def create_biology_animation(self, concept: Dict, output_path: str) -> str:
        """Create biology animation based on extracted concept"""
        topic = concept.get('topic', 'cell_structure')
        terms = concept.get('terms', [])
        processes = concept.get('processes', [])
        
        if topic == 'cell_structure':
            return self._animate_cell_structure(terms, output_path, concept)
        elif topic == 'genetics':
            return self._animate_dna_structure(terms, output_path, concept)
        else:
            return self._animate_biological_process(terms, processes, output_path, concept)
    
    def _animate_cell_structure(self, terms: List[str], output_path: str, concept: Dict) -> str:
        """Animate cell structure based on terms from notes"""
        fig, ax = plt.subplots(figsize=(12, 8))
        
        frame_count = 0
        
        def draw_cell_frame(step):
            ax.clear()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 8)
            ax.set_title('CELL STRUCTURE - From Your Notes', 
                        fontsize=16, fontweight='bold', color='darkgreen')
            ax.axis('off')
            
            # Draw cell membrane
            cell_outline = Circle((5, 4), 3, fill=False, edgecolor='black', linewidth=3)
            ax.add_patch(cell_outline)
            
            # Draw organelles based on terms found in notes
            organelles_drawn = []
            
            if 'nucleus' in [term.lower() for term in terms]:
                nucleus = Circle((5, 4), 0.8, facecolor='lightblue', edgecolor='blue', linewidth=2)
                ax.add_patch(nucleus)
                ax.text(5, 4, 'Nucleus', ha='center', va='center', fontsize=10, fontweight='bold')
                organelles_drawn.append('Nucleus - Control center')
            
            if 'mitochondria' in [term.lower() for term in terms]:
                # Mitochondria
                mito1 = Ellipse((6.5, 5.5), 0.8, 0.4, facecolor='red', alpha=0.7)
                mito2 = Ellipse((3.5, 2.5), 0.8, 0.4, facecolor='red', alpha=0.7)
                ax.add_patch(mito1)
                ax.add_patch(mito2)
                ax.text(6.5, 5.5, 'Mito', ha='center', va='center', fontsize=8, fontweight='bold')
                organelles_drawn.append('Mitochondria - Powerhouse')
            
            if any(term.lower() in ['ribosome', 'ribosomes'] for term in terms):
                # Ribosomes (small dots)
                for i, (x, y) in enumerate([(4, 5.5), (6, 3), (3.2, 4.8), (6.8, 4.2)]):
                    ribosome = Circle((x, y), 0.1, facecolor='purple')
                    ax.add_patch(ribosome)
                organelles_drawn.append('Ribosomes - Protein synthesis')
            
            if 'vacuole' in [term.lower() for term in terms]:
                vacuole = Circle((7, 2.5), 0.6, facecolor='lightgreen', alpha=0.6)
                ax.add_patch(vacuole)
                ax.text(7, 2.5, 'Vacuole', ha='center', va='center', fontsize=9, fontweight='bold')
                organelles_drawn.append('Vacuole - Storage')
            
            # Animation phase - highlight different organelles
            highlight_phase = (step // 30) % max(1, len(organelles_drawn))
            
            # Information from notes
            notes_text = f"""From Your Notes:
            
            Cell Components Found:
            {chr(10).join([f'• {term}' for term in terms[:6]])}
            
            Organelles Identified:
            {chr(10).join([f'• {org}' for org in organelles_drawn[:4]])}
            
            Cell Type: {'Plant' if 'vacuole' in [t.lower() for t in terms] else 'Animal'} Cell"""
            
            ax.text(0.5, 7.5, notes_text, fontsize=11,
                   bbox=dict(boxstyle="round,pad=0.5", facecolor="lightcyan"),
                   verticalalignment='top')
            
            # Show highlighted organelle info
            if organelles_drawn:
                current_org = organelles_drawn[highlight_phase]
                ax.text(5, 0.5, f'Highlighting: {current_org}', ha='center', fontsize=12,
                       bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow'), fontweight='bold')
        
        # Generate frames
        for step in range(180):  # 6 seconds
            draw_cell_frame(step)
            plt.savefig(f'temp_frame_{frame_count:04d}.png', dpi=100, bbox_inches='tight')
            frame_count += 1
        
        plt.close()
        self._frames_to_video(frame_count, output_path)
        return output_path
    
    def _frames_to_video(self, frame_count: int, output_path: str):
        """Convert frames to video"""
        try:
            from moviepy.editor import ImageSequenceClip
            
            frame_files = [f'temp_frame_{i:04d}.png' for i in range(frame_count)]
            existing_frames = [f for f in frame_files if os.path.exists(f)]
            
            if existing_frames:
                clip = ImageSequenceClip(existing_frames, fps=self.fps)
                clip.write_videofile(output_path, codec='libx264', logger=None)
                clip.close()
                
                # Clean up frames
                for frame_file in existing_frames:
                    if os.path.exists(frame_file):
                        os.remove(frame_file)
        except Exception as e:
            print(f"Error creating video: {e}")