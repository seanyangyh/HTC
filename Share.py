import datetime
import time
import ats
import ate
import system as s
import atsbase
import user as u
import subprocess
from datetime import datetime
from time import sleep, gmtime, strftime
import sys

project = str(s.PROJECT)

title='[SCD722][Mark.WW_Liu][ERROR]'
##----------------------------------------------------------------
class WebOutput():
    def Value(Item,IQT_Result,FC,Output):
        ate.UpdateMonitorReport(s.JOB_ID,Item,FC,IQT_Result,Output)
##----------------------------------------------------------------


#====================================



class Mark():
    def JudgeFail(Name,Value):
        r=True
        
        if Value == "0" or Value =="1" or Value == "":
            pass
        elif Value == int(1) or Value == int(0):
            pass
        else:
            print(title+"you enter "+Name+" value for "+str(Value))
            WebOutput.Value(Name,"Fail","",Name+" value for "+str(Value))
            r=False
        return r
    
    def JudgeFailA(Name,Value):
        r=True
        if Value == int(1) or Value == int(0):
            pass
        else:
            print(title+"you enter "+Name+" value for "+str(Value))
            WebOutput.Value(Name,"Fail","",Name+" value for "+str(Value))
            r=False
        return r
    def DefaultValue(name):
        r=True
        if hasattr(u,name):
            pass
        else:
            print(name,"Fail","","plase enter "+name+" value")
            WebOutput.Value(name,"Fail","","plase enter "+name+" value")
            r=False
        return r 
            
    def CheckA(UserName,*TrueName):
        g=True
        count=0
        r1=[]
        TrueNameA=TrueName
        TrueNameB=len((TrueName))
        if hasattr(u,UserName):
            r=getattr(u,UserName)
            r1.append(r)
            for i in range(TrueNameB):
                if r1[0] == TrueNameA[i]:
                    count=count+1
                    pass
            if count >= int(1):
                pass
            else:
                print(title+""+UserName+" fail "+str(r))
                WebOutput.Value(UserName,"Fail","","you enter for "+str(r))
                g=False
        return g
        
    
class CheckUserValue():

    def CheckDefaultValue():
        r=Mark.DefaultValue('loglevel')
        r1=Mark.DefaultValue('disabled_htclog')
        r2=Mark.DefaultValue('SSTLoginAccounts')
        if r == True and  r1 == True and  r2 == True:
            pass
        else:
            exit(0)

        
    

    def Check():
        r=CheckUserValue.UserValueSSTLoginAccounts()
        r1=CheckUserValue.Disabled_htclog()
        r2=CheckUserValue.loglevel()
        r3=CheckUserValue.UserValueDebug()
        r4=CheckUserValue.UserValueEnvironment()
        r5=CheckUserValue.UserValueEVTVolte()
        r6=CheckUserValue.UserValueSRGSR()
        r7=CheckUserValue.UserValueTime()
        if r == True and  r1 == True and  r2 == True and r3 ==True and r4 ==True and r5 ==True and r6 ==True and r7 ==True:
            pass
        else:
            exit(0)




        
#====================================
           
    def UserValueSSTLoginAccounts():#Sean Yang   SST Login Accounts
        r=True
        x=[]
        count=0
        fail=[]
        Accounts=['Gmail','Exchange','POPMail','IMAP','Facebook','Twitter','Dropbox','Plurk']
        countA=len(Accounts)
        if hasattr(u, 'SSTLoginAccounts'):
            gg=0
            AllAccount = u.SSTLoginAccounts.split(',')
            for y in AllAccount:
                if y != -1:
                    x.append(y)
            xA=len(x)
            
            for i in range(xA):
                if Accounts[0] == str(x[i]):
                  count=count+1
            if count >= int(1):
                pass
            else:
                gg=gg+1
                print(title+"you no enter Gmail")
                WebOutput.Value("SSTLoginAccounts","Fail","","you no enter Gmail")
                r=False

                

            check=0
            for i in range(xA):
                for ii in range(countA):
                    if x[i]==Accounts[ii]:
                        check=check+1
                if check >= int(1):
                    check=0
                else:
                    gg=gg+1
                    print(title+"you enter error "+x[i])
                    WebOutput.Value("SSTLoginAccounts","Fail","","you enter error "+x[i])
                    r=False
            if gg >= int(1):
                gg=0
                r=False
        return r

        
    def UserValueEVTVolte(): #EVE or Volte
        r=True
        countEV=0
        if hasattr(u, 'EYE') and hasattr(u, 'Volte'):
            countEV=countEV+1
            if (u.EYE == "1" and u.Volte =="1") or (u.EYE == "" and u.Volte =="") or (u.EYE == "0" and u.Volte =="0"):
                pass
            elif (u.EYE == int(1) and u.Volte ==int(1)) or (u.EYE == int(0) and u.Volte ==int(0)):
                pass
            elif u.EYE == "1" or u.EYE == "" or u.EYE =="0":
                Mark.JudgeFail('Volte',u.Volte)                
            elif u.EYE == int(1) or u.EYE ==int(0):
                Mark.JudgeFail('Volte',u.Volte)
            elif u.Volte == "1" or u.Volte == "" or u.Volte =="0":
                Mark.JudgeFail(EYE,u.EYE)
            elif u.Volte == int(1) or u.Volte == int(0):
                Mark.JudgeFail('EYE',u.EYE)
            else:
                print(title+"you user enter  EYE and Volte  value have error" )
                WebOutput.Value("EYE_Volte","Fail","","Plase check \"EYE\" or \"Volte\" the value")
                r=False
        if countEV == int(1):
            pass
        else:
            if hasattr(u, 'EYE'):
                Mark.JudgeFail('EYE',u.EYE)
            if hasattr(u, 'Volte'):
                Mark.JudgeFail('Volte',u.Volte)
        return r


#====================================
    def UserValueEnvironment():# TAIPEI or TAOYUAN
        return Mark.CheckA('Environment','TAIPEI','TAOYUAN','') 
#====================================
    def UserValueSRGSR():#GSR or SR or SR2.0
        r=True
        return Mark.CheckA('SRGSR','SR','GSR','SR2.0',"") 
#=====================================
    def UserValueTime(): # Time 0 to 500
        r=True
        countT=0
        TimeValue=[]
        for i in range(501):
            TimeValue.append(i)
            TimeValueA=len(TimeValue)
        if hasattr(u, 'time'):
            for i in range(TimeValueA):
                if u.time == str(TimeValue[i]) :
                    countT=countT+1
                    pass
                if u.time == int(TimeValue[i]):
                    countT=countT+1
                    pass
                if u.time == "":
                    countT=countT+1
                    pass
            if countT >= 1:
                pass
            else:
                print(title+"time error. you enter for "+str(u.time))
                WebOutput.Value("Time","Fail","","you enter for "+str(u.time))
                r=False
        return r
#====================================
    def UserValueDebug(): # debug value
        r=True
        countD=0
        if hasattr(u, 'debug_flag'):
            countD=u.debug_flag.count(',')
            if countD == 9:
                pass
            else:
                print(title+"Debug flag setup failed, please setup 10 numbers with comma to separate")
                WebOutput.Value("Debug","Fail","","you enter for "+str(u.debug_flag))
                r=False
        return r
#====================================
    def Disabled_htclog(): #Allen value 0 or 1
        if hasattr(u, 'disabled_htclog'):
            return Mark.JudgeFailA('disabled_htclog',u.disabled_htclog)
#==================================
    def loglevel(): #Allen value 0 or 1
        if hasattr(u, 'loglevel'):
            return Mark.JudgeFailA('loglevel',u.loglevel)
#=========================================
#=========================================
class DevicesValue():

    def GetOP(): #pass
        """
        [Function]
        Get devices the MCCMNC
        [Author]
        Mark.WW_Liu
        [Release Date]
        2015/03/11
        [input]
        None
        [output]
        MCCMNC(46692):[SCD722][Mark.WW_Liu] The operator is _FET

        MCCMNC(46601):[SCD722][Mark.WW_Liu] The operator is _CHT
        [Example]
        >>> SCD722.GetOP()
        [Note]
        None
        """
        MCCMNCA=[]
        Single=['46601\n','46692\n']
        MCCMNC = subprocess.getoutput("adb -s "+s.DEVICE_ID+" shell getprop gsm.sim.operator.numeric")
        AllAccount = MCCMNC.split(',')
        for y in AllAccount:
            if y != -1:
                MCCMNCA.append(y)
        if MCCMNCA[0] == str(46692)or MCCMNCA[0]==str(Single[1]):
            Operator = "_CHT"
            print("[SCD722][Mark.WW_Liu] The operator is " + Operator)
            WebOutput.Value("MCCMNC","Pass","","MCCMNC for "+str(Operator))
        elif MCCMNCA[0] ==  str(46601) or MCCMNCA[0]==str(Single[0]):
            Operator = "_FET"
            print("[SCD722][Mark.WW_Liu] The operator is " + Operator)
            WebOutput.Value("MCCMNC","Pass","","MCCMNC for "+str(Operator))
        else:
            print("[SCD722][Mark.WW_Liu][ERROR] you no sim1")
            WebOutput.Value("MCCMNC","Fail","","MCCMNC no SIM1  or  no CHT and FET")
            exit(0)
        
        return Operator
#============================================
    def GetSKU():#pass
        """
        [Function]
        Get devices the SKU Version.
        [Author]
        Mark.WW_Liu
        [Release Date]
        2015/03/11
        [input]
        None
        [output]
        PASS:[SCD722][Mark.WW_Liu] The SKU is 720

        FAIL:[SCD722][ERROR]SKU Type Not Match, please contact with Richard Lu
        [Example]
        >>> SCD722.GetSKU()
        [Note]
        None
        """
        ROM = subprocess.getoutput("adb -s "+s.DEVICE_ID+" shell getprop ro.product.version")
        SKU = ROM.split(".")
        try:
            SKU = str(SKU[2])
            print("[SCD722][Mark.WW_Liu] The SKU is " + SKU)
            WebOutput.Value("SKU","Pass","","SKU is "+str(SKU))
            return SKU
        except:
            print("[SCD722][ERROR]SKU Type Not Match, please contact with Richard Lu")
            WebOutput.Value("SKU","Fail","","please contact with Richard Lu")
            atsbase.event.is_finish = True
            exit(0)
#==============================================
    def GetAndroidVer(): #pass
        """
        [Function]
        Get user select Android Version.
        [Author]
        Mark.WW_Liu
        [Release Date]
        2015/03/11
        [input]
        None
        [output]
        PASS:[SCD722][Mark.WW_Liu] The Android version is _K44_

        FAIL:[SCD722][ERROR]This Android version can't be recognized, please contact with Richard Lu
        [Example]
        >>> SCD722.GetAndroidVer()
        [Note]
        None
        """
        Ver=("_K44_", "_K442_", "_K443_", "_K444_", "_JB412_", "_JB41_", "_JB422_", "_JB43_", "_L50_")
        count=0
        for v in Ver:
            if project.find(v) != -1:
                AndroidVer = str(v)
                count=count+1
                print("[SCD722][Mark.WW_Liu] The Android version is " + AndroidVer)

        if count is 0:
            print("[SCD722][ERROR]This Android version can't be recognized, please contact with Richard Lu")
            WebOutput.Value("AndroidVer","Fail","","please contact with Richard Lu")
            exit(0)
        else:
            WebOutput.Value("AndroidVer","Pass","","AndroidVer is "+str(AndroidVer))

        return AndroidVer
#==================================================
    def GetSenseVer(): #pass
        """
        [Function]
        Get user select Android Sense.
        [Author]
        Mark.WW_Liu
        [Release Date]
        2015/03/11
        [input]
        None
        [output]
        [SCD722][Mark.WW_Liu] The Sense version is SENSE60

        [Example]
        >>> SCD722.GetAndroidVer()
        [Note]
        None
        """
        count=0
        Sense=("SENSE50", "SENSE53", "SENSE55", "SENSE60","SENSE63","SENSE70")
        for s in Sense:
            if project.find(s) != -1:
                count=count+1
                SenseVer = str(s)
                print("[SCD722][Mark.WW_Liu] The Sense version is " + SenseVer)
        if count >= int(1):
            WebOutput.Value("SenseVer","Pass","","SenseVer is "+str(SenseVer))
        else:
            print("[SCD722[Mark.WW_Liu] SENSE version Error.")
            WebOutput.Value("SenseVer","Fail","","please contact with Richard Lu")
            exit(0)
        return SenseVer
#====================================================

    def GetDesire(): #pass
        """
        [Function]
        Get user select Project check whether for Desire
        [Author]
        Mark.WW_Liu
        [Release Date]
        2015/03/11
        [input]
        None
        [output]
        [SCD722][Mark.WW_Liu] DESIRE project

        [Example]
        >>> SCD722.GetDesire()
        [Note]
        None
        """
        if project.find("DESIRE") != -1:
            Desire = 'True'
            print("[SCD722][Mark.WW_Liu] DESIRE project")
            WebOutput.Value("DESIRE","Pass","","DESIRE project")
            return Desire
#======================================================



