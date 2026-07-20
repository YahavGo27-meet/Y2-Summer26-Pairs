import os
from anthropic import Anthropic
from dotenv import load_dotenv
from app1 import run_chat1
from app2 import run_chat2

load_dotenv()

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def main():
        mode=""
        while mode != "exit":
            mode=""
            print("Invalid input. Please enter 1 for CS or 2 for Entrepreneurship.")
            mode = input('''Do you need help with CS or Entrepreneurship? 
            1-CS 
            2-Entrepreneurship
                         ''')
            print("user chose", mode)
            
            if mode == "2":
                run_chat2()
                break
            elif mode == "1":
                run_chat1()
                break 


if __name__ == "__main__":
    main()


    
