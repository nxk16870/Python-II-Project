class StudentRecord:
    def __init__(self, student_id, first_name, last_name, age, gender, phone, email, grades=None):
        self.__student_id = str(student_id)
        self.__first_name = first_name
        self.__last_name = last_name
        self.__age = int(age)
        self.__gender = gender
        self.__phone = phone
        self.__email = email

        if grades is None:
            self.__grades = []
        else:
            self.__grades = grades

    def getStudentId(self):
        return self.__student_id

    def setStudentId(self, student_id):
        self.__student_id = str(student_id)

    def getFirstName(self):
        return self.__first_name

    def setFirstName(self, first_name):
        self.__first_name = first_name

    def getLastName(self):
        return self.__last_name

    def setLastName(self, last_name):
        self.__last_name = last_name

    def getAge(self):
        return self.__age

    def setAge(self, age):
        self.__age = int(age)

    def getGender(self):
        return self.__gender

    def setGender(self, gender):
        self.__gender = gender

    def getPhone(self):
        return self.__phone

    def setPhone(self, phone):
        self.__phone = phone

    def getEmail(self):
        return self.__email

    def setEmail(self, email):
        self.__email = email

    def getGrades(self):
        return self.__grades

    def setGrades(self, grades):
        self.__grades = grades

    def toDictionary(self):
        return {
            "student_id": self.__student_id,
            "first_name": self.__first_name,
            "last_name": self.__last_name,
            "age": self.__age,
            "gender": self.__gender,
            "phone": self.__phone,
            "email": self.__email,
            "grades": self.__grades
        }

    @staticmethod
    def fromDictionary(data):
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

    def __str__(self):
        return (f"Student ID: {self.__student_id}, "
                f"Name: {self.__first_name} {self.__last_name}, "
                f"Age: {self.__age}, Gender: {self.__gender}, "
                f"Phone: {self.__phone}, Email: {self.__email}")