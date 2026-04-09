

def choose_strategy():
    while True:
        print("Choose the prompting strategy:")
        print("1 for Zero-Shot")
        print("2 for Few-Shot")

        choice = input("Choice: ")

        if choice in ["1", "2"]:
            return choice

        print("Invalid choice, please try again.\n")