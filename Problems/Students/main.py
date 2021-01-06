class Student:

    def __init__(self, name, last_name, birth_year):
        self.name = name
        self.last_name = last_name
        self.birth_year = birth_year
        self.student_id = f"{name[0]}{last_name}{birth_year}"
        # calculate the student_id here


name_input = input()
last_name_input = input()
year_input = int(input())

student = Student(name_input, last_name_input, year_input)
print(student.student_id)
