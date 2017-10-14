
from bs4 import BeautifulSoup
import csv
import requests

with open('a.html') as fp:
    soup = BeautifulSoup(fp, "html.parser")

results = soup.find_all('tr', {'class':'results'})
all_titles = soup.find_all('div', {'class':'results-title'})
all_datetype = soup.find_all('div', {'class':'results-date-type'})
all_saledate = soup.find_all('div', {'class':'results-sale-date'})
all_auctionhouse = soup.find_all('div', {'class':'results-auction-house'})
all_estimate = soup.find_all('div', {'class':'results-estimate'})
all_resultsprice = soup.find_all('div', {'class':'results-price'})

all_href = soup.find_all('a', {'style':'color:#222'})

count = len(results)
# print len(results)
# print len(all_titles)
# print len(all_datetype)
# print len(all_saledate)
# print len(all_auctionhouse)
# print len(all_estimate)
# print len(all_href)

headers = {'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}

with open('output.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['link','title','date_type','sale_date','auction_house','estimate','price_sold','materials','measurements','size_notes','edition','markings','condition'])
    for i in range(0, count):

        fulllink = unicode('http://artsalesindex.artinfo.com' + all_href[i]['href']).encode('utf-8')
        print fulllink
        r = requests.get(fulllink, headers=headers)
        new_soup = BeautifulSoup(r.content, 'html.parser')
        all_artworkdetails = new_soup.find_all('p', {'class':'style14Reg555'})

        for j in range(0, len(all_artworkdetails)):
            all_artworkdetails[j] = unicode(all_artworkdetails[j].text.strip()).encode('utf-8')
        writer.writerow([
            fulllink,
            unicode(all_titles[i].text.strip()).encode('utf-8'),
            unicode(all_datetype[i].text.strip()).encode('utf-8'),
            unicode(all_saledate[i * 2].text.strip()).encode('utf-8'),
            unicode(all_auctionhouse[i].text.strip()).encode('utf-8'),
            unicode(all_estimate[i].text.strip()).encode('utf-8'),
            unicode(all_resultsprice[i].text.strip()).encode('utf-8')] +
            all_artworkdetails)
