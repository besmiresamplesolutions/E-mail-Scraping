# E-mail-Scraping

Python 3.x

Modules used:
  - urllib.request
  - re
  - codecs
  - pandas
  - requests
  - time
  - socket
  - lxml.html

Functions created:
  - verify_urls(file)
  - internal_links()
  - remove_duplicates(list)
  - scrape_emails()
  
Exceptions of possible error:
  - IOError
  - urllib.error.URLError
  - requests.exception.SSLError
  - requests.exceptions.ConnectionError

1) Verifying URLs at first, creating a list of only working URLs and redirect URLs (the last redirected URL)
2) Checking for internal links and getting top 50 links per URL
3) Scraping e-mails from links using RegEx excluding images, videos, gifs with the same syntax as e-mails
4) Saving scraped e-mails only, in a list
5) Removing duplicates and saving the final result in a .csv file 
