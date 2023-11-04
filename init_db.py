import sqlite3

connection = sqlite3.connect('flashcards.db')

try:
    with open('schema.sql') as f:
        connection.executescript(f.read())
except Exception as e:
    print(f"Error connecting to DB: {e}")

try:
        cur = connection.cursor()
        cur.execute("INSERT INTO QUESTIONS (SCORE, TOPIC, QUESTION, ANSWER, SESH) VALUES (?, ?, ?, ?, ?)",(1, 'HTML', 'What does HTML Stand For?', 'HypterText Markup Language', 1))
        cur.execute("INSERT INTO QUESTIONS (SCORE, TOPIC, QUESTION, ANSWER, SESH) VALUES (?, ?, ?, ?, ?)",(1, 'SQL', 'What does SQL stand for?', 'Structured Query Language', 1))
        cur.execute("INSERT INTO QUESTIONS (SCORE, TOPIC, QUESTION, ANSWER, SESH) VALUES (?, ?, ?, ?, ?)",(1, 'Python', 'What does Python stand for?', 'Python Programming Language', 1))
except Exception as e:
    print(f"Error Initializing Database : {e}")
finally:
    connection.commit()
    connection.close()

def get_question(topic: str = None, id: int = None):
    con = get_db_connection()
    try:
        if topic is None and id is not None:
            question = con.execute(
                'SELECT * FROM questions WHERE sesh < 4 AND id = ?', (id,)).fetchone()
        elif topic is not None and id is None:
            question = con.execute(
                'SELECT * FROM questions WHERE topic = ?', (topic,)).fetchone()
        else:
            question = con.execute(
                'SELECT * FROM questions WHERE id = ? AND topic = ?', (id, topic)).fetchone()
    except Exception as e:
        print(f"Error getting question: {e}")
        return None
    finally:
        con.close()
    return question
