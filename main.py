import bs4 as bs
import urllib2
import re

class FindCatShelterInfo:
  def __init__(self):
    self.url = "http://www.adoptapet.com/cat-adoption/search/50/miles/94403?color=Calico+or+Dilute+Calico&color_id=50"
    self.rescueGroupDic = {}
    self.catInfoDic = {}
    self.numCats = 5
    self.thumbnailPageResults = {}
    self.OpenThumbnailPage()

  def OpenThumbnailPage(self):
    source = urllib2.urlopen(self.url).read()
    soup = bs.BeautifulSoup(source, 'lxml')
    self.thumbnailPageResults = soup.findAll('span', {'class':'featured-thumbnail'})

  def ScrapeSingleCatInfo(self, result):
    single_cat_helper = urllib2.urlopen(result['href']).read()
    single_cat = bs.BeautifulSoup(single_cat_helper, 'lxml')
    story = single_cat.find('div', {'class':'hidden-xs body'}).parent.find_all('div')
    # print(story[0].text)
    # print(story[1].text)
    # print('')

  def ScrapeShelterInfo(self, result):
    single_shelter_helper = urllib2.urlopen(result['href']).read()
    single_shelter = bs.BeautifulSoup(single_shelter_helper, 'lxml')
    shelter = single_shelter.find('div', {'class': 'body contact_sidebar hidden-sm hidden-md hidden-lg'})
    flag=False
    temp={}
    if shelter:
      for li in shelter.find_all('li'):
        if flag is True:
          if li.find('b', text=re.compile('E-mail')):
            self.rescueGroupDic[temp]['E-mail']=li.find('a').text
          if li.find('b', text=re.compile('Contact')):
            self.rescueGroupDic[temp]['Contact']=li.contents[1]
          if li.find('b', text=re.compile('Phone')):
            self.rescueGroupDic[temp]['Phone']=li.find('a').text
          if li.find('b', text=re.compile('Fax')):
            self.rescueGroupDic[temp]['Fax']=li.contents[1]
          if li.find('b', text=re.compile('Website')):
            self.rescueGroupDic[temp]['Website']=li.find('a').text    
          if li.find('b', text=re.compile('Address')):
            self.rescueGroupDic[temp]['Address']=li.contents[2]                                          
        if li.find('b', text=re.compile('Rescue Group')) or li.find('b', text=re.compile('Shelter')):
          if li.find('a').text not in self.rescueGroupDic.keys():
            self.rescueGroupDic[li.find('a').text] = {}          
            self.rescueGroupDic[li.find('a').text]['count']=1  
            temp=li.find('a').text
            flag=True    
          else:
            self.rescueGroupDic[li.find('a').text]['count']+=1

  def ScrapeCatInfoPage(self):
    i=0
    for result in self.thumbnailPageResults:
      self.ScrapeShelterInfo(result.find('a', {'class': 'smaller_line_height'}))
      self.ScrapeSingleCatInfo(result.find('a', {'class': 'smaller_line_height'}))  
      i=i+1
      if i==self.numCats:
        break  
    for k, v in self.rescueGroupDic.items():
      print(k, v)

if __name__ == "__main__":
  catShelterScraper = FindCatShelterInfo()
  catShelterScraper.ScrapeCatInfoPage()

