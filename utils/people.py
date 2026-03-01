class Person:
    def __init__(self, name: str, birth_year: int, income):
        self.name: str = name
        self.birth_year: int = birth_year
        self.age = 0
        self.retirement_age = 65
        self.current_income = income
        self.future_incomes: list[int] = [self.current_income]

    #not super useful if initializing with incomes
    def set_income(self, income: int):
        if income < 0:
            raise ValueError("Income cannot be negative")
        self.future_incomes[0] = income

    def set_age(self, age: int):
        self.age = age

    def set_retirement_age(self, age: int):
        if age < self.age:
            raise ValueError("Retirement age cannot be less than current age")
        self.retirement_age = age

    def set_incomes(self, incomes: list[int]):
        self.incomes = incomes


