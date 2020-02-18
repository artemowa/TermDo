from app import ToDoItem, ToDoList
from app import exceptions


def run():
    todo = ToDoList()
    while True:
        command = input("Enter a command (or enter 'help'): ").lower()

        if command == 'help':
            print("\n\t'add': add new entry\n"
                  "\t'change': change selected entry\n"
                  "\t'delete': delete selected entry\n"
                  "\t'clear': delete all entries\n"
                  "\t'show': show all entries\n"
                  "\t'exit': exit the application\n")
        elif command == 'add':
            title = input('Enter a title for the entry: ')
            if not title:
                print('And what do you want to add?')
                continue

            try:
                todo.add(title)
            except SaveError as error:
                print(error.args[0])
                continue

        elif command == 'change':
            try:
                identifier = int(
                    input('Enter the ID of the entry you want to change: ')
                )
                new_title = input('Enter a new title for this entry: ')
                if not identifier or not new_title:
                    print('And what you want to change?')
                    continue

                todo.change(identifier, new_title)
            except exceptions.ChangeError as error:
                print(error.args[0])
            except ValueError:
                print('And what do you want to change?')

        elif command == 'delete':
            try:
                identifier = int(
                    input('Enter the ID of the entry you want to delete: ')
                )
                todo.delete(identifier)
            except exceptions.DeleteError as error:
                print(error.args[0])
            except ValueError:
                print('And what do you want to delete?')

        elif command == 'clear':
            todo.clear()
        elif command == 'show':
            print('\n' + str(todo))
        elif command == 'exit':
            break
        elif command == '':
            continue
        else:
            print(f"'{command}'? WTF, bruh?")


if __name__ == '__main__':
    run()
