# GPT-4o Image Analysis Project

This project uses OpenAI's GPT-4o to analyze and describe image content via the API.

## Setup Instructions (macOS, Python 3)

Follow these steps to set up and run the project using a local virtual environment and Jupyter Notebook.

```bash
# 1. Navigate to the project folder
cd path/to/this/project/folder

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Register the virtual environment as a Jupyter kernel
python3 -m ipykernel install --user --name=venv --display-name "venv"

# 5. Launch Jupyter Notebook
jupyter notebook
```
Select `venv` kernel in the Jupyter Notebook interface.
