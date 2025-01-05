function revealAnswer() {
  const button           = document.getElementById("show-answer-button");
        button.innerHTML = "Answer Revealed";
  button.classList.add("disabled");
  button.setAttribute("aria-disabled", "true");

  const answerText               = document.getElementById("answer-text");
        answerText.style.display = "block";
  answerText.classList.add("text-start");
}
