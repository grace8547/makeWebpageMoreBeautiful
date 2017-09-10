import bs4 as bs
import urllib2
<<<<<<< HEAD
import threading
def GetCatStory(result):
  cats = urllib2.urlopen(result['href']).read()
  s = bs.BeautifulSoup(cats, 'lxml')
  storys = s.find('div', {'class':'hidden-xs body'}).parent.find_all('div')
  for story in storys:
  	print(story.text)
  	# empty line
  	print('')
=======
import re
def ScrapCatInfo(result):
  single_cat_helper = urllib2.urlopen(result['href']).read()
  single_cat = bs.BeautifulSoup(single_cat_helper, 'lxml')
  story = single_cat.find('div', {'class':'hidden-xs body'}).parent.find_all('div')
  # print(story[0].text)
  # print(story[1].text)
  # print('')

def ScrapShelterInfo(result, rescueGroupDic):
  single_shelter_helper = urllib2.urlopen(result['href']).read()
  single_shelter = bs.BeautifulSoup(single_shelter_helper, 'lxml')
  shelter = single_shelter.find('div', {'class': 'body contact_sidebar hidden-sm hidden-md hidden-lg'})

  if shelter:
    for li in shelter.find_all('li'):
      if li.find('b', text=re.compile('Rescue Group')) or li.find('b', text=re.compile('Shelter')):
        if li.find('a').text not in rescueGroupDic.keys():
          rescueGroupDic[li.find('a').text]=1
        else:
          rescueGroupDic[li.find('a').text]+=1
>>>>>>> 231294fac9d88c09c7cd133322798eeaa2d22b44

  print(rescueGroupDic)

<<<<<<< HEAD
sauce = urllib2.urlopen("http://www.adoptapet.com/cat-adoption/search/50/miles/94403?color=Calico+or+Dilute+Calico&color_id=50").read()
soup = bs.BeautifulSoup(sauce, 'lxml')
results = soup.findAll('span', {'class':'featured-thumbnail'})
threads = []
for result in results:
	aTag = result.find('a', {'class': 'smaller_line_height'})
	t=threading.Thread(target = GetCatStory, args = (aTag,))
	threads.append(t)
	t.start()

for t in threads:
	t.join()


=======

source = urllib2.urlopen("http://www.adoptapet.com/cat-adoption/search/50/miles/94403?color=Calico+or+Dilute+Calico&color_id=50").read()
soup = bs.BeautifulSoup(source, 'lxml')
numCats = 10
results = soup.findAll('span', {'class':'featured-thumbnail'})
i=0
rescueGroupDic = {}
for result in results:
  ScrapCatInfo(result.find('a', {'class': 'smaller_line_height'}))
  ScrapShelterInfo(result.find('a', {'class': 'smaller_line_height'}), rescueGroupDic)
  i=i+1
  if i==numCats:
    break                                        
>>>>>>> 231294fac9d88c09c7cd133322798eeaa2d22b44
