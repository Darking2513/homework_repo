from collections import UserDict

class Field: # базовий клас
    def __init__(self, value):
        self.value = value

    def __str__(self): # метод для виведення значення
        return str(self.value)

class Name(Field):
    def __init__(self, value: str):
        self._validate(value)
        formatted = value.strip().title()
        super().__init__(formatted)

    def _validate(self, value): # метод для валідації імені
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        if not value.strip():
            raise ValueError("Name cannot be empty")
        if not value.replace(" ", "").isalpha():
            raise ValueError("Name must contain only letters and spaces")

class Phone(Field): # клас для телефону
    def __init__(self, value):
         super().__init__(value)
         self._validate(value)

    def _validate(self, value): # метод для валідації телефону
        if not isinstance(value, str):
            raise ValueError("Phone number must be a string")
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")
        if len(value) !=10:
            raise ValueError("Phone number must be exactly 10 digits long")
              

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_str: str): # метод для додавання телефону
        phone = Phone(phone_str)
        self.phones.append(phone)

    def remove_phone(self, phone_str: str): # метод для видалення телефону
        phone = self.find_phone(phone_str)
        if phone:
            self.phones.remove(phone)
        else:
            raise ValueError("Phone not found")

    def edit_phone(self, old_phone_str: str, new_phone_str: str): # метод для редагування телефону
        old = self.find_phone(old_phone_str)
        if old is None:
            raise ValueError("Old phone not found")
        self.remove_phone(old_phone_str)
        self.add_phone(new_phone_str)

    def find_phone(self, phone_str: str): # метод для пошуку телефону
        for p in self.phones:
            if p.value == phone_str:
                return p
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict): # клас для адресної книги

    def add_record(self, record: Record): # метод для додавання запису
        self.data[record.name.value] = record
    
    def find(self, name: str) -> Record: # метод для пошуку запису
        if name not in self.data:
              return None
        return self.data.get(name)
    
    def delete(self, name: str): # метод для видалення запису
        if name in self.data:
            del self.data[name]
    
    def __str__(self): # метод для виведення адресної книги
        return '\n'.join(str(record) for record in self.data.values())
    

# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі
print(book)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john) # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

# Видалення запису Jane
book.delete("Jane")