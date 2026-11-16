from speech import listen, speak
from nlp import understand
from actions import execute_action

def main():
    print("=" * 55)
    print("NOVA - NLP Desktop Voice Assistant")
    print("Say 'help' for commands, or 'exit' to quit.")
    print("=" * 55)
    speak("Hello! I am Nova. How can I help you?")

    while True:
        try:
            command = listen()
            if not command:
                continue

            print(f"\nYou: {command}")
            result = understand(command)

            if result["intent"] == "EXIT":
                speak("Goodbye!")
                break

            response = execute_action(result)

            print(f"NOVA: {response}")
            speak(response)
            print(f"NOVA: {response}")

        except KeyboardInterrupt:
            print("\nStopping NOVA...")
            speak("Goodbye!")
            break
        except Exception as exc:
            print(f"An error occurred: {exc}")
            speak("Sorry, something went wrong.")

if __name__ == "__main__":
    main()
