import requests
import json
import bs4
from bs4 import BeautifulSoup

def collect_cases():
    url = r'https://www.courtlistener.com/api/rest/v3/opinions'
    header = 'Token dffce215ac12d401f8915695a2dfee2fc399c8f6'
    response = requests.get(url, header)
    opinions_json = response.json()
    text_documents = []
    #print(opinions_json) -Uncomment if you need to check api cooldown time
    for x in range(1):
    # while opinions_json["next"] is not None:
        for x in range(len(opinions_json["results"])):
            if opinions_json["results"][x]["html_lawbox"]:
                print(opinions_json["results"][x]["id"])
                html = opinions_json["results"][x]["html_lawbox"]
                text_documents.append([html,opinions_json["results"][x]["id"]])
            elif opinions_json["results"][x]["plain_text"]:
                print(opinions_json["results"][x]["id"])
                html = opinions_json["results"][x]["plain_text"]
                text_documents.append([html,opinions_json["results"][x]["id"]])
        response = requests.get(opinions_json["next"])
        opinions_json = response.json()
    # print(opinions_json)
    # for case in opinions_json:
    #     print(case)
    # with open("dat.txt", w) as outfile:
    #     json.dump(data, outfile)

    print(text_documents)
    f = open("raw_cases.txt","w+")
    for x in text_documents:
        f.write(str(x))
    return text_documents
def parse_court_case(entry):
    data = [] #id,civil rights case, year, court
    data.append(entry[1])
    #Check civil rights
    civil_rights = False
    keywords = ["civil rights","civil rights violation","discrimination"]
    for word in keywords:
        if word in entry[0]:
            if len(data) < 2:
                data.append(True)
    #Check year
    start = entry[0].index("(")
    end = entry[0].index(")")
    data.append(entry[0][start+1:end])
    #Check court
    if entry[0].index("United States District Court, "):
        start = entry[0].index("United States District Court, ") + len("United States District Court, ")
        entry[0].index(" ",[start:])
    else :
        data.append("Invalid entry")
    #Write data
    return data


raw_cases = collect_cases()
clean_cases = []
for x in raw_cases:
    clean_cases.append(parse_court_case(x))

f = open("clean_cases.txt","w+")
for x in clean_cases:
    f.write(str(x))
