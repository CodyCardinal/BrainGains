from flask import Flask, redirect, url_for, render_template, request, flash

import sqlite3
import markdown2

app = Flask(__name__)


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
                "SELECT SECTION, GROUP_CONCAT(DISTINCT TOPIC) as TOPICS FROM QUESTIONS GROUP BY SECTION;").fetchall()
        except Exception as e:
            print(f"Error getting topics by section: {e}")
            return None
    topics_by_section = {row['SECTION']: row['TOPICS'].split(',') for row in sections}
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


@app.route("/", methods=("GET", "POST"))
def index():
    topics_by_section = get_topics_by_section()
    counts = get_total_questions_per_topic()
    return render_template("index.html", topics_by_section=topics_by_section, counts=counts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/question/<topic>", methods=("GET", "POST"))
def question(topic: str = None):
    query = dict(get_question(topic))
    if query:
        lowerCaseQuery = {k.lower(): v for k, v in query.items()}
        markdownQuery = lowerCaseQuery
        markdownQuery['question'] = markdown2.markdown(
            markdownQuery['question'])
        markdownQuery['answer'] = markdown2.markdown(markdownQuery['answer'])
    return render_template("question.html", query=markdownQuery)


@app.route("/next/<topic>/<id>", methods=("GET", "POST"))
def next(topic: str = None, id=None):
    query = dict(get_question(topic, id))
    if query:
        lowerCaseQuery = {k.lower(): v for k, v in query.items()}
        markdownQuery = lowerCaseQuery
        markdownQuery['question'] = markdown2.markdown(
            markdownQuery['question'])
        markdownQuery['answer'] = markdown2.markdown(markdownQuery['answer'])
    return render_template("next.html", query=markdownQuery)


@app.route("/answer/<topic>/<id>", methods=("GET", "POST"))
def answer(topic, id):
    score = int(request.form["score"])
    update_score(id, score)
    update_sesh(id, score)
    query = get_next_question(topic, id)
    if query is None:
        return redirect(url_for("index"))

    url = "/next/" + query["topic"] + "/" + str(query["id"])
    return redirect(url)


@app.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        topic = request.form.get("New") or request.form["topic"]
        question = request.form["question"]
        answer = request.form["answer"]
        section = request.form.get("section", "default")
        if create_new_question(topic, question, answer, section):
            return redirect(url_for("create"))
        else:
            return "Error creating question"
    elif request.method == "GET":
        topics_by_section = get_topics_by_section()
        counts = get_total_questions_per_topic()
        return render_template("create.html", topics_by_section=topics_by_section, counts=counts)


@app.route("/list", methods=("GET", "POST"))
def list():
    if request.method == "POST":
        query = select(request.form.get("topic"))
        return render_template("list.html", query=query)
    else:
        query = select()
        topics_by_section = get_topics_by_section()
        counts = get_total_questions_per_topic()
        return render_template("list.html", query=query, topics_by_section=topics_by_section, counts=counts)


@app.route("/edit/<int:id>", methods=("GET", "POST"))
def edit(id):
    if request.method == "POST":
        topic = request.form["topic"]
        question_text = request.form["question"]
        answer = request.form["answer"]
        score = request.form["score"]
        session = request.form["session"]
        update_question(id, topic, question_text, answer, score, session)
        return redirect(url_for("list"))
    else:
        question = get_question_by_id(id)

        if question is None:
            flash("Question not found", "error")
            return redirect(url_for("list"))

        return render_template("edit.html", question=question)


@app.route("/editTopic/<path:topic>", methods=("GET", "POST"))
def editTopic(topic):
    if request.method == "POST":
        newSection = request.form["section"]
        newTopic = request.form["topic"]
        edit_topic(topic, newTopic)
        edit_section(newTopic, newSection)
        return redirect(url_for("list"))
    if request.method == "GET":
        section = get_section_by_topic(topic)
        return render_template("editTopic.html", topic=topic, section=section)


def update_question(id, topic, question_text, answer, score, session):
    con = get_db_connection()
    if int(session) > 4:
        session = 4
    con.execute("UPDATE questions SET topic = ?, question = ?, answer = ?, score = ?, sesh = ? WHERE id = ?",
                (topic, question_text, answer, score, session, id))
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


@app.route("/delete/<int:id>", methods=("POST",))
def delete(id):
    question = get_question_by_id(id)
    if question is None:
        flash("Question not found", "error")
    else:
        delete_question(id)
    return redirect(url_for("list"))


@app.route("/deleteTopic/<topic>", methods=("POST",))
def deleteTopic(topic):
    topic = topic
    deleteATopic(topic)
    return redirect(url_for("list"))


if __name__ == "__main__":
    app.run()
