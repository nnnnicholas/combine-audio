# stitch wav files

## Prerequisites

- Python 3.x
- venv

## Installation

Please follow the instructions to set up and run the project:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/your-repo-name.git
    cd your-repo-name
    ```

2. Create a virtual environment:
    ```bash
    python3 -m venv venv
    ```

3. Activate the virtual environment:
    - On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    - On Unix or MacOS:
        ```bash
        source venv/bin/activate
        ```

4. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

Now, you should be able to run the project.

## Usage

1. Initialize the virtual environment (if you haven't already):
    ```bash
    source venv/bin/activate
    ```

2. Run the script:
    ```bash
    python3 stitch_wav_files.py -d <PATH_TO_DIRECTORY_CONTAINING_WAV_FILES>
    ```