from class_compl import AddressBook, Record

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "ValueError: Give me name and phone please."
        except KeyError:
            return "Key Error: Contact not found."
        except IndexError:
            return "IndexError: An error occurred. Please check your input."
    return inner


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


@input_error
def add_contact(args, contacts):
    if len(args) != 2:
        raise ValueError
    name, phone = args
    record = contacts.find(name)
    if not record:
        record = Record(name)
        record.add_phone(phone)
        contacts.add_record(record)
        return "Contact added."
    
    record.add_phone(phone)

    return "Contact added."


@input_error
def change_contact(args, contacts):
    if len(args) != 3:
        raise ValueError
    name, old_phone, new_phone = args
    record = contacts.find(name)
    if not record:
        raise ValueError(f"no name {name} in address book")
    record.edit_phone(old_phone,new_phone)
    return "Contact changed."


@input_error
def get_contact(args, contacts):
    if len(args) != 1:
        raise ValueError
    name = args[0]
    if name not in contacts:
        raise KeyError
    record = contacts.find(name)

    return str(record)


@input_error
def get_all(contacts):
    return str(contacts)

@input_error
def add_birthday(args,contacts):
    name,date = args
    contacts.find(name).add_birthday(date)
    return f"added birth date for {name}"


@input_error
def show_birthday(args,contacts):
    name, = args
    birthday = contacts.find(name).birthday

    if not birthday:
        return f"no saved birthday for {name}"

    return str(birthday)
    
@input_error
def birthdays(contacts):
    return contacts.get_birthdays_per_week()

    

def main():
    contacts = AddressBook()
    help_message = [
        "Welcome to the assistant bot!",
        "Commands:",
        " - 'hello' or 'start' - to start the conversation",
        " - 'add -> (username phone)' - to add a contact",
        " - 'change -> (username phone)' - to change a contact's phone number",
        " - 'phone -> (username)' - to get a contact's phone number",
        " - 'all' - to get all contacts",
        " - 'close' or 'exit' - to exit the bot"
        
        
    ]
    print("\n".join(help_message))

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command in ["hello", "start"]:
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(get_contact(args, contacts))
        elif command == "all":
            print(get_all(contacts))
        elif command == "add-birthday":
            print(add_birthday(args,contacts))
        elif command == "show-birthday":
            print(show_birthday(args,contacts))
        elif command == "birthdays":
            print(birthdays(contacts))
        else:
            print("Invalid command format or unknown command.")





if __name__ == "__main__":
    main()
