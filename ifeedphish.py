'''
The MIT License (MIT)

Copyright (c) 2014 Patrick Olsen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Author: Patrick Olsen
Email: patrick.olsen@sysforensics.org
Twitter: @patrickrolsen
'''
from BeautifulSoup import BeautifulSoup
import urllib2

url = "http://www.openphish.com/index.php"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page)

phish_table = soup.find('table', {'class': "pure-table pure-table-striped"})
phish_tr = phish_table.findAll('tr')
print "Phishing Site,Company,Time"
for tr in phish_tr:
    cols = tr.findAll('td')
    if len(cols) != 3:
        pass
    else: 
        urls = cols[0].find('a').get('href')
        for td in cols[1]:
            company = td
        for td in cols[2]:
            time = td
        print '%s,%s,%s UTC' % (urls.strip(), company.strip(), time.strip())
