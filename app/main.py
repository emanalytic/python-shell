import sys
import os


def main():
    # TODO: Uncomment the code below to pass the first stage
    while True:
        sys.stdout.write("$ ")
        command = input()
        if command == "exit":
            break
        elif command.startswith("echo"):
            print(command[5:])
        elif command.startswith("type"):
            if command[5:] == "echo":
                print("echo is a shell builtin")
            elif command[5:] == "type":
                print("type is a shell builtin")
            elif command[5:] == "exit":
                print("exit is a shell builtin")
            elif os.access(command[5:], os.X_OK):
                print(f"{command[5:]} is {os.access(command[5:], os.X_OK)}")
            else:
                print(f"{command[5:]}: not found")
        else:
            print(f"{command}: not found")



if __name__ == "__main__":
    main()
