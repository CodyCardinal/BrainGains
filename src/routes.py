from flask import Blueprint, redirect, url_for, render_template, request, flash
import markdown2
from .functions import *

app = Blueprint('app', __name__)


@app.route("/", methods=("GET", "POST"))
def index():
    topics_by_section = get_topics_by_section()
    counts = get_total_questions_per_topic()
    if topics_by_section is None or counts is None:
        return render_template("init_db.html")
    return render_template("index.html", topics_by_section=topics_by_section, counts=counts)


@app.route("/init_db", methods=("GET", "POST"))
def init_db():
    if request.method == "POST":
        initialize_db()
        return redirect(url_for("app.index"))
    return render_template("init_db.html")


@app.route("/reset_db", methods=(["POST"]))
def reset_db():
    if request.method == "POST":
        reinitialize_db()
        return redirect(url_for("app.index"))
    return render_template("init_db.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/question/<section>/<topic>", methods=("GET", "POST"))
@app.route("/question/<section>/<topic>/<id>", methods=("GET", "POST"))
def question(section: str = None, topic: str = None, id=None):
    if id:
        query = get_question(section, topic, id)
    else:
        query = get_question(section, topic)
        if query:
            return redirect(url_for('app.question', section=section, topic=topic, id=query['id']))

    if query:
        query_dict = dict(query)  # Convert sqlite3.Row to dictionary
        lowerCaseQuery = {k.lower(): v for k, v in query_dict.items()}
        markdownQuery = lowerCaseQuery
        markdownQuery['question'] = markdown2.markdown(
            markdownQuery['question'], extras=["fenced-code-blocks"])
        markdownQuery['answer'] = markdown2.markdown(
            markdownQuery['answer'], extras=["fenced-code-blocks"])
        return render_template("question.html", query=markdownQuery)
    else:
        flash("Question not found", "error")
        return redirect(url_for("app.index"))


@app.route("/answer/<section>/<topic>/<id>", methods=("GET", "POST"))
def answer(section, topic, id):
    score = int(request.form["score"])
    update_score(id, score)
    update_sesh(id, score)
    query = get_next_question(section, topic, id)
    if query is None:
        return redirect(url_for("app.index"))

    url = "/question/" + query["section"] + "/" + \
        query["topic"] + "/" + str(query["id"])
    return redirect(url)


@app.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        existing_section_and_topic = request.form.get(
            "existingsectionandtopic")
        new_section = request.form.get("newsection")
        new_topic = request.form.get("newtopic")
        question = request.form["question"]
        answer = request.form["answer"]

        if new_section:
            section = new_section
        else:
            section = existing_section_and_topic.split(" > ")[0]

        if new_topic:
            topic = new_topic
        else:
            topic = existing_section_and_topic.split(" > ")[1]

        if create_new_question(topic, question, answer, section):
            return redirect(url_for("app.create"))
        else:
            return "Error creating question"
    elif request.method == "GET":
        topics_by_section = get_topics_by_section()
        counts = get_total_questions_per_topic()
        if topics_by_section is None or counts is None:
            return render_template("init_db.html")
        latest_question = select()[-1]
        latest_topic = latest_question['TOPIC']
        latest_section = latest_question['SECTION']
        return render_template("create.html", topics_by_section=topics_by_section, counts=counts, latest_topic=latest_topic, latest_section=latest_section)


@app.route("/list", methods=("GET", "POST"))
def list():
    if request.method == "POST":
        query = select(request.form.get("topic"))
        return render_template("list.html", query=query)
    else:
        query = select()
        topics_by_section = get_topics_by_section()
        if query is None or topics_by_section is None:
            return render_template("init_db.html")
        return render_template("list.html", query=query, topics_by_section=topics_by_section)


@app.route("/edit/<int:id>", methods=("GET", "POST"))
def edit(id):
    if request.method == "POST":
        topic = request.form["topic"]
        question_text = request.form["question"]
        answer = request.form["answer"]
        score = request.form["score"]
        session = request.form["session"]
        section = request.form["section"]
        update_question(id, topic, question_text,
                        answer, score, session, section)
        return redirect(url_for("app.list"))
    else:
        question = get_question_by_id(id)

        if question is None:
            flash("Question not found", "error")
            return redirect(url_for("app.list"))
        return render_template("edit.html", question=question)


@app.route("/editTopic/<path:topic>", methods=("GET", "POST"))
def editTopic(topic):
    if request.method == "POST":
        newSection = request.form["section"]
        newTopic = request.form["topic"]
        edit_topic(topic, newTopic)
        edit_section(newTopic, newSection)
        return redirect(url_for("app.list"))
    if request.method == "GET":
        section = get_section_by_topic(topic)
        if section is None:
            flash("Section not found", "error")
            return redirect(url_for("app.list"))
        return render_template("editTopic.html", topic=topic, section=section)


@app.route("/delete/<int:id>", methods=("POST",))
def delete(id):
    question = get_question_by_id(id)
    if question is None:
        flash("Question not found", "error")
    else:
        delete_question(id)
    return redirect(url_for("app.list"))


@app.route("/deleteTopic/<topic>", methods=("POST",))
def deleteTopic(topic):
    deleteATopic(topic)
    return redirect(url_for("app.list"))
