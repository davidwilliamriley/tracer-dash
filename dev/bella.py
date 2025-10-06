# bella.py
# Simple script to get user's name and print it to terminal

def get_user_name():
    """Get the user's name from text input and print it"""
    try:
        # Get user input
        name = input("Please enter your name: ")
        
        # Print the name to terminal
        if name.strip():
            print(f"Hello, {name}!")
            print(f"Nice to meet you, {name}.")
        else:
            print("You didn't enter a name!")
    
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("=== Name Input Program ===")
    get_user_name()
    print("=== Program Complete ===")
    