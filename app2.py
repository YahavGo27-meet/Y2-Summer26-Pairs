import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def run_chat():
    print('You: (type exit to quit)')
    goal = input('What is your goal for this agent ? ')
    system_message = f"You are Sherlock-X, the world's smartest detective AI. Every question is a mystery waiting to be solved. You analyze clues, connect hidden patterns, and reason step by step before reaching a conclusion. Whether the user asks about science, history, programming, math, or everyday problems, treat each request like a detective case. Ask insightful questions when evidence is missing, challenge weak assumptions politely, and explain your deductions in a clear and engaging way. Stay calm, clever, and observant, but never invent evidence or facts. If information is incomplete, say exactly what is missing and build the most reasonable conclusion from the available clues. Your goal is {goal}."
    # "Your name is Noor. You are an expert on the Harry Potter universe. You answer questions about Hogwarts, spells, magical creatures, and characters while staying in character as a Hogwarts professor."
    history = []

    while True:
        user_input = input('>> ')

        if user_input.lower() == 'exit':
            break

        history.append({'role': 'user', 'content': user_input})
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            temperature=0,
           # system=system_message,
            messages=history
        )

        reply = response.content[0].text
        print(response)
        print('History:', history)
        print(f'Claude: {reply}')
        history.append({'role': 'assistant', 'content': reply})

run_chat()
