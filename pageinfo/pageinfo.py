from bs4 import BeautifulSoup
from HTMLParser import HTMLParseError
import requests
import json
import re
from urlparse import urlparse
from urlparse import urljoin


#get title, description, favicon, twitter card, facebook open graph data
def get_meta(url, html):
  data = {}
  data["title"] = ""
  data["description"] = None
  data["favicon"] = None
  data["facebook"] = {}
  data["twitter"] = {}

  try:
    
    # default to using html + url (we need url for favicon parsing)
    if html is not None and url is not None:
      soup = BeautifulSoup(html)

    # or use the url
    elif url is not None: 
      page = requests.get(url)
      
      if page.status_code == 200: 
        soup = BeautifulSoup(page.text)
      
      else:
        return "URL returned status %s" % page.status_code
    
    else:
      return "No url or html provided"

    #get title
    if soup.title.string:
      data["title"] = soup.title.string

    #get favicon
    parsed_uri = urlparse( url )
    if soup.find("link", rel="shortcut icon"):
      icon_rel = soup.find("link", rel="shortcut icon")["href"]
      icon_abs = urljoin( url, icon_rel )
      data["favicon"] = icon_abs
    else:
      domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
      data["favicon"] = domain + 'favicon.ico'

    #get description
    if soup.find('meta', attrs={'name':'description'}):
      data["description"] = soup.find('meta', attrs={'name':'description'})["content"]

    #get facebook open graph data
    if soup.findAll('meta', {"property":re.compile("^og")}):
      for tag in soup.findAll('meta', {"property":re.compile("^og")}):
        tag_type = tag['property']
        data["facebook"][tag_type] = tag['content']
        if tag_type == "og:description" and data["description"] is None:
          data["description"] = tag["content"]

    #get twitter card data
    if soup.findAll('meta', attrs={'name':re.compile("^twitter")}):
      for tag in soup.findAll('meta', attrs={'name':re.compile("^twitter")}):
        tag_type = tag['name']
        if 'content' in tag.attrs:
          data["twitter"][tag_type] = tag['content']
          if tag_type == "twitter:description" and data["description"] is None:
            data["description"] = tag["content"]

  except HTMLParseError:
    return "Error parsing page data"

  except:
    return "Oops, something went wrong"

  return data


#just get the title
def get_title(url, html):
  data = {}
  data["title"] = ""

  try:
    # default to using html
    if html is not None:
      soup = BeautifulSoup(html)

    # or use the url
    elif url is not None: 
      page = requests.get(url)
      
      if page.status_code == 200: 
        soup = BeautifulSoup(page.text)
      
      else:
        return "URL returned status %s" % page.status_code
    
    else:
      return "No url or html provided"
        
    #get title
    if soup.title.string:
      data["title"] = soup.title.string

    #return error if status code is anything but 200

  except HTMLParseError:
    return "Error parsing page data"

  except:
    return "Oops, something went wrong"

  return data



