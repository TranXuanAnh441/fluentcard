import openai
import os
import ast
import json
from .prompts import *

openai.api_key = os.environ.get("CHATGPT")

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
