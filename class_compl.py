from collections import UserDict
from datetime import datetime

DATE_FORMAT: str = "%d.%m.%Y"

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not (len(value) == 10 and value.isdigit()):
            raise ValueError("Phone number should contain 10 digits.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value: str):
        super().__init__(datetime.strptime(value, DATE_FORMAT).date())

    def eq(self, other):
        return self.value == other.value

    def __str__(self):
        return self.value.strftime(DATE_FORMAT)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        try:
            phone_obj = Phone(phone)
            self.phones.append(phone_obj)
        except ValueError as e:
            return str(e)

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return f"Phone {phone} removed."
        return f"Phone {phone} not found."

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return f"Phone {old_phone} changed to {new_phone}."
        return f"Phone {old_phone} not found."

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
        return f"Phone {phone} not found."

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        return "Birthday added"

    def __str__(self):
        return (
            f"Contact name: {self.name.value}, "
            f"phones: {'; '.join(p.value for p in self.phones)}"
        )


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        return None

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Record {name} deleted."
        return f"Record {name} not found."
    
    def __str__(self):
        result = ""
        for record in self.data.values():
            result += str(record) + "\n"

        return result.rstrip()


    def get_birthdays_per_week(self):
        users = []
        for record in self.data.values():
            birthday = record.birthday
            if birthday:
                users.append({"name": record.name.value,
                             "birthday": record.birthday.value})
        
        week_days = {"Monday": [], "Tuesday": [], "Wednesday": [],
                    "Thursday": [], "Friday": []}
        today = datetime.today().date()
        print(f"today {today}")

        for user in users:
            name = user["name"]
            birthday = user["birthday"]
            birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday.replace(year=today.year + 1)
            delta = birthday_this_year - today
            delta_days = delta.days
            print(f"""Name: {name}, Birthday: {birthday_this_year},
                Days to birthday: {delta_days}""")

            if delta_days < 7:
                weekday = birthday_this_year.weekday()

                if weekday in [0, 5, 6]:
                    week_days["Monday"].append(name)
                elif weekday == 1:
                    week_days["Tuesday"].append(name)
                elif weekday == 2:
                    week_days["Wednesday"].append(name)
                elif weekday == 3:
                    week_days["Thursday"].append(name)
                elif weekday == 4:
                    week_days["Friday"].append(name)

        result = ""

        for key, value in week_days.items():
            if value:
                result += f"{key}: {', '.join(value)}\n" 
        return result
            



def main():
    book = AddressBook()

    id_record = Record("ID")
    id_record.add_phone("1234567890")
    id_record.add_phone("5555555555")

    book.add_record(id_record)

    kat_record = Record("Kat")
    kat_record.add_phone("9876543210")
    book.add_record(kat_record)

    print("All records in the address book:")
    for name, record in book.data.items():
        print(record)

    id = book.find("ID")
    print("Editing phone for ID:")
    print(id.edit_phone("1234567890", "1112223333"))
    print(id)

    found_phone = id.find_phone("5555555555")
    print(f"Found phone in ID's record: {found_phone}")

    print("Deleting Kat record:")
    print(book.delete("Kat"))


if __name__ == "__main__":
    main()
