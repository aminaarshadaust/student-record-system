import json

def main_menu():
    print("""
    *****************************************
    *                                       *
    *   WELCOME TO STUDENT RECORD SYSTEM   *
    *                                       *
    *****************************************
    """)
    print("1. Add Student")
    print("2. Display Students")
    print("3. Search Student by Name")
    print("4. Mark Attendance")
    print("5. Enroll Course")
    print("6. Assign Grade")
    print("7. Calculate GPA")
    print("8. Update Student")
    print("9. Delete Student")
    print("10. Exit")
    
class StudentRecordSystem:
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.filename = "student_records.json"
        self.available_courses = ["Mathematics", "Physics", "Chemistry", "Computer Science", "English", "History"]
        self.load_data()

    def hash_function(self, key):
        return hash(key) % self.size

    def add_student(self):
        try:
            student_id = input("Enter Student ID: ")
            name = input("Enter Student Name: ")
            age = int(input("Enter Student Age: "))
            email = input("Enter Email (optional): ") or None
            phone = input("Enter Phone Number (optional): ") or None
            index = self.hash_function(student_id)
            for student in self.table[index]:
                if student["id"] == student_id:
                    print("Student ID already exists!")
                    return
            self.table[index].append({
                "id": student_id, "name": name, "age": age, "email": email, "phone": phone, 
                "courses": [], "attendance": {}, "gpa": 0.0, "report_card": {}
            })
            self.save_data()
            print("Student added successfully.")
        except ValueError:
            print("Invalid input for age. Please enter a number.")
    
    def assign_grade(self):
        student_id = input("Enter Student ID: ")
        course = input("Enter Course Name: ")
        grade = float(input("Enter Grade: "))
        student = self.get_student(student_id)
        if student:
            student["report_card"][course] = grade
            self.save_data()
            print("Grade assigned successfully.")
        else:
            print("Student not found!")
    
    def display_students(self):
        students_found = False
        for bucket in self.table:
            for student in bucket:
                print(f"ID: {student['id']}, Name: {student['name']}, Age: {student['age']}, Email: {student.get('email', 'N/A')}, Phone: {student.get('phone', 'N/A')}, GPA: {student.get('gpa', 0.0)}")
                students_found = True
        if not students_found:
            print("No students found.")
    
    def search_student_by_name(self):
        name = input("Enter Student Name: ")
        found = False
        for bucket in self.table:
            for student in bucket:
                if student["name"].lower() == name.lower():
                    print(f"ID: {student['id']}, Name: {student['name']}, Age: {student['age']}, Email: {student.get('email', 'N/A')}, Phone: {student.get('phone', 'N/A')}, GPA: {student.get('gpa', 0.0)}")
                    found = True
        if not found:
            print("Student not found.")
    
    def mark_attendance(self):
        student_id = input("Enter Student ID: ")
        date = input("Enter Date (YYYY-MM-DD): ")
        status = input("Enter Attendance Status (Present/Absent): ")
        student = self.get_student(student_id)
        if student:
            student["attendance"][date] = status
            self.save_data()
            print("Attendance marked successfully.")
        else:
            print("Student not found!")
    
    def enroll_course(self):
        student_id = input("Enter Student ID: ")
        student = self.get_student(student_id)
        if student:
            print("Available Courses:")
            for i, course in enumerate(self.available_courses, 1):
                print(f"{i}. {course}")
            try:
                choice = int(input("Choose a course to enroll (Enter number): "))
                if 1 <= choice <= len(self.available_courses):
                    course = self.available_courses[choice - 1]
                    if course not in student["courses"]:
                        confirm = input(f"Do you want to enroll in {course}? (yes/no): ").strip().lower()
                        if confirm == "yes":
                            student["courses"].append(course)
                            self.save_data()
                            print(f"Successfully enrolled in {course}.")
                        else:
                            print("Enrollment canceled.")
                    else:
                        print("Student is already enrolled in this course.")
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Please enter a valid number.")
        else:
            print("Student not found!")
    
    def calculate_gpa(self):
        student_id = input("Enter Student ID: ")
        student = self.get_student(student_id)
        if student:
            grades = student.get("report_card", {}).values()
            if grades:
                student["gpa"] = sum(grades) / len(grades)
                self.save_data()
                print(f"GPA calculated successfully: {student['gpa']:.2f}")
            else:
                print("No grades available to calculate GPA.")
        else:
            print("Student not found!")
    
    def update_student(self):
        print("Update functionality coming soon!")
    
    def delete_student(self):
        print("Delete functionality coming soon!")
    
    def get_student(self, student_id):
        index = self.hash_function(student_id)
        for student in self.table[index]:
            if student["id"] == student_id:
                return student
        return None

    def save_data(self):
        with open(self.filename, "w") as file:
            json.dump(self.table, file, indent=4)
    
    def load_data(self):
        try:
            with open(self.filename, "r") as file:
                self.table = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.table = [[] for _ in range(self.size)]

if __name__ == "__main__":
    system = StudentRecordSystem()
    while True:
        main_menu()
        choice = input("Enter your choice: ")
        if choice == "1":
            system.add_student()
        elif choice == "2":
            system.display_students()
        elif choice == "3":
            system.search_student_by_name()
        elif choice == "4":
            system.mark_attendance()
        elif choice == "5":
            system.enroll_course()
        elif choice == "6":
            system.assign_grade()
        elif choice == "7":
            system.calculate_gpa()
        elif choice == "8":
            system.update_student()
        elif choice == "9":
            system.delete_student()
        elif choice == "10":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")
