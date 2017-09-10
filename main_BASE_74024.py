import bs4 as bs
import urllib2

def ScrapCatInfo(result):
  cats = urllib2.urlopen(result['href']).read()
  s = bs.BeautifulSoup(cats, 'lxml')
  storys = s.find('div', {'class':'hidden-xs body'}).parent.find_all('div')
  for story in storys:
  	print(story.text)
  	# empty line
  	print('')


sauce = urllib2.urlopen("http://www.adoptapet.com/cat-adoption/search/50/miles/94403?color=Calico+or+Dilute+Calico&color_id=50").read()
soup = bs.BeautifulSoup(sauce, 'lxml')
numCats = 5
results = soup.findAll('span', {'class':'featured-thumbnail'})
i=0
for result in results:
	ScrapCatInfo(result.find('a', {'class': 'smaller_line_height'}))
	i=i+1
  	# just primt numCats cats
  	if i==numCats:
  		break                                        

