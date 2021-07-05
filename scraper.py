import scraperwiki
from bs4 import BeautifulSoup, Comment
import string
import unicodedata
import time

# Sample Apartment DataStructure
# ApartmentEntry = {
#   ApartmentComplex: 
#   RoomNum:
#   Price:
#   SqFt:
#   MoveInDate:
# 
#   #Optional for future development
#   Beds:
#   Baths:
# }

def scrapeAndSoup(url):
    response = scraperwiki.scrape(url)
    time.sleep(5)
    return BeautifulSoup(response)

apartments = []

## Courthouse Plaza ##
soup = scrapeAndSoup("https://www.equityapartments.com/arlington/courthouse/courthouse-plaza-apartments")
# find all 2 bedroom listings
twoBedroomsGrouped = soup.find(id="bedroom-type-2")
twoBedroomsList = twoBedroomsGrouped.find_all("li")

for listing in twoBedroomsList:
    # apartmentComplex
    apartmentEntry = {"apartmentComplex": "Courthouse Plaza"}
    # room #
        # find comments in each listing of the form <!-- ledgerId: 29828, buildingId: 01, unitId: 1119 -->
    for comments in listing.findAll(text=lambda text:isinstance(text, Comment)):
        roomNum = comments.split()[-1]
        apartmentEntry["roomNum"] = roomNum
        comments.extract()

    # price
    apartmentEntry["price"] = listing.find("span", {"class": "pricing"}).string
    
    # Sq Ft and  Move-In Date
    specs = listing.find("div", {"class": "specs"})
        # traverse to the sqft then split to get the number without the trailing 'sq.ft'
    apartmentEntry["sqft"] = specs.findAll("p")[2].findAll("span")[0].string.split()[0]
        # traverse to the available by date
    apartmentEntry["moveindate"] = specs.findAll("p")[3].string.split()[1]
    
    apartments.append(apartmentEntry)
    print(apartmentEntry)
# print(apartments)
