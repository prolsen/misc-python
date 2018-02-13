Misc.
=======

Misc Python scripts that I didn't want to create new repos for. It will be more of a general collection of random stuff.

Hostdetails
===============

                	hostdetails.py -sys SYSTEM -soft SOFTWARE

				<hostname>
				Microsoft Windows XP Service Pack 3 5.1 2600 x86
				Malay Peninsula Standard Time
				<domain>
				Thu Aug 26 08:32:11 2010 (UTC)
				NTFS Last Access Turned On

I found myself grabbing this information over-and-over so I decided to automate it. You can also use the sysinfo plugin within autoreg-parse to get the same information. https://github.com/sysforensics/autoreg-parse

Todo:

- [ ] Add some network information (IPs, etc.)
- [ ] Last shutdown time

Phishfeed
===============

Goes out to: openphish[.]com/feed[.]txt and parses the output given keywords then simply returns them.

You can specify multiple keywords. phishfeed.py -key one two three four etc

Example: Using a Keyword, "login" you would get the following. You can edit the keywords in the script itself.

Help:

				phishfeed.py -h
				
				usage: phishfeed.py [-h] [-key KEYWORDS [KEYWORDS ...]]
				
				Look up keywords against OpenFish Phishing feed.
				
				optional arguments:
				  -h, --help            show this help message and exit
				  -key KEYWORDS [KEYWORDS ...], --keywords KEYWORDS [KEYWORDS ...]
				                        List your keywords - one or many.
				                        
Output:

				phishfeed.py -key bank
		
				URL
				hxxp://sicherheitsverifikation-post-bank[.]cc/kundenservice/sicherheitscenter/legimitation
				hxxp://niyod[.]com/verify/bankofamerica[.]com/bankofamerica[.]com/29954b27b667de369126
				hxxp://www[.]buyrentimmo[.]com/bankofamerica[.]com/update/index[.]php
				hxxp://www[.]msbmielec[.]home[.]pl/multimedia/mmaudio/cwicz_03/standardbankc3/
				<snip>


ESXi auth.log and hostd.log Parser - esxi_logins.py
====================================================

I'm still running some tests and looking for more sources of information within the logs.

Help:

				python esxi_logins.py -h
				
				usage: esxi_logins.py [-h] [-auth AUTHLOG] [-hd HOSTDLOG]
				
				Parse ESXi login details from auth.log and hostd.log logs.
				
				optional arguments:
				  -h, --help            show this help message and exit
				  -auth AUTHLOG, --authlog AUTHLOG
				                        Path to the auth.log file you want to parse.
				  -hd HOSTDLOG, --hostdlog HOSTDLOG
				                        Path to the hostd.log file you want to parse.
			                        
Output:

				python esxi_logins.py -auth log/auth.log -hd log/hostd.log
				
				Time,Username,IP Address,Port,Method,Description
				2014-05-08T20:36:03Z,None,192.168.123.2,49720,None,Opened
				2014-10-30T20:12:48.456Z,root,10.38.10.78,None,VSphere,Success
				2014-05-08T20:36:03Z,None,192.168.123.2,None,None,Closed
				2014-10-30T20:19:15.677Z,root,10.38.10.85,None,VSphere,Success
				2014-05-08T20:36:05Z,None,192.168.123.2,49721,None,Opened
				2014-10-30T20:19:44.338Z,root,10.38.10.85,None,VSphere,Logout
				2014-05-08T20:36:05Z,root,192.168.123.2,49721,ssh2,Successful
				<snip>
