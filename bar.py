from bs4 import BeautifulSoup
import requests


url = 'http://artsalesindex.artinfo.com/auctions/Pablo-Picasso-6856122/Peintre-Debout-a-son-Chevalet,-avec-un-Modele-(from-Sable-Mouvant)-1966'

headers = {'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"}
result = requests.get(url, headers=headers)
soup = BeautifulSoup(result.content, 'html.parser')
print soup.prettify()

