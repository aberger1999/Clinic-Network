# CS631 Project

A web application with PostgreSQL database connectivity.

## Setup Instructions

1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with the following content:
   ```
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/cs631_project
   ```
   Replace `your_password` with your PostgreSQL password.

4. Create a database named `cs631_project` in pgAdmin:
   - Open pgAdmin
   - Right-click on "Databases"
   - Select "Create" > "Database"
   - Enter "cs631_project" as the database name
   - Click "Save"

5. Run the application:
   ```bash
   python app.py
   ```

6. Visit http://localhost:5000 in your web browser

## Project Structure

- `app.py`: Main Flask application file
- `requirements.txt`: Python dependencies
- `templates/`: HTML templates
  - `index.html`: Main page template
- `.env`: Environment variables (create this file manually)

## Testing Database Connection

1. Make sure PostgreSQL is running
2. Click the "Test Database Connection" button on the homepage
3. You should see a success message if the connection is working 