#!/usr/bin/python

#Fun little project to notify me when people I don't like get out of jail

import mechanize,urllib2,re,getpass,smtplib,os
from BeautifulSoup import BeautifulSoup as BS

tmpfile = "/tmp/tstatus.tmp"

if os.path.exists(tmpfile):
    print "Notifcations already sent, exiting..."
    exit()

def checkAssholeStatus():
    #Pull form data for inmates
    br = mechanize.Browser()
    br.open("https://public.co.travis.tx.us/tictoc/default.aspx")
    br.select_form(name="form1")

    #Warrant Number GOES HERE
    br["SearchInput"]=""

    response = br.submit()
    soup = BS(response)

    #html table data was written by what appears to be a three year old, this seems to find it every time
    table = soup.find('table', padding=3, border=1)
    th = table.find('th', text='In Custody')
    td = th.findNext('td').text
    return td

def mailStatus( to , status):
    #showing spam in gmail, but working for cell numbers for now. something effed up with headers
    sender = 'root <root@nickatnite.nicklozo.com>'
    receivers = to
    message = """Subject: Status for Inmate has changed to %s
User-Agent: Heirloom mailx 12.4 7/29/08
MIME-Version: 1.0
Content-Type: text/plain; charset=us-ascii
Content-Transfer-Encoding: 7bit
From: root <root@nickatnite.nicklozo.com>
The \"In Custody\" status for Inmate is now: %s
""" % (status, status)

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj = smtpObj.sendmail(sender, receivers, message)
        print "Successfully sent email"
    except smtplib.SMTPException:
        print "Error: Unable to send email"

#shall we begin
status=checkAssholeStatus()

if "True" in status:
    print "True"
else:
    print "Inmate status has changed to %s !" % status
    mailStatus('myphonenumber@messaging.sprintpcs.com', status)
    open("/tmp/tstatus.tmp","w").close()    



