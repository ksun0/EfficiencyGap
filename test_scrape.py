import requests
import json
import bs4
import re
from bs4 import BeautifulSoup

def collect_cases(number):
    url = r'https://www.courtlistener.com/api/rest/v3/opinions'
    head={'Authorization': 'Token dffce215ac12d401f8915695a2dfee2fc399c8f6'}
    response = requests.get(url, headers = head)
    opinions_json = response.json()
    text_documents = []
    #print(opinions_json) Uncomment to check if throttled
    last_link = ""
    for x in range(number):
        print(x)
        for x in range(len(opinions_json["results"])):
            if opinions_json["results"][x]["html_lawbox"]:
                print(opinions_json["results"][x]["id"])
                html = opinions_json["results"][x]["html_lawbox"]
                text_documents.append([html,opinions_json["results"][x]["id"]])
            elif opinions_json["results"][x]["plain_text"]:
                print(opinions_json["results"][x]["id"])
                html = opinions_json["results"][x]["plain_text"]
                text_documents.append([html,opinions_json["results"][x]["id"]])
            elif opinions_json["results"][x]["html"]:
                print(opinions_json["results"][x]["id"])
                html = opinions_json["results"][x]["html"]
                text_documents.append([html,opinions_json["results"][x]["id"]])
            else:
                print("Insufficient Data(I hate this API).")
        last_link = opinions_json["next"]
        response = requests.get(opinions_json["next"],headers = head)
        opinions_json = response.json()
    d = open("last_link.txt","a")
    d.write(last_link)
    d.close()
    for x in text_documents:
        f = open("raw_cases.txt","a")
        try:
            f.write(str(x[1]))
            f.write("\n")
            print(x[1])
            print("Written")
            f.close()
        except UnicodeEncodeError:
            print("Can't write!")
        f.close()
    return text_documents

states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota",
"Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia",
"Wisconsin","Wyoming"]

def parse_court_case(entry):
    data = [] #id,civil rights case, year, state
    data.append(entry[1])
    #Check civil rights
    civil_rights = False
    keywords = ["civil rights","civil rights violation","discrimination"]
    for word in keywords:
        if word in entry[0]:
            if len(data) < 2:
                data.append(True)
    if len(data) < 2:
        data.append(False)
    #Check year
    found = re.search("([(]\d{4}[)])|((Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\s+\d{1,2},\s+\d{4})",entry[0])
    if found:
        if len(found.group(0)) == 6:
            data.append(found.group(0)[1:len(found.group(0))-1])
        else:
            data.append(found.group(0)[len(found.group(0))-4:])
    else:
        #Work on this
        data.append("Date Unknown")
    #Check court
    for x in states:
        if x in entry[0]:
            data.append(x)
            break
    if len(data) < 4:
        data.append("Invalid entry")
    #Write data
    return data


raw_cases = collect_cases(10)
clean_cases = []
for x in raw_cases:
    clean_case = parse_court_case(x)
    clean_cases.append(clean_case)
    f = open("clean_cases.txt","a")

    f.write(str(clean_case))
    f.write("\n")
    f.close()
###Regex Expressions
#Dates
#(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\s+\d{1,2},\s+\d{4}
#[(]\d{4}[)]
#States
#([A-Z][.]){2}[ ]|([A-Z]{2}[ ])
