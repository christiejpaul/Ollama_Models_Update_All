import subprocess
import os
from textfsm import TextFSM

# Change the current working directory to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Fetch model list and parse with TextFSM
with open('model_name.textfsm') as f:
    template = TextFSM(f)

try:
    output = subprocess.check_output(["ollama", "list"], text=True).strip()
except subprocess.CalledProcessError as e:
    print(f"Failed to list models: {e}")
    exit(1)

# Parse all output at once
models = template.ParseText(output)

# Update each model
for model_name in models:
    if model_name[0].upper() != 'NAME':  # Check if it's not the header
        print(f"Updating model: {model_name[0]}")
        try:
            subprocess.check_call(["ollama", "pull", model_name[0]])
            print("Update successful")
        except subprocess.CalledProcessError as e:
            print(f"Update failed for {model_name[0]} with error: {e}")