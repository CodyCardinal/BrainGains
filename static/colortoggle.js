document.addEventListener("DOMContentLoaded", function () {
  const themeToggle = document.querySelector("#theme-toggle");
  const themeElements = document.querySelectorAll(".theme-toggle, .quiz-button");

  const updateThemeClasses = (theme) => {
    themeElements.forEach((el) => {
      if (theme === "dark") {
        el.classList.remove("btn-outline-dark");
        el.classList.add("btn-outline-light");
      } else {
        el.classList.remove("btn-outline-light");
        el.classList.add("btn-outline-dark");
      }
    });
  };

  const getStoredTheme = () => localStorage.getItem("theme");
  const setStoredTheme = (theme) => localStorage.setItem("theme", theme);

  const getPreferredTheme = () => {
    const storedTheme = getStoredTheme();
    if (storedTheme) {
      return storedTheme;
    }
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  };

  const setTheme = (theme) => {
    if (theme === "auto") {
      document.documentElement.setAttribute(
        "data-bs-theme",
        window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"
      );
    } else {
      document.documentElement.setAttribute("data-bs-theme", theme);
    }
    updateThemeClasses(theme);
  };

  setTheme(getPreferredTheme());

  const showActiveTheme = (theme, focus = false) => {
    const icon = themeToggle.querySelector("i");

    if (theme === "dark") {
      icon.classList.remove("bi-sun");
      icon.classList.add("bi-moon");
    } else {
      icon.classList.remove("bi-moon");
      icon.classList.add("bi-sun");
    }

    if (focus) {
      themeToggle.focus();
    }
  };

  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
    const storedTheme = getStoredTheme();
    if (storedTheme !== "light" && storedTheme !== "dark") {
      setTheme(getPreferredTheme());
    }
  });

  window.addEventListener("DOMContentLoaded", () => {
    showActiveTheme(getPreferredTheme());

    themeToggle.addEventListener("click", () => {
      const currentTheme = document.documentElement.getAttribute("data-bs-theme");
      const newTheme = currentTheme === "dark" ? "light" : "dark";
      setStoredTheme(newTheme);
      setTheme(newTheme);
      showActiveTheme(newTheme, true);
    });
  });
});
