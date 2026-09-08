#Mario Angeles
#CIS261
#WK10 VIBE Coding


class Student:
	"""Store the information and calculated results for one student."""

	def __init__(self, name, student_id, test_scores=None, average=0.0, grade=""):
		self.name = name
		self.id = student_id
		self.test_scores = test_scores if test_scores is not None else []
		self.average = average
		self.grade = grade


def calculate_average(test_scores):
	"""Return the average of a student's test scores."""
	return sum(test_scores) / len(test_scores)


def calculate_grade(average):
	"""Return a letter grade based on an average score."""
	if average >= 90:
		return "A"
	if average >= 80:
		return "B"
	if average >= 70:
		return "C"
	if average >= 60:
		return "D"
	return "F"


def get_score(score_number):
	"""Prompt for one valid score between 0 and 100."""
	while True:
		try:
			score = float(input(f"Enter test score {score_number}: "))
			if 0 <= score <= 100:
				return score
			print("Score must be between 0 and 100.")
		except ValueError:
			print("Please enter a number.")


def get_nonempty_input(prompt):
	"""Return a non-empty response from the user."""
	while True:
		value = input(prompt).strip()
		if value:
			return value
		print("This field cannot be blank.")


def add_student():
	"""Collect exactly three test scores and return a Student object."""
	print("\nAdd New Student")
	name = get_nonempty_input("\nEnter student name: ")
	student_id = get_nonempty_input("Enter student ID: ")
	test_scores = [get_score(score_number) for score_number in range(1, 4)]
	average = calculate_average(test_scores)
	return Student(name, student_id, test_scores, average, calculate_grade(average))


def format_student_row(student):
	"""Return one student as a formatted table row."""
	return (
		f"{student.name:<20} {student.id:<12} "
		f"{student.test_scores[0]:>7.2f} {student.test_scores[1]:>7.2f} "
		f"{student.test_scores[2]:>7.2f} {student.average:>8.2f} {student.grade:>5}"
	)


def display_students(students):
	"""Display all students in a formatted table."""
	if not students:
		print("No student records are available.")
		return

	header = (
		f"{'Name':<20} {'ID':<12} {'Test 1':>7} {'Test 2':>7} "
		f"{'Test 3':>7} {'Average':>8} {'Grade':>5}"
	)
	print("\nALL STUDENT RECORDS")
	print()
	print(header)
	print("-" * len(header))
	for student in students:
		print(format_student_row(student))
	print()
	print(f"Total Students: {len(students)}")


def search_students(students):
	"""Display students whose names match a case-insensitive search."""
	if not students:
		print("No student records are available.")
		return

	search_name = get_nonempty_input("\nEnter the name to search for: ").casefold()
	matches = [student for student in students if search_name in student.name.casefold()]
	if not matches:
		print(f'\nNo students found matching "{search_name}".')
		return

	print(f'\nStudents matching "{search_name}":\n')
	header = (
		f"{'Name':<20} {'ID':<12} {'Test 1':>7} {'Test 2':>7} "
		f"{'Test 3':>7} {'Average':>8} {'Grade':>5}"
	)
	print(header)
	print("-" * len(header))
	for student in matches:
		print(format_student_row(student))


def display_statistics(students):
	"""Display class averages and the grade distribution."""
	if not students:
		print("No student records are available for statistics.")
		return

	highest = max(students, key=lambda student: student.average)
	lowest = min(students, key=lambda student: student.average)
	class_average = calculate_average([student.average for student in students])
	grade_counts = {grade: 0 for grade in "ABCDF"}
	for student in students:
		grade = student.grade.upper()
		if grade in grade_counts:
			grade_counts[grade] += 1

	print("\n" + "=" * 50)
	print("CLASS STATISTICS")
	print("=" * 50)
	print(f"Class Average: {class_average:.2f}")
	print(f"Highest Average: {highest.average:.2f} ({highest.name})")
	print(f"Lowest Average: {lowest.average:.2f} ({lowest.name})")
	print("\nGrade Distribution")
	for grade, count in grade_counts.items():
		if count > 0:
			student_label = "student" if count == 1 else "students"
			print(f"{grade}: {count} {student_label}")


def load_students(filename="student_grades.txt"):
	"""Load pipe-delimited student records, skipping invalid records."""
	students = []
	try:
		with open(filename, "r", encoding="utf-8") as records_file:
			for line_number, line in enumerate(records_file, start=1):
				fields = line.strip().split("|")
				if len(fields) != 7:
					print(f"Skipping invalid record on line {line_number}.")
					continue
				try:
					name, student_id = fields[:2]
					test_scores = [float(score) for score in fields[2:5]]
					average = float(fields[5])
					grade = fields[6]
					if not name or not student_id or any(score < 0 or score > 100 for score in test_scores):
						raise ValueError
					students.append(Student(name, student_id, test_scores, average, grade))
				except ValueError:
					print(f"Skipping invalid record on line {line_number}.")
	except FileNotFoundError:
		print(f"No existing {filename} found. Starting with an empty class.")
	except OSError as error:
		print(f"Unable to load student records: {error}")
	return students


def save_students(students, filename="student_grades.txt"):
	"""Save students in the required pipe-delimited format."""
	try:
		with open(filename, "w", encoding="utf-8") as records_file:
			for student in students:
				record = [
					student.name,
					student.id,
					*(f"{score:.2f}" for score in student.test_scores),
					f"{student.average:.2f}",
					student.grade,
				]
				records_file.write("|".join(record) + "\n")
	except OSError as error:
		print(f"Unable to save student records: {error}")
		return False
	print(f"\nSaved {len(students)} student record(s) to {filename}.")
	return True


def display_menu():
    """Display the main menu and return the user's choice."""
    separator = "=" * 50
    print(f"\n{separator}")
    print("STUDENT GRADE CALCULATOR")
    print(separator)
    print("1. Add New Student")
    print("2. Display All Students")
    print("3. Search Student by Name")
    print("4. View Class Statistics")
    print("5. Save and Exit (or type ESC)")
    print(separator)
    return input("Select an option (1-5) or type ESC to exit: ").strip()

def main():
	separator = "=" * 50
	print(separator)
	print("WELCOME TO STUDENT GRADE CALCULATOR")
	print(separator)
	students = load_students()
	while True:
		choice = display_menu()
		if choice == "1":
			students.append(add_student())
			print("\nStudent added successfully.")
		elif choice == "2":
			display_students(students)
		elif choice == "3":
			search_students(students)
		elif choice == "4":
			display_statistics(students)
		elif choice == "5" or choice.casefold() == "esc" or choice == "\x1b":
			save_students(students)
			print("\nThank you for using Student Grade Calculator!")
			break
		else:
			print("Invalid option. Please choose 1-5 or type ESC to save and exit.")


if __name__ == "__main__":
	main()