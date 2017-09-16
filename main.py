import bs4 as bs
import urllib2
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
  flag=False
  temp={}
  if shelter:
    for li in shelter.find_all('li'):
      if flag is True:
        if li.find('b', text=re.compile('E-mail')):
          rescueGroupDic[temp]['E-mail']=li.find('a').text
        if li.find('b', text=re.compile('Contact')):
          rescueGroupDic[temp]['Contact']=li.contents[1]
        if li.find('b', text=re.compile('Phone')):
          rescueGroupDic[temp]['Phone']=li.find('a').text
        if li.find('b', text=re.compile('Fax')):
          rescueGroupDic[temp]['Fax']=li.contents[1]
        if li.find('b', text=re.compile('Website')):
          rescueGroupDic[temp]['Website']=li.find('a').text    
        if li.find('b', text=re.compile('Address')):
          rescueGroupDic[temp]['Address']=li.contents[2]                                          
      if li.find('b', text=re.compile('Rescue Group')) or li.find('b', text=re.compile('Shelter')):
        if li.find('a').text not in rescueGroupDic.keys():
          rescueGroupDic[li.find('a').text] = {}          
          rescueGroupDic[li.find('a').text]['count']=1  
          temp=li.find('a').text
          flag=True    
        else:
          rescueGroupDic[li.find('a').text]['count']+=1

source = urllib2.urlopen("http://www.adoptapet.com/cat-adoption/search/50/miles/94403?color=Calico+or+Dilute+Calico&color_id=50").read()
soup = bs.BeautifulSoup(source, 'lxml')
numCats = 3
results = soup.findAll('span', {'class':'featured-thumbnail'})
i=0
rescueGroupDic = {}
for result in results:
  ScrapShelterInfo(result.find('a', {'class': 'smaller_line_height'}), rescueGroupDic)
  ScrapCatInfo(result.find('a', {'class': 'smaller_line_height'}))  
  i=i+1
  if i==numCats:
    break  

for k, v in rescueGroupDic.items():
  print(k, v)
  print('')
