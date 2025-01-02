# BrainGains

BrainGains is a local Flash Card App that was originally my final project submission for CS50X! I've continued using it for all of the learning I'm doing and adding features along the way.

![Awakening](https://github.com/CodyCardinal/BrainGains/blob/main/static/Awakening.jpeg)

## What is BrainGains?

BrainGains is a flashcard app that uses the basic methods of the [Leitner System](https://en.wikipedia.org/wiki/Leitner_system). Use BrainGains to write flash cards in question and answer form. Then quiz yourself on the topic. By practicing recall with spaced repetition, it ensures we retain the information better.

The Leitner system is a method to schedule how often you might test recalling the answer to a flash card question, braingains automates that scheduling for you.

![Leitner Learning System](https://github.com/CodyCardinal/BrainGains/blob/main/static/2560px-Leitner_system_alternative.svg.png)

In the above method, questions are sorted into groups according to how easily the learner was able to recall the answer. The learners try to recall the solution written to a question. Clicking to reveal the answer. The learner then chooses correct or incorrect, which determines when or if the questions is asked again.

## [Outdated Video Demo](https://www.youtube.com/watch?v=qdZy8P7B4JA)

## Launch via Docker

1. Download free and install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. Using your terminal of choice, change to the dir that you have `flashcards.db` backed up in.
3. If you don't have a db yet, change to a new directory, and one will be created there once you begin.
4. Run the BrainGains container from [dockerhub](https://hub.docker.com/r/codesxcodes/braingains) with the following command:

```sh
   docker run -p 5000:5000 -v .:/app/db -e DATABASE_PATH=/app/db/flashcards.db codesxcodes/braingains:latest
```
5. Open your browser to `http://localhost:5000/`

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

## Instructions

Instructions

1. Take a Course
2. Write Flashcards
3. Quiz Daily
4. Choose Correct or Incorrect.
   > 5 corrects for a question in a row and it won't be asked. Incorrect and that count resets.
5. Repeat until no questions are offered

![Quiz Image]((https://github.com/CodyCardinal/BrainGains/blob/main/static/quiz.png))

## Newish Features and Bugfixes

- The Leitner 5 Box System is implemented automatically. Quiz daily until you run out of questions.
- Braingains is now published as a [Docker Container](https://hub.docker.com/repository/docker/codesxcodes/braingains/)!

## Possible Features List/To Do

- Export Option to Anki or a Mobile App.

## Completed Features List

- ~~DB reset is now an option on the [lists](http://127.0.0.1/lists) page.~~
- ~~No more manual init needed, if no `flashcards.db` is found, it will prompt you to create one.~~
- ~~A spaced repetition scheduler based on the Leitner system~~
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
