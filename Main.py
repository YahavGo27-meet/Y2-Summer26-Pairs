import os
from anthropic import Anthropic
from dotenv import load_dotenv
from app1 import run_chat1
from app2 import run_chat2

load_dotenv()

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

mode=""

def main():
    mode = input('''Do you need help with CS or Entrepreneurship? 
    1-CS 
    2-Entrepreneurship''')
    if mode == "2":
        run_chat2()
        print()
    elif mode == "1":
        run_chat1()  


if __name__ == "__main__":
    main()

    
