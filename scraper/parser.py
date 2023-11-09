from playwright.async_api import Page

from exam import Exam


async def parse_grades(page: Page) -> list[Exam]:
    # Wait for the page to load
    await page.wait_for_event("load")

    # Get the table with the grades
    grades_table = page.locator("//div[@class='container'][4]")
    grades_table_rows = grades_table.locator("//tr").all()

    exams = []
    subject = ""

    for row in await grades_table_rows:
        row_elements_count = await row.locator("//td").count()

        # If the row has only one element, it is the subject name
        if row_elements_count == 1:
            # Get the subject name
            subject = await row.text_content()

        # If the row has 4 elements, it is an exam with this properties:
        # [Course, Date, Exam name, Grade]
        if row_elements_count == 4:
            exam_props = row.locator("//td")
            exam_name = await exam_props.nth(2).text_content()

            # If we can't get the exam name, something went wrong, so we continue
            # with the next row
            if exam_name is None:
                continue

            # Click on the exam to see the grades
            await exam_props.nth(3).click()

            # Parse the grades of the exam and add it to the list
            exams.append(await parse_exam(page, subject, exam_name))

            # Go back to the grades page to keep parsing exams
            await page.go_back()

    return exams


async def parse_exam(page: Page, subject: str, exam_name: str) -> Exam:
    # Wait for page to load
    await page.wait_for_event("load")

    # Get the table with the grades
    table = page.locator("//table[@class='upv_listacolumnas']//tbody")

    # Get the exam students
    students = []
    for element in await table.locator("//td[1]").all():
        student = await element.text_content()
        if student is not None:
            students.append(student)

    # Get the exam grades
    grades = []
    for element in await table.locator("//td[2]").all():
        grade = await element.text_content()
        if grade is not None:
            grades.append(grade)

    return Exam(subject, exam_name, students, grades)
