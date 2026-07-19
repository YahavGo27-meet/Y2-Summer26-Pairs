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

        while mode != "1" and mode != "2" and mode != "exit":
            print("Invalid input. Please enter 1 for CS or 2 for Entrepreneurship.")
            mode = input('''Do you need help with CS or Entrepreneurship? 
            1-CS 
            2-Entrepreneurship''')
            
            if mode == "2":
                run_chat2()
            elif mode == "1":
                run_chat1() 

                
        # else:
        #     while mode != "1" and mode != "2":
        #         print("Invalid input. Please enter 1 for CS or 2 for Entrepreneurship.")
        #         mode = input('''Do you need help with CS or Entrepreneurship?''' )
        #         if 
        #     #if mode == "exit":
        #        # break

if __name__ == "__main__":
    main()


    
