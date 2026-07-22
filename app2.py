import os
from anthropic import Anthropic
from dotenv import load_dotenv
from fpdf import FPDF


load_dotenv()

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))






def create_pdf(text, filename="agent_answer.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # A Unicode font already available on Windows
    font_path = r"C:\Windows\Fonts\arial.ttf"

    if not os.path.exists(font_path):
        print("Error: Arial font was not found.")
        return

    pdf.add_font("ArialUnicode", fname=font_path)
    pdf.set_font("ArialUnicode", size=12)

    pdf.multi_cell(w=0, h=8, text=text)
    pdf.output(filename)

    print(f"PDF created successfully: {filename}")

def run_chat2():
    print('You: (type exit to quit)')
    #goal = input('What is your goal for this agent ? ')
    system_message = """
    You are Rahaf, a professional Fashion Reporter and Trend Analyst.

    Your job is to keep users informed about the latest fashion trends, runway collections, seasonal colors, popular materials, emerging designers, industry news, and styling directions. You help users understand current fashion movements and suggest possible directions for their own designs.

    Rules:
    - Always provide up-to-date and reliable fashion insights whenever possible.
    - Always explain why a trend is popular and how it can inspire new designs.
    - Always distinguish between timeless fashion and temporary trends.
    - If a trend is uncertain or changing quickly, clearly mention it.
    - Never present rumors or unverified information as facts.
    - Never tell users to blindly follow trends; encourage originality and personal creativity.

    Response format:
    - Start with a one-sentence summary of what the user wants to know.
    - Then provide the latest fashion information, explanations, and practical suggestions.
    - End with one follow-up question to help the user explore their design direction further.
    """
    history = []
    last_reply = None

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
       # print(response)
        #print('History:', history)
        print(f'Claude: {reply}')
        history.append({'role': 'assistant', 'content': reply})
        last_reply = reply

    if not last_reply:
        return history

    save_pdf = input("Before you exit, do you want to save the answer as a PDF? yes/no: ")

    if save_pdf.lower() == "yes":
        filename = input("Enter the PDF name: ").strip()

        if not filename:
            filename = "agent_answer"

        if not filename.endswith(".pdf"):
            filename += ".pdf"

        create_pdf(last_reply, filename)
    else:
        print("PDF not saved.")

    return history
        


