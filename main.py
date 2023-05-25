import json
from collections import defaultdict

# specify the name of the input file
jsonFile = open('1-input.json')

inputData = json.load(jsonFile)

# a dictionary to store the balance for each month
balanceSheet = defaultdict(int)

# adding balance values for each month in the balance sheet
for entry in inputData["expenseData"]:
    balanceSheet[entry["startDate"]] -= entry["amount"]

for entry in inputData["revenueData"]:
    balanceSheet[entry["startDate"]] += entry["amount"]

# final json output we want to be printed
outputData = {
    "balance": []
}

# finding the least and the maximum timestamp in the balancesheet.
minDate = None
maxDate = None

for date in balanceSheet:
    if minDate:
        if date < minDate:
            minDate = date
    else:
        minDate = date
    
    if maxDate:
        if date > maxDate:
            maxDate = date
    else:
        maxDate = date

# function to generate all the monthly timestamps between the minimum timestamp and the maximum timestamp
def generateDates(minDate, maxDate):
    dates = []
    minDate = minDate.split("-")
    maxDate = maxDate.split("-")
    minYear = int(minDate[0])
    minMonth = int(minDate[1])
    maxYear = int(maxDate[0])
    maxMonth = int(maxDate[1])

    if minYear == maxYear:
        for i in range(minMonth, maxMonth+1):
            if i < 10:
                dates.append(f"{minYear}-0{i}-01T00:00:00.000Z")
            else:
                dates.append(f"{minYear}-{i}-01T00:00:00.000Z")
    else:
        for i in range(minMonth, 13):
            if i < 10:
                dates.append(f"{minYear}-0{i}-01T00:00:00.000Z")
            else:
                dates.append(f"{minYear}-{i}-01T00:00:00.000Z")
        
        for i in range(minYear+1, maxYear):
            for j in range(minMonth, 13):
                if j < 10:
                    dates.append(f"{i}-0{j}-01T00:00:00.000Z")
                else:
                    dates.append(f"{i}-{j}-01T00:00:00.000Z")

        for i in range(1, maxMonth+1):
            if i < 10:
                dates.append(f"{maxYear}-0{i}-01T00:00:00.000Z")
            else:
                dates.append(f"{maxYear}-{i}-01T00:00:00.000Z")

    return dates

# adding the balance sheet values to the json outputData for each timestamp
dates = generateDates(minDate, maxDate)
for date in dates:
    outputData["balance"].append({"amount": balanceSheet[date], "startDate": date})

print(json.dumps(outputData, indent=4))
