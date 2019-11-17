from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
import concurrent.futures
import requests
import sys

# Create Parser class with a_href tag handler metod
class Parser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.links = []

  def handle_starttag(self, tag, attrs):
    for attr in attrs:
      if(tag == 'a' and attr[0] == 'href' and (attr[1].startswith('http://') 
         or attr[1].startswith('https://'))):
        self.links.append(attr[1])

  def get_links(self):
    return self.links

# Get unique set of links 
def get_links(URL, URL_links):
  try:
    URL_request = requests.get(URL)
    parser = Parser()
    parser.feed(str(URL_request.content))
    URL_links[URL] = set(parser.get_links())
  except Exception as exc:
    print("Error ocurred while processing URL: " + URL)
  return URL_links

# Print URL keys and links
def print_links(URL_links):
  for URL_key, link_set in URL_links.items():
    print(URL_key)
    for link in link_set:
      print("  " + link)	

if __name__ == '__main__':
  # Handle input parameters 
  if(len(sys.argv) != 3):
    print(f'Invalid number of arguments, please enter a single URL for crawling and number' + 
          f' of workers\nExample: python3 {sys.argv[0]} http://www.rescale.com 5')
    sys.exit()
  
  URL = sys.argv[1]  
  WORKERS = int(sys.argv[2])
  URL_links = {}
  URL_links = get_links(URL, URL_links)
  print_links(URL_links)
  
  # Create thread pool and feed URL link set into
  with concurrent.futures.ThreadPoolExecutor(max_workers = WORKERS) as executor:
    URL_future = {executor.submit(get_links, link, URL_links): link for link in URL_links[URL]}
    for future in concurrent.futures.wait(URL_future):
      for item in future:
        print_links(item.result())
