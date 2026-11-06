import os
from openai import OpenAI,APIError,AuthenticationError,RateLimitError
from dotenv import load_dotenv

load_dotenv()

api_key=os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY not found. Please configure your .env file."
    )

client = OpenAI(api_key=api_key)

messages = [
    {
        "role": "system",
        "content": "You are a helpful AI assistant. "
                   "Give clear and beginner-friendly answers."
    }
]

def chat_with_ai(user_input):
    messages.append({
        "role": "user",
        "content": user_input
    })

    try:
        response =client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            temperature=0.7
        )

        ai_response = response.choices[0].message.content
        messages.append({
            "role": "assistant",
            "content": ai_response
        })
        return ai_response

    except AuthenticationError:
        messages.pop()
        return "Authentication failed. Please check your API key."
    except RateLimitError:
        messages.pop()
        return "Rate limit exceeded. Please try again later."
    except APIError as e:
        messages.pop()
        return f"API error occurred: {e}"
    except Exception as e:
        messages.pop()
        return f"An unexpected error occurred: {e}"

def main():

    print("\n================================")
    print("       AI CLI CHATBOT")
    print("================================")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input.strip():
            print("Please enter a valid message.")
            continue

        if user_input.lower() == "exit":
            print("Exiting the chatbot. Goodbye!")
            break

        ai_response = chat_with_ai(user_input)
        print(f"AI: {ai_response}\n")

if __name__ == "__main__":
    main()        