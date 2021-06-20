from os import error
from bs4 import BeautifulSoup
import urllib.request
import http.cookiejar
import lxml
from datetime import datetime, date, timedelta
import locale
locale.setlocale(locale.LC_TIME, "de_DE")

class Stunde:
    def __init__(self, heading, content, color):
        self.heading = heading
        self.content = content
        self.color = color


class Scraper:
    def __init__(self):
        self.loggedIn = False
        self.url = 'https://www.hsgym.de/index.php/kissy/start'

    def scrape_plan(self, day, klasse):

        base_url = 'www.hsgym.de'
        https_base_url = 'https://' + base_url
        authentication_url = https_base_url + '/index.php/kissy/login'

        password = 'hans2020sachs'

        headers={"Content-Type":"application/x-www-form-urlencoded",
        "User-agent":"Mozilla/5.0 Chrome/81.0.4044.92",  
        "Host":base_url,
        "Origin":https_base_url,
        "Referer":https_base_url}

        cookie_jar = http.cookiejar.CookieJar()

        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
        urllib.request.install_opener(opener)

        payload = {
            'klasse':klasse,
            'passwort':password
        }

        data = urllib.parse.urlencode(payload)
        binary_data = data.encode('UTF-8')

        request = urllib.request.Request(authentication_url, binary_data, headers)
        response = urllib.request.urlopen(request)
        soup = BeautifulSoup(response, 'lxml')

        if date.today().weekday() == 5:
            today = date.today() + timedelta(days=2)
        elif date.today().weekday() == 6:
            today = date.today() + timedelta(days=1)
        elif day == 0:
            today = date.today()
        else:
            today = date.today() + timedelta(days=1)
        requestedDay = today.strftime("%d.%m.%Y")
        print(requestedDay)

        weekday = today.strftime("%A")

        self.title = "Vertretungsplan " + "für " + weekday+ " " + requestedDay

        if soup.find("a", text="Abmelden"):

            rows = soup.find_all("li",{"data-role": "list-divider"})
                
            # rows = soup.find_all("li")
            courseList = []

            for x in rows:
                if requestedDay in x.text:
                    for i in x.find_next_siblings("li"):
                        try:
                            if i["data-role"]:
                                break
                        except:
                            print(i)
                            try:
                                color = i["style"]
                                if color == "color:black":
                                    color = "black"
                                elif color == "color:red":
                                    color = "red"
                            except:
                                color = "black"
                            # try:
                            if color == "red":
                                pTags = i.find_all("p")
                                heading = pTags[1].text
                                content = i.text.replace(pTags[1].text, "")
                                content = content.replace(pTags[0].text, "")
                                if pTags[0].text != "":
                                    content = content + f"({pTags[0].text})"
                            
                            else:
                                try:
                                    if "ui-li-aside" in i.p["class"]:
                                        heading = i.p.text
                                        content = i.text.replace(i.p.text, "")    
                                except:
                                    heading = "Allgemein"
                                    content = str(i.p).replace("<br/>", "\n")
                                    content = content.replace("<p>", "")
                                    content = content.replace("</p>", "")

                            courseList.append(Stunde(heading, content, color))
            #logout
            urllib.request.urlopen("https://www.hsgym.de/index.php/kissy/logout")
            return courseList
        else:
            #get Oberstufenplan
            klasse.lower()
            courseList = []
            if day == 0:
                response = urllib.request.urlopen("https://www.hans-sachs-gymnasium.de/WocheHP/schuelerplan_heute.htm")
            else:
                response = urllib.request.urlopen("https://www.hans-sachs-gymnasium.de/WocheHP/schuelerplan_morgen.htm")
            soup = BeautifulSoup(response, 'lxml')
            announcements =  str(soup.select(".table-danger")[0].td)
            announcements = announcements.replace("Mitteilungen", "")
            announcements = announcements.replace("<td>", "")
            announcements = announcements.replace("</td>", "")
            announcements = announcements.replace("<br/>", "\n")
            courseList.append(Stunde("Allgemein", announcements, "black"))

            table = soup.select(".table-striped")[0]
            table.thead.replace_with('')
            for tableRow in table.find_all("tr"):
                if klasse in tableRow.td.text:
                    next_siblings = tableRow.td.find_next_siblings("td")
                    heading = next_siblings[0].text + ". Stunde"
                    content = next_siblings[1].text + " statt " + next_siblings[4].text + " in " + next_siblings[5].text + f"  {next_siblings[6].text}"
                    courseList.append(Stunde(heading, content, "red"))
            return courseList

