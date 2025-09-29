from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'


#Create a simple database
def init_database():
    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS notes
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT)''')
    connection.commit()
    connection.close()

@app.route('/')
def index():
    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM notes")
    notes = cursor.fetchall()
    connection.close
    return render_template('index.html', notes=notes)

@app.route('/add', methods=['POST'])
def add_note():
    title = request.form.get('title')
    content = request.form.get('content')

    #BUG 1: Title field has no server-side validation (can be empty)
    if not content:
        flash("Note content cannot be empty!", "error")
        return redirect(url_for('index'))
    
    connection = sqlite3.connect('test.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
    connection.commit()
    connection.close()
    flash("Note added successfully!", "success")
    return redirect(url_for('index'))

@app.route('/delete/<int:note_id>')
def delete_note(note_id):
    connection = sqlite3.connection('test.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM notes WHERE id=?", (note_id,))
    connection.commit()
    connection.close()
    flash("Note deleted successfully!", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_database()
    # BUG 2: Debug mode is on, which is a security no-no for production.
    app.run(debug=True)
