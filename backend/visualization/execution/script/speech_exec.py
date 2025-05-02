import subprocess
from fetchingScript import get_text_script
text_script = get_text_script("/Users/navneet/Documents/Internshiptasks/algorithmVisualizer/backend/src/controllers/trace.json")

# Optional: trim or escape quotes if needed
escaped_text = text_script.replace('"', '\\"')

# Call the shell script with the script as an argument
subprocess.run(['bash', '/Users/navneet/Documents/Internshiptasks/algorithmVisualizer/backend/visualization/execution/script/generate_audio.sh', escaped_text])
