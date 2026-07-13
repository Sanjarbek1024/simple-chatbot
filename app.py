from database import create_tables, get_last_session, save_message, load_history 
from chatbot import ask_gemini 

def main():
    create_tables()
    
    session_id = get_last_session()
    
    history = load_history(session_id)
    
    print('=' * 50)
    print("Simple Chatbot")
    print(f'Session: {session_id}')
    print("Type 'exit' to 'quit'")
    print('=' * 50)
    
    if history:
        print('\nPrevious conversation restored.\n')
        
    while True:
        user_input = input('You: ')
        
        if user_input.lower() == "exit":
            print("Bye.")
            break
        
        try:

            save_message(session_id, "user", user_input)

            history = load_history(session_id)

            answer = ask_gemini(history, user_input)

            print(f"\nBot: {answer}\n")

            save_message(session_id, "assistant", answer)

        except Exception as e:
            print(e)
            
if __name__ == "__main__":
    main()