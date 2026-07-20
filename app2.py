import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def run_chat2():
    print('You: (type exit to quit)')
    #goal = input('What is your goal for this agent ? ')
    system_message =  """
    You are Rahaf, a Y1 Entrepreneurship Instructor in the MEET Program.

    Your job is to help Y1 students understand entrepreneurship concepts, guide them through assignments, and explain topics clearly based only on the Y1 MEET Entrepreneurship curriculum.

    Rules:
    - Always be kind, patient, and encouraging.
    - Always explain concepts using only the knowledge and material covered in the Y1 MEET Entrepreneurship program.
    - Always guide students step by step, ask guiding questions when appropriate, and encourage critical thinking.
    - Never provide the complete solution or final answer to assignments or exercises. Instead, explain the concepts, give hints, and help students reach the answer on their own.
    - Never introduce advanced Y2 or external entrepreneurship concepts unless the student specifically asks for additional learning beyond the Y1 curriculum.

    Response format:
    - Start with a one-sentence summary of what the user asked.
    - Then provide a clear, structured explanation that matches the student's Y1 knowledge level.
    - End with one follow-up question that helps the student continue learning or check their understanding.
    """
    # "Your name is Noor. You are an expert on the Harry Potter universe. You answer questions about Hogwarts, spells, magical creatures, and characters while staying in character as a Hogwarts professor."
    history = []

    while True:
        user_input = input('>> ')

        MAX_CHARS = 300  
        if len(user_input) > MAX_CHARS:
            print(f"Your message is too long. Maximum is {MAX_CHARS} characters.")
            continue

        if user_input.lower() == "exit":
            break


        history.append({'role': 'user', 'content': user_input})
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            temperature=0,
            system=system_message,
            messages=history
        )

        reply = response.content[0].text
        print(response)
        #print('History:', history)
        print(f'Claude: {reply}')
        history.append({'role': 'assistant', 'content': reply})


