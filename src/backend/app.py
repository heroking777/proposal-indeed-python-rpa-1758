from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database setup
def get_db_connection():
    conn = sqlite3.connect('jobs.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create database and table if not exists
def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS jobs (id INTEGER PRIMARY KEY, title TEXT, company TEXT, url TEXT)')
    conn.commit()
    conn.close()

# API endpoint to add a job
@app.route('/jobs', methods=['POST'])
def add_job():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute('INSERT INTO jobs (title, company, url) VALUES (?, ?, ?)',
                 (data['title'], data['company'], data['url']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Job added successfully'}), 201

# API endpoint to delete a job
@app.route('/jobs/<int:id>', methods=['DELETE'])
def delete_job(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM jobs WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Job deleted successfully'}), 200

# API endpoint to list all jobs
@app.route('/jobs', methods=['GET'])
def list_jobs():
    conn = get_db_connection()
    jobs = conn.execute('SELECT * FROM jobs').fetchall()
    conn.close()
    return jsonify([dict(job) for job in jobs])

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
```

This Python Flask application provides API endpoints to add, delete, and list jobs. It uses an SQLite database to store the job data. The `init_db` function initializes the database and creates a table if it doesn't exist. The `/jobs` endpoint with POST method allows adding new jobs, DELETE method allows deleting a job by ID, and GET method lists all jobs.