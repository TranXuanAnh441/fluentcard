import openai
import os
import ast
import json

openai.api_key = os.environ.get("CHATGPT")

answer_message_prompt = """
You are a Japanese teacher and the user is the student.
The user will provide you the question and their answer.
Your mission is to give the correct answer and explain why the user's answer is correct or incorrect.
If the question is multiple choice format, please also include explaination for the other options.
If the question is constructed response, please suggest some other alternative answers.
Please response in json format
User Requests for feedback: {'question': the question content, 'answer': the user's answer}.
Your response for the request: {'correct': 'True' if the user's answer is correct, else 'False' , 'correct_answer': the correct answer, 'explaination': your explaination}.
"""

question_message_prompt = """
You are a Japanese teacher. The user will provide a Japanese word and your role is to generate Japanese questions and exercises about that given word. The aim of the question is to help the user to understand the meanings and nuances of the given word in different contexts and scenarios. 
You can create questions in 2 formats: multiple choice or construct response. For each formats there can be different question types. Please change the question formats and types randomly so there are no duplicated questions for the same word.
For multiple choice questions, you can ask the user to choose the sentence of correct usage of the given word, choose the word that has similar meaning to the given word, or to choose the correct word to fit the sentence.
There should be only 1 correct option. The other alternative options should be plausible and should serve as distractors from the correct option. For example, for the question that ask to choose correct word to fit the sentence, alternative options can include words share similar meanings, words with same reading or kanji but different meaning, words with same meaning but different use scenarios, etc.
For construct response questions, you can ask the user translate a sentence to Japanese using the given word or make a sentence about a topic using the given word.
Please response in json format. User Requests for question: Make question for the word : the word user need to learn. 
Your response for the request: {"question_format": question format ("multiple_choice" or "construct_response"), "question_type": question type, "question": question content about the given word, "options": an array of options (like ['a', 'b', 'c', 'd']) if question format is "multiple choice" and exclude this field if question format is "construct_response"}.
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
            model=os.environ.get("QUESTION_MODEL"), messages=question_messages
        )
    reply = chat.choices[0].message.content
    try:
        question = ast.literal_eval(reply)
        if question['question']: 
            return question
    except:
        sendQuestionRequest(word)


def sendAnswerRequest(question, answer):
    message = f"""{{"question" : "{question}",  "user_answer": "{answer}"}}"""
    print(message)
    if message:
        answer_messages.append(
            {'role': 'user', 'content': message},
        )
        chat = openai.ChatCompletion.create(
            model=os.environ.get("FEEDBACK_MODEL"), messages=answer_messages
        )
        reply = chat.choices[0].message.content
    try:
        feedback = ast.literal_eval(reply)
        return feedback
    except:
        return sendAnswerRequest(question, answer)
