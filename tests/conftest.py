import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

frontend_dir = os.path.join(project_root, 'frontend')
sys.path.insert(0, frontend_dir)

os.environ['GRADIO_ANALYTICS_ENABLED'] = 'False'