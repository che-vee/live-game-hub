# Game Hub Project

Data Storages M10-BKK-2024

## Getting Started


### Prerequisites

- [Python 3.x](https://www.python.org/downloads/)

- [Django](https://www.djangoproject.com/)

### Install and Run

1. Clone this repository to your local machine:

    ```
    git clone git@github.com:che-vee/live-game-hub.git
    ```

2. It's recommended to set up a virtual environment to manage dependencies. You can create one using the following command:

    ```
    python -m venv venv
    ```

3. Activate the virtual environment. On Windows:

    ```
    venv\Scripts\activate
    ```

    On macOS and Linux:

    ```
    source venv/bin/activate
    ```

4. Install the required dependencies:

    ```
    pip install -r requirements.txt
    ```

5. Create a copy of the `.env.example` file and rename it to `.env`:

    ```
    cp .env.example .env
    ```

6. Open the `.env` file and adjust the environment variables as needed.

7. Apply migrations to set up the database:

    ```
    python manage.py migrate
    ```

8. Run server:

    ```
    python manage.py runserver
    ```
