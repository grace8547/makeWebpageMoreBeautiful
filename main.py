import bs4 as bs
import urllib2
import pandas as pd

def ScrapCatInfo(result):
  cats = urllib2.urlopen(result['href']).read()
  s = bs.BeautifulSoup(cats, 'lxml')
  print(s.finds


sauce = urllib2.urlopen("http://www.adoptapet.com/cat-adoption/search/50/miles/94403?color=Calico+or+Dilute+Calico&color_id=50").read()
soup = bs.BeautifulSoup(sauce, 'lxml')

# results = soup.find('div',class_='results_wrapper')
# array = pd.ndarray(cats)
for result in soup.findAll('a', {'class': 'smaller_line_height'}): 
  ScrapCatInfo(result)                                                 


