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
import regex as re
import sys, csv
import argparse

ssh_time = re.compile("([0-9]{4}\-[0-9]{1,2}\-[0-9]{1,2}T[0-9]{1,2}\:[0-9]{1,2}\:[0-9]{1,2}Z)")
vsphere_time = re.compile("([0-9]{4}\-[0-9]{1,2}\-[0-9]{1,2}T[0-9]{1,2}\:[0-9]{1,2}\:[0-9]{1,2}\.[0-9]{3}Z)")
failed_ssh = re.compile("Failed\snone\sfor\sinvalid\suser\s(.*)\sfrom\s(.*)\sport\s(\d+)\s(.*)")
success_ssh = re.compile("Accepted\skeyboard\-interactive\/pam\sfor\s(.*)\sfrom\s(.*)\sport\s(\d+)\s(.*)")
closed_ssh = re.compile("Connection\sclosed\sby\s(.*)")
opened_ssh = re.compile("Connection\sfrom\s(.*)\sport\s(\d+)")
failed_vsphere = re.compile("Cannot\slogin\s(.*)@(.*)")
success_vsphere = re.compile("User\s(.*)@(.*)\slogged\sin\sas")
logout_vsphere = re.compile("User\s(.*)@(.*)\slogged\sout")

def vSphereClient(hostdlog):
    vSphere_logins = []
    vSphereloginDict = {}    
    with open(hostdlog) as f:
        for line in f:
            if failed_vsphere.search(line.strip()):
                failed = vsphere_time.findall(line.strip()), failed_vsphere.findall(line.strip())
                failed_cleaned = failed[0][0], failed[1][0][0], failed[1][0][1], "None", "VSphere", "Failed"
                vSphere_logins.append(failed_cleaned)
            elif success_vsphere.search(line.strip()):
                success = vsphere_time.findall(line.strip()), success_vsphere.findall(line.strip())
                success_cleaned = success[0][0], success[1][0][0], success[1][0][1], "None", "VSphere", "Success"
                vSphere_logins.append(success_cleaned)
            elif logout_vsphere.search(line.strip()):
                logout = vsphere_time.findall(line.strip()), logout_vsphere.findall(line.strip())
                logout_cleaned = logout[0][0], logout[1][0][0], logout[1][0][1], "None", "VSphere", "Logout"
                vSphere_logins.append(logout_cleaned)            
            else:
                pass
      
    return vSphere_logins
                
def sshLogin(authlog):
    ssh_logins = []
    sshLoginDict = {}
    with open(authlog) as f: 
        for line in f:
            if success_ssh.search(line.strip()):
                success = ssh_time.findall(line.strip()), success_ssh.findall(line.strip())
                success_cleaned = success[0][0], success[1][0][0], success[1][0][1], success[1][0][2], success[1][0][3], "Successful"
                ssh_logins.append(success_cleaned)
            elif failed_ssh.search(line.strip()):
                failed = ssh_time.findall(line.strip()), failed_ssh.findall(line.strip())
                failed_cleaned = failed[0][0], failed[1][0][0], failed[1][0][1], failed[1][0][2], failed[1][0][3], "Failed"
                ssh_logins.append(failed_cleaned)
            elif closed_ssh.search(line.strip()):
                closed = ssh_time.findall(line.strip()), closed_ssh.findall(line.strip())
                clean_closed = closed[0][0], "None", closed[1][0], "None", "None", "Closed"
                ssh_logins.append(clean_closed)
            elif opened_ssh.search(line.strip()):
                opened = ssh_time.findall(line.strip()), opened_ssh.findall(line.strip())
                clean_opened = opened[0][0], "None", opened[1][0][0], opened[1][0][1], "None", "Opened"
                ssh_logins.append(clean_opened)
            else:
                pass

    return ssh_logins

def output(ssh_login_details, vsphere_login_details):
    owriter = csv.writer(sys.stdout)
    owriter.writerow(["Time", "Username", "IP Address", "Port", "Method", "Description"])
    master = zip(ssh_login_details, vsphere_login_details)
    for entries in master:
        for items in entries:
            owriter.writerow([items[0], items[1], items[2], items[3], items[4], items[5]])

def main():
    parser = argparse.ArgumentParser(description='Parse ESXi login details from auth.log and hostd.log logs.')
    parser.add_argument('-auth', '--authlog', help='Path to the auth.log file you want to parse.')
    parser.add_argument('-hd', '--hostdlog', help='Path to the hostd.log file you want to parse.')

    args = parser.parse_args()

    if args.authlog:
        authlog = args.authlog
    else:
        print "You need to specify a auth.log file."
        exit(0)    
    if args.hostdlog:
        hostdlog = args.hostdlog
    else:
        print "You need to specify a hostd.log file."
        exit(0)
    
    ssh_login_details = sshLogin(authlog)
    vsphere_login_details = vSphereClient(hostdlog)   
    output(ssh_login_details, vsphere_login_details)
    
if __name__ == "__main__":
    main()
