import pytest
from utils.people import Person
from utils.plan import Plan

@pytest.fixture
def test_people():
    # Create test Person objects

    person1 = Person(name="Alice", birth_year=1980, income = 1)
    person1.set_retirement_age(65)
    person1.set_income(1)
    
    person2 = Person(name="Bob", birth_year=1990, income = 1)
    person2.set_retirement_age(70)
    person2.set_income(1)
    
    return [person1, person2]

@pytest.fixture(scope = 'function')
def test_plan(test_people): 
    # Create a Plan object
    plan = Plan(
        people=test_people,
        current_year=2023,
        inc_growth_factor=2.00,
        return_factor=1.05,
        spend=50000,
        age_at_death=90
    )
    return plan

def test_retirement_years(test_plan):
    person1, person2 = test_plan.people
    # Access the private method using name mangling - dunders are private
    retirement_years = test_plan._Plan__retirement_years()
    assert retirement_years == max(test_plan.age_at_death - person1.retirement_age, test_plan.age_at_death - person2.retirement_age)

def test_retirement_years2(test_plan):
   # Access the private method using name mangling - dunders are private
    retirement_years = test_plan._Plan__retirement_years()
    assert retirement_years == 25

def test_calculate_incomes(test_plan):
    expected_incomes = {}
    for person in test_plan.people:
        incomes = []
        for i in range(person.retirement_age - person.age):
            incomes.append([test_plan.current_year + i, 1 * (2**i)])
        expected_incomes[person.name] = incomes
    assert expected_incomes == test_plan.calculate_incomes()

def test_calculate_incomes_rand(test_plan):
    names = [
        "Amina", "Bao", "Chidi", "Diego", "Elif",
        "Farah", "Gautam", "Hana", "Ibrahim", "Jasmin"
    ]

    birth_years = [1960, 1975, 1988, 1990, 1955, 1980, 1970, 1995, 1965, 2000]
    retirement_years = [2025, 2035, 2045, 2040, 2020, 2040, 2035, 2060, 2030, 2065]
    incomes = [50_000, 60_000, 45_000, 80_000, 30_000, 70_000, 65_000, 40_000, 90_000, 55_000]

    expected = {}

    for name, by, ry, income in zip(names, birth_years, retirement_years, incomes, strict = False):
        p = Person(name, by, income)
        p.set_retirement_age(ry - by)
        test_plan.people.append(p)

        years = ry - test_plan.current_year
        expected[name] = round(
            income * test_plan.inc_growth_factor ** years,
            2
        )
    actual = {}
    output = test_plan.calculate_incomes()
    for name, list in output.items():
        actual[name] = list[-1][1]
    
    assert actual == expected