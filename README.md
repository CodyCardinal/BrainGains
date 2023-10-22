# BRAIN GAINS

![Brain Gains Art](https://github.com/CodyCardinal/BrainGains/blob/main/static/braingains.jpeg)

Brain gains is my final project submission for CS50X! 
I've used Python, Flask, SQLlite, and Bootstrap Javascript.

## [Video Demo](https://www.youtube.com/watch?v=qdZy8P7B4JA)

## How to start:

- Install Python 3.10+
- Install the requirements with `pip install -r requirements.txt`
- If you don't already have flashcards.db, then initialize the Database with `python init_db.py`
- Run the flask app locally with `flask run`
- Open your browser to `http://localhost:5000/`

## What is Brain Gains?

Brain Gains is a flashcard application designed for self-assessment in your learning journey. It adheres to the fundamental principles of the [Leitner System](https://en.wikipedia.org/wiki/Leitner_system).

Typically, you would engage in a course, attend a lecture, or watch an online video. Later, either on the same day or the following day, you'd challenge yourself to recall what you've learned. This approach combines recall and spacing as integral elements of effective learning. Utilizing spacing in our learning process can enhance the retention of information. This is because our brains are more adept at retaining knowledge when it is revisited and reinforced at intervals over time. The Leitner System provides a structured method for implementing this spaced repetition technique. This concept is analogous to how muscles are exercised: they are broken down during workouts through repetitive stress repition, and then allowed time to recover and grow stronger. Similarly, our brains benefit from spaced review and reinforcement to optimize learning.

![Leitner Learning System](https://github.com/CodyCardinal/BrainGains/blob/main/static/2560px-Leitner_system_alternative.svg.png)

In the above method, questions are sorted into groups according to how easily the learner was able to recall the answer. The learners try to recall the solution written to a question. Clicking to reveal the answer. Depending how difficult it was to recall the answer, the learner can rate their recall difficulty. The recall rating then determines when the questions is asked again.

![Animated gif of Leitner Learning System](https://github.com/CodyCardinal/BrainGains/blob/main/static/Leitner_system_animation.gif?raw=true)

In the above gif, we see that the first session starts with one container of questions. In the second session you're asked harder questions from the first session and the second containers questions. This process repeats until you're phased each question out into the final 5th container.


## Detailed How-To

- While you are taking a course or lecture. You would create a new topic in Brain Gains.
- Throughout that course, when you go to take notes, you would create a new question in Brain Gains in that topic.
- Wait a few hours or overnight to practice recall.
- Choose that topic on the home page.
- Proceed to read each question, mentally answer the question.
- Once you've answered it mentally, click the question button to expand the answer.
  - If you want to try again, click Again.
  - If you answered it correctly and easily, you would click Easy.
  - If you answered it correctly, but not easily, click Good.
  - If you failed to answer it, you would click Hard.
- Then proceed to the next question. Eventually you will be taken back to the front page once you've ehausted all questions in the topic.
- Come back and answer questions again tomorrow. And you should then space out visits back to this topic over time. Use the Leitner System link for specific timing ( until I build in that feature! ). Over time you will notice that the questions you chose easy for will stop being offered to you.
- Once you aren't asked any questions in that topic, you're done with that topic. It is now time for a new Topic!

## Newish Features and Bugfixes
- Create Page now always defaults to the newest topic
- now hiding the answer button until you've expanded the question
- Fixed Scoring Bug
- Pep8 Python Formatting Applied.
- List Page now has expanding sections for each topic

## Possible Features List

- Controls for number of questions per topic asked per day
- Markdown support for questions and answers
- A spaced repetition scheduler based on the Leitner system
- User accounts, so you can have your own set of topics and questions.
- Online Hosting after converting to a production build.
- Export Option to Anki or a Mobile App if i am really loving it.
- Way to go back a question if they are randomized
- ~~hide the answer button until you've expanded the question~~
- ~~MAYBE add a show answer button to the question card (denied)~~
- ~~Setting the Default Topic on the Create Page~~
- ~~List Page updated with per-topic expanding sections~~

  Art used with [permission](https://www.instagram.com/stephaniedyrby/).
