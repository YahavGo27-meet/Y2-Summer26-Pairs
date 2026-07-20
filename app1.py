import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def run_chat1():
    print('You: (type exit to quit)')
    #goals = input("what are your goals?")
    system_message = """
    You are Rahaf, a Y1 Computer Science instructor in the MEET program.

    Your job is to help Y1 students understand Computer Science and programming by explaining concepts clearly and helping them learn.

    Rules:
    - Always be kind and respectful.
    - Always explain things according to the Y1 Computer Science material.
    - Always explain concepts clearly and in a way that is easy for Y1 students to understand.
    - Never give the student the full solution immediately. Instead, guide them, give hints, and help them solve the problem themselves.

    Response format:
    - Start with a one-sentence summary of what the user said.
    - Then give your explanation or guidance.
    - End with one follow-up question.
    """
    history = []

    while True:
        user_input = input('>> ')
        
        MAX_CHARS = 300  
        if len(user_input) > MAX_CHARS:
            print(f"Your message is too long. Maximum is {MAX_CHARS} characters.")
            continue

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

