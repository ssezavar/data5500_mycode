# Sara Sezavar Dokhtfaroughi -- A02422030 -- DATA6500 -- Fall 2025
# HW3, Q2

# Employee.py
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def increase_salary(self, percent):
        self.salary = self.salary + (self.salary * percent / 100)

    def get_name(self):
        return self.name

    def get_salary(self):
        return self.salary

    def set_name(self, name):
        self.name = name

    def set_salary(self, salary):
        self.salary = salary


emp1 = Employee("John", 5000)
emp1.increase_salary(10)
print("the updated salary is:", emp1.get_salary())   # 5500.0

