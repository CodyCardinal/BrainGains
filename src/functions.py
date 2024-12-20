import sqlite3
import markdown2


def get_db_connection():
    try:
        con = sqlite3.connect("flashcards.db")
        con.row_factory = sqlite3.Row
        return con
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None


def get_question(topic: str = None, id: int = None):
    con = get_db_connection()
    try:
        if topic is None and id is not None:
            question = con.execute(
                "SELECT * FROM questions WHERE sesh < 4 AND id = ?", (id,)).fetchone()
        elif topic is not None and id is None:
            question = con.execute(
                "SELECT * FROM questions WHERE sesh < 4 AND topic = ?", (topic,)).fetchone()
        else:
            question = con.execute(
                "SELECT * FROM questions WHERE id = ? AND topic = ?", (id, topic)).fetchone()
    except Exception as e:
        print(f"Error getting question: {e}")
        return None
    finally:
        con.close()
    return question


def get_next_question(topic: str, id: int):
    con = get_db_connection()
    try:
        question = con.execute(
            "SELECT * FROM questions WHERE sesh < 4 AND id > ? AND topic = ?", (id, topic)).fetchone()
    except Exception as e:
        print(f"Error getting next question: {e}")
        return None
    finally:
        con.close()
    return question if question else None


def update_score(id: int, score: int):
    try:
        con = get_db_connection()
        con.execute('UPDATE questions SET score = ? WHERE id = ?', (score, id))
        con.commit()
    except Exception as e:
        print(f"Error updating score: {e}")
        return False
    finally:
        con.close()
    return True


def select(topic: str = None) -> list:
    try:
        with get_db_connection() as con:
            if topic == "Topic" or topic == "topic":
                topics = con.execute(
                    "SELECT * FROM QUESTIONS GROUP BY TOPIC").fetchall()
            elif topic is not None:
                topics = con.execute(
                    "SELECT * FROM QUESTIONS WHERE SESH < 4 AND TOPIC = ?", (topic,)).fetchall()
            else:
                topics = con.execute("SELECT * FROM QUESTIONS").fetchall()
    except Exception as e:
        print(f"Error selecting questions: {e}")
        return []
    return topics


def topicSelect() -> list:
    try:
        with get_db_connection() as con:
            topics = con.execute(
                "SELECT topic FROM questions GROUP BY topic ORDER BY MAX(id) DESC;").fetchall()
    except Exception as e:
        print(f"error retrieving topics: {e}")
        return []
    topics = [row[0] for row in topics]
    return topics


def update_sesh(id: int, score: int):
    sesh = get_sesh(id)
    sesh = sesh["sesh"]
    con = get_db_connection()
    try:
        if score == 0:
            sesh += 1
            if sesh > 4:
                sesh = 4
            con.execute(
                'UPDATE questions SET sesh = ? WHERE id = ?', (sesh, id))
        if score == 2:
            sesh = sesh - 1
            if sesh < 1:
                sesh = 1
            con.execute(
                'UPDATE questions SET sesh = ? WHERE id = ?', (sesh, id))
        con.commit()
    except Exception as e:
        print(f"Error updating session: {e}")
        return None
    finally:
        con.close()
    return sesh


def get_sesh(id: int):
    con = get_db_connection()
    try:
        sesh = con.execute(
            "SELECT sesh FROM questions WHERE id = ?", (id,)).fetchone()
    except Exception as e:
        print(f"Error getting session: {e}")
        return None
    finally:
        con.close()
    return sesh


def get_topics_by_section():
    with get_db_connection() as con:
        try:
            sections = con.execute(
                "SELECT SECTION, TOPIC, COUNT(*) as COUNT FROM QUESTIONS GROUP BY SECTION, TOPIC;").fetchall()
        except Exception as e:
            print(f"Error getting topics by section: {e}")
            return None
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
    section = con.execute(
        "SELECT SECTION FROM QUESTIONS WHERE TOPIC = ? LIMIT 1", (topic.strip(),)).fetchone()
    con.close()
    return section['SECTION'] if section else ''


def get_total_questions_per_topic():
    with get_db_connection() as con:
        try:
            counts = con.execute(
                "SELECT TOPIC, COUNT(*) FROM QUESTIONS GROUP BY TOPIC;").fetchall()
        except Exception as e:
            print(f"Error getting total questions per topic: {e}")
            return None
    sorted_counts = {row[0]: row[1] for row in counts}
    return sorted_counts


def create_new_question(topic, question, answer, section):
    with get_db_connection() as con:
        try:
            con.execute("INSERT INTO QUESTIONS (SCORE, TOPIC, QUESTION, ANSWER, SESH, SECTION) VALUES (?, ?, ?, ?, ?, ?)",
                        (1, topic.strip(), question.strip(), answer.strip(), 1, section.strip()))
            con.commit()
        except Exception as e:
            print(f"Error creating new question: {e}")
            return False
    return True


def edit_topic(old_topic: str, new_topic: str):
    con = get_db_connection()
    try:
        con.execute("UPDATE QUESTIONS SET TOPIC = ? WHERE TOPIC = ?",
                    (new_topic.strip(), old_topic.strip()))
        con.commit()
    except:
        print("Error updating questions with updated topic")
    con.close()


def edit_section(topic: str, section: str):
    con = get_db_connection()
    try:
        con.execute("UPDATE QUESTIONS SET SECTION = ? WHERE TOPIC = ?",
                    (section.strip(), topic.strip()))
        con.commit()
    except:
        print("Error updating questions with updated section")
    con.close()


def update_question(id, topic, question_text, answer, score, session, section):
    con = get_db_connection()
    if int(session) > 4:
        session = 4
    con.execute("UPDATE questions SET topic = ?, question = ?, answer = ?, score = ?, sesh = ?, section = ? WHERE id = ?",
                (topic, question_text, answer, score, session, section, id))
    con.commit()
    con.close()


def get_question_by_id(id):
    con = get_db_connection()
    question = con.execute(
        "SELECT * FROM questions WHERE id = ?", (id,)).fetchone()
    con.close()
    return question


def delete_question(id):
    con = get_db_connection()
    con.execute("DELETE FROM questions WHERE id = ?", (id,))
    con.commit()
    con.close()


def deleteATopic(topic):
    con = get_db_connection()
    con.execute("DELETE FROM questions WHERE topic = ?", (topic,))
    con.commit()
    con.close()
