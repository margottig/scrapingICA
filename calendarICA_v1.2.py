import bs4, requests
import csv
import pandas as pd

#request ICA'S calendar URL
webLink = requests.get('https://www.icacommission.org/calendar.html')
webLink.raise_for_status
icaSoup=bs4.BeautifulSoup(webLink.text, 'html.parser')

##get all relevant events
events=[]
for i in range(4,32):
    pTags=icaSoup.select('p')
    events.append(pTags[i].getText().split('\n'))

##clean data
cleanedData=[]
for row in events:
    temp=[]
    temp.append(row[0])
    temp.append(row[1])
    temp.append(row[2])
    cleanedData.append(temp)

##rearrange data
array=[]
for column in cleanedData:
    tempArr = column[0].split(',')
    if len(tempArr)>3:
        temp = tempArr[-1]
        tempArr.pop()
        temp2 = tempArr[-1]
        tempArr.pop()
        tempArr.append(temp+' '+temp2)
    elif len(tempArr)==2:
        tempArr.append('ND')
    elif len(tempArr)==1:
        tempArr.append('ND')
        tempArr.append('ND')
    else:
        pass
    tempArr.append(column[1])
    tempArr.append(column[2])
    array.append(tempArr)
    
#Write table
HEADER = ['Date', 'City', 'Country', 'Event Name', 'Link to event']
DATA = array
with open('ica_events.csv', 'w', encoding='utf-8', newline='') as csvfile:
    rows = csv.writer(csvfile)
    rows.writerow(HEADER)
    for row in DATA:
        rows.writerow(row)
read_file = pd.read_csv('ica_events.csv')
read_file.to_excel('ica_events.xlsx', index=None, header=True)