import os
from urllib import response
from anthropic import Anthropic
from dotenv import load_dotenv
from app1 import run_chat1
from app2 import run_chat2
from app2 import create_pdf 


load_dotenv()

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def main():
        mode=""
        while True:
            mode=""
            print("Please enter 1 for CS or 2 for Entrepreneurship.")
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
            elif mode == "exit":
                break

               # save_pdf = input("Do you want to save the answer as a PDF? yes/no: ")
                #if save_pdf.lower() == "yes":
                    #filename = input("Enter the PDF name: ").strip()

                    #if not filename:
                        #filename = "agent_answer"

                    #if not filename.lower().endswith(".pdf"):
                        #filename += ".pdf"

                    #reply = response.content[0].text
                    #create_pdf(reply, filename)
                    #break




if __name__ == "__main__":
    main()


    
