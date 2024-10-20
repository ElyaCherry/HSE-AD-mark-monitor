import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


NATALY_ID = 20083
PROJECT_ID = 222910  # щас это тесла
PROJECT_PAGE_PREFIX = "https://portfolio.hse.ru/Project/"
MARK_TYPES = ["промежуточная", "проекты", "итоговая"]


def notify(mark, mark_type):
    notification_text = "Новая оценка: {}: {}".format(MARK_TYPES[mark_type], mark)
    print(notification_text)


def monitor_marks():

    project_page = PROJECT_PAGE_PREFIX + str(PROJECT_ID)

    driver = webdriver.Firefox()
    driver.get(project_page)

    marks = []
    cur_marks = 0
    while True:
        time.sleep(5)  # seconds
        people = driver.find_elements(By.CLASS_NAME, "person")
        for person in people:
            person_link = person.find_element(By.CLASS_NAME, "person-link").get_attribute('href')
            person_id = int((person_link.split('/'))[-1])
            if person_id == NATALY_ID:
                nataly = person
                break
        else:
            raise AttributeError("Nataly not found on page {}.".format(project_page))

        work_rate_marks = nataly.find_elements(By.CLASS_NAME, "work-rate-mark")
        diff = len(work_rate_marks) - cur_marks
        if diff > 0:
            new_marks = []
            for mark_elem in work_rate_marks:
                new_marks.append(int(mark_elem.text))
            for i in range(len(marks), len(new_marks)):
                notify(new_marks[i], i)
            marks = new_marks
        time.sleep(300)  # seconds
        driver.refresh()


if __name__ == "__main__":
    monitor_marks()
