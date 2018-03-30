from bs4 import BeautifulSoup
import requests
from email_scraper import scrape_emails
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
import re, codecs, pandas as pd

filename = ('scraped_emails.csv')

f = open(filename, 'a')
f.seek(0)
f.truncate()

# a queue of urls to be crawled
# new_urls = deque(['https://www.sample.solutions/contact-us/','https://folkdays.com/pages/contact-us'])
# print(new_urls)

# a set of urls that we have already crawled
processed_urls = ['https://www.sample.solutions/contact-us/','https://folkdays.com/pages/contact-us']
print(processed_urls)

# a set of crawled emails
# emails = set()
emails = []

# process urls one by one until we exhaust the queue
# while len(new_urls):
for url in processed_urls:

    # move next url from the queue to the set of processed urls
    # url = new_urls.append()
    # processed_urls.append(url)
    # url = "https://folkdays.com/contact/"
    # extract base url to resolve relative links
    parts = urlsplit(url)
    # print("parts: ", parts)
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    # print("base_url: ", base_url)
    path = url[:url.rfind('/')+1] if '/' in parts.path else url
    # print("path: ", path)
    # get url's content
    # print("Processing %s" % url)
    try:
        response = requests.get(url)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        # ignore pages with errors
        # continue
        print("exception")

    # extract all email addresses and add them into the resulting set
    # new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
    new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
    # new_emails = scrape_emails(response.text)
    emails.append(new_emails)
    # print(emails)

    # create a beutiful soup for the html document
    soup = BeautifulSoup(response.text, 'html.parser')

    # find and process all the anchors in the document
    for anchor in soup.find_all('a[href^=mailto:]'):
        # extract link url from the anchor
        link = anchor.attrs["href"] if "href" in anchor.attrs else ''
        # resolve relative links
        if link.startswith('/'):
            link = base_url + link
        elif not link.startswith('http'):
            link = path + link
        # add the new url to the queue if it was not enqueued nor processed yet
        # if not link in new_urls and not link in processed_urls:
        if not link in processed_urls:
            processed_urls.append(link)

raw_data = {'urls': processed_urls,
            'emails': emails}

df = pd.DataFrame(raw_data, columns = ['urls','emails'])
# Trying to add duplicates
# df.drop_duplicates(subset=['site_name','html_title'], keep = False)
df.to_csv(f)
print(emails)