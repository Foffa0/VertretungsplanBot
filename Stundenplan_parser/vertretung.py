class Vertretung:
    def __init__(self, klasse, std, vertretung, fach, lehrer, raum, sonstiges):
        self.Klasse = klasse.lower()
        self.Stunde = int(std)
        self.Vertretung = vertretung
        self.Fach = fach
        self.Lehrkraft = lehrer
        self.Raum = raum
        self.Sonstiges = sonstiges
