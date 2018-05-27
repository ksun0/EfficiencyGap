with open('data.csv', newline='') as csvfile:
    data_reader = csv.reader(csvfile, delimiter=',')
    for row in data_reader:
        if row[1] == True:
            try int(row[2]):
                year = int(row[2])
            except ValueError:
