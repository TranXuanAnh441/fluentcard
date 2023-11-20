function requestQuestion(request_question_url, cur_card_id, question_num, countDown) {
    $.ajax({
        url: request_question_url,
        type: "POST",
        dataType: "json",
        data: {
            'card_id': cur_card_id
        },
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        success: (data) => {
            const question = data['question'];
            let options = data['options'];
            if(options != 'None') {
                options = JSON.parse(data['options']);
                options = options.replaceAll('[', '').replaceAll(']','').replaceAll(' ', '').replaceAll("'", '');
            }
            options = options.split(',');
            document.getElementById("question").textContent = question;
            document.getElementById("number-of-question").textContent =
                `${card_counter + 1} of ${question_num} questions`;
            if (options != 'None') {
                const div = document.getElementById("question_form");
                for (let i = 0; i < options.length; i++) {
                    div.innerHTML += `<div class="option-div" onclick="checker(this)">${options[i]}</button>`
                }
            } else {
                document.getElementById("question_form").innerHTML +=
                    `<label for="answer" class="form__label">Your answer: </label>
                <input type="input" class="form__field" onkeydown="submitAnswer(this)" placeholder="Your answer" name="answer" id='answer' required/>`
            }
            countDown();
        },
        error: (error) => {
            console.log(error);
        }
    })
}