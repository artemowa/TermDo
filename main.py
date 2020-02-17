from logic import ToDoItem, ToDoList


def run():
    todo = ToDoList()
    while True:
        command = input("Enter a command (or enter 'help'): ").lower()

        if command == 'help' or command == '':
            print("\n\t'get': view the desired entry\n"
                  "\t'add': add new entry\n"
                  "\t'delete': delete selected entry\n"
                  "\t'all': show all entries\n"
                  "\t'exit': exit the application\n")
        elif command == 'get':
            title = input('Enter a title value: ')
            if not title:
                print('And what do you want to get?')
                continue

            try:
                print('\n' + str(todo.get(title)) + '\n')
            except ValueError as error:
                print(error.args[0])
                continue

        elif command == 'add':
            title = input('Enter a title for the entry: ')
            content = input('Enter a content for the entry: ')
            if not title or not content:
                print('And what do you want to add?')
                continue

            try:
                todo.add(title, content)
            except ValueError as error:
                print(error.args[0])
                continue

        elif command == 'delete':
            title = input(
                'Enter the title of the entry you want to delete (all): '
            )
            try:
                todo.delete(title)
            except ValueError as error:
                print(error.args[0])

        elif command == 'all':
            print('\n' + str(todo))
        elif command == 'exit':
            break
        else:
            print(f"'{command}'? WTF, bruh?")


if __name__ == '__main__':
    run()
