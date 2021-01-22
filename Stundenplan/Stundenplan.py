import parse
import os
import urllib.request, urllib.error, urllib.parse


class Stundenplan:
    def __init__(self):
        self.adress = ["http://www.hans-sachs-gymnasium.de/WocheHP/schuelerplan_heute.htm", "http://www.hans-sachs-gymnasium.de/WocheHP/schuelerplan_morgen.htm"]
        self.plan = None
        try:
            os.mkdir("tmp")
        except FileExistsError:
            pass

    def get_plan(self, today): # Nimmt den Stundenplan und schreibt ihn in eine Datei
        url = self.adress[not today]
        response = urllib.request.urlopen(url)
        webcontent = response.read()
        f = open('tmp/tmp.html', 'w', encoding="UTF-16")
        f.write(webcontent.decode("UTF-16"))
        f.close()

    def parse_plan(self): #Schickt den stundenplan in der Datei an den Parser und erhällt ein Parser objekt
        par = parse.Parser("tmp/tmp.html")
        par.parse_header()
        par.parse_body()
        self.plan = par

    @staticmethod
    def remove_plan():
        os.remove("tmp/tmp.html")
        os.removedirs("./tmp")


if __name__ =="__main__":
    s = Stundenplan()
    s.get_plan(True)
    s.parse_plan()
    s.remove_plan()
    print(s.plan.Title)
    for i in s.plan.Vertretungen:
        if i.Klasse == '5C':

            print(i.Klasse, i.Stunde, i.Fach, i.Raum, i.Sonstiges)
