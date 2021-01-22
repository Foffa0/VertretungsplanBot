import Stundenplan_parser  #Importiert das Modul

s = Stundenplan_parser.stundenplan.Stundenplan() # Erstellt eine Stundenplan_Instanz
s.get_plan(True) #Downloaded den Plan für morgen
s.parse_plan()  #Parst den header und die Metadaten des Plans
s.remove_plan() # löscht die lokale Plan-Datei
print(s.plan.Title)  # Gibt den Titel des Plans aus