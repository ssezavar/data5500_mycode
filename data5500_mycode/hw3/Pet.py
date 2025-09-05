# Sara Sezavar Dokhtfaroughi -- A02422030 -- DATA6500 -- Fall 2025
# HW3, Q3

# Pet.py
class Pet:

    species_lifespans = {
        "dog": 13,
        "cat": 15,
        "parrot": 50
    }

    def __init__(self, name, age, species):
        self.name = name
        self.age = age
        self.species = species

    def calc_human_years(self):
        return self.age * 7

    def get_avg_lifespan(self):
        return Pet.species_lifespans.get(self.species, "Unknown")

    def get_name(self):
        return self.name

    def get_age(self):
        return self.age

    def get_species(self):
        return self.species

    def set_name(self, name):
        self.name = name

    def set_age(self, age):
        self.age = age

    def set_species(self, species):
        self.species = species


pet1 = Pet("Buddy", 5, "dog")
pet2 = Pet("Kitty", 3, "cat")
pet3 = Pet("Polly", 2, "parrot")

print(pet1.get_name(), pet1.calc_human_years(), pet1.get_avg_lifespan())
print(pet2.get_name(), pet2.calc_human_years(), pet2.get_avg_lifespan())
print(pet3.get_name(), pet3.calc_human_years(), pet3.get_avg_lifespan())