import json
import subprocess
from BFS import BFSVisualization
from DFS import DFSVisualizationEnhanced
from dijkstra import DijkstraVisualization
import os

# Load and assign data
with open('/Users/navneet/Documents/Internshiptasks/algorithmVisualizer/backend/src/controllers/trace.json') as file:
    data = json.load(file)


dest_file="/Users/navneet/Documents/Internshiptasks/algorithmVisualizer/backend/visualization/execution/customStore/manim_output.mp4"

# Now run Manim
if data["algorithmName"]=='bfs':
    subprocess.run([
        "manim",
        "BFS.py",
        "BFSVisualization",
        "-pql"  
    ])
    src_file="/Users/navneet/Documents/Internshiptasks/algorithmVisualizer/backend/visualization/execution/media/videos/BFS/480p15/BFSVisualization.mp4"
    subprocess.run(["mv", src_file, dest_file], check=True)

elif data["algorithmName"]=='dijkstra':
    subprocess.run([
        "manim",
        "dijkstra.py",
        "DijkstraVisualization",
        "-pql"  
    ])
    src_file="/Users/navneet/Documents/Internshiptasks/algorithmVisualizer/backend/visualization/execution/media/videos/dijkstra/480p15/DijkstraVisualization.mp4"
    subprocess.run(["mv", src_file, dest_file], check=True)
elif data["algorithmName"]=='dfs':
    subprocess.run([
        "manim",
        "DFS.py",
        "DFSVisualization",
        "-pql"  
    ])
    src_file="/Users/navneet/Documents/Internshiptasks/algorithmVisualizer/backend/visualization/execution/media/videos/DFS/480p15/DFSVisualizationEnhanced.mp4"
    subprocess.run(["mv", src_file, dest_file], check=True)
elif data["algorithmName"]=='merge':
    subprocess.run([
        "manim",
        "mergeSort.py",
        "MergeSortVisualization",
        "-pql"  
    ])
    src_file="/Users/navneet/Documents/Internshiptasks/algorithmVisualizer/backend/visualization/execution/media/videos/mergeSort/480p15/MergeSortVisualization.mp4"
    subprocess.run(["mv", src_file, dest_file], check=True)