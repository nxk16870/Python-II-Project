class GradeManager:
    def __init__(self, grades=None):
        if grades is None:
            self.__grades = []
        else:
            self.__grades = grades

    def addCourseGrades(self, course_name, scores):
        row = [course_name]

        for score in scores:
            row.append(float(score))

        self.__grades.append(row)

    def getGrades(self):
        return self.__grades

    def setGrades(self, grades):
        self.__grades = grades

    def calculateCourseAverage(self, course_name):
        for row in self.__grades:
            if row[0].lower() == course_name.lower():
                total = 0
                count = 0

                for score in row[1:]:
                    total += score
                    count += 1

                if count == 0:
                    return 0

                return total / count

        return None

    def calculateOverallAverage(self):
        total = 0
        count = 0

        for row in self.__grades:
            for score in row[1:]:
                total += score
                count += 1

        if count == 0:
            return 0

        return total / count

    def getLetterGrade(self, average):
        if average >= 90:
            return "A"
        elif average >= 80:
            return "B"
        elif average >= 70:
            return "C"
        elif average >= 60:
            return "D"
        else:
            return "F"

    def __str__(self):
        return str(self.__grades)