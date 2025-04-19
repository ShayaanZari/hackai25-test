# step 1: get a db working
import sqlite3 # downloaded the SQLite extension for visualization

# step 2: build a read & write API for this db
from fastapi import FastAPI # needed the fastapi[standard] version to get convenient 'fastapi dev main.py' command 

# step 3: start a frontend for this service
import gradio as gr 

# one time creation of db
"""
conn = sqlite3.connect("notes.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS notes (id Integer Primary Key Autoincrement, text TEXT)")
conn.commit()
conn.close()
"""

apiApp = FastAPI()

# Root
@apiApp.get("/")
def root():
    return {"message": "This is the root!"}

# Get all notes
@apiApp.get("/notes/")
def read_notes():
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes")
    notes = [{"id": row[0], "text": row[1]} for row in cursor.fetchall()]
    conn.close()
    return notes

# Add a note
@apiApp.post("/notes/")
def post_note(text: str):
    conn = sqlite3.connect('notes.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (text) VALUES (?)", (text,))
    conn.commit()
    note_id = cursor.lastrowid
    conn.close()
    return {"id": note_id, "text": text}

# at this point, do fastapi dev main.py and go to 127.0.0.1:8001/docs
# gradio integration next

def addNote(x):
    return post_note(x)

frontApp = gr.Interface(
    inputs=["text"],
    fn=addNote,
    outputs=["text"]
)

frontApp.launch()