
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
all_lotinfo = soup.find_all('div', {'class':'results-lot-info'})
all_estimate = soup.find_all('div', {'class':'results-estimate'})
all_resultsprice = soup.find_all('div', {'class':'results-price'})
all_resultspricetype = soup.find_all('div', {'class':'results-price-type'})
all_href = map(lambda x: x.contents[1]['href'], soup.find_all('div', {'class':'image'}))

count = len(results)
# print len(results)
# print len(all_href)
# print all_resultsprice[0].text.strip().split()

request_headers = {'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}

with open('output.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)

    headers = ['Link','Title','Date','Type','Sale Date','Auction House','Lot Info', 'Estimate Low','Estimate High','Price Sold', 'Price Type']
    if need_details:
        headers += ['materials','measurements','size_notes','edition','markings','condition']
    writer.writerow(headers)

    for i in range(0, count):
        fulllink = unicode('http://artsalesindex.artinfo.com' + all_href[i]).encode('utf-8')
        estimate_low = 'N/A'
        estimate_high = "N/A"
        date = 'N/A'
        thetype = 'N/A'
        datetype = all_datetype[i].text.split()
        lot_info = map(lambda x: x.strip(), all_lotinfo[i].text.split('\n\t'))
        price_sold = all_resultsprice[i].text.strip().split()
        price_type = all_resultspricetype[i].text.strip()

        if len(price_sold) == 3:
            price_sold = price_sold[1]
        else:
            price_sold = 'N/A'

        if len(lot_info) > 0:
            lot_info = lot_info[0]
        else:
            lot_info = 'N/A'

        if len(datetype) > 0:
            if datetype[0].isdigit():
                date = datetype[0]
                thetype = ' '.join(datetype[1:])
            else:
                thetype = ' '.join(datetype)

        estimate = all_estimate[i].text.split()
        if len(estimate) == 6:
            estimate_low = estimate[1]
            estimate_high = estimate[4]
        elif len(estimate) == 2:
            estimate_low = estimate[1]
            estimate_high = 'N/A'

        row = [
            fulllink,
            unicode(all_titles[i].text.strip()).encode('utf-8'),
            unicode(date).encode('utf-8'),
            unicode(thetype).encode('utf-8'),
            unicode(all_saledate[i * 2].text.strip()).encode('utf-8'),
            unicode(all_auctionhouse[i].text.strip()).encode('utf-8'),
            unicode(lot_info).encode('utf-8'),
            unicode(estimate_low).encode('utf-8'),
            unicode(estimate_high).encode('utf-8'),
            unicode(price_sold).encode('utf-8'),
            unicode(price_type).encode('utf-8')
        ]

        if need_details:
            # print fulllink
            # r = requests.get(fulllink, headers=request_headers)
            # new_soup = BeautifulSoup(r.content, 'lxml')
            with open('detail.html') as fp2:
                new_soup = BeautifulSoup(fp2, 'lxml')
            all_artworkdetails = new_soup.find_all('p', {'class':'style14Reg555'})
            for j in range(0, len(all_artworkdetails)):
                all_artworkdetails[j] = unicode(all_artworkdetails[j].text.strip()).encode('utf-8')
            rows += all_artworkdetails

        writer.writerow(row)
