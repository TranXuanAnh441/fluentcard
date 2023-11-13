import openai
import os

openai.api_key = os.environ.get("CHATGPT")

first_message_prompt = """
You are a Japanese teacher.
Please do rollplaying with the user in Japanese based on the prompt provided by the user.
The aim of this conversation is to practice speaking Japanesse. Please don't include English translation unless the user ask you to.
The role of you and the scenario be provided by the prompt by the user.
For example, the prompt is: 'user is a student who just finished the test. ChatGPT will play the role of the classmate', then the user's role is the student and your role is the classmate.
You will start first, then please wait for user's response and reply one after another to continue the conversation.
If the user ask you to reset the conversation, please start again with the new provided prompt. 
If you are asked to provide the review, please end the current conversation and provide the review.
"""

second_message_prompt = """
Let's start a new conversation
The prompt for the new roleplay is: {}. 
Please start the conversation first.
"""

end_message_prompt = """
Let's end the conversation here. 
Please provide your review of your previous roleplay practice for the user.
You can leave comments on the user language ability, like whether user's grammar or use of word is correct and suggest some improvements.
"""

roleplay_messages = [
    {'role': 'system', 'content': first_message_prompt},
]

def sendChatMessageRequest(message, first_message=False):
    if message:
        if first_message:
            message = second_message_prompt.format(message)
        roleplay_messages.append(
            {'role': 'user', 'content': message},
        )
        chat = openai.ChatCompletion.create(
            model=os.environ.get("GPT4_MODEL"), messages=roleplay_messages
        )
    reply = chat.choices[0].message.content
    roleplay_messages.append(
        {"role": "assistant", "content": reply}
    )
    return reply

def sendChatReviewRequest():
    message = end_message_prompt
    roleplay_messages.append(
        {'role': 'system', 'content': message},
    )
    chat = openai.ChatCompletion.create(
        model=os.environ.get("GPT4_MODEL"), messages=roleplay_messages
    )
    reply = chat.choices[0].message.content
    roleplay_messages.append(
        {"role": "assistant", "content": reply}
    )
    return reply