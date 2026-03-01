from utils.people import Person

class Plan:
    def __init__(
            self, 
            people: list[Person], 
            current_year: int, 
            inc_growth_factor: float, 
            return_factor: float,
            spend: int,
            age_at_death: int
    ):
        self.people = people
        self.current_year = current_year
        self.inc_growth_factor = inc_growth_factor
        self.return_factor = return_factor
        self.spend = spend
        self.age_at_death = age_at_death
        
        # initializing year-dependent personal attributes
        for person in people:
            person.set_age(self.current_year - person.birth_year)

    def __plan_retirement_years(self):
        retirement_years = 0
        for person in self.people:
            retirement_years = max(retirement_years, self.age_at_death - person.retirement_age)
        self.retirement_years = retirement_years
        
    def __total_savings(self):
        if self.retirement_years < 1:
            return 0
        total = self.spend
        year = 1
        while year < self.retirement_years:
            total /= 1.05
            total += self.spend
            year += 1
        return round(total,2)
            
    def calculate_incomes(self):
        self.incomes = {}
        for person in self.people:
            income_by_year = []
            # for each working year
            for i in range(person.retirement_age - person.age):
                income = person.current_income * (self.inc_growth_factor**i)
                income_by_year.append([self.current_year + i, round(income, 2)])
            self.incomes[person.name] = income_by_year
        return self.incomes

    def savings_per_year(self):
        
        pass

    def calculate(self, **kwargs):
        retirement_years = self.__retirement_years()
        savings_needed = self.__total_savings()
        print(f" You must save {savings_needed:_} at retirement, withdrawing {self.spend} per year over {retirement_years} years.")
        return savings_needed


def COL_conversion(amt: float, city:str):
    col_factor = {

    # Base city
    "Ottawa": 1.00,  # reference city

    # Canadian cities (Numbeo comparisons)
    "Toronto": 1.12,  # ~10–12% more expensive than Ottawa overall :contentReference[oaicite:2]{index=2}
    "Vancouver": 1.08,  # slightly above Ottawa (Numbeo range) :contentReference[oaicite:3]{index=3}
    "Montreal": 0.95,  # generally a bit cheaper than Ottawa :contentReference[oaicite:4]{index=4}

    # U.S. cities (Numbeo comparisons)
    "New York": 1.59,  # ~59–100% higher, depending on metric :contentReference[oaicite:5]{index=5}
    "Chicago": 1.15,  # US average mid-tier city on COL scale :contentReference[oaicite:6]{index=6}
    "San Francisco": 1.62,  # high-cost U.S. city :contentReference[oaicite:7]{index=7}

    # Chinese city (proxy)
    "Kunming": 0.34,  # ~66% cheaper than Ottawa (proxy estimate) :contentReference[oaicite:8]{index=8}

    # Other global examples (approximate scaled by popular data rankings)
    "London": 1.40,  # higher than Ottawa (global cost rankings) :contentReference[oaicite:9]{index=9}
    "Tokyo": 1.35,  # higher-cost Asian hub :contentReference[oaicite:10]{index=10}
    "Singapore": 1.50,  # high cost for Asia :contentReference[oaicite:11]{index=11}
}   
    if city not in col_factor:
        raise ValueError("City not found")
    
    return round(amt * col_factor[city])