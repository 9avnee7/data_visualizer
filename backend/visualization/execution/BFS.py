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

class BFSVisualization(Scene):
    def construct(self):
        # Sample graph (replace with your input)
        graph = graph_input
        
        # Sample tracing steps (replace with your input)
        tracing_steps =tracing_steps_input # Your provided tracing steps here
        
        # Create graph visualization
        nodes, edges = self.create_graph(graph)
        graph_mobj = VGroup(*nodes.values(), *edges.values())
        
        # Position elements
        self.position_elements(graph_mobj, len(graph))
        
        # Create queue and visited displays
        init_step = tracing_steps[0]["required_fields"]
        queue_mobj = self.create_queue_visualization(init_step["queue"])
        visited_mobj = self.create_visited_visualization(init_step["visited"])
        
        # Add initial elements
        self.add(graph_mobj, queue_mobj, visited_mobj)
        
        # Animate BFS steps
        self.animate_bfs(tracing_steps, nodes, edges, queue_mobj, visited_mobj)
    
    def create_graph(self, graph: Dict) -> Tuple[Dict, Dict]:
        """Create visual elements with automatic layout"""
        nodes = {}
        edges = {}
        
        # Calculate positions in a circle
        node_names = sorted(graph.keys())
        n = len(node_names)
        radius = 4.0  # Slightly larger for 6 nodes
        angles = np.linspace(0, 2*PI, n, endpoint=False)
        
        # Create nodes with labels
        for i, node in enumerate(node_names):
            angle = angles[i]
            pos = radius * np.array([np.cos(angle), np.sin(angle), 0])
            nodes[node] = Circle(radius=0.4, color=WHITE, fill_opacity=0.7)
            nodes[node].move_to(pos)
            nodes[node].label = Text(node, font_size=24).move_to(pos)
        
        # Create edges with natural curvature
        for u in graph:
            for v in graph[u]:
                if (v, u) not in edges:
                    # Use curved edges for better visibility
                    line = ArcBetweenPoints(
                        nodes[u].get_center(),
                        nodes[v].get_center(),
                        angle=0.3 if u < v else -0.3,
                        color=WHITE,
                        stroke_width=3
                    )
                    edges[(u, v)] = line
        
        return nodes, edges
    
    def position_elements(self, graph_mobj: VGroup, num_nodes: int):
        """Dynamically position elements based on graph size"""
        graph_mobj.scale(0.9).center()
    
    def create_queue_visualization(self, queue: List) -> VGroup:
        """Visualize the BFS queue with improved styling"""
        title = Text("Queue:", font_size=28, color=BLUE_B).to_corner(UL)
        items = VGroup()
        
        for node in queue:
            item = Text(node, font_size=24, color=BLUE_D)
            item.bg = SurroundingRectangle(item, color=BLUE_E, fill_opacity=0.2, corner_radius=0.1)
            items.add(VGroup(item.bg, item))
        
        if items:
            items.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            items.next_to(title, DOWN, aligned_edge=LEFT)
        else:
            empty = Text("<empty>", font_size=24, color=GRAY)
            empty.next_to(title, DOWN, aligned_edge=LEFT)
            items.add(empty)
        
        return VGroup(title, items)
    
    def create_visited_visualization(self, visited: List) -> VGroup:
        """Create visited nodes display with improved styling"""
        title = Text("Visited:", font_size=28, color=GREEN_B).to_corner(UR)
        items = VGroup()
        
        for node in visited:
            item = Text(node, font_size=24, color=GREEN_D)
            item.bg = SurroundingRectangle(item, color=GREEN_E, fill_opacity=0.2, corner_radius=0.1)
            items.add(VGroup(item.bg, item))
        
        if items:
            items.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            items.next_to(title, DOWN, aligned_edge=LEFT)
        else:
            empty = Text("<none>", font_size=24, color=GRAY)
            empty.next_to(title, DOWN, aligned_edge=LEFT)
            items.add(empty)
        
        return VGroup(title, items)
    
    def animate_bfs(self, steps: List, nodes: Dict, edges: Dict, 
               queue_mobj: VGroup, visited_mobj: VGroup):
        """Animate each step of BFS with enhanced visuals"""
        current_node_mobj = None
        temp_objects = []
        
        for step in steps:
            event = step["event"]
            fields = step.get("required_fields", {})
            
            # Clean up previous temporary objects
            self.remove(*temp_objects)
            temp_objects = []
            
            if event == "init":
                # Flash all nodes with wave effect
                anims = []
                for i, node in enumerate(nodes.values()):
                    anims.append(Flash(
                        node, 
                        color=BLUE_C,
                        flash_radius=0.6,
                        line_length=0.3,
                        run_time=0.5,
                        time_width=0.3,
                        lag_ratio=0.1*i
                    ))
                self.play(*anims)
                
                # Highlight starting node
                start_node = nodes[fields["start"]]
                self.play(
                    start_node.animate.set_fill(BLUE_E, opacity=0.9),
                    run_time=0.7
                )
                current_node_mobj = start_node
                
                # Initialize queue and visited displays
                new_queue = self.create_queue_visualization(fields["queue"])
                new_queue.move_to(queue_mobj.get_center())
                new_visited = self.create_visited_visualization(fields["visited"])
                new_visited.move_to(visited_mobj.get_center())
                
                self.play(
                    Transform(queue_mobj, new_queue),
                    Transform(visited_mobj, new_visited),
                    run_time=0.5
                )
            
            elif event == "dequeue":
                node = fields["node"]
                
                # Highlight current node with pulse effect
                self.play(
                    nodes[node].animate.set_fill(ORANGE, opacity=0.9),
                    Flash(
                        nodes[node],
                        color=ORANGE,
                        flash_radius=0.7,
                        line_length=0.4,
                        run_time=0.8
                    ),
                    run_time=0.8
                )
                current_node_mobj = nodes[node]
                
                # Update queue display with transform animation
                new_queue = self.create_queue_visualization(fields["queue"])
                new_queue.move_to(queue_mobj.get_center())
                
                # Update visited list
                new_visited = self.create_visited_visualization(fields["visited"])
                new_visited.move_to(visited_mobj.get_center())
                
                self.play(
                    Transform(queue_mobj, new_queue),
                    Transform(visited_mobj, new_visited),
                    run_time=0.5
                )
            
            elif event == "visit":
                node = step["node"]
                
                # Mark node as visited with smooth transition
                self.play(
                    nodes[node].animate.set_fill(GREEN, opacity=0.7),
                    run_time=0.5
                )
                
                # Update visited display
                new_visited = self.create_visited_visualization(fields["visited"])
                new_visited.move_to(visited_mobj.get_center())
                self.play(
                    Transform(visited_mobj, new_visited),
                    run_time=0.5
                )
            
            elif event == "neighbor_check":
                current = fields["current"]
                neighbor = fields["neighbor"]
                
                # Find the edge (handle both directions)
                edge = edges.get((current, neighbor)) or edges.get((neighbor, current))
                
                # Highlight edge and neighbor with animation
                self.play(
                    edge.animate.set_color(YELLOW).set_stroke(width=8),
                    nodes[neighbor].animate.set_color(YELLOW),
                    run_time=0.5
                )
                
                # Show checking text with fade-in effect
                check_text = Text(f"Checking {neighbor}", font_size=24, color=YELLOW)
                check_text.next_to(nodes[neighbor], UP, buff=0.3)
                temp_objects.append(check_text)
                self.play(
                    FadeIn(check_text, shift=UP*0.2),
                    run_time=0.5
                )
                self.wait(0.3)
                
                # Reset colors with smooth transition
                self.play(
                    edge.animate.set_color(WHITE).set_stroke(width=3),
                    nodes[neighbor].animate.set_color(WHITE),
                    run_time=0.3
                )
            
            elif event == "enqueue":
                node = fields["node"]
                
                # Highlight node being enqueued with bounce effect
                self.play(
                    nodes[node].animate.set_color(BLUE).scale(1.2),
                    run_time=0.3
                )
                self.play(
                    nodes[node].animate.set_color(BLUE).scale(1/1.2),
                    run_time=0.3
                )
                
                # Update queue display with transform animation
                new_queue = self.create_queue_visualization(fields["queue"])
                new_queue.move_to(queue_mobj.get_center())
                
                # Keep visited list updated
                new_visited = self.create_visited_visualization(fields["visited"])
                new_visited.move_to(visited_mobj.get_center())
                
                self.play(
                    Transform(queue_mobj, new_queue),
                    Transform(visited_mobj, new_visited),
                    run_time=0.5
                )
            
            elif event == "complete":
                # Create completion animation sequence
                completion_text = Text("BFS Complete!", font_size=36, color=GOLD_E)
                completion_text.to_edge(DOWN).shift(UP*0.5)
                
                # Create visited order display
                visited_order = VGroup(
                    Text("Visited Order:", font_size=28, color=GREEN_B)
                )
                
                for i, node in enumerate(fields["visited"]):
                    order_text = Text(f"{i+1}. {node}", font_size=24)
                    order_text.bg = SurroundingRectangle(
                        order_text, 
                        color=GREEN_E, 
                        fill_opacity=0.2,
                        corner_radius=0.1
                    )
                    visited_order.add(VGroup(order_text.bg, order_text))
                
                visited_order.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
                visited_order.next_to(completion_text, UP, buff=0.5)
                
                # Animate completion
                self.play(
                    FadeIn(completion_text, shift=UP*0.3),
                    run_time=0.7
                )
                self.play(
                    LaggedStart(
                        *[FadeIn(item, shift=UP*0.2) 
                        for item in visited_order[1:]],
                        lag_ratio=0.2
                    ),
                    run_time=2
                )
                self.wait(3)