
from bs4 import BeautifulSoup
import csv
import requests

need_details = False

with open('result.html') as fp:
    soup = BeautifulSoup(fp, "lxml")

results = soup.find_all('tr', {'class':'results'})
all_titles = soup.find_all('div', {'class':'results-title'})
all_datetype = soup.find_all('div', {'class':'results-date-type'})
all_saledate = soup.find_all('div', {'class':'results-sale-date'})
all_auctionhouse = soup.find_all('div', {'class':'results-auction-house'})
all_estimate = soup.find_all('div', {'class':'results-estimate'})
all_resultsprice = soup.find_all('div', {'class':'results-price'})

all_href = soup.find_all('a', {'style':'color:#222'})

count = 1#len(results)

headers = {'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}

with open('output.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)

    headers = ['link','title','date','type','sale_date','auction_house','estimate_low','estimate_high','price_sold']
    if need_details:
        headers += ['materials','measurements','size_notes','edition','markings','condition']
    writer.writerow(headers)

    for i in range(0, count):
        fulllink = unicode('http://artsalesindex.artinfo.com' + all_href[i]['href']).encode('utf-8')
        datetype = all_datetype[i].text.split()
        estimate = all_estimate[i].text.split()
        estimate_low = 'Oops'
        estimate_high = "Oops again"
        if len(estimate) == 6:
            estimate_low = estimate[1]
            estimate_high = estimate[4]
        elif len(estimate) == 2:
            estimate_low = estimate[1]
            estimate_high = 'N/A'

        row = [
            fulllink,
            unicode(all_titles[i].text.strip()).encode('utf-8'),
            unicode(datetype[0]).encode('utf-8'),
            unicode(datetype[1]).encode('utf-8'),
            unicode(all_saledate[i * 2].text.strip()).encode('utf-8'),
            unicode(all_auctionhouse[i].text.strip()).encode('utf-8'),
            unicode(estimate_low).encode('utf-8'),
            unicode(estimate_high).encode('utf-8'),
            unicode(all_resultsprice[i].text.strip()).encode('utf-8')
        ]

        if need_details:
            # print fulllink
            # r = requests.get(fulllink, headers=headers)
            # new_soup = BeautifulSoup(r.content, 'lxml')
            with open('detail.html') as fpb:
                new_soup = BeautifulSoup(fpb, 'lxml')
            all_artworkdetails = new_soup.find_all('p', {'class':'style14Reg555'})
            for j in range(0, len(all_artworkdetails)):
                all_artworkdetails[j] = unicode(all_artworkdetails[j].text.strip()).encode('utf-8')
            rows += all_artworkdetails

        writer.writerow(row)
