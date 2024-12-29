import sqlite3
import os
import logging
from datetime import datetime
from flask.cli import AppGroup

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
db_cli = AppGroup("db")
DATABASE_PATH = os.getenv("DATABASE_PATH", "/app/db/flashcards.db")

leitner_boxes = 6

leitner_intervals = {
    1: 1,   # Box 1: Review every day
    2: 2,   # Box 2: Review every 2 days
    3: 4,   # Box 3: Review every 4 days
    4: 8,   # Box 4: Review every 8 days
    5: 16   # Box 5: Review every 16 days
}

# Database Handling


def _initialize_db():
    if os.path.exists(DATABASE_PATH):
        logging.debug(
            f"The file '{DATABASE_PATH}' already exists. Cancelling DB initialization.")
        return
    else:
        logging.debug(
            f"The file '{DATABASE_PATH}' does not exist. Creating a new one.")
        connection = sqlite3.connect(DATABASE_PATH)

    try:
        logging.debug(
            f"Creating schema for '{DATABASE_PATH}' using 'schema.sql'.")
        with open('schema.sql') as f:
            connection.executescript(f.read())
    except Exception as e:
        logging.error(f"Error connecting to DB: {e}")
        return

    try:
        logging.debug("Inserting sample data into the database.")
        cur = connection.cursor()
        cur.execute("INSERT INTO QUESTIONS (TOPIC, QUESTION, ANSWER, BOX, SECTION, LASTREVIEW) VALUES (?, ?, ?, ?, ?, ?)",
                    ('HTML', 'What does HTML Stand For?', 'HyperText Markup Language', 1, 'Web Development', None))
        cur.execute("INSERT INTO QUESTIONS (TOPIC, QUESTION, ANSWER, BOX, SECTION, LASTREVIEW) VALUES (?, ?, ?, ?, ?, ?)",
                    ('SQL', 'What does SQL stand for?', 'Structured Query Language', 1, 'Databases', None))
        cur.execute("INSERT INTO QUESTIONS (TOPIC, QUESTION, ANSWER, BOX, SECTION, LASTREVIEW) VALUES (?, ?, ?, ?, ?, ?)",
                    ('Python', 'What does Python stand for?', 'Python Programming Language', 1, 'Programming Languages', None))
        logging.debug("Database Initialized Successfully.")
    except Exception as e:
        logging.error(f"Error Initializing Database: {e}")
    finally:
        connection.commit()
        connection.close()


@db_cli.command("initialize")
def initialize_db():
    _initialize_db()


def reinitialize_db():
    if os.path.exists(DATABASE_PATH):
        logging.debug(f"Deleting database file '{DATABASE_PATH}'", "info")
        os.remove(DATABASE_PATH)
    logging.debug("Reinitializing database", "info")
    _initialize_db()


def get_db_connection():
    if not os.path.exists(DATABASE_PATH):
        logging.debug(f"Database file '{DATABASE_PATH}' does not exist.")
        return None
    try:
        con = sqlite3.connect(DATABASE_PATH)
        con.row_factory = sqlite3.Row
        return con
    except Exception as e:
        logging.error(f"Error connecting to database: {e}")
        return None


# Queries
def get_question(section: str = None, topic: str = None, id: int = None, min_id: int = None):
    con = get_db_connection()
    if con is None:
        return None
    try:
        query = "SELECT * FROM questions WHERE box < ?"
        params = [leitner_boxes]

        if id is not None:
            query += " AND id = ?"
            params.append(id)
        if section is not None:
            query += " AND section = ?"
            params.append(section)
        if topic is not None:
            query += " AND topic = ?"
            params.append(topic)
        if min_id is not None:
            query += " AND id > ?"
            params.append(min_id)

        questions = con.execute(query, params).fetchall()
        today = datetime.now().date()

        for question in questions:
            if question['LASTREVIEW'] is None:
                logging.debug(
                    f"Returning unanswered question from {section}>{topic}>{id}")
                return question
            last_review_date = datetime.strptime(
                question['LASTREVIEW'], '%Y-%m-%d %H:%M:%S.%f').date()
            interval = leitner_intervals.get(question['BOX'], 1)
            if (today - last_review_date).days >= interval:
                logging.debug(
                    f"Returning question in box {interval} from {section}>{topic}>{id}")
                return question
            # Include questions that should be reviewed today
            if interval == 1 and (today - last_review_date).days == 0:
                logging.debug(
                    f"Returning question in box {interval} from {section}>{topic}>{id}")
                return question
    except Exception as e:
        logging.error(f"Error getting question: {e}")
        return None
    finally:
        con.close()
    return None


def select(topic: str = None) -> list:
    con = get_db_connection()
    if con is None:
        return []
    try:
        if topic == "Topic" or topic == "topic":
            topics = con.execute(
                "SELECT * FROM QUESTIONS GROUP BY TOPIC").fetchall()
        elif topic is not None:
            topics = con.execute(
                "SELECT * FROM QUESTIONS WHERE BOX < ? AND TOPIC = ?", (leitner_boxes, topic)).fetchall()
        else:
            topics = con.execute("SELECT * FROM QUESTIONS").fetchall()
    except Exception as e:
        logging.error(f"Error selecting questions: {e}")
        return []
    return topics


def topicSelect() -> list:
    con = get_db_connection()
    if con is None:
        return []
    try:
        topics = con.execute(
            "SELECT topic FROM questions GROUP BY topic ORDER BY MAX(id) DESC;").fetchall()
    except Exception as e:
        logging.error(f"error retrieving topics: {e}")
        return []
    topics = [row[0] for row in topics]
    return topics


def update_box(id: int, score: int):
    con = get_db_connection()
    if con is None:
        return None
    if score > leitner_boxes:
        score = leitner_boxes
    if score < 1:
        score = 1
    try:
        con.execute(
            'UPDATE questions SET box = ? WHERE id = ?', (score, id))
        con.commit()
    except Exception as e:
        logging.error(f"Error updating box: {e}")
        return None
    finally:
        con.close()
    return score


def get_box(id: int):
    con = get_db_connection()
    if con is None:
        return None
    try:
        box = con.execute(
            "SELECT box FROM questions WHERE id = ?", (id,)).fetchone()
    except Exception as e:
        logging.error(f"Error getting box: {e}")
        return None
    finally:
        con.close()
    return box


def reset_questions(section: str, topic: str):
    con = get_db_connection()
    if con is None:
        return False
    try:
        con.execute(
            "UPDATE questions SET box = 1, lastreview = NULL WHERE section = ? AND topic = ?", (section, topic))
        con.commit()
        return True
    except Exception as e:
        logging.error(f"Error resetting questions: {e}")
        return False
    finally:
        con.close()


def get_topics_by_section():
    con = get_db_connection()
    if con is None:
        return None
    try:
        sections = con.execute(
            "SELECT SECTION, TOPIC, COUNT(*) as COUNT FROM QUESTIONS GROUP BY SECTION, TOPIC;").fetchall()
    except Exception as e:
        logging.error(f"Error getting topics by section: {e}")
        return None
    finally:
        con.close()
    topics_by_section = {}
    for row in sections:
        section = row['SECTION']
        topic = row['TOPIC']
        count = row['COUNT']
        if section not in topics_by_section:
            topics_by_section[section] = []
        topics_by_section[section].append({'topic': topic, 'count': count})
    return topics_by_section


def get_section_by_topic(topic: str):
    con = get_db_connection()
    if con is None:
        return ''
    try:
        section = con.execute(
            "SELECT SECTION FROM QUESTIONS WHERE TOPIC = ? LIMIT 1", (topic.strip(),)).fetchone()
    except Exception as e:
        logging.error(f"Error getting section by topic: {e}")
        return ''
    finally:
        con.close()
    return section['SECTION'] if section else ''


def get_total_questions_per_topic():
    con = get_db_connection()
    if con is None:
        return None
    try:
        counts = con.execute(
            "SELECT TOPIC, COUNT(*) FROM QUESTIONS GROUP BY TOPIC;").fetchall()
    except Exception as e:
        logging.error(f"Error getting total questions per topic: {e}")
        return None
    finally:
        con.close()
    sorted_counts = {row[0]: row[1] for row in counts}
    return sorted_counts


def get_total_uncompleted_questions_per_topic():
    con = get_db_connection()
    if con is None:
        return None
    try:
        counts = con.execute(
            "SELECT TOPIC, COUNT(*) FROM QUESTIONS WHERE BOX < 6 GROUP BY TOPIC;").fetchall()
    except Exception as e:
        logging.error(f"Error getting total questions per topic: {e}")
        return None
    finally:
        con.close()
    sorted_counts = {row[0]: row[1] for row in counts}
    return sorted_counts


def get_uncompleted_topics_by_section():
    con = get_db_connection()
    if con is None:
        return None
    try:
        sections = con.execute(
            "SELECT SECTION, TOPIC, COUNT(*) as COUNT FROM QUESTIONS WHERE BOX < 6 GROUP BY SECTION, TOPIC;").fetchall()
    except Exception as e:
        logging.error(f"Error getting topics by section: {e}")
        return None
    finally:
        con.close()
    topics_by_section = {}
    for row in sections:
        section = row['SECTION']
        topic = row['TOPIC']
        count = row['COUNT']
        if section not in topics_by_section:
            topics_by_section[section] = []
        topics_by_section[section].append({'topic': topic, 'count': count})
    return topics_by_section


def create_new_question(topic, question, answer, section):
    con = get_db_connection()
    if con is None:
        return False
    try:
        con.execute("INSERT INTO QUESTIONS (TOPIC, QUESTION, ANSWER, BOX, SECTION, LASTREVIEW) VALUES (?, ?, ?, ?, ?, ?)",
                    (topic.strip(), question.strip(), answer.strip(), 1, section.strip(), None))
        con.commit()
    except Exception as e:
        logging.error(f"Error creating new question: {e}")
        return False
    finally:
        con.close()
    return True


def edit_topic(old_topic: str, new_topic: str):
    con = get_db_connection()
    if con is None:
        return
    try:
        con.execute("UPDATE QUESTIONS SET TOPIC = ? WHERE TOPIC = ?",
                    (new_topic.strip(), old_topic.strip()))
        con.commit()
    except Exception as e:
        logging.error(f"Error updating topic: {e}")
    finally:
        con.close()


def edit_section(topic: str, section: str):
    con = get_db_connection()
    if con is None:
        return
    try:
        con.execute("UPDATE QUESTIONS SET SECTION = ? WHERE TOPIC = ?",
                    (section.strip(), topic.strip()))
        con.commit()
    except Exception as e:
        logging.error(f"Error updating section: {e}")
    finally:
        con.close()


def update_lastreview(id, time):
    con = get_db_connection()
    if con is None:
        return
    try:
        con.execute("UPDATE QUESTIONS SET LASTREVIEW = ? WHERE ID = ?",
                    (time, id))
        con.commit()
    except Exception as e:
        logging.error(f"Error updating last review: {e}")
    finally:
        con.close()


def update_question(id, topic, question_text, answer, box, section, lastreview=None):
    con = get_db_connection()
    if con is None:
        return
    if lastreview is None:
        lastreview = datetime.now()

    if int(box) > leitner_boxes:
        box = leitner_boxes
    try:
        con.execute("UPDATE questions SET topic = ?, question = ?, answer = ?, box = ?, section = ?, lastreview = ? WHERE id = ?",
                    (topic, question_text, answer, box, section, lastreview, id))
        con.commit()
    except Exception as e:
        logging.error(f"Error updating question: {e}")
    finally:
        con.close()


def get_question_by_id(id):
    con = get_db_connection()
    if con is None:
        return None
    try:
        question = con.execute(
            "SELECT * FROM questions WHERE id = ?", (id,)).fetchone()
    except Exception as e:
        logging.error(f"Error getting question by id: {e}")
        return None
    finally:
        con.close()
    return question


def delete_question(id):
    con = get_db_connection()
    if con is None:
        return
    try:
        con.execute("DELETE FROM questions WHERE id = ?", (id,))
        con.commit()
    except Exception as e:
        logging.error(f"Error deleting question: {e}")
    finally:
        con.close()


def deleteATopic(topic):
    con = get_db_connection()
    if con is None:
        return
    try:
        con.execute("DELETE FROM questions WHERE topic = ?", (topic,))
        con.commit()
    except Exception as e:
        logging.error(f"Error deleting topic: {e}")
    finally:
        con.close()


def are_all_questions_mastered(section: str, topic: str) -> bool:
    con = get_db_connection()
    if con is None:
        return False
    try:
        query = "SELECT COUNT(*) FROM questions WHERE section = ? AND topic = ? AND box != 6"
        params = [section, topic]
        count = con.execute(query, params).fetchone()[0]
        return count == 0
    except Exception as e:
        logging.error(f"Error checking if all questions are mastered: {e}")
        return False
    finally:
        con.close()
