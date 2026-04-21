class StudentRecord:
    def __init__(self, student_id, first_name, last_name, age, gender, phone, email, grades=None):
        self.student_id = str(student_id)
        self.first_name = str(first_name).strip()
        self.last_name = str(last_name).strip()
        self.age = int(age)
        self.gender = str(gender).strip().upper()
        self.phone = str(phone).strip()
        self.email = str(email).strip().lower()
        self.grades = [] if grades is None else [list(row) for row in grades]

    def getStudentId(self):
        return self.student_id

    def setStudentId(self, student_id):
        self.student_id = str(student_id)

    def getFirstName(self):
        return self.first_name

    def setFirstName(self, first_name):
        self.first_name = str(first_name).strip()

    def getLastName(self):
        return self.last_name

    def setLastName(self, last_name):
        self.last_name = str(last_name).strip()

    def getAge(self):
        return self.age

    def setAge(self, age):
        self.age = int(age)

    def getGender(self):
        return self.gender

    def setGender(self, gender):
        self.gender = str(gender).strip().upper()

    def getPhone(self):
        return self.phone

    def setPhone(self, phone):
        self.phone = str(phone).strip()

    def getEmail(self):
        return self.email

    def setEmail(self, email):
        self.email = str(email).strip().lower()

    def getGrades(self):
        return [list(row) for row in self.grades]

    def setGrades(self, grades):
        self.grades = [] if grades is None else [list(row) for row in grades]

    def getFullName(self):
        return f"{self.first_name} {self.last_name}"

    def to_dictionary(self):
        return {
            "student_id": self.student_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "gender": self.gender,
            "phone": self.phone,
            "email": self.email,
            "grades": [list(row) for row in self.grades]
        }

    def toDictionary(self):
        return self.to_dictionary()

    def from_dictionary(data):
        return StudentRecord(
            data["student_id"],
            data["first_name"],
            data["last_name"],
            data["age"],
            data["gender"],
            data["phone"],
            data["email"],
            data.get("grades", [])
        )

    def fromDictionary(data):
        return StudentRecord.from_dictionary(data)

    def __str__(self):
        return (
            f"Student ID: {self.student_id}, "
            f"Name: {self.first_name} {self.last_name}, "
            f"Age: {self.age}, Gender: {self.gender}, "
            f"Phone: {self.phone}, Email: {self.email}"
        )
