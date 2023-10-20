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
                // $(input).css('border-color', 'green');
            } else {
                $(input).addClass('incorrect');
                // $(input).css('border-color', 'red');
            }
            document.getElementById("feedback").textContent = data['explanation'];
            document.getElementById("card-title").textContent = data['card-title'];
            document.getElementById("card-content").textContent = data['card-content'];

        },
        error: (error) => {
            console.log(error);
        }
    })
}