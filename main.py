def multipleChoice(question, options):
    question += "\n"
    valid = ""
    i = 0

    while i < len(options):
        question += chr(i + 97)
        valid += chr(i + 97)
        question += ") "
        question += options[i]
        question += "\n"

        i += 1

    while True:
        userInput = input(question)
        if (userInput in valid) and (len(userInput) == 1):
            return userInput
        else:
            print("Invalid input")

mode = multipleChoice("Would you like simple or advanced mode?", ["simple", "advanced"])
