from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os



def create_app(test_config=None):
    app = Flask(__name__)
    #app.secret_key = 'supersecretkey'

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY='dev-secret-key',
            DATABASE = 'test.db',
            DEBUG = False #Security fix: debug mode off by default
        )
    else:
        app.config.update(test_config)

    def get_db_connection():
        connection = sqlite3.connect(app.config['DATABASE'])
        connection.row_factory = sqlite3.Row
        return connection

    #Create a simple database
    def init_database():
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS notes
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL DEFAULT 'Untitled',
                    content TEXT NOT NULL)''')
        connection.commit()
        connection.close()

    @app.route('/')
    def index():
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM notes")
        notes = cursor.fetchall()
        connection.close()
        return render_template('index.html', notes=notes)

    @app.route('/add', methods=['POST'])
    def add_note():
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip() 
        
        #BUG 1: Title field has no server-side validation (can be empty) [FIXED]
        if not title:
            title = "Untitled"
        if not content:
            flash("Note content cannot be empty!", "error")
            return redirect(url_for('index'))
        
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
        connection.commit()
        connection.close()
        flash("Note added successfully!", "success")
        return redirect(url_for('index'))

    @app.route('/delete/<int:note_id>')
    def delete_note(note_id):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM notes WHERE id=?", (note_id,))
        connection.commit()
        connection.close()
        flash("Note deleted successfully!", "success")
        return redirect(url_for('index'))
    
    #init database when app starts
    with app.app_context():
        init_database()
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug = app.config['DEBUG'])
