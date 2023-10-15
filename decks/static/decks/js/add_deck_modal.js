var modal = document.getElementById("addDeckModal");
var btn = document.getElementById("addDeckBtn");
var span = document.getElementsByClassName("close")[0];
var bg = document.getElementsByClassName("bg")[0];

btn.onclick = function () {
    modal.style.display = "block";
    bg.classList.add("blur");
}

span.onclick = function () {
    modal.style.display = "none";
    bg.classList.remove("blur");
}

window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
        bg.classList.remove("blur");
    }
}