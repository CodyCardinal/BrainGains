# BRAIN GAINS

Brain gains is my final project submission for CS50X! 
I've used Python, Flask, SQLlite, and Bootstrap Javascript.

## [Video Demo](https://www.youtube.com/watch?v=qdZy8P7B4JA)

## How to start:
Start by Initializing the DB ( you can also use this to reset! ):
```py
python init_db.py
```

Now going forward just run the website with flask!

```py
flask run
```


Brain Gains is following the basic methods of the [Leitner System](https://en.wikipedia.org/wiki/Leitner_system). Test yourself after learning so that you can retain whatever you learned better. The use of spacing in our learning can lead to better retention of information. This is because the brain is better at remembering things that are spaced out over time. The Leitner System is a way to organize that spacing. This is similar to how a muscle should be broken down, and given time to repair itself stronger.

![Leitner Learning System](https://github.com/CodyCardinal/CS50Final/blob/main/static/2560px-Leitner_system_alternative.svg.png?raw=true)

In the above method, questions are sorted into groups according to how easily the learner was able to recall the answer. The learners try to recall the solution written to a question. Clicking to reveal the answer. Depending how difficult it was to recall the answer, the learner can rate their recall difficulty. The recall rating then determines when the questions is asked again.

![Animated gif of Leitner Learning System](https://github.com/CodyCardinal/CS50Final/blob/main/static/Leitner_system_animation.gif?raw=true)

In the above gif, we see that the first session starts with one container of questions. In the second session you're asked harder questions from the first session and the second containers questions. This process repeats until you're phased each question out into the final 5th container.


## Detailed How-To

- Start by creating a few questions in a topic.
- Once the topic has around 20 questions stop creating questions.
- Go back to the home page and choose that topic.
- Proceed to read each question, mentally answer the question.
- Once you've answered it mentally, click to expand the answer.
- If you answered it correctly and easily, you would click Easy.
- If you answered it correctly, but not easily, click Good.
- If you failed to answer it, you would click Hard.
- Then proceed to the next question. Eventually you will be taken back to the front page.
- Come back and answer questions again tomorrow. Eventually you will notice that questions stop being offered to you.
- Once you aren't asked questions anymore, you can consider quizzing on a new topic, because you've successfully recalled all of the questions.
