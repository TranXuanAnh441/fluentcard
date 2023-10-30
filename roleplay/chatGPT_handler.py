import openai
import os

openai.api_key = os.environ.get("CHATGPT")

first_message_prompt = """
You are a Japanese teacher.
Please do rollplaying with the user in Japanese based on the prompt provided by the user.
The aim of this conversation is to practice speaking Japanesse, please don't use any English.
While doing rollplay, please leave a comment on the user language ability, like whether user's grammar or use of word is correct and suggest some improvements.
You will start first, then please wait for user's response and reply one after another.
"""

second_message_prompt = """
The prompt for roleplay is: {}. Please start the conversation first.
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
            model="gpt-3.5-turbo", messages=roleplay_messages
        )
    reply = chat.choices[0].message.content
    return reply