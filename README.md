# website screenshot tool
## Setup
1. Install Python and Dependencies
First, ensure that you have Python installed on your system. To install the required dependencies, follow these steps:

Optional (Recommended): Create a Virtual Environment
It’s a good idea to create a virtual environment to keep dependencies isolated. Run the following command to create a virtual environment:

```bash
python -m venv .venv
```

Activate the Environment:
Windows:

```bash
source .venv/Scripts/activate
```

macOS/Linux:

```
source .venv/bin/activate
```

2. Install Dependencies
With the environment activated (if using), install the required dependencies by running:

```bash
pip install -r requirements.txt
```

in your terminal.

## Running the Application
1. Navigate to the Root Folder
Open your terminal and navigate to the root folder.

2. Run the Application
Execute the following command to start the application, replacing the name with the file you wish to execute:

```bash
python master.py
```

## Creating an executable
This program uses pyinstalled to bundle and create an executable file for users.

To create the executables, run the following command in the terminal
``` bash
pyinstaller --onefile master.py
```