# BrainGains

BrainGains is a local Flash Card App that was originally my final project submission for CS50X! I've continued using it for all of the learning I'm doing and adding features along the way.

![Awakening](https://github.com/CodyCardinal/BrainGains/blob/main/static/Awakening.jpeg)

## What is BrainGains?

BrainGains is a flashcard application designed for self-assessment in your learning journey. It adheres to the fundamental principles of the [Leitner System](https://en.wikipedia.org/wiki/Leitner_system).

Typically, you would engage in a course, attend a lecture, or watch an online video. Later, either on the same day or the following day, you'd challenge yourself to recall what you've learned. This approach combines recall and spacing as integral elements of effective learning. Utilizing spacing in our learning process can enhance the retention of information. This is because our brains are more adept at retaining knowledge when it is revisited and reinforced at intervals over time. The Leitner System provides a structured method for implementing this spaced repetition technique. This concept is analogous to how muscles are exercised: they are broken down during workouts through repetitive stress repition, and then allowed time to recover and grow stronger. Similarly, our brains benefit from spaced review and reinforcement to optimize learning.

![Leitner Learning System](https://github.com/CodyCardinal/BrainGains/blob/main/static/2560px-Leitner_system_alternative.svg.png)

In the above method, questions are sorted into groups according to how easily the learner was able to recall the answer. The learners try to recall the solution written to a question. Clicking to reveal the answer. Depending how difficult it was to recall the answer, the learner can rate their recall difficulty. The recall rating then determines when the questions is asked again.

![Animated gif of Leitner Learning System](https://github.com/CodyCardinal/BrainGains/blob/main/static/Leitner_system_animation.gif?raw=true)

In the above gif, we see that the first session starts with one container of questions. In the second session you're asked harder questions from the first session and the second containers questions. This process repeats until you're phased each question out into the final 5th container.

## [Outdated Video Demo](https://www.youtube.com/watch?v=qdZy8P7B4JA)

## Launch via Docker

1. Download free and install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. Using your terminal of choice, change to the dir that you have `flashcards.db` backed up in.
3. If you don't have a db yet, change to a new directory, and one will be created here once you begin.
4. Run the BrainGains container from [dockerhub](https://hub.docker.com/r/codesxcodes/braingains) with the following command:

```sh
   docker run -p 5000:5000 -v .:/app/db -e DATABASE_PATH=/app/db/flashcards.db codesxcodes/braingains:latest
```

## Launch Locally via Python and Flask

- Install Python 3.10+
- Clone the Repo and Move into the directory.

```sh
  git clone https://github.com/CodyCardinal/BrainGains.git
  cd BrainGains
```

- If you have a `flashcards.db`, place it in the `db` directory and the app will use it.
- Install the requirements with `pip install -r requirements.txt`
- Run the flask app locally with `flask run`
- Open your browser to `http://localhost:5000/`

## Recommended Use

## 1. Take a coding course

- While you are taking a course or lecture. Use braingains to take notes in the form of flashcards.
- When you go to take notes, [create](http://127.0.0.1:5000/create) a new question and answer in BrainGains, specifying that course and topic.
- You can use markdown for code snippets, and Braingains will add code coloring for most languages using `markdown2`.

## 2. Review what your learned over the next 6 days

- Wait a few hours ( at least ) or overnight to practice recall and quiz yourself.
- Choose that topic on the home page.
- Read each question, mentally answer the question.
- Once you've answered it mentally, click the answer button to reveal the answer.
  - Self Evalutate how you did in your answer.
  - If you want to try again, click Again.
  - If you answered it correctly and easily, click Easy.
  - If you answered it correctly, but not easily, click Good.
  - If you failed to answer it, you would click Hard.
- Choosing will proceed to the next question.
- Once you answer all questions in your current session, you will return to the index.

## 3. Space out quizzing yourself again

- Continue to re-take these questions daily for about [6 days](https://en.wikipedia.org/wiki/Spaced_repetition#/media/File:ForgettingCurve.svg)
- Space out quizzing back to this topic over time. Let the app hide questions you have mastered. Or you can use the [Leitner System](https://en.wikipedia.org/wiki/Leitner_system).
- Mastering a question means it has a session set to 4. Therefore answering "easy" three times in a row is what it takes to make a question no longer appear.
- Once you aren't asked any questions in that topic, you're done with that topic. It is now time for a new Topic!
- If you want to reset any questions, set their session back to 0.

## Newish Features and Bugfixes

- Braingains is now published as a [Docker Container](https://hub.docker.com/repository/docker/codesxcodes/braingains/)!
- DB reset is now an option on the [lists](http://127.0.0.1/lists) page.
- No more manual init needed, if no `flashcards.db` is found, it will prompt you to create one.

## Possible Features List/To Do

- Controls for number of questions per topic asked per day
- A spaced repetition scheduler based on the Leitner system
- User accounts, so you can have your own set of topics and questions.
- Online Hosting after converting to a production build.
- Export Option to Anki or a Mobile App.
- Way to go back a question if they are randomized.

## Completed Features List

- ~~Sections and Markdown support added.~~
- ~~Code refactor, moved functions and routes into their own file. implementing blueprints.~~
- ~~move either routes or crud functions into their own library for reuse.~~
- ~~Sections for topics. So the hierarchy is sections>topics>questions.~~
- ~~Markdown support for questions and answers~~
- ~~Ref/Markdown/HTML Snippet section for the questions. This way you can q&a against a reference.~~
- ~~Get functions for creation out of the /create route itself.~~
- ~~list questions on the create page~~
- ~~hide the answer button until you've expanded the question~~
- ~~MAYBE add a show answer button to the question card (denied)~~
- ~~Setting the Default Topic on the Create Page~~
- ~~List Page updated with per-topic expanding sections~~
- ~~Create Page now always defaults to the newest topic~~
- ~~Pep8 Python Formatting Applied.~~
- ~~Deleting and Editing Topics added.~~

"Awakening" is used with permission from the artist [Stephanie Dryby](https://www.instagram.com/stephaniedyrby/).
