from Tkinter import *
import tkMessageBox
import tkSimpleDialog
import matplotlib
import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import datetime
import time
import fileinput
import bcrypt
import gdax
import sklearn
import os


# Code designed and written by: Selmane Tabet
# Andrew ID: stabet
# File Created: 9:00PM, November 7, 2017. 
# Version 0.5, November 12th, 2017.
#
# Changelog:
# [CODE]
# - Beta Release
#

matplotlib.use("TkAgg")

########################## MAIN GUI CODE ############################

class Mainw(Tk): #Main Window
    def __init__(self,usd=0,btc=0,eth=0,ltc=0,logslist=[]):
        

        #####################################   INITIALIZING MAIN WINDOW   #####################################
        
        print "Initializing"
        
        Tk.__init__(self)
        self.title("Cryptocurrency Investment Advisor")
        self.geometry("800x280")
        self.frame=Frame(self)
        self.frame.pack(expand=True,fill=BOTH)

        #####################################   INITIALIZING VALUES AND API CLIENT   #####################################
        
        self.balance=usd
        self.BTCbal=btc
        self.ETHbal=eth
        self.LTCbal=ltc
        self.logs=logslist
        self.totalchange=0 #Total earnings made by the user.
        self.BTCtrendval=0 #Current trend in percentage.
        self.ETHtrendval=0
        self.LTCtrendval=0
        self.BTCdelta=0 #Earnings made so far on this specific cryptocurrency
        self.ETHdelta=0
        self.LTCdelta=0
        self.BTCval=0
        self.ETHval=0
        self.LTCval=0

        print "Window initialized and input values ready..."
        
        self.req=gdax.PublicClient() #GDAX Public Client
        
        print "API initialized..."

        
##        self.menu=Menu(self)
##        self.menubar=Menu(self.menu)
##        self.menubar.add_command(label="Top Up", command=lambda: self.TopUp())
##        print "C1"
##        self.menubar.add_command(label="Quit", command=lambda: self.clientexit())
##        print "C2"
##        self.menu.add_cascade(label="Options",menu=self.menubar)

        #####################################   GENERATING BUTTONS AND LABELS    #####################################
        
        
        self.RButton=Button(self.frame,text="Refresh",command=lambda: self.refresh())
        self.RButton.grid(row=0,column=0)
        self.balabel=Label(self.frame,text="Balance (USD): $"+str(self.balance))
        self.balabel.grid(row=0,column=13)
        self.BTClabel=Label(self.frame,text="Balance (BTC): "+str(self.BTCbal)+" BTC")
        self.BTClabel.grid(row=0,column=4)
        self.ETHlabel=Label(self.frame,text="Balance (ETH): "+str(self.ETHbal)+" ETH")
        self.ETHlabel.grid(row=0,column=5)
        self.LTClabel=Label(self.frame,text="Balance (LTC): "+str(self.LTCbal)+" LTC")
        self.LTClabel.grid(row=0,column=7)
        
        #####################################   PERSONAL USER STATISTICS    #####################################
        
        self.totdelta=Label(self.frame,text="Current total profit/losses")
        self.totdelta.grid(row=2,column=12)
        self.totdeltadisp=Label(self.frame,text=str(self.totalchange))
        self.totdeltadisp.grid(row=3,column=12)
        self.breakdowndisp=Label(self.frame,text="Earnings Breakdown")
        self.breakdowndisp.grid(row=5,column=12)
        self.BTCdeltadisp=Label(self.frame,text="BTC: "+str(self.BTCdelta))
        self.BTCdeltadisp.grid(row=6,column=12)
        self.ETHdeltadisp=Label(self.frame,text="ETH: "+str(self.ETHdelta))
        self.ETHdeltadisp.grid(row=7,column=12)
        self.LTCdeltadisp=Label(self.frame,text="LTC: "+str(self.LTCdelta))
        self.LTCdeltadisp.grid(row=8,column=12)

        print "Statistics loaded..."


##        #####################################   TREND VALUES    #####################################
##        
##        self.BTCtrendvaldisp=Label(self.frame,text=str(self.BTCtrendval)) #Consider formatting this according to sign. Refer to refresh function and add if statements for formatting and data analysis.
##        self.BTCtrendvaldisp.grid(row=11,column=2)
##        self.ETHtrendvaldisp=Label(self.frame,text=str(self.ETHtrendval)) #Consider formatting this according to sign.
##        self.ETHtrendvaldisp.grid(row=11,column=4)
##        self.LTCtrendvaldisp=Label(self.frame,text=str(self.LTCtrendval)) #Consider formatting this according to sign.
##        self.LTCtrendvaldisp.grid(row=11,column=7)


        #####################################   ACTION BUTTONS    #####################################
        
        self.investbutton=Button(self.frame,text="Invest",command=lambda: self.invest())
        self.investbutton.grid(row=13,column=4)
        self.cashoutbutton=Button(self.frame,text="Cashout",command=lambda: self.cashout())
        self.cashoutbutton.grid(row=13,column=7)

        
        #####################################   CRYPTOCURRENCY SELECTOR    #####################################
        
        self.selvar=IntVar() #Selection variable
        self.BTCselect=Radiobutton(self.frame,text="BTC",variable=self.selvar,value=1,command=lambda:self.showplot())
        self.BTCselect.grid(row=2,column=3)
        self.ETHselect=Radiobutton(self.frame,text="ETH",variable=self.selvar,value=2,command=lambda:self.showplot())
        self.ETHselect.grid(row=2,column=5)
        self.LTCselect=Radiobutton(self.frame,text="LTC",variable=self.selvar,value=3,command=lambda:self.showplot())
        self.LTCselect.grid(row=2,column=7)
        self.BTCselect.select() #Default selection
        print "Buttons generated..."

        
        #####################################   EXCHANGE RATE MINI-DASHBOARD    #####################################
        
        self.exrate=Label(self.frame,text="Exchange Rates")
        self.exrate.grid(row=10,column=4)

        self.BTCvaldisp=Label(self.frame,text="BTC: "+str(self.BTCval)+" |  "+str(self.BTCtrendval))
        self.BTCvaldisp.grid(row=11,column=3)
        self.ETHvaldisp=Label(self.frame,text="ETH: "+str(self.ETHval)+" |  "+str(self.ETHtrendval))
        self.ETHvaldisp.grid(row=11,column=4)
        self.LTCvaldisp=Label(self.frame,text="LTC: "+str(self.LTCval)+" |  "+str(self.LTCtrendval))
        self.LTCvaldisp.grid(row=11,column=5)

        print "Value labels set..."
        #self.refresh() #Fetch all values.
        
        
        

    def TopUp(self):
        print "topup"
        self.amt=tkSimpleDialog.askfloat("Balance Top Up (US Dollars)","How much are you willing to top up?")
        self.balance+=self.amt
        self.f=open(Logwin.U.get()+".txt")
        self.templist=self.f.readlines()
        self.f.close()
        self.templist.pop(2)
        self.templist.insert(2,"USDbal="+str(self.balance)+"\n")
        self.g=open(Logwin.U.get()+".txt","w")
        self.g.writelines(self.templist)
        self.g.write("@"+datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")+"@"+"Top Up"+"@"+str(self.amt)+"\n")
        self.g.close()
        self.logs.append(("@"+datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")+"@"+"Top Up"+"@"+str(self.amt)).split("@")) #Inaccurate only on a slow computer
        
        self.refresh()

    def refresh(self):
        #Fetch new updates and check radio buttons
        print "refreshing"

        
        self.progressbar=ttk.Progressbar(orient=HORIZONTAL,length=100,mode='determinate')
        self.progressbar.grid(row=1,column=3)
        self.progressbar.start()
        #####################################   FETCHING CURRENCY RATES   #####################################
        self.BTCcurrencydata=self.req.get_product_trades("BTC-USD") #Use the last trade made at the time of request as the way of fetching the currency value. Done for all currencies.
        self.BTCval=float(self.BTCcurrencydata[0]["price"])
        self.ETHcurrencydata=self.req.get_product_trades("ETH-USD")
        self.ETHval=float(self.ETHcurrencydata[0]["price"])
        self.LTCcurrencydata=self.req.get_product_trades("LTC-USD")
        self.LTCval=float(self.LTCcurrencydata[0]["price"])
        
        self.progressbar.step(15)


        
        #####################################   PLOTTING BTC VALUE VS TIME GRAPH    #####################################
        
        self.bdata=self.req.get_product_historic_rates("BTC-USD",start=(datetime.datetime.utcnow()-datetime.timedelta(days=1)).isoformat(),end=datetime.datetime.utcnow().isoformat()) #Granularity is about 400 at 24 hours

        self.BTCdata=[]
        for i in range(len(self.bdata)):
            self.BTCaveragedatapoint=(((self.bdata[i][1]+self.bdata[i][2])/2)+((self.bdata[i][3]+self.bdata[i][4])/2))/2  #Average High/Low Vs. Average Open/Close - epoch time difference is about 2 minutes so this should be fine.
            self.BTCdata.append(self.BTCaveragedatapoint)
            
        self.BTCtimes=[]
        for i in range(len(self.bdata)):
            #self.BTCtimes.append(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(self.bdata[i][0])))
            self.BICtimes.append(datetime.datetime.fromtimestamp(self.bdata[i][0]))
            
        self.BTCdates=matplotlib.dates.date2num(self.BTCtimes)

        self.progressbar.step(25)

        self.BTCf=Figure(figsize=(5,5),dpi=100)
        self.BTCp=self.BTCf.add_subplot(111)
        self.BTCp.pyplot.plot_date(self.BTCdates,self.BTCdata)
        
        self.progressbar.step(5)

        #####################################   PLOTTING ETH VALUE VS TIME GRAPH    #####################################

        
        self.edata=self.req.get_product_historic_rates("ETH-USD",start=(datetime.datetime.utcnow()-datetime.timedelta(days=1)).isoformat(),end=datetime.datetime.utcnow().isoformat()) #Granularity is about 400 at 24 hours
        self.ETHdata=[]
        for i in range(len(self.edata)):
            self.ETHaveragedatapoint=(((self.edata[i][1]+self.edata[i][2])/2)+((self.edata[i][3]+self.edata[i][4])/2))/2  #Average High/Low Vs. Average Open/Close - epoch time difference is about 2 minutes so this should be fine.
            self.ETHdata.append(self.ETHaveragedatapoint)
        self.ETHtimes=[]
        for i in range(len(self.edata)):
            #self.ETHtimes.append(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(self.edata[i][0])))
            self.ETHtimes.append(datetime.datetime.fromtimestamp(self.edata[i][0]))
        self.ETHdates=matplotlib.dates.date2num(self.ETHtimes)

        self.progressbar.step(25)
        
        self.ETHf=Figure(figsize=(5,5),dpi=100)
        self.ETHp=self.ETHf.add_subplot(111)
        self.ETHp.pyplot.plot_date(self.ETHdates,self.ETHdata)

        self.progressbar.step(5)

        #####################################   PLOTTING LTC VALUE VS TIME GRAPH    #####################################

        self.ldata=self.req.get_product_historic_rates("LTC-USD",start=(datetime.datetime.utcnow()-datetime.timedelta(days=1)).isoformat(),end=datetime.datetime.utcnow().isoformat()) #Granularity is about 400 at 24 hours
        self.LTCdata=[]
        for i in range(len(self.ldata)):
            self.LTCaveragedatapoint=(((self.ldata[i][1]+self.ldata[i][2])/2)+((self.ldata[i][3]+self.ldata[i][4])/2))/2  #Average High/Low Vs. Average Open/Close - epoch time difference is about 2 minutes so this should be fine.
            self.LTCdata.append(self.LTCaveragedatapoint)
        self.LTCtimes=[]
        for i in range(len(self.ldata)):
            #self.LTCtimes.append(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(self.ldata[i][0])))
            self.LTCtimes.append(datetime.datetime.fromtimestamp(self.ldata[i][0]))
        self.LTCdates=matplotlib.dates.date2num(self.LTCtimes)

        self.progressbar.step(20)

        self.LTCf=Figure(figsize=(5,5),dpi=100)
        self.LTCp=self.LTCf.add_subplot(111)
        self.LTCp.pyplot.plot_date(self.LTCdates,self.LTCdata)

        self.progressbar.step(3)
        
        

        #####################################   CALCULATING TOTAL EARNINGS/LOSS    #####################################
        
        if self.logs==[]:
            self.totalchange=0
        else:
            #Total change = Total withdrawn value - Total invested
            self.TotalInvested=0
            self.TotalWithdrawn=0
            for i in range(len(self.logs)):
                if "Investment" in self.logs[i]:
                    self.TotalInvested+=float(self.logs[i][2])
                elif "Withdrawal" in self.logs[i]:
                    self.TotalWithdrawn+=float(self.logs[i][2])

            self.totalchange=self.TotalWithdrawn-self.TotalInvested #Update the amount of profit made so far. Format color accordingly.


                    
        
        #Update the trend values and trend status. DATA ANALYSIS REQUIRED!




        #####################################   UPDATE INVESTMENT LOG    #####################################    
        flog=open(Logwin.U.get()+".txt")
        tnew=flog.readlines()
        flog.close()
        if len(tnew)>6:
            self.logs=self.tnew[6:]
        
        self.progressbar.step(2)
        self.progressbar.close()

        
        AppWin.update() #update all elements on the window.

    def invest(self):
        print "invest"
        investor=Investment()
        pass #Toplevel window, entered values will be returned here, balances will be updated accordingly.

    def cashout(self):
        print "cashout"
        cashoutwin=Withdrawal()
        

    def showplot(self):
        stat=self.selvar.get()
        if stat==1:
            canvas=FigureCanvasTkAgg(self.BTCf,self)
            canvas.show()
            canvas.get_tk_widget().grid(row=3,column=1)
            #canvas.get_tk_widget().pack(side=TOP,fill=BOTH,expand=True)
        elif stat==2:
            canvas=FigureCanvasTkAgg(self.ETHf,self)
            canvas.show()
            canvas.get_tk_widget().grid(row=3,column=1)
            #canvas.get_tk_widget().pack(side=TOP,fill=BOTH,expand=True)
        else:
            canvas=FigureCanvasTkAgg(self.LTCf,self)
            canvas.show()
            canvas.get_tk_widget().grid(row=3,column=1)
            #canvas.get_tk_widget().pack(side=TOP,fill=BOTH,expand=True)

    
    def clientexit(self):
        
        print "exiting"
        #Save data
        exit()





class Investmemt(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title("Investment Window")
        self.geometry("400x500")
        self.frame=Frame(self)
        self.frame.pack(expand=True,fill=BOTH)
        self.received="Fill in the above fields first, then click Analyze."
        self.Potential="Fill in the above fields first, then click Analyze."
        self.USDinvestdisp=Label(self.frame,text="Amount in USD: $")
        self.USDinvestdisp.grid(row=1,column=0)
        self.USDinvest=Entry(self.frame)
        self.USDinvest.grid(row=1,column=1)

        self.CurrencyChoice=Label(self,text="What do you want to invest in?")
        self.CurrencyChoice.grid(row=2,column=0)
        
        self.CurrencyVar=IntVar() #Selection variable
        self.BTCselect=Radiobutton(self.frame,text="BTC",variable=self.CurrencyVar,value=1)
        self.BTCselect.grid(row=3,column=0)
        self.ETHselect=Radiobutton(self.frame,text="ETH",variable=self.CurrencyVar,value=2)
        self.ETHselect.grid(row=3,column=1)
        self.LTCselect=Radiobutton(self.frame,text="LTC",variable=self.CurrencyVar,value=3)
        self.LTCselect.grid(row=3,column=2)

        self.receivedisp=Label(self.frame,text="You would receive:  "+self.received)
        self.receivedisp.grid(row=4,column=0)

        self.Potentialdisp=Label(self.frame,text="Net earning wihin one week:   "+self.Potential)
        self.Potentialdisp.grid(row=5,column=0)

        self.Analyzebtn=Button(self.frame,text="Analyze",command=lambda: self.InvestAnalyze(self.CurrencyVar.get(),self.USDinvest.get()))
        self.Analyzebtn.grid(row=7,column=0)

        self.Investbtn=Button(self.frame,text="Invest!",command=lambda: self.InvestFunction(self.CurrencyVar.get(),self.USDinvest.get()))
        self.Investbtn.grid(row=8,column=0)
        

    def InvestAnalyze(self,choice,USDamount):
        if choice==1:
            self.received=str(float(USDamount)/self.BTCval)+" BTC"
        elif choice==2:
            self.received=str(float(USDamount)/self.ETHval)+" ETH"
        elif choice==3:
            self.received=str(float(USDamount)/self.LTCval)+" LTC"
        else:
            self.received="0"

        #Also add projected delta values within 1wk by analyzing the graphs.
        #Then update window with analysis results.
        

    def InvestFunction(self,choice,USDamount):
        if float(USDamount)>self.balance:
            tkMessageBox.showinfo("Invalid input.","You cannot invest with more than what you have.\nLower the investment value or top up your USD Balance.")
        elif float(USDamount)<0:
            tkMessageBox.showinfo("Invalid input.","You cannot invest a negative amount of money.\nMake sure that the investment amount is a positive value.")
        elif float(USDamount)==0:
            tkMessageBox.showinfo("Zero investment.","Your investment cannot be zero. You might as well not do anything.")
        else:
            pass
            #Write to log.
        #Probably execute refresh function too?
        pass

class Withdrawal(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title("Cashout Window")
        self.geometry("250x300")
        self.frame=Frame(self)
        self.frame.pack(expand=True,fill=BOTH)


#########################################   LOGIN STEP CODE    #########################################
class LoginWindow(Tk): #Login Page
    def __init__(self):
        Tk.__init__(self)
        self.title("Login")
        self.geometry("250x300")
        self.loggedin=False
        self.frame=Frame(self)
        self.frame.pack(expand=True,fill=BOTH)
        self.ulabel=Label(self.frame,text="Username")
        self.ulabel.pack()
        self.U=Entry(self.frame)
        self.U.pack()
        self.plabel=Label(self.frame,text="Password")
        self.plabel.pack()
        self.P=Entry(self.frame,show="*")
        self.P.pack()
        self.addButton = Button(self.frame,text="OK",command=lambda: self.LOGIN(self.U.get(),self.P.get()))
        self.addButton.pack()
        self.nothing=Label(self.frame,text="")
        self.nothing.pack()
        self.newuserbtn=Button(self.frame,text="New User? Create an account!",command=lambda: self.newacc())
        self.newuserbtn.pack()
        
    def LOGIN(self,username,password):
        if os.path.exists(username+".txt"):
            f=open(username+".txt")
            tlist=f.readlines()
            for i in range(len(tlist)):
                tlist[i]=tlist[i].strip()
            salt=tlist[0]
            target=tlist[1]
            hashedpw=bcrypt.hashpw(password+salt+"ROFLMAOXD",salt)
            if hashedpw==target:
                self.USDbalance=float(tlist[2][7:])
                self.BTCbalance=float(tlist[3][7:])
                self.ETHbalance=float(tlist[4][7:])
                self.LTCbalance=float(tlist[5][7:])
                if len(tlist)>6: 
                    self.logsunsplit=tlist[6:]
                    self.logs=[]
                    for i in range(len(self.logunsplit)):
                        self.logs.append(self.logunsplit[i].split("@"))
                else:
                    self.logs=[]
                tkMessageBox.showinfo("Success!","Login successful! Welcome to the trading world!")
                self.loggedin=True
                self.destroy()
            else:
                tkMessageBox.showinfo("Wrong credentials","Wrong password, please try again.")
            
        else:
            tkMessageBox.showinfo("Wrong credentials","Username incorrect or does not exist.\nIf you are a new user, create an account before logging in.")

    def newacc(self):
        new=AccCreation()
        
class AccCreation(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title("New User")
        self.geometry("250x300")
        self.frame=Frame(self)
        self.frame.pack(expand=True,fill=BOTH)
        self.header=Label(self.frame,text="New User Creation")
        self.header.pack()
        self.spacer=Label(self.frame,text="")
        self.spacer.pack()
        self.ulabel=Label(self.frame,text="Username")
        self.ulabel.pack()
        self.U=Entry(self.frame)
        self.U.pack()
        self.plabel=Label(self.frame,text="Password")
        self.plabel.pack()
        self.P=Entry(self.frame,show="*")
        self.P.pack()
        self.Pconl=Label(self.frame,text="Confirm Password")
        self.Pconl.pack()
        self.Pcon=Entry(self.frame,show="*")
        self.Pcon.pack()
        self.addButton = Button(self.frame,text="OK",command=lambda: self.Create(self.U.get(),self.P.get(),self.Pcon.get()))
        self.addButton.pack()

    def Create(self,username,password,passconf):
        if os.path.exists(username+".txt"):
            tkMessageBox.showinfo("Username taken","Username already exists, enter a different username.")
            self.tkraise()
        elif username=="" or password=="" or passconf=="":
            tkMessageBox.showinfo("Invalid input!","Make sure you have filled in all the fields!")
            self.tkraise()
        elif password!=passconf:
            tkMessageBox.showinfo("Invalid input!","Passwords do not match!\nMake sure that you have typed the passwords correctly.")
            self.tkraise()
        
        else:
            f=open(username+".txt","w")
            salt=bcrypt.gensalt()
            f.write(salt+"\n")
            f.write(bcrypt.hashpw(password+salt+"ROFLMAOXD", salt)+"\n")
            f.write("USDbal=0\n")
            f.write("BTCbal=0\n")
            f.write("ETHbal=0\n")
            f.write("LTCbal=0\n")
            f.close()
            tkMessageBox.showinfo("Creation success!","Account successfully created!\nYou may now login with your credentials.")
            self.destroy() #And create new account window

            
Logwin=LoginWindow() #Initialize and display the Login screen.
Logwin.mainloop()

if Logwin.loggedin==False:
    os._exit(0) #If the user destroyed the window, exit the whole program and do not initialize Main window.
else:
    AppWin=Mainw(usd=Logwin.USDbalance,btc=Logwin.BTCbalance,eth=Logwin.ETHbalance,ltc=Logwin.LTCbalance,logslist=Logwin.logs) #Initialize and display the Main window otherwise.
    AppWin.mainloop()
