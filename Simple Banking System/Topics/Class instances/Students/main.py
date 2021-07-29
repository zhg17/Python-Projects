first = input()
last = input()
year = input()

first = first[0]


class Student:
    def __init__(self, name, last_name, birth_year):
        self.name = name
        self.last_name = last_name
        self.birth_year = birth_year
        self.student_id = first + last + year

    def print_student_id(self):
        print(self.student_id)


sample_student = Student(first, last, year)
sample_student.print_student_id()
