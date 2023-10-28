import openai
import os
import ast
import json

openai.api_key = os.environ.get("CHATGPT")

answer_message_prompt = """
This is a Japanese learning app, your role is to give feedback for user's answer of a question.
Please explain why the answer is correct or incorrect. Please provide detail explanations, some alternative answers to the question or additional knowledge relating the answer.
The response should look like: {{"correct" : "True" if the user's answer is correct, "explanation": your explaination}}
"""

question_message_prompt = """
This is a Japanese learning app. 
The user will provide a Japanese word and your role is to generate Japanese exercise to help user learn the meaning of a given word.
The aim of the question is to help the user's understanding of the word in different contexts and distinguish words with similar meanings.
You can ask user to write a sentence, in which sentences the word's meaning is correct, what is the correct word to use in the sentence. 
The question can be in any types: multiple choice, make a sentence, etc. 
Please change the question randomly so there are no duplicated questions for the same word.
Please response in json format
User Requests for question: Make question for the word : the word user need to learn
Your response for the request: {"question_type": question type, "question": question content about the given word, "options": an array of options (like ['a', 'b', 'c', 'd']) if quesiton_type is multiple choice and exclude this field if not }
"""

question_messages = [
    {'role': 'system', 'content': question_message_prompt},
]

answer_messages = [
    {'role': 'system', 'content': answer_message_prompt},
]


def sendQuestionRequest(word):
    message = "Make question for the word: " +  word
    if message:
        question_messages.append(
            {'role': 'user', 'content': str(message)},
        )
        chat = openai.ChatCompletion.create(
            model=os.environ.get("MODEL"), messages=question_messages
        )
    reply = chat.choices[0].message.content
    print(reply)
    try:
        question = ast.literal_eval(reply)
        if question['question'] and question['question'] != '':
            return question
        else:
            raise KeyError
    except:
        sendQuestionRequest(word)


def sendAnswerRequest(question, answer):
    message = "For the question {0}, my answer is : {1}.".format(question, answer)
    if message:
        answer_messages.append(
            {'role': 'user', 'content': message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=answer_messages
        )
        reply = chat.choices[0].message.content
    try:
        feedback = json.loads(reply)
        print(feedback)
        if feedback['correct'] and feedback['explanation']:
            return feedback
        else:
            raise KeyError
    except:
        return sendAnswerRequest(question, answer)
