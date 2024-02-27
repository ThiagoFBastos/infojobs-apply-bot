import sqlite3
import os
import os.path

if not os.path.isdir('models'):
    os.mkdir('models')

con = sqlite3.connect("models/jobs")

cur = con.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY,
    url VARCHAR(512) NOT NULL UNIQUE,
    visited DATETIME DEFAULT CURRENT_TIMESTAMP,
    applied INTEGER NOT NULL
);
""")

con.commit()

con.close()

