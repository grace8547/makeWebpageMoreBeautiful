import bs4 as bs
import urllib2
import re
import threading
def ScrapCatInfo(result):
  single_cat_helper = urllib2.urlopen(result['href']).read()
  single_cat = bs.BeautifulSoup(single_cat_helper, 'lxml')
  story = single_cat.find('div', {'class':'hidden-xs body'}).parent.find_all('div')
  # print(story[0].text)
  # print(story[1].text)
  # print('')

def ScrapShelterInfo(result, rescueGroupDic, lock):
  single_shelter_helper = urllib2.urlopen(result['href']).read()
  single_shelter = bs.BeautifulSoup(single_shelter_helper, 'lxml')
  shelter = single_shelter.find('div', {'class': 'body contact_sidebar hidden-sm hidden-md hidden-lg'})
  firstFound = False
  rescueInfo = {}
  lastShelter = {}
  if shelter:
    for li in shelter.find_all('li'):
      if li.find('b', text=re.compile('Rescue Group')) or li.find('b', text=re.compile('Shelter')):
        lock.acquire()
        if li.find('a').text not in rescueGroupDic.keys():
          rescueGroupDic[li.find('a').text]={}
          rescueGroupDic[li.find('a').text]['count']=1
          firstFound = True
          lastShelter = li.find('a').text
        else:
          rescueGroupDic[li.find('a').text]['count']+=1
        lock.release()

      if firstFound:
        if li.find('b', text=re.compile('Contact')):
          rescueGroupDic[lastShelter]['Contact']=li.contents[1]
        if li.find('b', text=re.compile('E-mail')):
          rescueGroupDic[lastShelter]['E-mail']=li.find('a').text


source = urllib2.urlopen("http://www.adoptapet.com/cat-adoption/search/50/miles/94403?color=Calico+or+Dilute+Calico&color_id=50").read()
soup = bs.BeautifulSoup(source, 'lxml')
results = soup.findAll('span', {'class':'featured-thumbnail'})
rescueGroupDic = {}
threads = []
rescueGroupDiclock = threading.Lock()
for result in results:
  # t1 = threading.Thread(target = ScrapCatInfo, args = [result.find('a', {'class': 'smaller_line_height'}),])
  t2 = threading.Thread(target = ScrapShelterInfo, args = [result.find('a', {'class': 'smaller_line_height'}), rescueGroupDic, rescueGroupDiclock, ])
  # t1.start()
  t2.start()
  # threads.append(t1)
  threads.append(t2)

for t in threads:
  t.join()

print(rescueGroupDic)
