import csv

inputs = []
def list_parser(list):
    list = list[1:len(list)-2]
    ar = list.split(",")
    inputs.append(ar)
with open("clean_cases_1.txt","r") as openfile:
    list = openfile.readlines()
    for x in list:
        list_parser(x)

with open("data.csv", "a") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(inputs)
