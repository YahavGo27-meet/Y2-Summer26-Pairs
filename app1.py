import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def run_chat():
    print('You: (type exit to quit)')
    goals = input("what are your goals?")
    system_message =  f"""
You are yotam, a meet student.

Your job is to help others.
goals: {goals}
Rules:
- Always be stupid
- Always love liverpool
- Never say the word "bad"

Response format:
- Start with a one-sentence summary of what the user said.
- Then give your response.
- End with "i love football" sentence.
"""
    history = []

    while True:
        user_input = input('>> ')

        if user_input.lower() == 'exit':
            break

        elif user_input.lower() == '/summery':
            print(history)
            continue

        history.append({'role': 'user', 'content': user_input})

        response = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=300,
            temperature=0.7,
            system=system_message,
            messages=history
        )

        reply = response.content[0].text
        #print(response)
        print(f'Claude: {reply}')
        #print('History:', history)
        history.append({'role': 'assistant', 'content': reply})

run_chat()
