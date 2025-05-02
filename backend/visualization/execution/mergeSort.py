from manim import *
from typing import Dict, List, Tuple
import numpy as np

import json
import subprocess


# Load and assign data
with open('/Users/navneet/Documents/Internshiptasks/algorithmVisualizer/backend/src/controllers/trace.json') as file:
    data = json.load(file)


graph_input=data["graph"]
tracing_steps_input=data["trace"]
class MergeSortVisualization(Scene):
    def construct(self):
        # Load tracing steps
        tracing_steps = tracing_steps_input
        
        # Create initial array visualization
        initial_array = tracing_steps[0]["required_fields"]["array"]
        array_mobj = self.create_array_visualization(initial_array)
        self.play(FadeIn(array_mobj))
        self.wait(1)
        
        # Create a stack to keep track of recursive calls
        call_stack = []
        current_level = 0
        
        # Animate each step
        for step in tracing_steps[1:]:
            event = step["event"]
            fields = step["required_fields"]
            
            if event == "split":
                # Create visualization for the split
                parent_array = fields["parent_array"]
                left_half = fields["left_half"]
                right_half = fields["right_half"]
                
                # Find the parent array mobject
                parent_mobj = self.find_array_mobject(array_mobj, parent_array)
                
                # Create split animation
                self.play(
                    parent_mobj.animate.set_color(GRAY),
                    run_time=0.5
                )
                
                # Create left and right halves
                left_mobj = self.create_array_visualization(left_half, color=BLUE_E)
                right_mobj = self.create_array_visualization(right_half, color=RED_E)
                
                # Position them below the parent
                group = VGroup(left_mobj, right_mobj)
                group.arrange(RIGHT, buff=1.5)
                group.next_to(parent_mobj, DOWN, buff=1.0)
                
                # Draw arrows from parent to children
                left_arrow = Arrow(
                    parent_mobj.get_bottom(), 
                    left_mobj.get_top(), 
                    color=BLUE_C,
                    buff=0.2
                )
                right_arrow = Arrow(
                    parent_mobj.get_bottom(), 
                    right_mobj.get_top(), 
                    color=RED_C,
                    buff=0.2
                )
                
                # Animate the split
                self.play(
                    FadeIn(left_mobj),
                    FadeIn(right_mobj),
                    GrowArrow(left_arrow),
                    GrowArrow(right_arrow),
                    run_time=1
                )
                
                # Add to call stack
                call_stack.append((parent_mobj, left_mobj, right_mobj, left_arrow, right_arrow))
                current_level += 1
                
            elif event == "merge":
                # Get the left and right halves to merge
                left = fields["left"]
                right = fields["right"]
                merged = fields["merged"]
                
                # Find the left and right mobjects
                left_mobj = self.find_array_mobject(array_mobj, left)
                right_mobj = self.find_array_mobject(array_mobj, right)
                
                # Highlight the halves being merged
                self.play(
                    left_mobj.animate.set_color(BLUE),
                    right_mobj.animate.set_color(RED),
                    run_time=0.5
                )
                
                # Create merged array
                merged_mobj = self.create_array_visualization(merged, color=GREEN_E)
                
                # Position it above the halves being merged
                parent_info = call_stack.pop()
                parent_pos = parent_info[0].get_center()
                merged_mobj.move_to(parent_pos)
                
                # Create merge animation
                self.play(
                    ReplacementTransform(left_mobj.copy(), merged_mobj),
                    ReplacementTransform(right_mobj.copy(), merged_mobj),
                    run_time=1.5
                )
                
                # Remove the old halves and arrows
                self.play(
                    FadeOut(left_mobj),
                    FadeOut(right_mobj),
                    FadeOut(parent_info[3]),  # left arrow
                    FadeOut(parent_info[4]),  # right arrow
                    run_time=0.5
                )
                
                # Replace parent with merged array
                self.play(
                    Transform(parent_info[0], merged_mobj),
                    run_time=0.7
                )
                
                # Reset color
                self.play(
                    parent_info[0].animate.set_color(WHITE),
                    run_time=0.3
                )
                
                current_level -= 1
                
            elif event == "complete":
                # Final sorted array
                sorted_array = fields["sorted_array"]
                final_mobj = self.find_array_mobject(array_mobj, sorted_array)
                
                # Celebration animation
                self.play(
                    final_mobj.animate.set_color(GOLD).scale(1.1),
                    run_time=0.5
                )
                self.play(
                    final_mobj.animate.set_color(GREEN).scale(1/1.1),
                    run_time=0.5
                )
                
                # Add completion text
                completion_text = Text("Merge Sort Complete!", font_size=36, color=GOLD_E)
                completion_text.next_to(final_mobj, DOWN, buff=1.0)
                
                self.play(
                    Write(completion_text),
                    run_time=1
                )
                self.wait(2)
    
    def create_array_visualization(self, array: List, color=WHITE) -> VGroup:
        """Create visual representation of an array"""
        elements = VGroup()
        
        for i, num in enumerate(array):
            # Create rectangle for array element
            rect = Rectangle(
                width=0.8, 
                height=0.8, 
                color=color,
                fill_opacity=0.3
            )
            
            # Add number text
            num_text = Text(str(num), font_size=24).move_to(rect.get_center())
            
            # Group rectangle and text
            element = VGroup(rect, num_text)
            elements.add(element)
        
        # Arrange elements horizontally
        elements.arrange(RIGHT, buff=0.1)
        return elements
    
    def find_array_mobject(self, root_mobj: VGroup, array: List) -> VGroup:
        """Find the mobject representing a specific array in the visualization"""
        # This is a simplified version - in a full implementation you'd need to track
        # which mobject represents which array throughout the animation
        # For this example, we'll just return the first matching mobject we find
        
        # Check if this is the root array
        if len(root_mobj) == len(array):
            match = True
            for i in range(len(array)):
                if root_mobj[i][1].text != str(array[i]):
                    match = False
                    break
            if match:
                return root_mobj
        
        # Recursively check children (not fully implemented in this example)
        # In a complete implementation, you would track parent-child relationships
        
        # For this demo, we'll create a new one if not found
        return self.create_array_visualization(array)