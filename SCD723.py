"""
[Change list/history]

2015/5/12[Ver2.3.2]
1. [SST][ScriptEnableAccounts]Add try/except to judge error/exception via error code.

2015/4/28[Ver2.3.1]
1. [SST][ScriptEnableAccounts]Add Share.WebOutput.Value("SSTLoginAccounts",Result["IQT_Result"],Result["FC"],Result["Output"]) from Share.py

2015/4/23[Ver2.3]
1. [SST][ScriptEnableAccounts]Make sure SST/ScriptEnableAccounts return value is workable by Result = dict (IQT_Result='Pass',FC='',Output='')

2015/3/4[Ver2.2]
1. rename as SCD723.py
2. [Flashman]support HIMA download mode related command
3. [Flashman]S-ON mode change to S-DEB for RSA key check disable and unblock downgrade to base ROM.

2014/12/9[Ver2.1]
1. Beta version first release.

"""

# -*- coding: utf-8 -*-
import os, datetime, time, ats, atsbase, sys, getopt, os.path, inspect, traceback, subprocess, fnmatch, smtplib, shutil, csv, traceback
import system as s
import user as u
from datetime import datetime
from time import sleep, gmtime, strftime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
title= '[IQT][SCD723][Sean_Yang][' + s.DEVICE_ID + ']'
easyinstallResultPillow = subprocess.getoutput("C:\Python34\Scripts\easy_install.exe Pillow")
easyinstallResultjson = subprocess.getoutput("C:\Python34\Scripts\easy_install.exe json")
easyinstallResultrequests = subprocess.getoutput("C:\Python34\Scripts\easy_install.exe requests")
print(title + "[easy_install][Pillow] " + str(easyinstallResultPillow))
print(title + "[easy_install][json] " + str(easyinstallResultjson))
print(title + "[easy_install][requests] " + str(easyinstallResultrequests))
import Share
from PIL import Image
from PIL import ImageGrab

class SST():
    def ScriptEnableAccounts():
        """
        [Function]
        Set ScriptEnableAccounts depend on user input SRGSR
        
        [Author]
        Sean_Yang
        
        [Version]
        2.3.2
        
        [Modify Date]
        2015/5/12
        
        [User Input(User.py)]
        SRGSR = 'SR'
        SSTLoginAccounts = 'Gmail,Exchange,POPMail,IMAP,Facebook,Twitter,Dropbox'
        
        [input]
        None
        
        [output]
        Result = dict (IQT_Result='Pass',FC='',Output='')
            
        [Example]
        >>> import SCD723
        >>> Result = SCD723.SST.ScriptEnableAccounts()
        >>> print("[IQT][SCD723][Sean_Yang] " + Result["IQT_Result"] + " , " + Result["FC"] + " , " + Result["Output"])
        
        [Note]
        None
        
        """
        
        Result = dict (IQT_Result='Pass',FC='',Output='')
        try:
            if u.SSTLoginAccounts is '':
                raise ValueError('User has no filled in "SSTLoginAccounts"')
            
            if hasattr(u, 'SRGSR'):
                if u.SRGSR == "SR":
                    print(title + "[ScriptEnableAccounts] Set SR related prop/value.")
                
                    allaccount = u.SSTLoginAccounts.split(',')
                    print(title + "[ScriptEnableAccounts] allaccount split by , = " + str(allaccount))
                    account1 = ''
                    for a in allaccount:
                        if a != -1:
                            account1 = account1 + a + '\n'
                            print(title + "[ScriptEnableAccounts] SSTLoginAccounts = " + account1)
                    print(title + "[ScriptEnableAccounts] SSTLoginAccounts = " + account1)
                
                    ats.RunDeviceCommand("shell mkdir /data/at")
                    ats.RunDeviceCommand("shell mkdir /data/at/script")
                    ats.RunDeviceCommand("shell mkdir /data/at/script/extra")
                    ats.RunDeviceCommand("shell \"echo '" + account1 + "' > /data/at/script/extra/SST_EnabledAccounts.txt\"")
                    ats.RunDeviceCommand("shell chmod 777 /data/at")
                    time.sleep(30)
                elif u.SRGSR == "GSR":
                    print(title + "[ScriptEnableAccounts] Set GSR related prop/value.")
                    ats.RunDeviceCommand("shell \"echo 'Enable_Login=" + u.SSTLoginAccounts + "' >> /mnt/sdcard/UserInput.txt\"")
                    time.sleep(30)
                elif u.SRGSR == "SR2.0":
                    print(title + "[ScriptEnableAccounts] Set SR2.0 related prop/value.")
                    ats.RunDeviceCommand("shell \"echo 'Enable_Login=" + u.SSTLoginAccounts + "' >> /mnt/sdcard/UserInput.txt\"")
                    time.sleep(30)
                else:
                    print(title + "[ScriptEnableAccounts] Set SR2.0 related prop/value by default.")
                    ats.RunDeviceCommand("shell \"echo 'Enable_Login=" + u.SSTLoginAccounts + "' >> /mnt/sdcard/UserInput.txt\"")
                    time.sleep(30)
            else:
                print(title + "[ScriptEnableAccounts] Set SR2.0 related prop/value by default.")
                ats.RunDeviceCommand("shell \"echo 'Enable_Login=" + u.SSTLoginAccounts + "' >> /mnt/sdcard/UserInput.txt\"")
                time.sleep(30)
                    
            print(title + "[ScriptEnableAccounts] Start to check pass/fail and return result.")
        
            if u.SRGSR == "SR":
                print(title + "[ScriptEnableAccounts] allaccount = " + str(allaccount))
                r = ats.RunDeviceCommandA("shell cat /data/at/script/extra/SST_EnabledAccounts.txt")
                r2 = r["outputstring"]
                #account2 = r2["StandardOutput"].lstrip('\r\n\r\n').rstrip('\r\n\r\n').split('\r\n\r\n')
                account2 = list(filter(None, r2["StandardOutput"].split('\r\n')))
                print(title + "[ScriptEnableAccounts] account2 = " + str(account2))
                if allaccount == account2 :
                    Result=dict(IQT_Result='Pass',FC='',Output='')
                else:
                    raise LookupError('Enable accounts is not matching user input, cat value is:'+str(r2))
                    #Result=dict(IQT_Result='Fail',FC='FC#0010',Output='Enable accounts is not matching user input, cat value is:'+str(r2))
            else:
                r = ats.RunDeviceCommandA("shell cat /mnt/sdcard/UserInput.txt")
                r2 = r["outputstring"]
                rc = r2["StandardOutput"].find("Enable_Login=" + u.SSTLoginAccounts)
                if rc is not -1 :
                    Result=dict(IQT_Result='Pass',FC='',Output='')
                else:
                    raise LookupError('Enable accounts is not matching user input, cat value is:'+str(r2))
                    #Result=dict(IQT_Result='Fail',FC='FC#0010',Output='Enable accounts is not matching user input, cat value is:'+str(r2))
            print(title + "[ScriptEnableAccounts] The return value is " + Result["IQT_Result"])
        
        except ValueError as v:
            print(title + "[ScriptEnableAccounts][ERROR] " + str(v.args))
            Result=dict(IQT_Result='Fail',FC='#0001',Output=v.args[0])
            Share.WebOutput.Value("SSTLoginAccounts",Result["IQT_Result"],Result["FC"],Result["Output"])
            exit(1)
        
        except LookupError as l:
            print(title + "[ScriptEnableAccounts][ERROR] " + str(l.args))
            Result=dict(IQT_Result='Fail',FC='#0010',Output=l.args[0])
            Share.WebOutput.Value("SSTLoginAccounts",Result["IQT_Result"],Result["FC"],Result["Output"])
            exit(1)
        
        except:
            print(title + "[ScriptEnableAccounts][ERROR] Python exception occurred ==> " + str(traceback.format_exc()))
            Result=dict(IQT_Result='Fail',FC='#0000',Output='Python exception error occurred.')
            Share.WebOutput.Value("SSTLoginAccounts",Result["IQT_Result"],Result["FC"],Result["Output"])
            exit(1)
            
        Share.WebOutput.Value("SSTLoginAccounts",Result["IQT_Result"],Result["FC"],Result["Output"])
        return Result
                
class Flashman():
    """
    def _FlashmanResultSummary(testrun, resultfolder):
    
        Flashman Result summary. (end round)
    
        [Input]
        int Current test round, str concurrent result directory.
        [Output]
        NA
    
    
        csvfilelist = fnmatch.filter(os.listdir(resultfolder + '\\' + str(testrun+1)), '*.csv')
    
        for i in csvfilelist[]:
            f = open(resultfolder + csvfilelist[i] , 'r')
            for row in csv.reader(f):
                if(row[2] == 'PASS'):
                    print (row)
            f.close()

    
        # Sender account info.
        gmail_user = 'iqt.aat.automailer@gmail.com'
        gmail_pwd = 'Pass2005'

        # Sender/Receiver Info
        fromaddress = "iqt.aat.automailer@gmail.com"
        toaddress = [s.OWNER+'@htc.com','sean_yang@htc.com']

        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "[IQT_Auto_mail][Flashman automation][" + s.PLATFORM + "][" + s.PROJECT + "] Result summary."
        msg['From'] = fromaddress
        msg['To'] = toaddress

        # Create the body of the message (a plain-text and an HTML version).

        html = \
        <html>
          <head></head>
          <body>
            <p>Dear all, this is Flashman automation test result summary.<br>
               Log: <a href="file:///\\SCD723_FLASHMAN\Flashman_Result">Path</a>.
            </p>
            <table border="1">
        　    <tr><td> + str(testrun+1) + run</td><td>Pass.</td></tr>
    　        <tr><td> + str(testrun+2) + run</td><td>Fail.</td></tr>
            </table>
          </body>
        </html>
    
        part = MIMEText(html, 'html')
        msg.attach(part)

        try:
            smtpObj = smtplib.SMTP("smtp.gmail.com",587)
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.ehlo()
            #Login account
            smtpObj.login(gmail_user, gmail_pwd)
            smtpObj.sendmail(fromaddress, toaddress, msg.as_string())
            smtpObj.quit()
            print(title + "[_FlashmanResultSummary][" + str(testrun+1) + " run] Already send Result summary mail to user.")
        except SMTPException:
            print(title + "[_FlashmanResultSummary][" + str(testrun+1) + " run] Fail to send Result summary mail.")
        
        #Check if User Stop/Abort the task
        if(atsbase.event.is_finish == True):
            print(title + "[_FlashmanResultSummary][" + str(testrun+1) + " run] Receive User Abort/Stop this task.")
            exit(0)
    """
    def _FlashmanLogArchive(testrun, resultfolder):
        """
        [Function]
        Flashman log archive. (each round)
        [Input]
        int Current test round, str concurrent result directory.
        [Output]
        NA
        """
        #Screen Capture to get Flashman test result
        ImageGrab.grab().save(resultfolder + '\\Flashman_automation_result_round_' + str(testrun+1) + '.jpg')
        print(title + "[_FlashmanLogArchive][" + str(testrun+1) + " run] Screen capture " + str(testrun+1) + " round result.")
    
        #Copy RUU_*log to current round result folder
        ruulog = max(fnmatch.filter(os.listdir(u.flashmanworkingdirectory + '\\log'), '*.log'))
        print (ruulog)
        shutil.copy(u.flashmanworkingdirectory + '\\log\\' + ruulog, resultfolder)
        print(title + "[_FlashmanLogArchive][" + str(testrun+1) + " run] Copy " + str(testrun+1) + " round RUU_*.log to " + str(testrun+1) + " round result directory.")
    
        #Check if User Stop/Abort the task
        if(atsbase.event.is_finish == True):
            print(title + "[_FlashmanLogArchive][" + str(testrun+1) + " run] Receive User Abort/Stop this task.")
            exit(0)
    
    def _FlashmanSendErrorNotifyMail(testrun, flashmandevicecount):
        """
        [Function]
        Send an error mail or summarize flashman log files to user.
        [Input]
        int Current test round, int Flashman device count.
        [Output]
        NA
        """
        #Sender account info.
        gmail_user = 'iqt.aat.automailer@gmail.com'
        gmail_pwd = 'Pass2005'
    
        #Sender/Receiver info
        fromaddress = "iqt.aat.automailer@gmail.com"
        toaddress = [s.OWNER+'@htc.com','sean_yang@htc.com']
    
        #Mail Subject 
        msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n" % (fromaddress, ", ".join(toaddress), '[IQT_Auto_mail][Flashman automation][' + str(testrun+1) + ' run] Notify user should go to that PC to recover device manually.'))
    
        #Mail content
        info = ''
        info += ('\n'+'[IQT][SCD723][Sean_Yang][' + s.DEVICE_ID + '][FlashmanCheckFastbootDevice][' + str(testrun+1) + ' run] Fail, there are not ' + str(flashmandevicecount) + ' devices in fastboot mode before Flashman, user should go to that PC to check.'+'\n'+'Please help to make sure device:'+'\n'+'1. ATS debug flag is enabled.'+'\n'+'2. Security-ON.'+'\n'+'3. Under fastboot mode.')
    
        try:
            smtpserver = smtplib.SMTP("smtp.gmail.com",587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo()
            # Login account
            smtpserver.login(gmail_user, gmail_pwd)
            smtpserver.sendmail(fromaddress, toaddress, msg+info)
            smtpserver.quit()
            print(title + "[_FlashmanSendErrorNotifyMail][" + str(testrun+1) + " run] Already send Error notify mail to user.")
        except SMTPException:
            print(title + "[_FlashmanSendErrorNotifyMail][" + str(testrun+1) + " run] Fail to send Error notify mail to user.")
        
        #Check if User Stop/Abort the task
        if(atsbase.event.is_finish == True):
            print(title + "[_FlashmanSendErrorNotifyMail][" + str(testrun+1) + " run] Receive User Abort/Stop this task.")
            exit(0)
    
    def _FlashmanFileFilldone(testrun):
        """
        [Function]
        Create .txt to count how many devices Flash ROM done.
        fill SN + "done" into D:\FlashCount\FlashROMCount.txt
        [Input]
        int Current test round.
        [Output]
        NA
        """
        file=open("D:\\FlashCount\\FlashROMCount.txt","a")
        file.write(s.DEVICE_ID+" done\n")
        print(title + "[_FlashmanFileFilldone][" + str(testrun+1) + " run] Flash ROM done")
        file.close()
    
        #Check if User Stop/Abort the task
        if(atsbase.event.is_finish == True):
            print(title + "[_FlashmanFileFilldone][" + str(testrun+1) + " run] Receive User Abort/Stop this task.")
            exit(0)

    def _FlashmanFileSyncAlldeviceProgress(testrun):
        """
        [Function]
        Create .txt to count and sync all device progress.
        [Input]
        int Current test round.
        [Output]
        NA
        """
        FlashROMCount=0
        while (FlashROMCount != u.flashmandevicecount):
            file=open("D:\\FlashCount\\FlashROMCount.txt","r")
            readfile=file.read()
            FlashROMCount=str.count(readfile, "done")
            print(title + "[_FlashmanFileSyncAlldeviceProgress][" + str(testrun+1) + " run] FlashROMCount = " + str(FlashROMCount))
            #Check if User Stop/Abort the task
            if(atsbase.event.is_finish == True):
                print(title + "[_FlashmanFileSyncAlldeviceProgress][" + str(testrun+1) + " run] Receive User Abort/Stop this task.")
                exit(0)
            time.sleep(60)

    def _FlashmanLOGCountNew(testrun,logcount,resultfolder):
        """
        [Function]
        While loop to query device flash done and then it will generate new .csv
        [Input]
        int Current test round, int Original flashman log file *.csv count
        [Output]
        NA
        """
        LOGCountNew = logcount
        while (LOGCountNew != logcount+u.flashmandevicecount):
            LOGCountNew = len(fnmatch.filter(os.listdir(resultfolder), '*.csv'))
            print(title + "[_FlashmanLOGCountNew][" + str(testrun+1) + " run] Flashman is in progress, there are " + str(LOGCountNew) + " Flashman log files.")
            #Check if User Stop/Abort the task
            if(atsbase.event.is_finish == True):
                print(title + "[_FlashmanLOGCountNew][" + str(testrun+1) + " run] Receive User Abort/Stop this task.")
                exit(0)
            time.sleep(60)
        print(title + "[_FlashmanLOGCountNew][" + str(testrun+1) + " run] Flashman update ROM done, there are " + str(LOGCountNew) + " Flashman log files.")

    def FlashmanUpdateBaseROM(testrun):
        """
        [Function]
        FlashmanUpdateBaseROM
        adb in, adb out
        [Input]
        int Current test round.
        [Output]
        NA
        """
        ats.CheckDeviceStatus("-mode 15 -bugreport true")
        print(title + "[FlashmanUpdateBaseROM][" + str(testrun+1) + " run] Device is in OS mode.")
        ats.RunDeviceCommand("reboot oem-78")
        print(title + "[FlashmanUpdateBaseROM][" + str(testrun+1) + " run] adb reboot to RUU.")
        time.sleep(60)
        #os.system("fastboot -s " + s.DEVICE_ID + " flash disvercheck D:\disvercheck.txt")
        #print(title + "[FlashmanUpdateBaseROM][" + str(testrun+1) + " run] ats_debug disvercheck done.")
        time.sleep(10)
        ats.UpdateROM(boot=False,partial=False)
        print(title + "[FlashmanUpdateBaseROM][" + str(testrun+1) + " run] Device already update to base ROM.")
    
        #Check if User Stop/Abort the task
        if(atsbase.event.is_finish == True):
            print(title + "[FlashmanUpdateBaseROM][" + str(testrun+1) + " run] Receive User Abort/Stop this task.")
            exit(0)
        
    def FlashmanCheckDeviceandSkipOOBE(testrun):
        """
        [Function]
        FlashmanCheckDeviceandSkipOOBE
        adb in, adb out
        [Input]
        int Current test round.
        [Output]
        NA
        """
        ats.CheckDeviceStatus("-mode 15 -bugreport true")
        print(title + "[FlashmanCheckDeviceandSkipOOBE][" + str(testrun+1) + " run] Device is in OS mode.")
        ats.SkipOOBE()
        print(title + "[FlashmanCheckDeviceandSkipOOBE][" + str(testrun+1) + " run] ATS already execute skipOOBE.exe.")
        time.sleep(60)
        ats.CheckDeviceStatus("-mode 15 -bugreport true")
        print(title + "[FlashmanCheckDeviceandSkipOOBE][" + str(testrun+1) + " run] Device is in OS mode.")
    
        #Check if User Stop/Abort the task
        if(atsbase.event.is_finish == True):
            print(title + "[FlashmanCheckDeviceandSkipOOBE][" + str(testrun+1) + " run] Receive User Abort/Stop this task.")
            exit(0)

    def FlashmanAdbToBootloader(testrun):
        """
        [Function]
        FlashmanAdbToBootloader
        adb in, fastboot out
        [Input]
        int Current test round
        [Output]
        NA
        """
        ats.CheckDeviceStatus("-mode 15 -bugreport true")
        print(title + "[FlashmanAdbToBootloader][" + str(testrun+1) + " run] Device is in OS mode.")
        ats.RunDeviceCommand("reboot download")
        print(title + "[FlashmanAdbToBootloader][" + str(testrun+1) + " run] adb reboot to download mode.")
        time.sleep(30)
    
        #Check if User Stop/Abort the task
        if(atsbase.event.is_finish == True):
            print(title + "[FlashmanAdbToBootloader][" + str(testrun+1) + " run] Receive User Abort/Stop this task.")
            exit(0)
        
    def FlashmanWriteSecureFlag(testrun,secureflag):
        """
        [Function]
        FlashmanWriteSecureFlag
        Fastboot in, adb out
        [Input]
        int Current test round, int secureflag(S-DEB is 2 or S-OFF is 0.)
        [Output]
        NA
        """
        os.system("fastboot -s " + s.DEVICE_ID + " oem writesecureflag " + secureflag)
        print(title + "[FlashmanWriteSecureFlag][" + str(testrun+1) + " run] writesecureflag " + secureflag + ".")
        time.sleep(30)
        os.system("fastboot -s " + s.DEVICE_ID + " reboot")
        print(title + "[FlashmanWriteSecureFlag][" + str(testrun+1) + " run] fastboot reboot to OS.")
        time.sleep(120)
        ats.CheckDeviceStatus("-mode 15 -bugreport true")
        print(title + "[FlashmanWriteSecureFlag][" + str(testrun+1) + " run] Device is in OS mode.")
        
        #Check if User Stop/Abort the task
        if(atsbase.event.is_finish == True):
            print(title + "[FlashmanWriteSecureFlag][" + str(testrun+1) + " run] Receive User Abort/Stop this task.")
            exit(0)
    
    def FlashmanCheckSecureflag(testrun):
        """
        [Function]
        FlashmanCheckSecureflag
        Fastboot in, Fastboot out
        [Input]
        int Current test round.
        [Output]
        Return True = device is S-DEB
        Return False = device is S-OFF
        """
        #Check S-DEB or S-OFF
        CheckSON=subprocess.getoutput("fastboot -s " + s.DEVICE_ID + " oem readsecureflag")
        print(title + "[FlashmanCheckSecureflag][" + str(testrun+1) + " run] readsecureflag.")
        print(CheckSON)
        x = str.count(CheckSON,"S-DEB")
        print(title + "[FlashmanCheckSecureflag][" + str(testrun+1) + " run] Check output.")
        print(x)
        if (x == 1):
            print(title + "[FlashmanCheckSecureflag][" + str(testrun+1) + " run] Device is S-DEB.")
            return True
        else:
            print(title + "[FlashmanCheckSecureflag][" + str(testrun+1) + " run] Device is S-OFF.")
            return False
                
        #Check if User Stop/Abort the task
        if(atsbase.event.is_finish == True):
            print(title + "[FlashmanCheckSecureflag][" + str(testrun+1) + " run] Receive User Abort/Stop this task.")
            exit(0)
        
    def FlashmanCheckFastbootDevice(testrun):
        """
        [Function]
        FlashmanCheckFastbootDevice
        Fastboot in, Fastboot out    
        [Input]
        int Current test round.
        [Output]
        NA
        """
        #Get concurrent devices count via fastboot devices
        ConcurrentFastbootStatus = subprocess.getoutput("fastboot devices")
        print(title + "[FlashmanCheckFastbootDevice][" + str(testrun+1) + " run] Check concurrent fastboot devices.")
        print(ConcurrentFastbootStatus)
        y = str.count(ConcurrentFastbootStatus, "fastboot") #Get how many devices in fastboot mode
        print(title + "[FlashmanCheckFastbootDevice][" + str(testrun+1) + " run] Print fastboot mode count.")
        print(y)
        if (y == u.flashmandevicecount):
            print(title + "[FlashmanCheckFastbootDevice][" + str(testrun+1) + " run] Pass, Flashman is good to go.")
        else:
            print(title + "[FlashmanCheckFastbootDevice][" + str(testrun+1) + " run] Fail, there are not " + str(u.flashmandevicecount) + " devices in fastboot mode on this PC, user should go to that PC to check.")
            #Check if User Stop/Abort the task
            if(atsbase.event.is_finish == True):
                print(title + "[FlashmanCheckFastbootDevice][" + str(testrun+1) + " run] Receive User Abort/Stop this task.")
                exit(0)
            _FlashmanSendErrorNotifyMail(testrun, u.flashmandevicecount)
            time.sleep(1800)
            FlashmanCheckFastbootDevice(testrun)
    
        #Check if User Stop/Abort the task
        if(atsbase.event.is_finish == True):
            print(title + "[FlashmanCheckFastbootDevice][" + str(testrun+1) + " run] Receive User Abort/Stop this task.")
            exit(0)
    
    def Flashman_main():
        """
        [Function]
        Flashman main job, the other 15 sub jobs perform at the same time.
        
        [Author]
        Sean Yang
    
        [Version]
        2.2
    
        [Modify Date]
        2015/3/4
        
        [User Input(User.py)]
        flashmantestround = 3
        flashmandevicecount = 9
        flashmanworkingdirectory = r'D:\Flashman_Console_test_version\FlashMan_1.5.1.32'
        flashmanplatform = r'Android' 
        flashmanrompath = r'D:\ROM\FullROM.zip'
        flashmanpartialrompath = r'D:\ROM\PartialROM.zip'
        flashmanlogoutput = r'D:\Flashman_Result'
    
        [intput]
        None
    
        [output]
        None
    
        #Example
        >>> import SCD723
        >>> SCD723.Flashman.Flashman_main()
        >>> SCD723.Flashman.Flashman_sub()
        
        [Note]
        None
        
        """
        #Set Job retry count = 3
        ats.SetJobRetryCount(3)
    
        #Define autoit and create a new file D:\FlashCount\FlashROMCount.txt to count
        #autoit = win32com.client.Dispatch("AutoItX3.Control")
        file = open("D:\\FlashCount\\FlashROMCount.txt","w")
        file.close()
    
        #Create Flashman log directory.
        resultfolder = u.flashmanlogoutput
        if(os.path.exists(resultfolder) == False):
            os.mkdir(resultfolder)
            print(title + "[FlashmanPreInitial] Create " + resultfolder + ".")
    
        resultfolder = u.flashmanlogoutput + '\\' + s.PROJECT
        if(os.path.exists(resultfolder) == False):
            os.mkdir(resultfolder)
            print(title + "[FlashmanPreInitial] Create " + resultfolder + ".")
        
        resultfolder = u.flashmanlogoutput + '\\' + s.PROJECT + '\\' + str(s.TASK_ID)
        if(os.path.exists(resultfolder) == False):
            os.mkdir(resultfolder)
            print(title + "[FlashmanPreInitial] Create " + resultfolder + ".")
            
        for i in range (0,u.flashmantestround,1):
            
            #Create D:\Flashman_Result\Project\Task ID\i+1 for result query
            resultfolder = u.flashmanlogoutput + '\\' + s.PROJECT + '\\' + str(s.TASK_ID) + '\\' + str(i+1)
            print(title + "[FlashmanInitial][" + str(i+1) + " run] Create " + resultfolder + ".")
            os.mkdir(resultfolder)
            print(title + "[FlashmanInitial][" + str(i+1) + " run] Create " + str(i+1) + " round's result directory.")
        
            #Update to base ROM
            FlashmanUpdateBaseROM(i)
            time.sleep(210)
        
            #Check device status and skipOOBE, adb in, adb out
            FlashmanCheckDeviceandSkipOOBE(i)
        
            #Prepare to S-ON, adb to bootloader, adb in, fastboot out   
            FlashmanAdbToBootloader(i)
            time.sleep(30)
        
            #Make sure device is S-DEB, fastboot in, fastboot out
            if(FlashmanCheckSecureflag(i) == False):
                #Write secureflag, fastboot in, adb out
                FlashmanWriteSecureFlag(i,r'2')
                #Make sure device enter to fastboot, adb in, fastboot out
                FlashmanAdbToBootloader(i)
            else:
                time.sleep(10)
                
            #[File]fill SN + "done" into D:\FlashCount\FlashROMCount.txt
            _FlashmanFileFilldone(i)
        
            #[File]Sync all device progress
            _FlashmanFileSyncAlldeviceProgress(i)
                
            #[Main job]Make sure there are all devices in Fastboot mode.
            FlashmanCheckFastbootDevice(i)
        
            #[Main job]Wipe and create a new FlashROMcount.txt
            file=open("D:\\FlashCount\\FlashROMCount.txt","w")
            file.close()
        
            #Count concurrent how many *.csv in Flashman log folder
            FlashmanLOGCount = len(fnmatch.filter(os.listdir(resultfolder), '*.csv'))
            print(title + "[FlashmanPrepareToGo][" + str(i+1) + " run] Before Flashman process, there are " + str(FlashmanLOGCount) + " Flashman log files.")
        
            #[Main job]Close Flashman.exe
            os.system("taskkill /im Flashman.exe /f")
            print(title + "[FlashmanPrepareToGo][" + str(i+1) + " run] Close Flashman.exe and to do next action console command.")
       
            #[Main job]Change working directory to Flashman.exe path what user define
            os.chdir(u.flashmanworkingdirectory)
            os.getcwd()
        
            #[Main job]Flashman.exe console command execute
            flashmanprocess = subprocess.Popen(['Flashman.exe','-os',u.flashmanplatform,'-rom',u.flashmanrompath,'-partial',u.flashmanpartialrompath,'-output',resultfolder])
            print(title + "[FlashmanConsole][" + str(i+1) + " run] Console command already execute.")
        
            #While loop to query device flash done and then it will generate new .csv
            _FlashmanLOGCountNew(i,FlashmanLOGCount,resultfolder)
        
            #[Main job]Change working directory back to default
            os.chdir("C:\\Users\\sqa_stability")
            os.getcwd()
                
            #ATC recover USB connection by using USBSCSI.exe to call device usb debugging wake up.
            time.sleep(600)
            FlashmanCheckDeviceandSkipOOBE(i)
        
            #[Main job]Come out result by mail to user.
            _FlashmanLogArchive(i, resultfolder)
        
            print(title + "[FlashmanEnd][" + str(i+1) + " run] Flashman test done.")
                
                
        ats.CheckDeviceStatus("-mode 15 -bugreport true")
        print(title + "[FlashmanEnd][" + str(i+1) + " run] Device is in OS mode.")
        print(title + "[FlashmanEnd][" + str(i+1) + " run] All Flashman test done.")

    def Flashman_sub():
        """
        [Function]
        Flashman sub job, almost the same as main, just w/o Flashman.exe related leading control
        """
        #Set Job retry count = 3
        ats.SetJobRetryCount(3)
    
        for i in range (0,u.flashmantestround,1):
    
            #D:\Flashman_Result\Project\Task ID\i+1 for result query
            resultfolder = u.flashmanlogoutput + '\\' + s.PROJECT + '\\' + str(s.TASK_ID) + '\\' + str(i+1)
            print(title + "[FlashmanInitial][" + str(i+1) + " run] Result folder = " + resultfolder + ".")
        
            #Update to base ROM
            FlashmanUpdateBaseROM(i)
            time.sleep(210)
        
            #Check device status and skipOOBE, adb in, adb out
            FlashmanCheckDeviceandSkipOOBE(i)
        
            #Prepare to S-ON, adb to bootloader, adb in, fastboot out   
            FlashmanAdbToBootloader(i)
            time.sleep(30)
        
            #Make sure device is S-DEB, fastboot in, fastboot out
            if(FlashmanCheckSecureflag(i) == False):
                #Write secureflag, fastboot in, adb out
                FlashmanWriteSecureFlag(i,r'2')
                #Make sure device enter to fastboot, adb in, fastboot out
                FlashmanAdbToBootloader(i)
            else:
                time.sleep(10)
            
            #fill SN + "done" into D:\FlashCount\FlashROMCount.txt
            _FlashmanFileFilldone(i)
            
            #Sync all device progress
            _FlashmanFileSyncAlldeviceProgress(i)
                           
            #Count concurrent how many *.csv in Flashman log folder
            FlashmanLOGCount = len(fnmatch.filter(os.listdir(resultfolder), '*.csv'))
            print(title + "[FlashmanPrepareToGo][" + str(i+1) + " run] Before Flashman process, there are " + str(FlashmanLOGCount) +" Flashman log files.")
        
            #While loop to query device flash done and then it will generate new .csv
            _FlashmanLOGCountNew(i,FlashmanLOGCount,resultfolder)
                
            #ATC recover USB connection by using USBSCSI.exe to call device usb debugging wake up.
            time.sleep(600)
            FlashmanCheckDeviceandSkipOOBE(i)
        
            print(title + "[FlashmanEnd][" + str(i+1) + " run] Flashman test done.")
        
        ats.CheckDeviceStatus("-mode 15 -bugreport true")
        print(title + "[FlashmanEnd][" + str(i+1) + " run] Device is in OS mode.")            
        print(title + "[FlashmanEnd][" + str(i+1) + " run] All Flashman test done.")  

    
#if __name__ == '__main__' :
    #SST.ScriptEnableAccounts()
    #Flashman_main()
    #Flashman_sub()
    #testrun = 0
    #resultfolder = r'D:\Flashman_Result\A3QHD_CL_K44_DESIRE_SENSE60_VZW\1428154'
    #_FlashmanResultSummary(testrun, resultfolder)
    

