from manim import *
from typing import Dict, List, Tuple
import numpy as np
tracing_steps_input=[
    {
      "event": "init",
      "description": "Initialization of the algorithm",
      "required_fields": {
        "start": "A",
        "stack": [
          "A"
        ],
        "visited": []
      }
    },
    {
      "event": "push",
      "description": "When a node is pushed to the stack",
      "required_fields": {
        "node": "A",
        "stack": [
          "A"
        ],
        "visited": []
      }
    },
    {
      "event": "pop",
      "description": "When a node is processed from the stack",
      "required_fields": {
        "node": "A",
        "stack": [],
        "visited": [
          "A"
        ]
      }
    },
    {
      "event": "neighbor_check",
      "description": "When checking a neighbor node",
      "required_fields": {
        "current": "A",
        "neighbor": "B",
        "visited": [
          "A"
        ]
      }
    },
    {
      "event": "push",
      "description": "When a node is pushed to the stack",
      "required_fields": {
        "node": "B",
        "stack": [
          "B"
        ],
        "visited": [
          "A"
        ]
      }
    },
    {
      "event": "pop",
      "description": "When a node is processed from the stack",
      "required_fields": {
        "node": "B",
        "stack": [],
        "visited": [
          "A",
          "B"
        ]
      }
    },
    {
      "event": "neighbor_check",
      "description": "When checking a neighbor node",
      "required_fields": {
        "current": "B",
        "neighbor": "D",
        "visited": [
          "A",
          "B"
        ]
      }
    },
    {
      "event": "push",
      "description": "When a node is pushed to the stack",
      "required_fields": {
        "node": "D",
        "stack": [
          "D"
        ],
        "visited": [
          "A",
          "B"
        ]
      }
    },
    {
      "event": "pop",
      "description": "When a node is processed from the stack",
      "required_fields": {
        "node": "D",
        "stack": [],
        "visited": [
          "A",
          "B",
          "D"
        ]
      }
    },
    {
      "event": "neighbor_check",
      "description": "When checking a neighbor node",
      "required_fields": {
        "current": "A",
        "neighbor": "C",
        "visited": [
          "A",
          "B",
          "D"
        ]
      }
    },
    {
      "event": "push",
      "description": "When a node is pushed to the stack",
      "required_fields": {
        "node": "C",
        "stack": [
          "C"
        ],
        "visited": [
          "A",
          "B",
          "D"
        ]
      }
    },
    {
      "event": "pop",
      "description": "When a node is processed from the stack",
      "required_fields": {
        "node": "C",
        "stack": [],
        "visited": [
          "A",
          "B",
          "D",
          "C"
        ]
      }
    },
    {
      "event": "neighbor_check",
      "description": "When checking a neighbor node",
      "required_fields": {
        "current": "C",
        "neighbor": "B",
        "visited": [
          "A",
          "B",
          "D",
          "C"
        ]
      }
    },
    {
      "event": "neighbor_check",
      "description": "When checking a neighbor node",
      "required_fields": {
        "current": "C",
        "neighbor": "D",
        "visited": [
          "A",
          "B",
          "D",
          "C"
        ]
      }
    },
    {
      "event": "complete",
      "description": "When algorithm finishes",
      "required_fields": {
        "visited": [
          "A",
          "B",
          "D",
          "C"
        ]
      }
    }
  ]
class DFSVisualizationEnhanced(Scene):
    def construct(self):
        # Graph structure
        graph = {
            'A': ['B', 'C'],
            'B': ['A', 'D'],
            'C': ['A', 'D'],
            'D': ['B', 'C']
        }
        
        # Tracing steps
        tracing_steps = tracing_steps_input
        
        # Create graph visualization
        nodes, edges = self.create_graph(graph)
        graph_mobj = VGroup(*nodes.values(), *edges.values())
        
        # Position elements with better spacing
        graph_mobj.scale(1.2).to_edge(LEFT, buff=1.5)
        
        # Create initial stack and visited displays
        init_step = tracing_steps[0]["required_fields"]
        stack_mobj = self.create_stack_visualization(init_step["stack"])
        visited_mobj = self.create_visited_visualization(init_step["visited"])
        
        # Add descriptions box
        description_box = self.create_description_box("Initializing DFS...")
        
        # Add all elements to scene
        self.add(graph_mobj, stack_mobj, visited_mobj, description_box)
        
        # Track DFS path edges and current node
        self.path_edges = []
        self.current_node = None
        
        # Animate DFS steps
        self.animate_enhanced_dfs(tracing_steps, nodes, edges, stack_mobj, visited_mobj, description_box)
    
    def create_graph(self, graph: dict) -> tuple:
        """Create visual elements with automatic layout"""
        nodes = {}
        edges = {}
        
        # Calculate positions in a circle with better spacing
        node_names = sorted(graph.keys())
        n = len(node_names)
        radius = 3.0
        angles = np.linspace(0, 2*PI, n, endpoint=False)
        
        # Create nodes with labels
        for i, node in enumerate(node_names):
            angle = angles[i]
            pos = radius * np.array([np.cos(angle), np.sin(angle), 0])
            nodes[node] = Circle(radius=0.5, color=WHITE, fill_opacity=0)
            nodes[node].move_to(pos)
            nodes[node].label = Text(node, font_size=32).move_to(pos)
        
        # Create edges with natural curvature
        for u in graph:
            for v in graph[u]:
                if (v, u) not in edges:
                    line = CurvedArrow(
                        nodes[u].get_center(),
                        nodes[v].get_center(),
                        angle=-0.4 if u < v else 0.4,
                        color=GRAY,
                        stroke_width=4
                    )
                    edges[(u, v)] = line
        
        return nodes, edges
    
    def create_stack_visualization(self, stack: list) -> VGroup:
        """Visualize the DFS stack with LIFO ordering"""
        title = Text("Stack", font_size=32, color=ORANGE).to_corner(UR, buff=1.2)
        title.shift(LEFT * 0.5)
        
        # Create stack container
        container = Rectangle(
            width=2.5, height=3.5,
            color=ORANGE, stroke_width=2
        )
        container.next_to(title, DOWN, buff=0.3)
        
        items = VGroup()
        y_offset = container.get_top()[1] - 0.6
        
        # Display stack with top element first (LIFO)
        for i, node in enumerate(reversed(stack)):
            item = Text(node, font_size=28, color=WHITE)
            item_bg = RoundedRectangle(
                width=2.0, height=0.6,
                color=ORANGE, fill_opacity=0.3,
                corner_radius=0.2
            )
            item_group = VGroup(item_bg, item)
            item_group.move_to([container.get_center()[0], y_offset - i*0.7, 0])
            items.add(item_group)
        
        return VGroup(title, container, items)
    
    def create_visited_visualization(self, visited: list) -> VGroup:
        """Create visited nodes display"""
        title = Text("Visited", font_size=32, color=GREEN).to_corner(UL, buff=1.2)
        title.shift(RIGHT * 0.5)
        
        items = VGroup()
        y_offset = title.get_bottom()[1] - 0.5
        
        for i, node in enumerate(visited):
            item = Text(node, font_size=28, color=WHITE)
            item_bg = RoundedRectangle(
                width=0.7, height=0.7,
                color=GREEN, fill_opacity=0.3,
                corner_radius=0.2
            )
            item_group = VGroup(item_bg, item)
            item_group.move_to([title.get_center()[0], y_offset - i*0.8, 0])
            items.add(item_group)
        
        return VGroup(title, items)
    
    def create_description_box(self, initial_text: str) -> VGroup:
        """Create a box for step descriptions"""
        box = Rectangle(
            width=6, height=1.5,
            color=BLUE, fill_opacity=0.2,
            stroke_width=2
        )
        box.to_edge(DOWN, buff=0.5)
        
        title = Text("DFS Step:", font_size=28, color=BLUE)
        title.next_to(box.get_top(), DOWN, buff=0.2)
        
        description = Text(initial_text, font_size=24, color=WHITE)
        description.move_to(box.get_center())
        
        return VGroup(box, title, description)
    
    def update_description(self, description_box: VGroup, text: str) -> Animation:
        """Update the description text with fade animation"""
        new_text = Text(text, font_size=24, color=WHITE)
        new_text.move_to(description_box[0].get_center())
        
        return Transform(description_box[2], new_text)
    
    def animate_enhanced_dfs(self, steps: list, nodes: dict, edges: dict, 
                       stack_mobj: VGroup, visited_mobj: VGroup,
                       description_box: VGroup):
        """Animate each step of DFS with enhanced visuals and proper alignment"""
        for step in steps:
            event = step["event"]
            fields = step["required_fields"]
            desc = step["description"]
            
            # Update description with fade effect
            self.play(
                self.update_description(description_box, desc),
                run_time=0.5
            )
            
            if event == "init":
                # Highlight starting node
                start_node = nodes[fields["start"]]
                self.play(
                    start_node.animate.set_fill(BLUE, opacity=0.7),
                    start_node.label.animate.set_color(BLUE),
                    run_time=0.7
                )
                self.current_node = start_node
                
                # Initialize stack and visited displays
                new_stack = self.create_stack_visualization(fields["stack"])
                new_stack.move_to(stack_mobj.get_center())
                new_visited = self.create_visited_visualization(fields["visited"])
                new_visited.move_to(visited_mobj.get_center())
                
                self.play(
                    Transform(stack_mobj, new_stack),
                    Transform(visited_mobj, new_visited),
                    run_time=0.7
                )
                self.wait(0.5)
            
            elif event == "push":
                node = fields["node"]
                
                # Highlight node being pushed
                self.play(
                    nodes[node].animate.set_fill(TEAL, opacity=0.7),
                    nodes[node].label.animate.set_color(TEAL),
                    run_time=0.5
                )
                
                # Update stack display
                new_stack = self.create_stack_visualization(fields["stack"])
                new_stack.move_to(stack_mobj.get_center())
                self.play(
                    Transform(stack_mobj, new_stack),
                    run_time=0.7
                )
                
                # Highlight the edge being added to DFS path if coming from current node
                if self.current_node:
                    current_node_name = self.current_node.label.original_text
                    edge_found = False
                    for (u, v), edge in edges.items():
                        if (u == current_node_name and v == node) or (v == current_node_name and u == node):
                            if edge not in self.path_edges:
                                self.path_edges.append(edge)
                                self.play(
                                    edge.animate.set_color(TEAL).set_stroke(width=6),
                                    run_time=0.7
                                )
                                edge_found = True
                                break
                    
                    if not edge_found:
                        # Create a temporary edge if not found (shouldn't happen with proper graph)
                        temp_edge = Line(
                            self.current_node.get_center(),
                            nodes[node].get_center(),
                            color=TEAL,
                            stroke_width=6
                        )
                        self.add(temp_edge)
                        self.play(
                            Create(temp_edge),
                            run_time=0.7
                        )
                        self.remove(temp_edge)
                self.wait(0.3)
            
            elif event == "pop":
                node = fields["node"]
                
                # Highlight current node being processed
                self.play(
                    nodes[node].animate.set_fill(ORANGE, opacity=0.7),
                    nodes[node].label.animate.set_color(ORANGE),
                    Flash(
                        nodes[node],
                        color=ORANGE,
                        flash_radius=0.8,
                        line_length=0.5,
                        run_time=1.0
                    ),
                    run_time=1.0
                )
                self.current_node = nodes[node]
                
                # Update stack display
                new_stack = self.create_stack_visualization(fields["stack"])
                new_stack.move_to(stack_mobj.get_center())
                self.play(
                    Transform(stack_mobj, new_stack),
                    run_time=0.7
                )
                
                # Update visited display
                new_visited = self.create_visited_visualization(fields["visited"])
                new_visited.move_to(visited_mobj.get_center())
                self.play(
                    Transform(visited_mobj, new_visited),
                    run_time=0.7
                )
                self.wait(0.5)
            
            elif event == "neighbor_check":
                current = fields["current"]
                neighbor = fields["neighbor"]
                
                # Find the edge (handle both directions)
                edge = edges.get((current, neighbor)) or edges.get((neighbor, current))
                
                if edge is None:
                    # Create a temporary edge if not found (shouldn't happen with proper graph)
                    temp_edge = Line(
                        nodes[current].get_center(),
                        nodes[neighbor].get_center(),
                        color=YELLOW,
                        stroke_width=8
                    )
                    self.add(temp_edge)
                    anims = [
                        Create(temp_edge),
                        nodes[neighbor].animate.set_fill(YELLOW, opacity=0.5),
                        nodes[neighbor].label.animate.set_color(YELLOW),
                    ]
                else:
                    anims = [
                        edge.animate.set_color(YELLOW).set_stroke(width=8),
                        nodes[neighbor].animate.set_fill(YELLOW, opacity=0.5),
                        nodes[neighbor].label.animate.set_color(YELLOW),
                    ]
                
                # Highlight edge and neighbor with animation
                self.play(
                    *anims,
                    run_time=0.7
                )
                
                # Show checking text
                check_text = Text(f"Checking {neighbor}", font_size=28, color=YELLOW)
                check_text.next_to(nodes[neighbor], UP, buff=0.4)
                self.play(
                    FadeIn(check_text, shift=UP*0.2),
                    run_time=0.5
                )
                self.wait(0.5)
                
                # Reset colors
                reset_anims = [
                    nodes[neighbor].animate.set_fill(WHITE, opacity=0),
                    nodes[neighbor].label.animate.set_color(WHITE),
                    FadeOut(check_text),
                ]
                
                if edge is None:
                    reset_anims.append(FadeOut(temp_edge))
                else:
                    reset_anims.append(
                        edge.animate.set_color(
                            WHITE if edge not in self.path_edges else TEAL
                        ).set_stroke(width=4)
                    )
                
                self.play(
                    *reset_anims,
                    run_time=0.5
                )
            
            elif event == "complete":
                # Create completion animation
                completion_text = Text("DFS Traversal Complete!", font_size=36, color=GOLD)
                completion_box = SurroundingRectangle(
                    completion_text,
                    color=GOLD,
                    fill_opacity=0.2,
                    corner_radius=0.2,
                    buff=0.4
                )
                completion_group = VGroup(completion_box, completion_text)
                completion_group.next_to(description_box, UP, buff=0.5)
                
                # Create visited order display
                visited_order_title = Text("Visitation Order:", font_size=28, color=BLUE)
                visited_order_title.next_to(completion_group, UP, buff=0.5)
                
                visited_nodes = VGroup()
                for i, node in enumerate(fields["visited"]):
                    order_text = Text(f"{i+1}. {node}", font_size=24)
                    order_bg = RoundedRectangle(
                        width=1.5, height=0.6,
                        color=BLUE, fill_opacity=0.2,
                        corner_radius=0.2
                    )
                    order_group = VGroup(order_bg, order_text)
                    visited_nodes.add(order_group)
                
                visited_nodes.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
                visited_nodes.next_to(visited_order_title, DOWN, buff=0.3)
                visited_nodes.shift(LEFT * 1.5)
                
                # Animate completion
                self.play(
                    FadeIn(completion_group, shift=UP*0.3),
                    run_time=0.7
                )
                self.play(
                    FadeIn(visited_order_title),
                    LaggedStart(
                        *[FadeIn(item, shift=RIGHT*0.3) 
                        for item in visited_nodes],
                        lag_ratio=0.2
                    ),
                    run_time=1.5
                )
                
                # Highlight the complete DFS tree
                self.play(
                    *[edge.animate.set_color(TEAL).set_stroke(width=6) 
                    for edge in self.path_edges],
                    run_time=1.5
                )
                self.wait(3)