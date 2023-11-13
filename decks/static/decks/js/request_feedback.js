function requestFeedback(request_feedback_url, cur_question, cur_answer, cur_card_id, input) {
    question_str = cur_question['question']
    if (cur_question['options']) {
        question_str += 'options:' + cur_question['options']
    }
    console.log(question_str);
    $.ajax({
        url: request_feedback_url,
        type: "POST",
        dataType: "json",
        data: {
            'question': question_str,
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
            document.getElementsByClassName('card-title')[0].style.borderBottom = '1px solid #D9D9D9';
            document.getElementsByClassName('spelling')[0].style.borderLeft = '3px solid #4D59FB';
            document.getElementById("word-slug").innerHTML = data['word-slug'] + ` <i class="fas fa-volume-up"></i>`;
            document.getElementById("word-kanji").textContent = data['word-kanji'];
            document.getElementById("word-hiragana").textContent = data['word-hiragana'];
            document.getElementById("word-definitions").textContent = data['word-definitions'];
            document.getElementById("word-slug").lastElementChild.onclick = () => {
                const synth = window.speechSynthesis;
                const utterThis = new SpeechSynthesisUtterance(data['word-slug']);
                utterThis.lang = "ja-JP";
                synth.speak(utterThis);
            }
        },
        error: (error) => {
            console.log(error);
        }
    })
}