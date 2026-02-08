import pytest
from utils.people import Person, Plan

@pytest.fixture
def test_people():
    # Create test Person objects
    person1 = Person(name="Alice", birth_year=1980)
    person1.set_retirement_age(65)
    person1.set_income(1)
    
    person2 = Person(name="Bob", birth_year=1990)
    person2.set_retirement_age(70)
    person2.set_income(1)
    
    return [person1, person2]

@pytest.fixture
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