import sqlite3

connection = sqlite3.connect('flashcards.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# cur.execute("INSERT INTO QUESTIONS (SCORE, TOPIC, QUESTION, ANSWER, SESH) VALUES (?, ?, ?, ?, ?)",(1, 'HTML', 'What does HTML Stand For?', 'HypterText Markup Language', 1))
# cur.execute("INSERT INTO QUESTIONS (SCORE, TOPIC, QUESTION, ANSWER, SESH) VALUES (?, ?, ?, ?, ?)",(1, 'SQL', 'What does SQL stand for?', 'Structured Query Language', 1))
# cur.execute("INSERT INTO QUESTIONS (SCORE, TOPIC, QUESTION, ANSWER, SESH) VALUES (?, ?, ?, ?, ?)",(1, 'Python', 'What does Python stand for?', 'Python Programming Language', 1))

connection.commit()
connection.close()