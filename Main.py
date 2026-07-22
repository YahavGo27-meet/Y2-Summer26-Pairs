import os
from urllib import response
from anthropic import Anthropic
from dotenv import load_dotenv
from app1 import run_chat1
from app2 import run_chat2
from app2 import create_pdf

def main():
        mode=""
        while True:
            mode=""
            print("Please enter 1 for Fashion Researcher or 2 for Design Assistan.")
            mode = input('''Do you need help with CS or Design Assistan? 
            1-Fashion Researcher 
            2-Design Assistan
                         ''')
            print("user chose", mode)
            
            if mode == "2":
                app2_history = run_chat2()

                continue_to_research = input(
                    "Would you like the Design Assistant to build on this answer? yes/no: "
                ).strip().lower()
                if continue_to_research in {"yes", "y"}:
                    run_chat1(app2_history)
                break
            elif mode == "1":
                run_chat1()
                break
            elif mode == "exit":
                break

              




if __name__ == "__main__":
    main()
    
