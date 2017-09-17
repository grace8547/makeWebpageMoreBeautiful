import bs4 as bs
import urllib2
import re
import threading

class FindCatShelterInfo:
  def __init__(self):
    self.url = "http://www.adoptapet.com/cat-adoption/search/50/miles/94403?color=Calico+or+Dilute+Calico&color_id=50"
    self.rescueGroupDic = {}
    self.catInfoDic = {}
    self.thumbnailPageResults = {}
    self.threads = []
    self.nextThumbnailPageLink = {};
    self.lock = threading.Lock() 
    self.OpenThumbnailPage()

  def OpenNextThumbnailPage(self):
    self.url = self.nextThumbnailPageLink
    self.OpenThumbnailPage()

  def OpenThumbnailPage(self):
    source = urllib2.urlopen(self.url).read()
    soup = bs.BeautifulSoup(source, 'lxml')
    self.thumbnailPageResults = soup.findAll('span', {'class':'featured-thumbnail'})
    nextPage = soup.find('span', {'class':'next_link'})
    if nextPage:
      self.nextThumbnailPageLink = nextPage.find('a', href=True)['href']
    else:
      self.nextThumbnailPageLink = {}


  def ScrapeSingleCatInfo(self, result):
    if result['href']:
      single_cat_helper = urllib2.urlopen(result['href']).read()
      single_cat = bs.BeautifulSoup(single_cat_helper, 'lxml')
      story = single_cat.find('div', {'class':'hidden-xs body'}).parent.find_all('div')
      # print(story[0].text)
      # print(story[1].text)
      # print('')

  def FindShelterName(self, li, newShelterFound, shelterName):
    if li.find('b', text=re.compile('Rescue Group')) or li.find('b', text=re.compile('Shelter')):
      if li.find('a').text not in self.rescueGroupDic.keys():
        self.rescueGroupDic[li.find('a').text] = {}          
        self.rescueGroupDic[li.find('a').text]['count']=1  
        shelterName=li.find('a').text
        newShelterFound=True 
      else:
        # shelter already in doc, update count and skip scrape shelter infomation
        self.rescueGroupDic[li.find('a').text]['count']+=1  

  def FindShelterInfoByName(self, li, shelterName, info):
    if li.find('b', text=re.compile(info)):
      if info is 'E-mail' or 'Phone' or 'Website':
        self.rescueGroupDic[shelterName][info]=li.find('a').text
      elif info is 'Contact':
        self.rescueGroupDic[shelterName][info]=li.contents[1]
      elif info is 'Address':
        self.rescueGroupDic[shelterName][info]=li.contents[2]

  def ScrapeShelterInfo(self, result):
    if result['href']:
      single_shelter_helper = urllib2.urlopen(result['href']).read()
      single_shelter = bs.BeautifulSoup(single_shelter_helper, 'lxml')
      shelter = single_shelter.find('div', {'class': 'body contact_sidebar hidden-sm hidden-md hidden-lg'})
      newShelterFound=False
      shelterName={}
      if shelter:
        for li in shelter.find_all('li'):
          self.lock.acquire()
          if newShelterFound is True:
            self.FindShelterInfoByName(li, shelterName, 'E-mail')
            self.FindShelterInfoByName(li, shelterName, 'Contact')
            self.FindShelterInfoByName(li, shelterName, 'Phone')
            self.FindShelterInfoByName(li, shelterName, 'Fax')
            self.FindShelterInfoByName(li, shelterName, 'Website')
            self.FindShelterInfoByName(li, shelterName, 'Address')
          else: 
            self.FindShelterName(li, newShelterFound, shelterName)  
          self.lock.release()                                        


  def ScrapeCatInfoPage(self):
    for result in self.thumbnailPageResults: 
      # t1 = threading.Thread(target = self.ScrapeSingleCatInfo, args = [result.find('a', {'class': 'smaller_line_height'}),])
      t2 = threading.Thread(target = self.ScrapeShelterInfo, args = [result.find('a', {'class': 'smaller_line_height'}), ])
      # t1.start()
      t2.start()
      # self.threads.append(t1)
      self.threads.append(t2)

    for t in self.threads:
      t.join()


if __name__ == "__main__":
  pageIndex = 0
  progress = 0
  catShelterScraper = FindCatShelterInfo()
  catShelterScraper.ScrapeCatInfoPage()
  while catShelterScraper.nextThumbnailPageLink:
    pageIndex+=1;
    progress = pageIndex/13.0*100
    print('Analyzing ' + str(round(progress,2)) + '%')
    catShelterScraper.OpenNextThumbnailPage()
    catShelterScraper.ScrapeCatInfoPage()

  for k, v in catShelterScraper.rescueGroupDic.items():
    print(k, v)

