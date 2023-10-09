from flask import Flask, redirect, url_for, render_template, request
import sqlite3


# BUGS: errors if you get to the end of the questions
# BUGS: if you choose a type other than HTML, it still loads question 1 ( an html question ) and you're now working through HTML questions

# Initialize Flask
app = Flask(__name__)


def get_db_connection():
    con = sqlite3.connect('flashcards.db')
    con.row_factory = sqlite3.Row
    return con


def get_question(topic: str = None, id: int = None):
    con = get_db_connection()
    if topic is None and id is not None:
        question = con.execute('SELECT * FROM questions WHERE sesh < 4 AND id = ?', (id,)).fetchone()
    if topic is not None and id is None:
        question = con.execute('SELECT * FROM questions WHERE topic = ?', (topic,)).fetchone()
    else:
        question = con.execute('SELECT * FROM questions WHERE id = ? AND topic = ?', (id, topic)).fetchone()
    con.close()
    return question


def get_next_question(topic: str, id: int):
    con = get_db_connection()
    question = con.execute('SELECT * FROM questions WHERE sesh < 4 AND id > ? AND topic = ?', (id, topic)).fetchone()
    con.close()
    return question


def update_score(topic: str, id: int, score: int):
    con = get_db_connection()
    con.execute('UPDATE questions SET score = ? WHERE id = ?', (score, id))
    con.commit()
    con.close()


def select(topic: str = None) -> list:
    with get_db_connection() as con:
        # Select Distinct Topics
        if topic == 'Topic':
            topics = con.execute('SELECT DISTINCT(TOPIC) FROM QUESTIONS').fetchall()
        # Select Specific Topic
        elif topic != None:
            topics = con.execute('SELECT * FROM QUESTIONS WHERE SESH < 4 AND TOPIC = ?', (topic,)).fetchall()
        # Select Everything.
        else:
            topics = con.execute('SELECT * FROM QUESTIONS').fetchall()
    con.close()
    return topics


def update_sesh(id: int, score: int):
    sesh = get_sesh(id)
    sesh = sesh['SESH']
    con = get_db_connection()
    if score == 1:
        sesh += 1
        if sesh > 4:
            sesh = 4
        con.execute('UPDATE questions SET sesh = ? WHERE id = ?', (sesh, id))
    
    if score == 3:
        sesh = sesh - 1
        if sesh < 1:
            sesh = 1
        con.execute('UPDATE questions SET sesh = ? WHERE id = ?', (sesh, id))

    con.commit()
    con.close()
    return sesh


def get_sesh(id: int):
    con = get_db_connection()
    sesh = con.execute('SELECT sesh FROM questions WHERE id = ?', (id,)).fetchone()
    con.close()
    return sesh


# App Routes
@app.route('/', methods=('GET', 'POST'))
def index():
    query = select('Topic')
    return render_template('index.html', query=query)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/question/<topic>', methods=('GET', 'POST'))
def question(topic: str = None):
    query = get_question(topic)
    return render_template('question.html', query=query)


@app.route('/next/<topic>/<id>', methods=('GET', 'POST'))
def next(topic: str = None, id=None):
    query = get_question(topic, id)
    return render_template('next.html', query=query)


@app.route('/answer/<topic>/<id>', methods=('GET', 'POST'))
def answer(topic, id):
    # get score as int
    score = int(request.form['Score'])
    # Update Score
    update_score(topic, id, score)
    # Get Next Question
    query = get_next_question(topic, id)
    if query is None:
        print('Trying to end session')
        query = select(topic)
        for q in query:
            print(f'Updating Sesh for {q["id"]}')
            update_sesh(q['id'], q['score'])
        return render_template('index.html')

    url = '/next/' + query['topic'] + '/' + str(query['id'])
    # Redirect to next question
    return redirect(url)


@app.route('/createnew', methods=('GET', 'POST'))
def createnew():
    if request.method == 'POST':
        if request.form['New']:
            topic = request.form['New']
        else:
            topic = request.form['Topic']
        score = 1
        question = request.form['Question']
        answer = request.form['Answer']
        sesh = 1
        with get_db_connection() as con:
            con.execute('INSERT INTO QUESTIONS (SCORE, TOPIC, QUESTION, ANSWER, SESH) VALUES (?, ?, ?, ?, ?)', 
            (score, topic, question, answer, sesh))
            con.commit()
        con.close()
        return redirect(url_for('create'))
    return render_template('index.html')


@app.route('/create', methods=('GET', 'POST'))
def create():
    query = select('Topic')
    return render_template('create.html', query=query)


@app.route('/list', methods=('GET', 'POST'))
def list():
    if request.method == 'POST':
        query = select(request.form.get('Topic'))
        return render_template('list.html', query=query)
    else:
        query = select()
        return render_template('list.html', query=query)


@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    if request.method == 'POST':
        # Update the question's data
        topic = request.form['Topic']
        question_text = request.form['Question']
        answer = request.form['Answer']
        
        # Update the question in the database
        update_question(id, topic, question_text, answer)
        
        # Redirect to the list of questions
        return redirect(url_for('list'))
    else:
        # Get the question data from the database
        question = get_question_by_id(id)
        
        if question is None:
            # Handle the case where the question with the given ID doesn't exist
            flash('Question not found', 'error')
            return redirect(url_for('list'))
        
        return render_template('edit.html', question=question)

# Add a new function to update the question in the database
def update_question(id, topic, question_text, answer):
    con = get_db_connection()
    con.execute('UPDATE questions SET topic = ?, question = ?, answer = ? WHERE id = ?', (topic, question_text, answer, id))
    con.commit()
    con.close()

# Add a new function to get a question by its ID
def get_question_by_id(id):
    con = get_db_connection()
    question = con.execute('SELECT * FROM questions WHERE id = ?', (id,)).fetchone()
    con.close()
    return question



if __name__ == '__main__':
    app.run()