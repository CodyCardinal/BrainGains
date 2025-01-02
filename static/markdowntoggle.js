document.addEventListener("DOMContentLoaded", function () {
  let tabEnabled = true;

  function enableTab(id) {
    var el = document.getElementById(id);
    el.addEventListener("keydown", function (e) {
      if (tabEnabled && e.key === "Tab" && e.shiftKey) {
        e.preventDefault();
        var start = this.selectionStart;
        var end = this.selectionEnd;
        this.value = this.value.substring(0, start) + "\t" + this.value.substring(end);
        this.selectionStart = this.selectionEnd = start + 1;
      }
    });
  }

  enableTab("question");
  enableTab("answer");

  document.getElementById("toggle-tab").addEventListener("click", function (e) {
    e.preventDefault();
    tabEnabled = !tabEnabled;
    const icon = document.getElementById("toggle-icon");
    if (tabEnabled) {
      icon.classList.remove("bi-toggle-off");
      icon.classList.add("bi-toggle-on");
    } else {
      icon.classList.remove("bi-toggle-on");
      icon.classList.add("bi-toggle-off");
    }
  });
});
