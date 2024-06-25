import os

from playwright.sync_api import Page

from exam import Exam
from logger import log


def parse_to_toml(page: Page, base_dir: str) -> None:
    log("Parsing exams...")

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
                log(
                    "Couldn't parse subject or exam name, no subject or exam name",
                    level="ERROR",
                )
                continue

            # Format subject and exam appropriately
            subject = subject.lower().replace(" ", "_").replace(".", "_")
            exam_name = exam_name.lower().replace("/", "|").replace(".", "_")

            # If we already have the exam parsed in the fylesystem, we skip it
            exam_path = os.path.join(base_dir, subject, f"{exam_name}.toml")
            if os.path.exists(exam_path):
                log(f"[{subject} -> {exam_name}] already parsed", level="WARN")
                continue

            # Check if there is grade, if not, continue with the next row
            if exam_props.nth(3).text_content() == "":
                log(
                    f"Couldn't parse [{subject} -> {exam_name}], no grades found",
                    level="ERROR",
                )
                continue

            try:
                # Click on the exam to see the grades
                exam_props.nth(3).click()

                # If the page title is "Error", something went wrong, so we go back
                if page.title() != "UPV - Menú Intranet":
                    log(
                        f"Couldn't parse [{subject} -> {exam_name}], error page present",
                        level="ERROR",
                    )
                    continue

                # Wait for the page to load
                page.wait_for_selector("//table[@class='upv_listacolumnas']//tbody")

            except Exception:
                log(
                    f"Couldn't parse [{subject} -> {exam_name}], page did not load correctly",
                    level="ERROR",
                )
                page.go_back()
                continue

            # If everything went well, we parse the exam and create the file
            exam = parse_exam(page, subject, exam_name)

            if exam is not None:
                exam.create_file(base_dir)

            # Go back to the grades page to keep parsing exams
            page.go_back()


def parse_exam(page: Page, subject: str, exam_name: str) -> Exam | None:

    # Get the table with the grades
    table = page.locator("//table[@class='upv_listacolumnas']//tbody")

    # If the table is empty, something went wrong, so we go back
    if table.count() == 0:
        log(
            f"Couldn't parse [{subject} -> {exam_name}], no grades in the table",
            level="ERROR",
        )
        return

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
