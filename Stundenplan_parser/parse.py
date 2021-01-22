import Stundenplan_parser.vertretung as vertretung


class Parser:
    def __init__(self, link_to_file):
        with open(link_to_file, "r", encoding="UTF-16") as file:
            self.text = file.read().strip("\t")
        self.Title = ""
        self.geaendert_am = ""
        self.Header = """"""
        self.Vertretungen = [] # Besteht aus Vertretungen

    def parse_header(self):
        title = self.text.split("<Title>")[1]
        self.Title = title.split("</Title>")[0]

        ga = self.text.split('Schülerplan - Stand: ')[1]
        self.geaendert_am = ga.split("</th>")[0]

        header = self.text.split("<td>")
        header = header[1].split("</td>")[0]
        self.Header = header.replace("<BR /> ", "\n")


    def parse_body(self):
        table = self.text.split('<table class="table table-striped table-sm" style="font-size: .9rem">')[1]
        table = table.split('</table>')[0]
        table = table.split('<tr class="UngeradeZeileTabelleVertretungen">')
        table.pop(0)
        spalten = []
        for spalte in table:
            for i in spalte.split('<tr class="ZeileGeradeTabelleVertretungen">'):
                spalten.append(i)

        for spalte in spalten:
            args = []
            for i in spalte.split("</td>"):
                x = i.split(">")[1]
                args.append(x)
            self.Vertretungen.append(vertretung.Vertretung(args[0], int(args[1]), str(args[2]), str(args[3]),
                                                           str(args[5]), str(args[6]), str(args[7])))