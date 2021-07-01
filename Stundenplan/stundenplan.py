# from bs4.element import PYTHON_SPECIFIC_ENCODINGS
import Stundenplan.scraper as scraper
from datetime import datetime
class Stundenplan():
    def __init__(self):
        self.courses = []
    
    def getPlan(self, klasse, day):
        self.klasse = klasse
        self.day = day
        s = scraper.Scraper()
        courses = s.scrape_plan(self.day, self.klasse)

        removeCourses=[]
        for count, stunde in enumerate(courses):
            if count == 0 or stunde.color == "red":
                continue

            if courses[count-1].heading == stunde.heading:
                for line in courses[count].content.split("\n"):
                    lines = courses[count].content.split("\n")
                    if len(lines) == 1:
                        removeCourses.append(courses[count])
                    else:
                        # get the last course that is not red
                        if courses[count-1].color == "red":
                            if not courses[count-2].color == "red":
                                offset = 1
                            else:
                                offset = 2

                        text = courses[count-offset].content.split("statt",1)[1]
                        if text[:4].strip() in line:
                            courses[count].content = courses[count].content.replace(line, "")
                            

        for removeCourse in removeCourses:
            courses.remove(removeCourse)
        self.courses = courses
        geandert = datetime.today()
        geandert = geandert.strftime("%d.%m.%Y, %H:%M")
        self.geandert = geandert
        self.title = s.title
        vertretungen = []
        for x in self.courses:
            if x.color == "red" or x.color == "blue" or x.heading == "Allgemein":
                vertretungen.append(x)
        self.vertretungen = vertretungen