import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def main():
    mode = input('''Do you need help with CS or Entrepreneurship? 
    1-CS 
    2-Entrepreneurship''')

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
            system=system_message,
            messages=history
        )

        reply = response.content[0].text
        print(response)
        #print('History:', history)
        print(f'Claude: {reply}')
        history.append({'role': 'assistant', 'content': reply})



if __name__ == "__main__":
    main()

    if mode == 2:
        run_chat2()
    elif mode==1:
        run_chat1()     

