import os
from anthropic import Anthropic
from dotenv import load_dotenv
import certifi

os.environ["SSL_CERT_FILE"] = certifi.where()

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def search_web(query):
    if not query.strip():
        return "Please enter a search query."

    try:
        messages = [{
            "role": "user",
            "content": (
                "Search the web for the following question. Give a brief, "
                "clear answer suitable for a Y1 Computer Science student:\n"
                f"{query}"
            )
        }]
        tools = [{
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": 3,
        }]

        for _ in range(3):
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=1000,
                messages=messages,
                tools=tools,
            )

            if response.stop_reason != "pause_turn":
                break

            messages.append({"role": "assistant", "content": response.content})
        else:
            return "The web search took too long. Please try again."

        answer = "\n".join(
            block.text
            for block in response.content
            if block.type == "text"
        ).strip()

        if not answer:
            return "Rahaf could not create an answer from the search results."

        return answer

    except Exception as error:
        return f"Error searching the web: {error}"

def run_chat1(history=None):
    print("You: (type exit to quit, or /search to search the web)")
    #goals = input("what are your goals?")
    system_message = """
    You are Rahaf, a professional Fashion Researcher and Design Assistant.

    Your job is to help users research fashion by finding inspiration, color palettes, fabrics, materials, historical fashion references, similar designs, fashion aesthetics, garment construction ideas, and design trends. You provide well-researched, accurate, and creative information that helps users develop their own fashion concepts.

    Rules:
    - Always provide accurate and well-organized fashion research.
    - Always explain why you recommend a specific color palette, fabric, or design reference.
    - Always encourage creativity while respecting the user's design goals and preferences.
    - If information is uncertain or trend-based, clearly state that.
    - Never copy or encourage copying another designer's work; use references only for inspiration.
    - Never invent facts or claim research that you cannot verify.
    - Never design the entire collection or complete project for the user; guide and inspire them instead.

    Response format:
    - Start with a one-sentence summary of what the user is looking for.
    - Then provide your research, recommendations, and explanations using clear headings and bullet points when appropriate.
    - End with one follow-up question to better understand the user's design.
    """

    # App 2 can pass its conversation here so this agent knows its answer.
    history = list(history) if history else []

    while True:
        user_input = input('>> ')

        MAX_CHARS = 300  
        if len(user_input) > MAX_CHARS:
            print(f"Your message is too long. Maximum is {MAX_CHARS} characters.")
            continue

        if user_input.lower() == 'exit':
            break

        elif user_input.lower() == "/search":
            query = input("What would you like to search for? ").strip()

            print("Searching the web...")

            answer = search_web(query)

            print(f"\nSearch result:\n{answer}\n")

            history.append({
                "role": "user",
                "content": f"Web search: {query}"
            })

            history.append({
                "role": "assistant",
                "content": answer
            })

            continue

        history.append({"role": "user", "content": user_input})

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
