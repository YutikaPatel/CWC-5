import json
import csv

#store data from jason into dict
with open("Stock List.json","r") as f:
    data=json.load(f)
    stocks=data["stocks"]

#write the stocks keys and all values into csv file
with open("stockList.csv","w") as f:
    fieldnames=stocks[0].keys()
    writer=csv.DictWriter(f,fieldnames=fieldnames)
    writer.writeheader()
    for stock in stocks:
        writer.writerow(stock)


