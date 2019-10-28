from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
import concurrent.futures
import requests
import sys

class HTMLParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.links = []

  def handle_starttag(self, tag, attrs):
    for attr in attrs:
      if(tag == 'a' and attr[0] == 'href' and (attr[1].startswith('http://') or attr[1].startswith('https://'))):
        self.links.append(attr[1])

  def get_links(self):
    return self.links

def get_links(URL):
  URL_request = requests.get(URL)
  parser = HTMLParser()
  parser.feed(str(URL_request.content))
  URL_links = set(parser.get_links())
  
  return URL_links

def print_links(URL, URL_links):
  print(URL)
  for link in URL_links:
    print("  " + link)	

if __name__ == '__main__':
  if(len(sys.argv) != 2):
    print("Invalid number of arguments, please enter a single URL for crawling")
    sys.exit()
  URL = sys.argv[1]  
  URL_links = get_links(URL)
  print_links(URL, URL_links)
  workers = 4
  
  with concurrent.futures.ThreadPoolExecutor(max_workers = workers) as executor:
    URL_future = {executor.submit(get_links, link): link for link in URL_links}
    for future in concurrent.futures.wait(URL_future):
      future.result()
	
    #URL_future = {executor.map(get_links, link): link for link in URL_links}
    #for future in concurrent.futures.wait(URL_future):
    #  print_links(link, URL_future)
    #  link = URL_future[future]
    #  try:
    #    data = future.result()
    #  except Exception as exc:
    #    print('%r generated an exception: %s' % (link, exc))
    #  else:
    #    print(data)
    #for link in URL_links:
    # print_links(link, URL_links)
