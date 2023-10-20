function requestFeedback(request_feedback_url, cur_question, cur_answer, cur_card_id, input) {
    $.ajax({
        url: request_feedback_url,
        type: "POST",
        dataType: "json",
        data: {
            'question': JSON.stringify(cur_question),
            'answer': cur_answer,
            'card_id': cur_card_id,
            'time': timeLeft.textContent,
        },
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        success: (data) => {
            console.log(data);
            $(input).removeClass('check');
            if ((data['correct'] == 'True') || (data['correct'] == 'true') || (data['correct'] == true)) {
                $(input).addClass('correct');
            } else {
                $(input).addClass('incorrect');
            }
            document.getElementById("feedback").textContent = data['explanation'];
            document.getElementById("word-slug").innerHTML = data['word-slug'] + `<i class="fas fa-volume-up"></i>`;
            document.getElementById("word-kanji").textContent = data['word-kanji'];
            document.getElementById("word-hiragana").textContent = data['word-hiragana'];
            document.getElementById("word-definitions").textContent = data['word-definitions'];
        },
        error: (error) => {
            console.log(error);
        }
    })
}