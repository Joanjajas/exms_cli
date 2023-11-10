import subprocess
import os

from logger import log

EXAM_FILES_PATH = "/Users/joan/Downloads/not"


class Exam:
    def __init__(self, subject: str, name: str, students: list[str], grades: list[str]):
        self.name = name.lower()
        self.subject = subject.lower()
        self.students = students
        self.grades = grades

    def create_file(self):
        # Create a folder for the subject if it doesn't exist
        dir_path = f"{EXAM_FILES_PATH}/{self.subject}"
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        # Create a file with the exam data
        file_path = f"{dir_path}/{self.name}"
        with open(file_path, "w") as f:
            f.write(self.__str__())

        # Parse the file in the correct toml format
        subprocess.run(["parser", file_path])
        log(f"Created file {file_path}.toml")

    def __str__(self):
        str = ""
        for name, grade in zip(self.students, self.grades):
            str += f"{name} {grade}\n"

        return str
