# FastAPI Project

Welcome to the FastAPI project! Follow these instructions to set up the project on your local machine and get everything running smoothly.

## Prerequisites

Before you begin, the project assumes the following:

- A Linux environment, or WSL (if using Windows)
- Python 3.10 or later installed.
- PostgreSQL installed.

A Makefile has been provided for easy project setup.

## Setup Instructions

- **Clone the Repository**

   ```bash
   git clone https://github.com/Pythonian/fastapi_web.git
   ```

- Change into the cloned repository

   ```bash
   cd fastapi_web
   ```

- **Create a Virtual Environment**

   ```bash
   make venv
   ```

   Activate the virtual environment with the command:

   ```bash
   source .venv/bin/activate
   ```

   *Ensure the virtual environment is activated before running any further commands.*

- **Install Dependencies**

   ```bash
   make install
   ```

   This command will copy an `.env` file into your directory. Open it and update the values before you proceed.

- **Run Checks**

   Ensure that everything is set up correctly:

   ```bash
   make check
   ```

- **Run the Development Server**

   To start the development server, use:

   ```bash
   make run
   ```

   You can then view the API docs at `http://127.0.0.1:8000/docs/`.

- **Cleaning Up**

   To clean up the project directory, removing unnecessary files and directories, use:

   ```bash
   make clean
   ```

   You can run the command `make` to see all available commands.

## Credits

- [HNG Boilerplate](https://github.com/hngprojects/hng_boilerplate_python_fastapi_web)
- [FastAPI Tutorial](https://www.youtube.com/playlist?list=PLEt8Tae2spYnHy378vMlPH--87cfeh33P)
