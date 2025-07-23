from agent import handle_prompt

if __name__ == "__main__":
    print("Gemini File Assistant (type 'exit' to quit)")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = handle_prompt(user_input)
        print("Agent:", response)
