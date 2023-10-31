var deck_info = document.getElementsByClassName("deck-info");

for (var i = 0; i < deck_info.length; i++) {
    var progress = deck_info[i].querySelector(".progress");
    ratio = parseInt((progress.getAttribute("learnt-card-num"))) / parseInt((progress.getAttribute("card-num"))) * 100;
    if (parseInt((progress.getAttribute("card-num"))) - parseInt((progress.getAttribute("learnt-card-num"))) <= 0) {
        deck_info[i].querySelector("#learn-deck-btn").disabled = true;
        deck_info[i].querySelector("#learn-deck-btn").style.backgroundColor = "grey";
        deck_info[i].querySelector("#learn-deck-btn a").removeAttribute("href");
    }
    progress.style.setProperty('--bar-width', ratio + '%');
}