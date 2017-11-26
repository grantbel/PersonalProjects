# -*- coding: utf-8 -*-
"""
a script to scrape data on LA neighborhood from city-data.com 

@author: grantbelsterling
"""
from bs4 import BeautifulSoup
import urllib.request

cd_LA_url = 'http://www.city-data.com/city/Los-Angeles-California.html'
page = urllib.request.urlopen(cd_LA_url)
soup = BeautifulSoup(page, "html.parser")

neighbs = soup.find(class_="neighborhoods")

neighbDict = {}
for entry in neighbs("a"):
    link = 'http://www.city-data.com/'+entry['href']
    neighbDict[entry.string] = link
    

# %% Cell 2

#take the string name of the url and the citydata url itself 
#for a neighborhood. returns a dictionary with fields scraped from
#the citydata page. note there are a few junk fields due to the scraping
#that will need to be removed in the data analysis portion
def pullNeighborhood(name, neighbURL):
    soupObj = BeautifulSoup(urllib.request.urlopen(neighbURL),'lxml')
    contents = soupObj.find_all(class_='content-item')
    varsDict = {}
    for entry in contents:
        textList = entry.find_all(text=True)
        stack = []
        for elt in textList:
            elt= elt.strip()
            if(elt and elt[-1]==':'):
                stack.append(elt)
            elif(elt and (elt[0].isnumeric() or elt[0]=="$")):
                var = ''
                for layer in stack:
                    if name in layer:
                        layer = 'Here'
                    var = var + layer
                varsDict[var] = elt
                stack.pop
                
    #keep only entries relating to the neighborhood by deleting
    #entries relating to Los Angeles in aggregate
    filteredDict = {}
    for key, value in varsDict.items():
        if key and 'Los Angeles' not in key and 'city' not in key.lower():
            filteredDict[key] = value
            
    filteredDict['Neighborhood']= name        
    return filteredDict
    
# %% Cell 3


rows=[]
for name, url in neighbDict.items():
    name = name[:-13] #remove 'neighborhood' that was affixed to each string
    rows.append(pullNeighborhood(name,url))


# %% Cell 4
import csv

fieldnames = set()
for row in rows:
    for key in row:
        fieldnames.add(key)
        
fieldnames = list(fieldnames)
    
with open('neighbData.csv', 'w') as csvfile:
    writer = csv.DictWriter((csvfile), fieldnames=fieldnames)

    writer.writeheader()
    for entry in rows:
        writer.writerow(entry)


    
