from models.person import Person

class Student(Person):

	def __init__(self, first_name, last_name, unavailability, rating, instructor):
		super().__init__(first_name, last_name, unavailability)
		self.rating = rating
		self.instructor = instructor
