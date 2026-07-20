import json


# 1. Reverse a string
def reverse_string(text):
    return text[::-1]


# 2. Count duplicate characters
def count_duplicate_characters(text):
    character_count = {}

    for character in text:
        if character != " ":
            character_count[character] = character_count.get(character, 0) + 1

    duplicates = {
        character: count
        for character, count in character_count.items()
        if count > 1
    }

    return duplicates


# 3. Find missing number
def find_missing_number(numbers):
    expected_count = len(numbers) + 1

    expected_sum = expected_count * (expected_count + 1) // 2
    actual_sum = sum(numbers)

    return expected_sum - actual_sum


# 4. Remove duplicates from a list
def remove_duplicates(items):
    return list(dict.fromkeys(items))


# 5. Read a file
def read_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return f"File '{filename}' was not found."


# 6. Parse JSON
def parse_json(json_string):
    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        return "Invalid JSON data."


# 7. Sort data
def sort_numbers(numbers):
    return sorted(numbers)


def sort_people_by_age(people):
    return sorted(people, key=lambda person: person["age"])


# 8. Dictionary and list manipulations
def dictionary_and_list_examples():
    numbers = [10, 20, 30, 40]

    # Add item to list
    numbers.append(50)

    # Remove item from list
    numbers.remove(20)

    # Create squares using list comprehension
    squares = [number**2 for number in numbers]

    employee = {
        "name": "Manoj",
        "role": "QA Automation Engineer",
        "experience": 8,
    }

    # Add dictionary item
    employee["location"] = "Toronto"

    # Update dictionary item
    employee["experience"] = 9

    return numbers, squares, employee


# 9. Basic OOP
class Employee:
    def __init__(self, name, role, experience):
        self.name = name
        self.role = role
        self.experience = experience

    def display_details(self):
        return (
            f"Name: {self.name}, "
            f"Role: {self.role}, "
            f"Experience: {self.experience} years"
        )

    def is_senior(self):
        return self.experience >= 5


# Main execution
if __name__ == "__main__":

    print("1. Reverse a string")
    text = "Python"
    print(reverse_string(text))

    print("\n2. Count duplicate characters")
    text = "programming"
    print(count_duplicate_characters(text))

    print("\n3. Find missing number")
    numbers = [1, 2, 3, 5, 6]
    print("Missing number:", find_missing_number(numbers))

    print("\n4. Remove duplicates")
    items = [1, 2, 2, 3, 4, 4, 5]
    print(remove_duplicates(items))

    print("\n5. Read a file")
    print(read_file("sample.txt"))

    print("\n6. Parse JSON")
    json_data = '{"name": "Manoj", "role": "QA Engineer", "experience": 8}'
    parsed_data = parse_json(json_data)
    print(parsed_data)

    if isinstance(parsed_data, dict):
        print("Name:", parsed_data["name"])

    print("\n7. Sort data")
    numbers = [5, 2, 9, 1, 3]
    print("Sorted numbers:", sort_numbers(numbers))

    people = [
        {"name": "John", "age": 35},
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 30},
    ]

    print("People sorted by age:")
    print(sort_people_by_age(people))

    print("\n8. Dictionary and list manipulations")
    numbers, squares, employee = dictionary_and_list_examples()

    print("Updated list:", numbers)
    print("Squares:", squares)
    print("Employee dictionary:", employee)

    print("\n9. Basic OOP")
    employee_object = Employee(
        "Manoj",
        "QA Automation Engineer",
        8,
    )

    print(employee_object.display_details())
    print("Is senior employee:", employee_object.is_senior())