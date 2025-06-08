# Todo Application
This is a FastAPI-based Todo application that allows users to manage tasks with a PostgreSQL database backend. It uses SQLModel for ORM and supports CRUD operations for todos.

Prerequisites
Before running the application, ensure you have the following installed:

Python: Version 3.8 or higher
PostgreSQL: A running PostgreSQL database server
pip: Python package manager
Git: For cloning the repository (optional)
Installation
Follow these steps to set up and run the application locally:

1. Clone the Repository
Clone the project repository to your local machine:
git clone <repository-url>
cd <repository-directory>

2. Set Up a Virtual Environment
Create and activate a virtual environment to manage dependencies:
python -m venv venv
venv\Scripts\activate

3. Install Dependencies
Install the required Python packages listed in requirements.txt:
pip install -r requirements.txt

4. Configure Environment Variables
Create a .env file in the project root directory and configure your PostgreSQL database connection. Use the provided example.env as a template:
DATABASE_URL=postgresql://<username>:<password>@localhost:5432/<database_name>

Replace <username>, <password>, and <database_name> with your PostgreSQL credentials and database name. Ensure the database exists in PostgreSQL before proceeding.

To create a database in PostgreSQL:
psql -U <username>
CREATE DATABASE <database_name>;

6. Run the Application
Start the FastAPI application using Uvicorn:
uvicorn main:app --reload