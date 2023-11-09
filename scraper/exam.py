import os

EXAM_FILES_PATH = "/Users/joan/Downloads/not"


class Exam:
    def __init__(self, subject: str, name: str, students: list[str], grades: list[str]):
        self.name = name
        self.subject = subject
        self.students = students
        self.grades = grades

    def create_file(self):
        # Create a folder for the subject if it doesn't exist
        dir_path = f"{EXAM_FILES_PATH}/{self.subject}"
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        # Create a file with the exam data
        file_path = f"{EXAM_FILES_PATH}/{self.subject}/{self.name}"
        with open(file_path, "w") as f:
            f.write(self.__str__())

    def __str__(self):
        str = ""
        for name, grade in zip(self.students, self.grades):
            str += f"{name} {grade}\n"

        return str
