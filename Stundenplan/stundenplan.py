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
        self.courses = courses
        geandert = datetime.today()
        geandert = geandert.strftime("%d.%m.%Y, %H:%M")
        self.geandert = geandert
        self.title = s.title
        vertretungen = []
        for x in self.courses:
            print(x.color)
            if x.color == "red" or x.heading == "Allgemein":
                vertretungen.append(x)
        self.vertretungen = vertretungen