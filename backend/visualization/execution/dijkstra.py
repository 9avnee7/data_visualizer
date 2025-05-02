from manim import *
import json
from typing import Dict, List, Tuple

# Load and assign data
with open('/Users/navneet/Documents/Internshiptasks/algorithmVisualizer/backend/src/controllers/trace.json') as file:
    data = json.load(file)


graph_input=data["graph"]
tracing_steps_input=data["trace"]


true=1

class DijkstraVisualization(Scene):
    def construct(self):
        # Graph structure
        graph=graph_input
        # graph = {
        #     'A': [('B', 4), ('C', 1)],
        #     'B': [('A', 4), ('C', 2), ('D', 5)],
        #     'C': [('A', 1), ('B', 2), ('D', 5)],
        #     'D': [('B', 5), ('C', 5)]
        # }
        
        # Tracing steps data
        tracing_steps = tracing_steps_input
        
       # Create visual elements with automatic layout
        nodes, edges, edge_labels = self.create_graph(graph)
        graph_mobj = VGroup(*nodes.values(), *edges.values(), *edge_labels.values())
        
        # Initial state
        init_step = tracing_steps[0]["required_fields"]
        distance_labels = self.create_distance_labels(nodes, init_step["distances"])
        queue_mobj = self.create_queue_visualization(init_step["queue"])
        
        # Dynamic positioning based on graph size
        self.position_elements(graph_mobj, queue_mobj, len(graph))
        
        # Add static elements
        self.add(graph_mobj, queue_mobj)
        
        # Animation control
        visited_text = Text("Visited: ", font_size=24).to_corner(UR)
        self.add(visited_text)
        
        # Animate all steps
        self.animate_steps(tracing_steps, nodes, edges, distance_labels, queue_mobj, visited_text)
    
    def position_elements(self, graph_mobj: VGroup, queue_mobj: VGroup, num_nodes: int):
        """Dynamically position elements based on graph size"""
        if num_nodes <= 4:
            graph_mobj.center().shift(LEFT*2)
            queue_mobj.to_edge(RIGHT).shift(DOWN*0.5)
        else:
            # For larger graphs, make everything more compact
            graph_mobj.scale(0.8).center()
            queue_mobj.scale(0.9).to_corner(DR)

    def create_graph(self, graph: Dict) -> Tuple[Dict, Dict, Dict]:
        """Create visual elements with automatic layout for any graph size"""
        nodes = {}
        edges = {}
        edge_labels = {}
        
        # Calculate node positions in a circle
        node_names = sorted(graph.keys())
        n = len(node_names)
        radius = 3.5 if n <= 4 else 4.0  # Larger radius for more nodes
        angles = np.linspace(0, 2*PI, n, endpoint=False)
        
        # Create nodes
        for i, node in enumerate(node_names):
            angle = angles[i]
            pos = radius * np.array([np.cos(angle), np.sin(angle), 0])
            nodes[node] = Circle(radius=0.4, color=WHITE, fill_opacity=0.7)
            nodes[node].move_to(pos)
            nodes[node].label = Text(node, font_size=20).move_to(pos)
        
        # Create edges
        for u in graph:
            for v, weight in graph[u]:
                if (v, u) not in edges:  # Avoid duplicates
                    line = Line(nodes[u].get_center(), nodes[v].get_center(), 
                              color=WHITE, stroke_width=2.5)
                    edges[(u, v)] = line
                    
                    # Position edge labels intelligently
                    edge_center = line.get_center()
                    edge_angle = angle_of_vector(line.get_vector())
                    
                    # Offset label position based on graph density
                    label_pos = edge_center + rotate_vector(
                        UP*0.2, 
                        edge_angle + PI/2
                    )
                    
                    edge_labels[(u, v)] = Text(str(weight), font_size=18
                                              ).move_to(label_pos)
        
        return nodes, edges, edge_labels
    
    def create_distance_labels(self, nodes: Dict, distances: Dict) -> Dict:
        """Create distance labels for nodes."""
        labels = {}
        for node, circle in nodes.items():
            dist = distances[node]
            text = "∞" if dist == "Infinity" else str(dist)
            labels[node] = Text(text, color=YELLOW, font_size=24
                              ).next_to(circle, DOWN, buff=0.3)
        return labels
    
    def create_queue_visualization(self, queue: List) -> VGroup:
        """Visualize the priority queue."""
        title = Text("Priority Queue:", font_size=28).to_edge(UP).shift(LEFT*4)
        items = VGroup()
        
        for priority, node in sorted(queue):
            text = "∞" if priority == "Infinity" else str(priority)
            items.add(Text(f"{text}: {node}", font_size=24))
        
        if items:
            items.arrange(DOWN, aligned_edge=LEFT, buff=0.3
                         ).next_to(title, DOWN, aligned_edge=LEFT)
        else:
            # Show empty queue message
            items.add(Text("<empty>", font_size=24, color=GRAY)
                      .next_to(title, DOWN, aligned_edge=LEFT))
        
        return VGroup(title, items)
    
    def animate_steps(self, steps: List, nodes: Dict, edges: Dict, 
                     distance_labels: Dict, queue_mobj: VGroup, visited_text: Text):
        """Animate each step of Dijkstra's algorithm."""
        current_node_mobj = None
        temp_objects = []
        
        for step in steps:
            event = step["event"]
            fields = step["required_fields"]
            
            # Clean up previous temporary objects
            self.remove(*temp_objects)
            temp_objects = []
            
            if event == "init":
                # Flash all nodes to show initialization
                self.play(*[Flash(node, color=BLUE_C, flash_radius=0.6) 
                          for node in nodes.values()], run_time=1.5)
                self.wait(0.5)
                
                # Show starting node
                start_node = nodes[fields["start"]]
                self.play(
                    start_node.animate.set_fill(BLUE_E, opacity=0.9),
                    run_time=0.7
                )
                current_node_mobj = start_node
            
            elif event == "visit":
                node = fields["node"]
                
                # Update visited list display
                new_visited_text = Text(
                    f"Visited: {', '.join(fields['visited'])}", 
                    font_size=24
                ).move_to(visited_text)
                self.play(Transform(visited_text, new_visited_text))
                
                # Highlight current node
                if current_node_mobj:
                    self.play(
                        current_node_mobj.animate.set_fill(GRAY, opacity=0.3),
                        nodes[node].animate.set_fill(BLUE_E, opacity=0.9),
                        run_time=0.7
                    )
                else:
                    self.play(
                        nodes[node].animate.set_fill(BLUE_E, opacity=0.9),
                        run_time=0.7
                    )
                current_node_mobj = nodes[node]
                self.wait(0.3)
            
            elif event == "check_relax":
                u, v = fields["from"], fields["to"]
                edge = edges.get((u, v), edges.get((v, u)))
                
                # Highlight the edge being checked
                self.play(
                    edge.animate.set_color(YELLOW).set_stroke(width=6),
                    run_time=0.5
                )
                
                # Show comparison information
                old_dist = "∞" if fields["old_distance"] == "Infinity" else str(fields["old_distance"])
                new_dist = str(fields["new_distance"])
                
                comparison = VGroup(
                    Text(f"Current distance: {old_dist}", font_size=22),
                    Text(f"New distance: {fields['current_distance']} + {fields['edge_weight']} = {new_dist}", 
                        font_size=22)
                ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
                
                comparison.next_to(edge, DOWN if edge.get_center()[1] > 0 else UP, buff=0.3)
                comparison.set_color(WHITE)
                
                temp_objects.append(comparison)
                self.play(Write(comparison))
                self.wait(0.7)
                
                if fields["will_update"]:
                    update_text = Text("Will update!", color=GREEN, font_size=24)
                    update_text.next_to(comparison, DOWN, buff=0.2)
                    temp_objects.append(update_text)
                    self.play(Write(update_text))
                    self.wait(0.5)
                
                # Reset edge color
                self.play(
                    edge.animate.set_color(WHITE).set_stroke(width=3),
                    run_time=0.3
                )
                self.wait(0.2)
            
            elif event == "relax":
                node = fields["to"]
                new_dist = str(fields["new_distance"])
                
                # Update distance label
                new_label = Text(new_dist, color=GREEN, font_size=24)
                new_label.move_to(distance_labels[node].get_center())
                
                # Update queue visualization
                new_queue = self.create_queue_visualization(fields["queue"])
                new_queue.move_to(queue_mobj.get_center())
                
                self.play(
                    Transform(distance_labels[node], new_label),
                    nodes[node].animate.set_color(GREEN),
                    Transform(queue_mobj, new_queue),
                    run_time=0.7
                )
                self.wait(0.3)
            
            elif event == "complete":
                # Create a clean final display
                final_box = Rectangle(
                    width=min(4, len(nodes)*0.7),
                    height=min(3, len(nodes)*0.5),
                    color=GOLD_E
                )
                final_box.to_edge(DR if len(nodes) > 4 else RIGHT)
                
                final_title = Text("Final Distances", font_size=24, color=GOLD_E)
                final_title.next_to(final_box, UP)
                
                final_items = VGroup()
                for node, dist in fields["final_distances"].items():
                    dist_text = "∞" if dist == "Infinity" else str(dist)
                    final_items.add(Text(f"{node}: {dist_text}", font_size=20))
                
                final_items.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
                final_items.move_to(final_box)
                
                self.play(
                    FadeIn(final_box),
                    FadeIn(final_title),
                    run_time=0.7
                )
                self.play(
                    Write(final_items),
                    run_time=1.5
                )
                self.wait(3)