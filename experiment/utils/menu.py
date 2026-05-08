

def choose_input_type():
    print("Choose the input type:")
    print("1 for HTML")
    print("2 for Images")
    print("3 for functionality extraction")

    choice = input("Choice: ")

    if choice == "1":
        return "html"
    elif choice == "2":
        return "image"
    elif choice == "3": 
        return "extraction"
    else:
        print("Invalid choice, defaulting to HTML.")
        return "html"


def choose_strategy():
    print("Choose the prompting strategy:")
    print("1 for Zero-Shot")
    print("2 for Few-Shot")
    print("3 for functionality extraction")

    choice = input("Choice: ").strip()
    return choice