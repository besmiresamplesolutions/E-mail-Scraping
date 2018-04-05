import urllib.request 
import re
import codecs
import pandas as pd
from fake_useragent import UserAgent
import requests
import requests_cache
from bs4 import BeautifulSoup
from time import sleep
import socket
import lxml.html


working_urls = []
urls_to_scrape = []
scraped_emails = []


fileurls = codecs.open('urls-to-scrape.csv', 'r', 'latin-1')
filename = "scraped-emails.csv"

try:
	f = open(filename, "a")
	f.seek(0)
	f.truncate()
except IOError:
	print("Close the .csv file in order for changes to append and re-execute")

# ua = UserAgent()
# header = {'user-agent':ua.chrome}


# The function to verify URLs
def verify_urls(file):

	# sleep(50)
	linelist = file.readlines()
	for url in linelist:
		url = url.strip('\r\n')
		try:
			socket.setdefaulttimeout(8000)

			# requests_cache.install_cache('demo_cache')
			req = requests.get("http://" + url)
			r = req.status_code
			request = str(r)

			if(request[0] == '2'):
				working_url = req.url
				working_urls.append(working_url)
			else:
				continue

		except urllib.error.URLError as e:
			# print(e.reason)
			continue

		except requests.exceptions.SSLError as q:
			continue

		except requests.exceptions.ConnectionError:
			continue		


# The function to find top 50 internal links of a URL
def internal_links():
	for url in working_urls:
		fi = urllib.request.urlopen(url)
		s = fi.read().decode('utf-8')

		nlines = 0
		dom = lxml.html.fromstring(s)
		for link in dom.xpath('//a/@href'):
			# print(link)
			nlines += 1
			# working_urls.append(link)
			if nlines >= 50:
				break
			urls_to_scrape.append(link)


# The function to remove duplicates on a list
def remove_duplicates(list):

	output = []
	seen = set()
	for element in list:
		if element not in seen:
			output.append(element)
			seen.add(element)
	return output


# The function to scrape emails
def scrape_emails():

	# sleep(30)
	for url in urls_to_scrape:
		if(len(url)==0):
				continue
		try:
			fi = urllib.request.urlopen(url)
			s = fi.read().decode('utf-8')

			emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", s)
			for email in emails:
				if(email[-3:] == 'gif' or email[-3:] == 'png' or email[-3:] == 'jpg' or email[-3:] == 'tif' or email[-3:] == 'svg'):
					continue
				else:
					# print(email)
					scraped_emails.append(email)

		except urllib.error.URLError:
			# The reason for this error. It can be a message string or another exception instance.
			continue

		except requests.exceptions.ConnectionError:
			# print("Connection Refused")
			continue

		except:
			continue


# Calling functions
verify_urls(fileurls)
internal_links()
scrape_emails()

# re_dup = remove_duplicates(scraped_emails)
# print(re_dup)
# emails_list.append(re_dup)

# Creating dataframe and saving the result
raw_data = {'Scraped e-mails': scraped_emails}
df = pd.DataFrame(raw_data, columns=['Scraped e-mails'])
df = df.drop_duplicates('Scraped e-mails')
# print(df.duplicated())
df.to_csv(f, index = False)


f.close()