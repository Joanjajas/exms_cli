from playwright.sync_api import Page

from exam import Exam
from logger import log


def parse_exams(page: Page) -> None:
    log("Parsing exams...")

    # Wait for the page to load
    page.wait_for_event("load")

    # Get the table with the grades
    grades_table = page.locator("//div[@class='container'][4]")
    grades_table_rows = grades_table.locator("//tr").all()

    subject = ""

    for row in grades_table_rows:
        row_elements_count = row.locator("//td").count()

        # If the row has only one element, it is the subject name
        if row_elements_count == 1:
            # Get the subject name
            subject = row.text_content()

        # If the row has 4 elements, it is an exam with this properties:
        # [Course, Date, Exam name, Grade]
        elif row_elements_count == 4:
            exam_props = row.locator("//td")
            exam_name = exam_props.nth(2).text_content()

            # If we can't get the subject or the exam name, something went wrong,
            # so we continue with the next row
            if subject is None or exam_name is None:
                continue

            # Check if there is grade, if not, continue with the next row
            if exam_props.nth(3).text_content() == "":
                continue

            # Click on the exam to see the grades
            exam_props.nth(3).click()

            # If the page title is "Error", something went wrong, so we continue
            # with the next row
            if page.title() == "Error":
                log(f"Couldn't parse {subject}: {exam_name}")
                page.go_back()
                continue

            # If everything went well, we parse the exam and create the file
            exam = parse_exam(page, subject, exam_name)
            exam.create_file()

            # Go back to the grades page to keep parsing exams
            page.go_back()


def parse_exam(page: Page, subject: str, exam_name: str) -> Exam:
    # Wait for page to load
    page.wait_for_event("load")

    # Get the table with the grades
    table = page.locator("//table[@class='upv_listacolumnas']//tbody")

    # Get the exam students
    students = []
    for element in table.locator("//td[1]").all():
        student = element.text_content()
        if student is not None:
            students.append(student)

    # Get the exam grades
    grades = []
    for element in table.locator("//td[2]").all():
        grade = element.text_content()
        if grade is not None:
            grades.append(grade)

    return Exam(subject, exam_name, students, grades)
