const btn = document.querySelector(".btn-toggle");

const currentTheme = localStorage.getItem("theme");

if (currentTheme == "dark") {
    document.body.classList.toggle("dark-mode");
} else if (currentTheme == "light") {
    document.body.classList.toggle("light-mode");
}

btn.addEventListener("click", function () {
    document.body.classList.toggle("dark-mode");
    var theme = document.body.classList.contains("dark-mode") ? "dark" : "light";

    localStorage.setItem("theme", theme);
});
