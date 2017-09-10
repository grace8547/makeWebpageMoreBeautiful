import bs4 as bs
import urllib2
import threading
def GetCatStory(result):
  cats = urllib2.urlopen(result['href']).read()
  s = bs.BeautifulSoup(cats, 'lxml')
  storys = s.find('div', {'class':'hidden-xs body'}).parent.find_all('div')
  for story in storys:
  	print(story.text)
  	# empty line
  	print('')


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


