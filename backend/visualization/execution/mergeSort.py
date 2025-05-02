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
        
        # Configuration
        self.array_height = 0.7
        self.array_width = 0.7
        self.level_spacing = 1.5
        self.horizontal_spacing = 1.2
        self.animation_speed = 0.5
        
        # Track all created mobjects with parent-child relationships
        self.array_mobjects = {}  # Key: str(array), Value: (mobject, parent_key)
        self.arrows = []
        self.level_positions = {}
        
        # Create initial visualization
        self.initial_array = tracing_steps[0]["required_fields"]["array"]
        self.initialize_visualization()
        
        # Animate each step
        self.process_steps(tracing_steps[1:])
    
    def initialize_visualization(self):
        """Create initial array visualization"""
        initial_mobj = self.create_array_mobject(
            self.initial_array, 
            level=0,
            position=ORIGIN
        )
        self.array_mobjects[str(self.initial_array)] = (initial_mobj, None)
        self.play(FadeIn(initial_mobj))
        self.wait(self.animation_speed)
        
        # Set up level positions
        max_depth = 3  # Based on your sample data
        for level in range(max_depth + 1):
            self.level_positions[level] = UP * (3 - level) * self.level_spacing
    
    def process_steps(self, steps):
        """Process each step in the trace"""
        for step in steps:
            self.handle_step(step)
    
    def handle_step(self, step):
        """Handle different types of steps"""
        event = step["event"]
        fields = step["required_fields"]
        
        if event == "split":
            self.animate_split(
                fields["parent_array"],
                fields["left_half"],
                fields["right_half"]
            )
        elif event == "merge":
            self.animate_merge(
                fields["left"],
                fields["right"],
                fields["merged"]
            )
        elif event == "complete":
            self.animate_completion(fields["sorted_array"])
    
    def animate_split(self, parent_array, left_half, right_half):
        """Animate splitting an array into two halves"""
        parent_mobj, _ = self.array_mobjects[str(parent_array)]
        level = self.get_level(parent_mobj)
        new_level = level + 1
        
        # Calculate positions
        left_pos = parent_mobj.get_center() + LEFT * self.horizontal_spacing + DOWN * self.level_spacing
        right_pos = parent_mobj.get_center() + RIGHT * self.horizontal_spacing + DOWN * self.level_spacing
        
        # Create left and right halves
        left_mobj = self.create_array_mobject(left_half, new_level, left_pos)
        right_mobj = self.create_array_mobject(right_half, new_level, right_pos)
        
        # Create connecting arrows
        left_arrow = Arrow(
            parent_mobj.get_bottom(),
            left_mobj.get_top(),
            color=BLUE_C,
            buff=0.1,
            stroke_width=3
        )
        right_arrow = Arrow(
            parent_mobj.get_bottom(),
            right_mobj.get_top(),
            color=RED_C,
            buff=0.1,
            stroke_width=3
        )
        
        # Animate
        self.play(
            parent_mobj.animate.set_color(GRAY),
            run_time=self.animation_speed
        )
        self.play(
            AnimationGroup(
                FadeIn(left_mobj, shift=UP*0.3),
                FadeIn(right_mobj, shift=UP*0.3),
                GrowArrow(left_arrow),
                GrowArrow(right_arrow),
                lag_ratio=0.3
            ),
            run_time=self.animation_speed * 1.5
        )
        
        # Store references with parent information
        self.array_mobjects[str(left_half)] = (left_mobj, str(parent_array))
        self.array_mobjects[str(right_half)] = (right_mobj, str(parent_array))
        self.arrows.extend([left_arrow, right_arrow])
        
        # Add split indicator
        split_text = Text("Split", font_size=20, color=YELLOW)
        split_text.next_to(parent_mobj, UP, buff=0.2)
        self.play(Write(split_text), run_time=self.animation_speed/2)
        self.play(FadeOut(split_text), run_time=self.animation_speed/2)
    
    def animate_merge(self, left, right, merged):
        """Animate merging two sorted halves"""
        left_mobj, left_parent_key = self.array_mobjects[str(left)]
        right_mobj, right_parent_key = self.array_mobjects[str(right)]
        
        # Both halves should have the same parent
        parent_key = left_parent_key
        parent_mobj, _ = self.array_mobjects[parent_key]
        
        # Highlight halves being merged
        self.play(
            left_mobj.animate.set_color(BLUE),
            right_mobj.animate.set_color(RED),
            run_time=self.animation_speed
        )
        
        # Create merged array at parent position
        merged_mobj = self.create_array_mobject(
            merged,
            level=self.get_level(parent_mobj),
            position=parent_mobj.get_center(),
            color=GREEN
        )
        
        # Animate elements merging
        merge_animations = []
        for i in range(len(left)):
            merge_animations.append(Transform(left_mobj[i].copy(), merged_mobj[i]))
        for j in range(len(right)):
            merge_animations.append(Transform(right_mobj[j].copy(), merged_mobj[len(left)+j]))
        
        self.play(
            AnimationGroup(*merge_animations, lag_ratio=0.1),
            run_time=self.animation_speed * 2
        )
        
        # Replace parent with merged array
        self.play(
            Transform(parent_mobj, merged_mobj),
            run_time=self.animation_speed
        )
        
        # Clean up
        self.play(
            FadeOut(left_mobj),
            FadeOut(right_mobj),
            *[FadeOut(arrow) for arrow in self.get_connected_arrows(left_mobj, right_mobj)],
            run_time=self.animation_speed
        )
        
        # Update references
        self.array_mobjects[str(merged)] = (parent_mobj, self.array_mobjects[parent_key][1])
        parent_mobj.set_color(WHITE)
    
    def animate_completion(self, sorted_array):
        """Animate final sorted array"""
        final_mobj, _ = self.array_mobjects[str(sorted_array)]
        
        # Celebration animation
        self.play(
            final_mobj.animate.set_color(GOLD).scale(1.1),
            run_time=self.animation_speed
        )
        
        completion_text = Text("Merge Sort Complete!", font_size=36, color=GOLD)
        completion_text.next_to(final_mobj, DOWN, buff=1)
        
        self.play(
            final_mobj.animate.scale(1/1.1).set_color(GREEN),
            Write(completion_text),
            run_time=self.animation_speed * 1.5
        )
        self.wait(2)
    
    def create_array_mobject(self, array, level=0, position=None, color=WHITE):
        """Create a visual representation of an array"""
        if position is None:
            position = self.level_positions[level]
        
        elements = VGroup()
        for num in array:
            # Create element with background
            rect = Rectangle(
                height=self.array_height,
                width=self.array_width,
                color=color,
                fill_opacity=0.3
            )
            num_text = Text(str(num), font_size=24).move_to(rect.get_center())
            element = VGroup(rect, num_text)
            elements.add(element)
        
        # Arrange elements
        elements.arrange(RIGHT, buff=0.1)
        elements.move_to(position)
        
        # Add array identifier
        elements.array_data = array.copy()
        elements.level = level
        
        return elements
    
    def get_level(self, mobject):
        """Get the recursion level of an array mobject"""
        return getattr(mobject, "level", 0)
    
    def get_connected_arrows(self, *mobjects):
        """Get arrows connected to these mobjects"""
        connected = []
        for arrow in self.arrows:
            for mobj in mobjects:
                if (arrow.get_start() == mobj.get_top() or 
                    arrow.get_end() == mobj.get_top()):
                    connected.append(arrow)
        return connected