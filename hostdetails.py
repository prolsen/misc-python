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
'''

from Registry import Registry
import sys, os, time, argparse

def getComputerName(reg_sys):
    current = getControlSet(reg_sys)
    computerName = reg_sys.open("%s\\Control\\ComputerName\\ComputerName" % (current))
    comp_name = computerName.value("ComputerName").value()
    return comp_name

def getLastAccess(reg_sys):
    current = getControlSet(reg_sys)
    last_access = reg_sys.open("%s\\Control\\FileSystem" % (current))
    try:
	laccess = last_access.value("NtfsDisableLastAccessUpdate").value()
    except:
	laccess = "None"
    if laccess == 1:
        return "NTFS Last Access Turned Off"
    else:
        return "NTFS Last Access Turned On"
     
def getProcArch(reg_sys):
    try:
        current = getControlSet(reg_sys)
        arch = reg_sys.open("%s\\Control\\Session Manager\\Environment" % (current))
        proc_arch = arch.value("PROCESSOR_ARCHITECTURE").value()
        return proc_arch
    
    except Registry.RegistryKeyNotFoundException as e:
        pass

def getControlSet(reg_sys):
    try:
        select = reg_sys.open("Select")
        current = select.value("Current").value()
        controlsetnum = "ControlSet00%d" % (current)
        return controlsetnum
    except Registry.RegistryKeyNotFoundException as e:
        pass

def getDomain(reg_sys):
    try:
        current = getControlSet(reg_sys)
        tcip_params = reg_sys.open(current + "\\services\\Tcpip\\Parameters")
        domain = tcip_params.value("Domain").value()
        return domain
    except Registry.RegistryKeyNotFoundException as e:
        pass

def getTimeZone(reg_sys, sysinfo):
    current = getControlSet(reg_sys)
    key = reg_sys.open(current + "\\Control\\TimeZoneInformation")
    if sysinfo[1] == "5.1":
        return key.value("StandardName").value()
    elif sysinfo[1] != "5.1":
        return key.value("TimeZoneKeyName").value()

def getCurrentVerionInfo(reg_sys, reg_soft):
    key = reg_soft.open("Microsoft\\Windows NT\\CurrentVersion")
    product_name = key.value("ProductName").value()
    current_version = key.value("CurrentVersion").value()
    current_build = key.value("CurrentBuildNumber").value()
    try:
        csd_version = key.value("CSDVersion").value()
    except Registry.RegistryValueNotFoundException:
        csd_version = 'Not Present'
    install_date = time.strftime('%a %b %d %H:%M:%S %Y (UTC)', \
                                 time.gmtime(key.value("InstallDate").value()))

    return product_name, current_version, current_build, csd_version, str(install_date)

def output(sysinfo, timezone, domain, arch, lastaccess, compname):
    print(compname)
    print(sysinfo[0], sysinfo[3], sysinfo[1], sysinfo[2], arch)
    print(timezone)
    print(domain)
    print(sysinfo[4])
    print(lastaccess)

def main():
    parser = argparse.ArgumentParser(description='Parse some host details from SYSTEM and SOFTWARE hives.')
    parser.add_argument('-sys', '--system', help='Path to the SYSTEM hive you want parsed.')
    parser.add_argument('-soft', '--software', help='Path to the SOFTWARE hive you want parsed.')
    args = parser.parse_args()

    if args.software:
        reg_soft = Registry.Registry(args.software)
    else:
        exit(0)
    if args.system:
        reg_sys = Registry.Registry(args.system)
    else:
        exit(0)

    sysinfo = getCurrentVerionInfo(reg_sys, reg_soft)
    timezone = getTimeZone(reg_sys, sysinfo)
    domain = getDomain(reg_sys)
    arch = getProcArch(reg_sys)
    lastaccess = getLastAccess(reg_sys)
    compname = getComputerName(reg_sys)
    
    output(sysinfo, timezone, domain, arch, lastaccess, compname)

if __name__ == "__main__":
    main() 
