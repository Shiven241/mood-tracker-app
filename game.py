command=""
started = True
while command != "exit":
    command = input("Enter a command (type 'exit' to quit): ")
    if command == "hello":
        if not started:
            started = True
            print("Game started!")
        print("Hello, player!")
    elif command == "help":
        started = False
        print("Help: This is a simple game command interface.")
        print("""Available commands: hello, help, exit""")
    elif command == "exit":
        print("exit Goodbye!")
    else:
        command = "Ronny"
        print("Unknown command. Type 'help' for a list of commands.")