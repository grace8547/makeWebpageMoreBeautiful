import bs4 as bs
import urllib2

def ScrapCatInfo(result):
  single_cat_helper = urllib2.urlopen(result['href']).read()
  single_cat = bs.BeautifulSoup(single_cat_helper, 'lxml')
  story = single_cat.find('div', {'class':'hidden-xs body'}).parent.find_all('div')
  print(story[0].text)
  print(story[1].text)
  print('')

def ScrapShelterInfo(result):
  single_shelter_helper = urllib2.urlopen(result['href']).read()
  single_shelter = bs.BeautifulSoup(single_shelter_helper, 'lxml')
  shelter = single_shelter.find('div', {'class': 'body contact_sidebar hidden-sm hidden-md hidden-lg'}).find_all('li')
  print(shelter[0].find('b').text + " " +shelter[0].find('a').text)
  print(shelter[1].find('b').text + " " +shelter[1].text)
  print(shelter[2].find('b').text + " " +shelter[2].find('a').text)
  print(shelter[3].find('b').text + " " +shelter[3].find('a').text)
  print(shelter[4].find('b').text + " " +shelter[4].text)

source = urllib2.urlopen("http://www.adoptapet.com/cat-adoption/search/50/miles/94403?color=Calico+or+Dilute+Calico&color_id=50").read()
soup = bs.BeautifulSoup(source, 'lxml')
numCats = 1
results = soup.findAll('span', {'class':'featured-thumbnail'})
i=0
for result in results:
  ScrapCatInfo(result.find('a', {'class': 'smaller_line_height'}))
  ScrapShelterInfo(result.find('a', {'class': 'smaller_line_height'}))
  i=i+1
  if i==numCats:
    break                                        