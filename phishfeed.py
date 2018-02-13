import sys
import csv
import urllib2
import argparse

url_feed = "http://www.openphish.com/feed.txt"
headers = { 'User-Agent' : 'Mozilla/5.0' }

def get_phishes(url_feed, headers, keyword):
    """ Retreive the phishing sites """
    urls = []
    hits = []
    url_links = []
    
    req = urllib2.Request(url_feed, None, headers)
    feed = urllib2.urlopen(req)
    data = feed.readlines()
    for url in data:
        urls.append(url)
    for url in urls:
        if keyword == None:
            hits.append(url.strip())
        else:
            for word in keyword:
                if word in url.lower():
                    hits.append(url.strip())
                else:
                    pass
    # Dedup the results then append to url_links list.
    for links in list(set(hits)):
        urls1 = links.replace("http://", "hxxp://");
        urls2 = urls1.replace(".", "[.]")
        url_links.append(urls2)

    return url_links

def outputResults(urls):
    urlwriter = csv.writer(sys.stdout)
    urlwriter.writerow(['URL'])
    for url in urls:
        urlwriter.writerow([url])

def main():
    """ Main function """
    parser = argparse.ArgumentParser(description='Look up keywords against OpenFish Phishing feed.')
    parser.add_argument('-key', '--keywords', type=str, nargs="+",
                        help='List your keywords - one or many.')
    args = parser.parse_args()
    if args.keywords:
        keyword = args.keywords
    else:
        keyword = None
    
    urls = get_phishes(url_feed, headers, keyword)
    outputResults(urls)
if __name__ == "__main__":
    main()
