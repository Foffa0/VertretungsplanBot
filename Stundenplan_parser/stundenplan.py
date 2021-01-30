import Stundenplan_parser.parse as parse
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

    def get_plan(self, today): # Nimmt den Stundenplan_parser und schreibt ihn in eine Datei
        url = self.adress[not today]
        response = urllib.request.urlopen(url)
        webcontent = response.read()
        if not today:
            name = "Today"
        else:
            name = "Tomorrow"
        f = open(f'tmp/{name}.html', 'w', encoding="UTF-16")
        f.write(webcontent.decode("UTF-16"))
        f.close()

    def parse_plan(self, today): #Schickt den stundenplan in der Datei an den Parser und erhällt ein Parser objekt
        if not today:
            name = "Today"
        else:
            name = "Tomorrow"
        par = parse.Parser(f"tmp/{name}.html")
        par.parse_header()
        par.parse_body()
        self.plan = par

    @staticmethod
    def remove_plan():
        try:
            os.remove("tmp/Today.html")
        except FileNotFoundError:
            pass
        try:
            os.remove("tmp/Tomorrow.html")
        except FileNotFoundError:
            pass
        os.removedirs("./tmp")


def getStundenplan():
    s = Stundenplan()
    return s