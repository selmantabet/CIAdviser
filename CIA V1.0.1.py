from Tkinter import * #GUI library.
import ttk #For progressbar.
import time #To put the program on sleep so that the progressbar could appear smoother.
import tkMessageBox #For info box displays.
import tkSimpleDialog #For quick dialog inputs.
import matplotlib
matplotlib.use("TkAgg") #Using Tk backend of matplotlib.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #Canvas for Tkinter matplotlib backend.
from matplotlib.figure import Figure #Containers for the graphs.
import numpy #For Ordinary Least Square regression (line of best fit).
import datetime #For logging and sending requests.
import bcrypt #For password.
import gdax #API interface.
import os #For processing data save files.


# Code designed and written by: Selmane Tabet
# Andrew ID: stabet
#
# File Created: 9:00PM, November 7, 2017. 
# Version 1.0.1, November 26th, 2017.
#
# Changelog:
#
# - Final Release (for 15-112 presentation)
#
# [CODE]
#
# - Improved login and account creation experience by initalizing the login/account creation window with already focused Entry fields and binded the login/create function with the Enter key.
# - Fixed Main window content.
# - Improved auto-saving mechanism across the entire app.
# - Fixed auto-saving issues that are caused by the cashout and investment functions.
# - Adjusted Tk window geometry to fit the content neatly.
# - Fixed numerical display and made all dollar figures appear to the nearest cent. But the value will always be stored as a float.
# - Added more detailed comments across the whole source code.
# - Improved the refreshing print statements.
# - Removed redundant lines of code.
# - Added Progress bar.
#
# [FEATURES]
#
# - Added Investment Logs feature:
#  ~ Display logs of every action performed by the user, also used to track some of the user's statistics. Logs data is updated upon every action perfomed by the user.
#
# - Added plots for cryptocurrencies.
#  ~ Simple graphs of all the cryptocurrencies, the user can switch between graphs via the selection of radiobuttons.
#  ~ Includes best line fit to analyze the trend based on data from the past 24 hours.
#  ~ Formatted trend value string colors depending on signs of 24 hour trend and weekly trend.
#
# - Added Instructions page.
#
# - Formatted the colors of Personal Statistics labels according to numerical sign values.
#
# - Added disclaimer at the bottom of the main window along with a color code legend.
#


########################## MAIN GUI CODE ############################

class Mainw(Tk): #Main Window
    def __init__(self,usd=0,btc=0,eth=0,ltc=0,logslist=[]):
        

        #####################################   INITIALIZING MAIN WINDOW   #####################################

        print "Initializing..."
        
        Tk.__init__(self)
        self.title("Cryptocurrency Investment Adviser")
        self.geometry("1150x675")
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
        self.BTCdelta=0 #Earnings made so far on this specific cryptocurrency.
        self.ETHdelta=0
        self.LTCdelta=0
        self.BTCval=0
        self.ETHval=0
        self.LTCval=0

        print "Window initialized and input values ready..."
        
        self.req=gdax.PublicClient() #GDAX Public Client.
        
        print "API initialized..."

        menubar = Menu(self)
        menubar.add_command(label="Top Up",command=self.TopUp)
        menubar.add_command(label="Help",command=self.helpme)
        menubar.add_command(label="Quit",command=self.destroy)
        
        self.config(menu=menubar)

        #####################################   GENERATING BUTTONS AND LABELS    #####################################
        
        
        self.RButton=Button(self.frame,text="Refresh",command=lambda: self.refresh())
        self.RButton.grid(row=0,column=0)
        self.balabel=Label(self.frame,text="Balance (USD): $"+str(self.balance))
        self.balabel.grid(row=0,column=9)
        self.BTClabel=Label(self.frame,text="Balance (BTC): "+str(self.BTCbal)+" BTC")
        self.BTClabel.grid(row=0,column=3)
        self.ETHlabel=Label(self.frame,text="Balance (ETH): "+str(self.ETHbal)+" ETH")
        self.ETHlabel.grid(row=0,column=4)
        self.LTClabel=Label(self.frame,text="Balance (LTC): "+str(self.LTCbal)+" LTC")
        self.LTClabel.grid(row=0,column=5)
        
        #####################################   PERSONAL USER STATISTICS    #####################################
        
        self.totdelta=Label(self.frame,text="Current total profit/losses")
        self.totdelta.grid(row=5,column=9)
        self.totdeltadisp=Label(self.frame,text="USD "+str(self.totalchange)) #Shows the total profit made throughout the user's trading career.
        self.totdeltadisp.grid(row=6,column=9)
        self.spacer3=Label(self.frame,text="")
        self.spacer3.grid(row=7,column=9)
        self.breakdowndisp=Label(self.frame,text="Earnings Breakdown")
        self.breakdowndisp.grid(row=8,column=9)
        self.BTCdeltadisp=Label(self.frame,text="BTC: "+str(self.BTCdelta)) #Shows which currency the user has been doing best in, etc.
        self.BTCdeltadisp.grid(row=9,column=9)
        self.ETHdeltadisp=Label(self.frame,text="ETH: "+str(self.ETHdelta))
        self.ETHdeltadisp.grid(row=10,column=9)
        self.LTCdeltadisp=Label(self.frame,text="LTC: "+str(self.LTCdelta))
        self.LTCdeltadisp.grid(row=11,column=9)

        print "Statistics loaded..."


        #####################################   ACTION BUTTONS    #####################################
        
        self.investbutton=Button(self.frame,text="Invest",command=lambda: self.invest())
        self.investbutton.grid(row=10,column=3)
        self.logsbutton=Button(self.frame,text="Transaction Logs",command=lambda: self.showlogs())
        self.logsbutton.grid(row=10,column=4)
        self.cashoutbutton=Button(self.frame,text="Cashout",command=lambda: self.cashout())
        self.cashoutbutton.grid(row=10,column=5)

        
        #####################################   CRYPTOCURRENCY SELECTOR    #####################################
        
        self.selvar=IntVar() #Selection variable.
        self.BTCselect=Radiobutton(self.frame,text="BTC",variable=self.selvar,value=1,command=lambda:self.showplot())
        self.BTCselect.grid(row=2,column=3)
        self.ETHselect=Radiobutton(self.frame,text="ETH",variable=self.selvar,value=2,command=lambda:self.showplot())
        self.ETHselect.grid(row=2,column=4)
        self.LTCselect=Radiobutton(self.frame,text="LTC",variable=self.selvar,value=3,command=lambda:self.showplot())
        self.LTCselect.grid(row=2,column=5)
        self.BTCselect.select() #Default selection.
        print "Buttons generated..."

        
        #####################################   EXCHANGE RATE MINI-DASHBOARD    #####################################
        
        self.exrate=Label(self.frame,text="Exchange Rates | 24 Hour Trend | Week Trend")
        self.exrate.grid(row=6,column=4)

        self.BTCvaldisp=Label(self.frame,text="BTC: $"+str(self.BTCval)+" |  "+str(self.BTCtrendval))
        self.BTCvaldisp.grid(row=7,column=3)
        self.ETHvaldisp=Label(self.frame,text="ETH: $"+str(self.ETHval)+" |  "+str(self.ETHtrendval))
        self.ETHvaldisp.grid(row=7,column=4)
        self.LTCvaldisp=Label(self.frame,text="LTC: $"+str(self.LTCval)+" |  "+str(self.LTCtrendval))
        self.LTCvaldisp.grid(row=7,column=5)
        self.notice=Label(self.frame,text="Red: Steadily decreasing        Green: Steadily increasing        Black: Stable\nRefer to the Help page for more details and advice.\n\nINVEST AT YOUR OWN RISK!")
        self.notice.grid(row=12,column=4)

        print "Value labels set..."

        self.firstrun=True #This variable helps in getting the program to perform certain actions that are only meant to be done on the very first run (upon initializing the app).
        
        self.refresh() #Fetch all values.

        
        
        

    def TopUp(self): #This function prompts the user to enter an amount of money that would be added to their USD balance.
        print "Top Up"
        self.legalTopUp=False
        while self.legalTopUp==False: #Keep on prompting the user until they provides a valid input.
            self.amt=tkSimpleDialog.askfloat("Balance Top Up (US Dollars)","How much are you willing to top up?")
            if self.amt<0:
                tkMessageBox.showinfo("Illegal value.","Your top up value cannot be negative.\nInput zero if you wish to cancel.")
            else:
                self.legalTopUp=True #To break the while loop condition, since the input is now valid.
                if self.amt==None:
                    print "No input."
                elif self.amt==0:
                    print "Zero input."
                else:
                    self.balance+=self.amt
                    self.f=open(Logwin.userid+".txt")
                    self.templist=self.f.readlines() #Read out the lines, replace the USD balance number, write to log and overwrite the original save file.
                    self.f.close()
                    self.templist.pop(2)
                    self.templist.insert(2,"USDbal="+str(self.balance)+"\n")
                    self.g=open(Logwin.userid+".txt","w")
                    self.g.writelines(self.templist)
                    self.g.write(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")+"@"+"Top Up"+"@"+str(self.amt)+"@N/A@N/A"+"\n")
                    self.g.close()

                    self.refresh()

    def refresh(self): #This function fetches all the latest values and data via the GDAX API, and uses the received data to plot new graphs and display new trend values.
        print "Refreshing..."

        self.progress=ttk.Progressbar(self.frame,orient="horizontal",mode="determinate")
        self.progress.grid(row=2,column=0)
        self.update_idletasks()
        time.sleep(0.1)
        
        #####################################   FETCHING CURRENCY RATES   #####################################
        
        self.BTCcurrencydata=self.req.get_product_trades("BTC-USD") #Use the last trade made at the time of request as the way of fetching the currency value. Done for all currencies.
        self.BTCval=float(self.BTCcurrencydata[0]["price"])
        self.ETHcurrencydata=self.req.get_product_trades("ETH-USD")
        self.ETHval=float(self.ETHcurrencydata[0]["price"])
        self.LTCcurrencydata=self.req.get_product_trades("LTC-USD")
        self.LTCval=float(self.LTCcurrencydata[0]["price"])

        self.progress["value"]=6
        self.update_idletasks()
        time.sleep(0.1)

        #####################################   UPDATING LABELS AND FIGURES   #####################################
        
        self.balabel.config(text="Balance (USD): $"+str(round(float(self.balance),2)))
        self.BTClabel.config(text="Balance (BTC): "+str(self.BTCbal)+" BTC")
        self.ETHlabel.config(text="Balance (ETH): "+str(self.ETHbal)+" ETH")
        self.LTClabel.config(text="Balance (LTC): "+str(self.LTCbal)+" LTC")

        print "Exchange rates retrieved."
        print "------------------------"
        print "BTC= $"+str(self.BTCval)
        print "ETH= $"+str(self.ETHval)
        print "LTC= $"+str(self.LTCval)
        print "------------------------"
        
        
        #####################################   PLOTTING BTC VALUE VS TIME GRAPH    #####################################
        
        print "Receiving BTC data..."
        
        self.bdata=self.req.get_product_historic_rates("BTC-USD",start=(datetime.datetime.utcnow()-datetime.timedelta(days=7)).isoformat(),end=datetime.datetime.utcnow().isoformat(),granularity="1500") #Maximum granularity for this specific time-frame, the server does not allow requests that result in anything more than ~400 data points.

        self.progress["value"]=12
        self.update_idletasks()
        time.sleep(0.1)
        
        print "BTC data retrieved, generating lists and graph..."
        
        self.BTCdata=[]
        for i in range(len(self.bdata)):
            self.BTCaveragedatapoint=(((self.bdata[i][1]+self.bdata[i][2])/2)+((self.bdata[i][3]+self.bdata[i][4])/2))/2  #Average High/Low Vs. Average Open/Close - epoch time difference is about 2 minutes so this should be fine.
            self.BTCdata.append(self.BTCaveragedatapoint)

        self.progress["value"]=18
        self.update_idletasks()
        time.sleep(0.1)
        
        self.BTCtimes=[]
        for i in range(len(self.bdata)):
            self.BTCtimes.append(datetime.datetime.fromtimestamp(self.bdata[i][0])) #Convert from UNIX time to ISO format.

        self.BTCdates=matplotlib.dates.date2num(self.BTCtimes) #Convert numbers to values that are recognized and usable by matplotlib.

        self.progress["value"]=20
        self.update_idletasks()
        time.sleep(0.1)
        
        self.BTCf=Figure(figsize=(10,4),dpi=100) #Create figure.
        self.BTCp=self.BTCf.add_subplot(111,xlabel='Time (YY-MM-DD)', ylabel='BTC-USD', title='BTC Value Vs. Time (Past Week)') #Place the graph inside this figure.
        self.BTCp.plot_date(self.BTCdates,self.BTCdata,"c-",label="Precise BTC Value") #Real data plot.
        self.BTCp.plot(numpy.unique(self.BTCdates),numpy.poly1d(numpy.polyfit(self.BTCdates,self.BTCdata,1))(numpy.unique(self.BTCdates)),label="BTC Best Line Fit Trend") #Line of best fit plot.

        self.BTCp.legend(loc='upper left')

        self.progress["value"]=30
        self.update_idletasks()
        time.sleep(0.1)
        
        print "BTC data and plot ready."
        
        #####################################   PLOTTING ETH VALUE VS TIME GRAPH    #####################################

        #SAME PROCEDURE AS IN BTC FROM NOW ONWARDS.
        
        print "Receiving ETH data..."
        
        self.edata=self.req.get_product_historic_rates("ETH-USD",start=(datetime.datetime.utcnow()-datetime.timedelta(days=7)).isoformat(),end=datetime.datetime.utcnow().isoformat(),granularity="1500") #Granularity is about 400 at 24 hours

        self.progress["value"]=36
        self.update_idletasks()
        time.sleep(0.1)
        
        print "ETH data retrieved, generating lists and graph..."

        self.ETHdata=[]
        for i in range(len(self.edata)):
            self.ETHaveragedatapoint=(((self.edata[i][1]+self.edata[i][2])/2)+((self.edata[i][3]+self.edata[i][4])/2))/2  #Average High/Low Vs. Average Open/Close - epoch time difference is about 2 minutes so this should be fine.
            self.ETHdata.append(self.ETHaveragedatapoint)
        
        self.ETHtimes=[]
        for i in range(len(self.edata)):
            self.ETHtimes.append(datetime.datetime.fromtimestamp(self.edata[i][0]))
        self.ETHdates=matplotlib.dates.date2num(self.ETHtimes)

        self.progress["value"]=43
        self.update_idletasks()
        time.sleep(0.1)
        
        self.ETHf=Figure(figsize=(10,4),dpi=100)
        self.ETHp=self.ETHf.add_subplot(111,xlabel='Time (YY-MM-DD)', ylabel='ETH-USD', title='ETH Value Vs. Time (Past Week)')
        self.ETHp.plot_date(self.ETHdates,self.ETHdata,"c-",label="Precise ETH Value")
        self.ETHp.plot(numpy.unique(self.ETHdates),numpy.poly1d(numpy.polyfit(self.ETHdates,self.ETHdata,1))(numpy.unique(self.ETHdates)),label="ETH Best Line Fit Trend")
        self.ETHp.legend(loc='upper left')

        self.progress["value"]=48
        self.update_idletasks()
        time.sleep(0.1)

        print "ETH data and plot ready."
        
        #####################################   PLOTTING LTC VALUE VS TIME GRAPH    #####################################
        
        print "Receiving LTC data..."

        self.ldata=self.req.get_product_historic_rates("LTC-USD",start=(datetime.datetime.utcnow()-datetime.timedelta(days=7)).isoformat(),end=datetime.datetime.utcnow().isoformat(),granularity="1500") #Granularity is about 400 at 24 hours

        self.progress["value"]=54
        self.update_idletasks()
        time.sleep(0.1)

        print "LTC data retrieved, generating lists and graph..."

        self.LTCdata=[]
        for i in range(len(self.ldata)):
            self.LTCaveragedatapoint=(((self.ldata[i][1]+self.ldata[i][2])/2)+((self.ldata[i][3]+self.ldata[i][4])/2))/2  #Average High/Low Vs. Average Open/Close - epoch time difference is about 2 minutes so this should be fine.
            self.LTCdata.append(self.LTCaveragedatapoint)
            
        self.LTCtimes=[]
        for i in range(len(self.ldata)):
            self.LTCtimes.append(datetime.datetime.fromtimestamp(self.ldata[i][0]))
        self.LTCdates=matplotlib.dates.date2num(self.LTCtimes)

        self.progress["value"]=61
        self.update_idletasks()
        time.sleep(0.1)

        self.LTCf=Figure(figsize=(10,4),dpi=100)
        self.LTCp=self.LTCf.add_subplot(111,xlabel='Time (YY-MM-DD)', ylabel='LTC-USD', title='LTC Value Vs. Time (Past Week)')
        self.LTCp.plot_date(self.LTCdates,self.LTCdata,"c-",label="Precise LTC Value")
        self.LTCp.plot(numpy.unique(self.LTCdates),numpy.poly1d(numpy.polyfit(self.LTCdates,self.LTCdata,1))(numpy.unique(self.LTCdates)),label="LTC Best Line Fit Trend")
        self.LTCp.legend(loc='upper left')

        self.progress["value"]=68
        self.update_idletasks()
        time.sleep(0.1)

        print "LTC data and plot ready."

        self.BTCvaldisp.config(text="BTC: $"+str(self.BTCval)+" |  "+str(self.BTCtrendval))
        self.ETHvaldisp.config(text="ETH: $"+str(self.ETHval)+" |  "+str(self.ETHtrendval))
        self.LTCvaldisp.config(text="LTC: $"+str(self.LTCval)+" |  "+str(self.LTCtrendval))

        self.progress["value"]=75
        self.update_idletasks()
        time.sleep(0.1)

        #####################################   UPDATE TRANSACTION LOGS    #####################################    

        print "Updating logs and stats..."
        
        flog=open(Logwin.userid+".txt")
        tnew=flog.readlines()
        flog.close()
        if len(tnew)>6:
            self.logs=tnew[6:] #The first 6 lines are for user information, logs are from 7th line onward.

        self.progress["value"]=77
        self.update_idletasks()
        time.sleep(0.1)

        #####################################   CALCULATING TOTAL EARNINGS/LOSS    #####################################

        
        if self.logs==[]:
            self.totalchange=0
        else:
            #Total change = Total withdrawn - Total invested
            self.TotalInvested=0
            self.TotalWithdrawn=0
            
            self.BTCinvested=0
            self.BTCwithdrawn=0

            self.ETHinvested=0
            self.ETHwithdrawn=0

            self.LTCinvested=0
            self.LTCwithdrawn=0
            for i in range(len(self.logs)): #Accumulate all investments/cashouts together, also do this by currency.
                if "Investment" in self.logs[i]:
                    self.TotalInvested+=float(self.logs[i].strip().split("@")[2])
                    if "BTC" in self.logs[i]:
                        self.BTCinvested+=float(self.logs[i].strip().split("@")[2])
                    elif "ETH" in self.logs[i]:
                        self.ETHinvested+=float(self.logs[i].strip().split("@")[2])
                    else:
                        self.LTCinvested+=float(self.logs[i].strip().split("@")[2])
                        
                elif "Cashout" in self.logs[i]:
                    self.TotalWithdrawn+=float(self.logs[i].strip().split("@")[2])
                    if "BTC" in self.logs[i]:
                        self.BTCwithdrawn+=float(self.logs[i].strip().split("@")[2])
                    elif "ETH" in self.logs[i]:
                        self.ETHwithdrawn+=float(self.logs[i].strip().split("@")[2])
                    else:
                        self.LTCwithdrawn+=float(self.logs[i].strip().split("@")[2])

            self.progress["value"]=81
            self.update_idletasks()
            time.sleep(0.1)
                        
            self.totalchange=self.TotalWithdrawn-self.TotalInvested #Update the nominal amount of profit made so far. Format color accordingly.

            self.BTCdelta=self.BTCwithdrawn-self.BTCinvested #Update the profit figure specific to the currency.
            self.ETHdelta=self.ETHwithdrawn-self.ETHinvested
            self.LTCdelta=self.LTCwithdrawn-self.LTCinvested

            self.progress["value"]=84
            self.update_idletasks()
            time.sleep(0.1)

            if self.totalchange>0: #Format the label according to the delta signs.
                self.totdeltadisp.config(text="$ "+str(round(self.totalchange,2)),fg="dark green")
            elif self.totalchange<0:
                self.totdeltadisp.config(text="$ "+str(round(self.totalchange,2)),fg="red")
            else:
                self.totdeltadisp.config(text="$ "+str(round(self.totalchange,2)))

            if self.BTCdelta>0:
                self.BTCdeltadisp.config(text="BTC: $ "+str(round(self.BTCdelta,2)),fg="dark green")
            elif self.BTCdelta<0:
                self.BTCdeltadisp.config(text="BTC: $ "+str(round(self.BTCdelta,2)),fg="red")
            else:
                self.BTCdeltadisp.config(text="BTC: $ "+str(round(self.BTCdelta,2)))
                
            if self.ETHdelta>0:
                self.ETHdeltadisp.config(text="ETH: $ "+str(round(self.ETHdelta,2)),fg="dark green")
            elif self.ETHdelta<0:
                self.ETHdeltadisp.config(text="ETH: $ "+str(round(self.ETHdelta,2)),fg="red")
            else:
                self.ETHdeltadisp.config(text="ETH: $ "+str(round(self.ETHdelta,2)))

                
            if self.LTCdelta>0:
                self.LTCdeltadisp.config(text="LTC: $ "+str(round(self.LTCdelta,2)),fg="dark green")
            elif self.LTCdelta<0:
                self.LTCdeltadisp.config(text="LTC: $ "+str(round(self.LTCdelta,2)),fg="red")
            else:
                self.LTCdeltadisp.config(text="LTC: $ "+str(round(self.LTCdelta,2)))

        self.progress["value"]=89
        self.update_idletasks()
        time.sleep(0.1)

        #####################################   CALCULATING CURRENCY TRENDS    #####################################

        print "Running data analysis..."
        
        self.BTC24hr=((self.BTCval-self.BTCdata[57])/self.BTCdata[57])*100 #Because 24 hours consists of ~58 data points. The difference between today's rates and yesterday's is ratioed.
        self.BTC1wk=((self.BTCval-self.BTCdata[len(self.BTCdata)-1])/self.BTCdata[len(self.BTCdata)-1])*100 #Last data bucket is the beginning of the week-long interval. The difference between today's rates and last week's is ratioed.

        self.ETH24hr=((self.ETHval-self.ETHdata[57])/self.ETHdata[57])*100
        self.ETH1wk=((self.ETHval-self.ETHdata[len(self.ETHdata)-1])/self.ETHdata[len(self.ETHdata)-1])*100

        self.LTC24hr=((self.LTCval-self.LTCdata[57])/self.LTCdata[57])*100
        self.LTC1wk=((self.LTCval-self.LTCdata[len(self.LTCdata)-1])/self.LTCdata[len(self.LTCdata)-1])*100

        self.progress["value"]=95
        self.update_idletasks()
        time.sleep(0.1)


        if self.BTC24hr>0 and self.BTC1wk>0: #If both trends are positive, then there is a steady increase in the value.
            self.BTCvaldisp.config(text="BTC: $"+str(self.BTCval)+" |  "+str(round(self.BTC24hr,3))+"% | "+str(round(self.BTC1wk,3))+"%",fg="dark green")
        elif self.BTC24hr<0 and self.BTC1wk<0: #If both trends are negative, then there is a steady decrease in the value.
            self.BTCvaldisp.config(text="BTC: $"+str(self.BTCval)+" |  "+str(round(self.BTC24hr,3))+"% | "+str(round(self.BTC1wk,3))+"%",fg="red")
        else: #Otherwise, it is a bit shaky/stable.
            self.BTCvaldisp.config(text="BTC: $"+str(self.BTCval)+" |  "+str(round(self.BTC24hr,3))+"% | "+str(round(self.BTC1wk,3))+"%")

        if self.ETH24hr>0 and self.ETH1wk>0:
            self.ETHvaldisp.config(text="ETH: $"+str(self.ETHval)+" |  "+str(round(self.ETH24hr,3))+"% | "+str(round(self.ETH1wk,3))+"%",fg="dark green")
        elif self.ETH24hr<0 and self.ETH1wk<0:
            self.ETHvaldisp.config(text="ETH: $"+str(self.ETHval)+" |  "+str(round(self.ETH24hr,3))+"% | "+str(round(self.ETH1wk,3))+"%",fg="red")
        else:
            self.ETHvaldisp.config(text="ETH: $"+str(self.ETHval)+" |  "+str(round(self.ETH24hr,3))+"% | "+str(round(self.ETH1wk,3))+"%")

        if self.LTC24hr>0 and self.LTC1wk>0:
            self.LTCvaldisp.config(text="LTC: $"+str(self.LTCval)+" |  "+str(round(self.LTC24hr,3))+"% | "+str(round(self.LTC1wk,3))+"%",fg="dark green")
        elif self.LTC24hr<0 and self.LTC1wk<0:
            self.LTCvaldisp.config(text="LTC: $"+str(self.LTCval)+" |  "+str(round(self.LTC24hr,3))+"% | "+str(round(self.LTC1wk,3))+"%",fg="red")
        else:
            self.LTCvaldisp.config(text="LTC: $"+str(self.LTCval)+" |  "+str(round(self.LTC24hr,3))+"% | "+str(round(self.LTC1wk,3))+"%")

        self.progress["value"]=100
        self.update_idletasks()
        time.sleep(0.1)

        print "Data analysis complete."

        self.progress.grid_forget()
        self.showplot() #Update the matplotlib canvas.
        
        self.update() #Update all Tkinter elements on the window.

        print "Done."



    def invest(self):
        print "Invest"
        investor=Investment(self.balance) #Create Investment Window Toplevel object.

    def showlogs(self):
        print "Logs"
        logger=LogsWindow(self.logs) #Create Logs Window Toplevel object.

    def cashout(self):
        print "Cashout"
        cashoutwin=Withdrawal() #Create Cashout Window Toplevel object.

    def helpme(self):
        print "Help"
        helper=Instructions() #Create Help Window Toplevel object.
        

    def showplot(self):
        stat=self.selvar.get()
        if stat==1: #BTC Choice
            canvas=FigureCanvasTkAgg(self.BTCf,master=self.frame) #Canvas where the figure is contained.
            if self.firstrun==False: #To check if there was already a canvas that it should overwrite.
                canvas.get_tk_widget().grid_forget()
                canvas.show()
                canvas.get_tk_widget().grid(row=3,column=1,columnspan=10)
            else:
                canvas.show() #Otherwise, this is the first run. Grid the canvas.
                canvas.get_tk_widget().grid(row=3,column=1,columnspan=10)
                self.firstrun=False
        elif stat==2: #ETH Choice
            canvas=FigureCanvasTkAgg(self.ETHf,master=self.frame)
            if self.firstrun==False:
                canvas.get_tk_widget().grid_forget()
                canvas.show()
                canvas.get_tk_widget().grid(row=3,column=1,columnspan=10)
            else:
                canvas.show()
                canvas.get_tk_widget().grid(row=3,column=1,columnspan=10)
                self.firstrun=False
        else:   #LTC Choice
            canvas=FigureCanvasTkAgg(self.LTCf,master=self.frame)
            if self.firstrun==False:
                canvas.get_tk_widget().grid_forget()
                canvas.show()
                canvas.get_tk_widget().grid(row=3,column=1,columnspan=10)
            else:
                canvas.show()
                canvas.get_tk_widget().grid(row=3,column=1,columnspan=10)
                self.firstrun=False


    def clientexit(self): #Exits the program.
        
        print "Exit"
        exit()



########################## INVESTMENT WINDOW CLASS ############################

class Investment(Toplevel):
    def __init__(self,userbal):
        Toplevel.__init__(self)
        self.title("Investment Window")
        self.balance=userbal
        self.geometry("600x250")
        self.frame=Frame(self)
        self.frame.pack(expand=True,fill=BOTH)
        self.received="Fill in the above fields first, then click Analyze."
        self.Potential="Fill in the above fields first, then click Analyze."
        self.USDinvestdisp=Label(self.frame,text="Amount in USD:                                                                                                      $")
        self.USDinvestdisp.grid(row=0,column=2)
        self.USDinvest=Entry(self.frame)
        self.USDinvest.grid(row=0,column=3)
        self.USDinvest.focus() #Automatically selects the entry field.

        self.CurrencyChoice=Label(self.frame,text="What do you want to invest in?")
        self.CurrencyChoice.grid(row=2,column=2)
        
        self.CurrencyVar=IntVar() #Selection variable
        self.BTCselect=Radiobutton(self.frame,text="BTC",variable=self.CurrencyVar,value=1)
        self.BTCselect.grid(row=3,column=0)
        self.ETHselect=Radiobutton(self.frame,text="ETH",variable=self.CurrencyVar,value=2)
        self.ETHselect.grid(row=3,column=2)
        self.LTCselect=Radiobutton(self.frame,text="LTC",variable=self.CurrencyVar,value=3)
        self.LTCselect.grid(row=3,column=3)
        self.BTCselect.select() #Default selection

        self.receivedisp=Label(self.frame,text="You would receive:  "+self.received)
        self.receivedisp.grid(row=5,column=2)

        self.spacer=Label(self.frame,text="")
        self.spacer.grid(row=6,column=2)

        self.Potentialdisp=Label(self.frame,text="Net earning wihin one week:   "+self.Potential)
        self.Potentialdisp.grid(row=7,column=2)

        self.spacer2=Label(self.frame,text="")
        self.spacer2.grid(row=8,column=2)

        self.Analyzebtn=Button(self.frame,text="Analyze",command=lambda: self.InvestAnalyze(self.CurrencyVar.get(),self.USDinvest.get()))
        self.Analyzebtn.grid(row=9,column=2)

        self.spacer3=Label(self.frame,text="")
        self.spacer3.grid(row=10,column=2)

        self.Investbtn=Button(self.frame,text="Invest!",command=lambda: self.InvestFunction(self.CurrencyVar.get(),self.USDinvest.get()))
        self.Investbtn.grid(row=11,column=2)
        

    def InvestAnalyze(self,choice,USDamount): #This function checks how much the user would earn within one week period based on the daily and weekly trends of the selected cryptocurrency.
        if float(USDamount)>self.balance: #Check for illegal inputs.
            tkMessageBox.showinfo("Invalid input.","You cannot invest with more than what you have.\nPlease lower the investment value or top up your USD Balance.")
            self.lift() #Raise the window back up after closing the message box.
        elif float(USDamount)<0:
            tkMessageBox.showinfo("Invalid input.","You cannot invest a negative amount of money.\nMake sure that the investment amount is a positive value.")
            self.lift()
        elif float(USDamount)==0:
            tkMessageBox.showinfo("Zero investment.","Your investment cannot be zero. You might as well not do anything.")
            self.lift()
        else:

            #####################################   ANALYZING BTC INVESTMENT    #####################################
            
            if choice==1: #BTC Choice
                self.received=str(float(USDamount)/AppWin.BTCval)+" BTC"
                self.BTCpredicted24hr=float(USDamount)*(((AppWin.BTC24hr/100)+1)**7) #7 day delta based on extrapolating the 24 hour trend throughout the week. So it goes as Amount*(1+trend ration)^time, similar to compound interest.
                self.BTCpredicted1wk=float(USDamount)*(1+(AppWin.BTC1wk/100)) #Extrapolating the weekly growth by multiplying the current value with 1+trend ratio.
                self.Potential=(self.BTCpredicted24hr+self.BTCpredicted1wk)/2 #Average the result we get from both extrapolations.
                self.receivedisp.config(text="You would receive:  "+self.received)
                if self.Potential-float(USDamount)<0: #Format according to numerical signs.
                    self.Potentialdisp.config(text="Net earning wihin one week:  $ "+str(self.Potential-float(USDamount)),fg="red")
                else:
                    self.Potentialdisp.config(text="Net earning wihin one week:  $ "+str(self.Potential-float(USDamount)))
                    

            #####################################   ANALYZING ETH INVESTMENT    #####################################
            
            elif choice==2: #ETH Choice
                self.received=str(float(USDamount)/AppWin.ETHval)+" ETH"
                self.ETHpredicted24hr=float(USDamount)*(((AppWin.ETH24hr/100)+1)**7) #7 day delta based on extrapolating the 24 hour trend throughout the week.
                self.ETHpredicted1wk=float(USDamount)*(1+(AppWin.ETH1wk/100))
                self.Potential=(self.ETHpredicted24hr+self.ETHpredicted1wk)/2 #Average the result we get from both extrapolations.
                self.receivedisp.config(text="You would receive:  "+self.received)
                if self.Potential-float(USDamount)<0:
                    self.Potentialdisp.config(text="Net earning wihin one week:  $ "+str(self.Potential-float(USDamount)),fg="red")
                else:
                    self.Potentialdisp.config(text="Net earning wihin one week:  $ "+str(self.Potential-float(USDamount)))


            #####################################   ANALYZING LTC INVESTMENT    #####################################
                
            elif choice==3: #LTC Choice
                self.received=str(float(USDamount)/AppWin.LTCval)+" LTC"
                self.LTCpredicted24hr=float(USDamount)*(((AppWin.LTC24hr/100)+1)**7) #7 day delta based on extrapolating the 24 hour trend throughout the week.
                self.LTCpredicted1wk=float(USDamount)*(1+(AppWin.LTC1wk/100))
                self.Potential=(self.LTCpredicted24hr+self.LTCpredicted1wk)/2 #Average the result we get from both extrapolations.
                self.receivedisp.config(text="You would receive:  "+self.received)
                if self.Potential-float(USDamount)<0:
                    self.Potentialdisp.config(text="Net earning wihin one week:  $ "+str(float(USDamount)-self.Potential),fg="red")
                else:
                    self.Potentialdisp.config(text="Net earning wihin one week:  $ "+str(self.Potential-float(USDamount)))
                    
            else:
                self.received="0"

        

    def InvestFunction(self,choice,USDamount): #Takes an amount from the user's USD balance and converts it to a cryptocurrency of the user's choice. Then it auto-saves and logs this activity.
        if USDamount=="" or USDamount==None:
            tkMessageBox.showinfo("Empty input!","Please enter a valid figure in the entry box.")
            self.lift()
        else:
            if self.Potential-float(USDamount)<0: #Check if the user is sure to invest even though it is predicted that he would be losing money.
                self.confirminv=tkMessageBox.askyesno("Confirm investment.","The potential earning for this investment seems to be negative.\nAre you sure of your decision?")
            else:
                self.confirminv=True

            if self.confirminv==True:
                if float(USDamount)>self.balance: #Check for illegal inputs.
                    tkMessageBox.showinfo("Invalid input.","You cannot invest with more than what you have.\nPlease lower the investment value or top up your USD Balance.")
                    self.lift()
                elif float(USDamount)<0:
                    tkMessageBox.showinfo("Invalid input.","You cannot invest a negative amount of money.\nMake sure that the investment amount is a positive value.")
                    self.lift()
                elif float(USDamount)==0:
                    tkMessageBox.showinfo("Zero investment.","Your investment cannot be zero. You might as well not do anything.")
                    self.lift()
                else:
                    self.balance-=float(USDamount) #Deduct from balance and overwrite save data file. Then update cryptocurrency balance, write new investment log and overwrite the save data file.
                    self.f=open(Logwin.userid+".txt")
                    self.templist=self.f.readlines()
                    self.f.close()
                    self.templist.pop(2)
                    self.templist.insert(2,"USDbal="+str(self.balance)+"\n")
                    self.g=open(Logwin.userid+".txt","w")
                    self.g.writelines(self.templist)
                    if choice==1: #BTC Choice
                        self.g.write(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")+"@Investment@"+str(USDamount)+"@BTC@"+str(AppWin.BTCval)+"\n")
                        self.g.close()
                        AppWin.BTCbal+=float(USDamount)/AppWin.BTCval
                        AppWin.balance=self.balance
                        
                        self.f2=open(Logwin.userid+".txt")
                        self.templist2=self.f2.readlines()
                        self.f2.close()
                        self.templist2.pop(3)
                        self.templist2.insert(3,"BTCbal="+str(AppWin.BTCbal)+"\n")
                        self.g2=open(Logwin.userid+".txt","w")
                        self.g2.writelines(self.templist2)
                        self.g2.close()
                        
                    elif choice==2: #ETH Choice
                        self.g.write(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")+"@Investment@"+str(USDamount)+"@ETH@"+str(AppWin.ETHval)+"\n")
                        self.g.close()
                        AppWin.ETHbal+=float(USDamount)/AppWin.ETHval
                        AppWin.balance=self.balance

                        self.f2=open(Logwin.userid+".txt")
                        self.templist2=self.f2.readlines()
                        self.f2.close()
                        self.templist2.pop(4)
                        self.templist2.insert(4,"ETHbal="+str(AppWin.ETHbal)+"\n")
                        self.g2=open(Logwin.userid+".txt","w")
                        self.g2.writelines(self.templist2)
                        self.g2.close()
                        
                    else: #LTC Choice
                        self.g.write(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")+"@Investment@"+str(USDamount)+"@LTC@"+str(AppWin.LTCval)+"\n")
                        self.g.close()
                        AppWin.LTCbal+=float(USDamount)/AppWin.LTCval
                        AppWin.balance=self.balance

                        self.f2=open(Logwin.userid+".txt")
                        self.templist2=self.f2.readlines()
                        self.f2.close()
                        self.templist2.pop(5)
                        self.templist2.insert(5,"LTCbal="+str(AppWin.LTCbal)+"\n")
                        self.g2=open(Logwin.userid+".txt","w")
                        self.g2.writelines(self.templist2)
                        self.g2.close()
                    
                    self.destroy()
                    AppWin.refresh()
            else:
                self.lift() #If the user wasn't sure of his/her input, display the investment window.


########################## CASHOUT WINDOW CLASS ############################

class Withdrawal(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.title("Cashout Window")
        self.geometry("600x250")
        self.frame=Frame(self)
        self.frame.pack(expand=True,fill=BOTH)
        self.USDreceived="Fill in the above fields first, then click Refresh."
        self.postcashout="Fill in the above fields first, then click Refresh."
        self.selectorlabel=Label(self.frame,text="Select the currency that you'd like to withdraw from: ")
        self.selectorlabel.grid(row=0,column=1)
        self.selvar=StringVar() #Selection variable.
        self.BTCcashoutselect=Radiobutton(self.frame,text="BTC",variable=self.selvar,value="BTC",command=lambda:self.corefresh())
        self.BTCcashoutselect.grid(row=1,column=0)
        self.ETHcashoutselect=Radiobutton(self.frame,text="ETH",variable=self.selvar,value="ETH",command=lambda:self.corefresh())
        self.ETHcashoutselect.grid(row=1,column=1)
        self.LTCcashoutselect=Radiobutton(self.frame,text="LTC",variable=self.selvar,value="LTC",command=lambda:self.corefresh())
        self.LTCcashoutselect.grid(row=1,column=2)
        self.BTCcashoutselect.select() #Default selection.
        self.cashoutentrylabel=Label(self.frame,text="How much are you willing to cashout?                                                            "+self.selvar.get())
        self.cashoutentrylabel.grid(row=2,column=1)
        self.cashoutentry=Entry(self.frame)
        self.cashoutentry.grid(row=2,column=2)
        self.cashoutentry.focus()
        self.spacer1=Label(self.frame,text="")
        self.spacer1.grid(row=3,column=1)
        self.cashoutdisp=Label(self.frame,text="You get: USD "+str(self.USDreceived))
        self.cashoutdisp.grid(row=4,column=1)
        self.aftercashout=Label(self.frame,text="Total earnings after this cashout: "+self.postcashout)
        self.aftercashout.grid(row=5,column=1)
        self.spacer2=Label(self.frame,text="")
        self.spacer2.grid(row=6,column=1)
        self.cashoutrefreshbtn=Button(self.frame,text="Refresh",command=lambda:self.CashoutRefresh())
        self.cashoutrefreshbtn.grid(row=7,column=1)
        self.spacer3=Label(self.frame,text="")
        self.spacer3.grid(row=8,column=1)
        self.cashoutrefreshbtn=Button(self.frame,text="Cashout!",command=lambda:self.CashoutFunction(self.selvar.get(),self.cashoutentry.get()))
        self.cashoutrefreshbtn.grid(row=9,column=1)

    def corefresh(self): #To update the cryptocurrency symbol according the choice of the user.
        self.cashoutentrylabel.config(text="How much are you willing to cashout?                                                            "+self.selvar.get()) #This is in order to adjust the currency shown next to the entry box depending on the selection of the currency buttons.
        self.update()


    def CashoutRefresh(self): #Calculates and display the figures the the user would get if the cashout was to happen.
        costat=self.selvar.get()
        if self.cashoutentry.get()==None or self.cashoutentry.get()=="":
            tkMessageBox.showinfo("Empty input!","Please enter a valid figure in the entry box.")
            self.lift()
        else:
            if costat=="BTC":
                self.USDreceived=float(self.cashoutentry.get())*AppWin.BTCval

            elif costat=="ETH":
                self.USDreceived=float(self.cashoutentry.get())*AppWin.ETHval

            else:
                self.USDreceived=float(self.cashoutentry.get())*AppWin.LTCval

            self.postcashout=AppWin.totalchange+self.USDreceived

            if float(self.cashoutentry.get())>AppWin.BTCbal and costat=="BTC":
                self.cashoutdisp.config(text="Insufficient BTC balance.")
                self.aftercashout.config(text="Insufficient BTC balance.")

            elif float(self.cashoutentry.get())>AppWin.ETHbal and costat=="ETH":
                self.cashoutdisp.config(text="Insufficient ETH balance.")
                self.aftercashout.config(text="Insufficient ETH balance.")

            elif float(self.cashoutentry.get())>AppWin.LTCbal and costat=="LTC":
                self.cashoutdisp.config(text="Insufficient LTC balance.")
                self.aftercashout.config(text="Insufficient LTC balance.")

            else:
                self.cashoutdisp.config(text="You get: USD "+str(round(self.USDreceived,2)))
                self.aftercashout.config(text="Total earnings after this cashout: USD "+str(round(self.postcashout,2)))

            self.update()

    def CashoutFunction(self,choice,amount): #Takes an amount out of the user's cryptocurrency balance and convert it to USD, then it adds that USD amount to the user's USD balance, logs the acrivity and auto-saves.
        if amount=="" or amount==None:
            tkMessageBox.showinfo("Empty input!","Please enter a valid figure in the entry box.")
            self.lift()
        else:

            #####################################   BTC CASHOUT    #####################################
            
            if choice=="BTC":
                if float(amount)>AppWin.BTCbal:
                    tkMessageBox.showinfo("Invalid input.","You cannot cashout with more than what you have.\nPlease lower the cashout value.")
                    self.lift()
                elif float(amount)<0:
                    tkMessageBox.showinfo("Invalid input.","You cannot cashout a negative amount of money.\nMake sure that the cashout amount is a positive value.")
                    self.lift()
                elif float(amount)==0:
                    tkMessageBox.showinfo("Zero cashout.","Your cashout cannot be zero. You might as well not do anything.")
                    self.lift()
                else:
                    AppWin.balance+=float(amount)*AppWin.BTCval
                    AppWin.BTCbal-=float(amount)
                    self.f=open(Logwin.userid+".txt")
                    self.templist=self.f.readlines()
                    self.f.close()
                    self.templist.pop(2)
                    self.templist.insert(2,"USDbal="+str(AppWin.balance)+"\n")
                    self.templist.pop(3)
                    self.templist.insert(3,"BTCbal="+str(AppWin.BTCbal)+"\n")
                    self.g=open(Logwin.userid+".txt","w")
                    self.g.writelines(self.templist)
                    self.g.write(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")+"@Cashout@"+str(float(amount)*AppWin.BTCval)+"@BTC@"+str(AppWin.BTCval)+"\n")
                    self.g.close()

            #####################################   ETH CASHOUT    #####################################

            elif choice=="ETH":
                if float(amount)>AppWin.ETHbal:
                    tkMessageBox.showinfo("Invalid input.","You cannot cashout with more than what you have.\nPlease lower the cashout value.")
                    self.lift()
                elif float(amount)<0:
                    tkMessageBox.showinfo("Invalid input.","You cannot cashout a negative amount of money.\nMake sure that the cashout amount is a positive value.")
                    self.lift()
                elif float(amount)==0:
                    tkMessageBox.showinfo("Zero cashout.","Your cashout cannot be zero. You might as well not do anything.")
                    self.lift()
                else:
                    AppWin.balance+=float(amount)*AppWin.ETHval
                    AppWin.ETHbal-=float(amount)
                    self.f=open(Logwin.userid+".txt")
                    self.templist=self.f.readlines()
                    self.f.close()
                    self.templist.pop(2)
                    self.templist.insert(2,"USDbal="+str(AppWin.balance)+"\n")
                    self.templist.pop(4)
                    self.templist.insert(4,"ETHbal="+str(AppWin.ETHbal)+"\n")
                    self.g=open(Logwin.userid+".txt","w")
                    self.g.writelines(self.templist)
                    self.g.write(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")+"@Cashout@"+str(float(amount)*AppWin.ETHval)+"@ETH@"+str(AppWin.ETHval)+"\n")
                    self.g.close()

            #####################################   LTC CASHOUT    #####################################

            else:
                if float(amount)>AppWin.LTCbal:
                    tkMessageBox.showinfo("Invalid input.","You cannot cashout with more than what you have.\nPlease lower the cashout value.")
                    self.lift()
                elif float(amount)<0:
                    tkMessageBox.showinfo("Invalid input.","You cannot cashout a negative amount of money.\nMake sure that the cashout amount is a positive value.")
                    self.lift()
                elif float(amount)==0:
                    tkMessageBox.showinfo("Zero cashout.","Your cashout cannot be zero. You might as well not do anything.")
                    self.lift()
                else:
                    AppWin.balance+=float(amount)*AppWin.LTCval
                    AppWin.LTCbal-=float(amount)
                    self.f=open(Logwin.userid+".txt")
                    self.templist=self.f.readlines()
                    self.f.close()
                    self.templist.pop(2)
                    self.templist.insert(2,"USDbal="+str(AppWin.balance)+"\n")
                    self.templist.pop(5)
                    self.templist.insert(5,"LTCbal="+str(AppWin.LTCbal)+"\n")
                    self.g=open(Logwin.userid+".txt","w")
                    self.g.writelines(self.templist)
                    self.g.write(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")+"@Cashout@"+str(float(amount)*AppWin.LTCval)+"@LTC@"+str(AppWin.LTCval)+"\n")
                    self.g.close()

            self.destroy()
            AppWin.refresh()


########################## TRANSACTION RECORD WINDOW CLASS ############################
        
class LogsWindow(Toplevel):
    def __init__(self,logdata=[]):
        Toplevel.__init__(self)
        self.title("Transaction Records Window")
        self.logs=logdata
        self.frame=Frame(self)
        self.frame.pack(expand=True,fill=BOTH)
        self.LogsBanner=Label(self.frame,text="Transaction Logs") #Initialize and grid table headers/titles.
        self.LogsBanner.grid(row=0,column=3)
        self.isodates=Label(self.frame,text="Time and Date (UTC YYYY-MM-DD hh:mm:ss)")
        self.isodates.grid(row=1,column=1)
        self.transactiontype=Label(self.frame,text="Type")
        self.transactiontype.grid(row=1,column=2)
        self.AmountinUSD=Label(self.frame,text="Amount (USD)")
        self.AmountinUSD.grid(row=1,column=3)
        self.Currency=Label(self.frame,text="Curerency")
        self.Currency.grid(row=1,column=4)
        self.CurrentValue=Label(self.frame,text="Currency value in USD")
        self.CurrentValue.grid(row=1,column=5)
        if self.logs==[] or set(self.logs)==set([""]) or set(self.logs)==set(["\n"]): #If there were no meaningful logs, or ones that comply with the correct pattern of a log. (regex can also be used instead)
            self.firstlog=Label(self.frame,text="You do not have any logs to show, please go ahead and top-up, invest or cashout funds in order to display any logs.")
            self.firstlog.grid(row=2,column=3)
        else:
            for i in range(len(self.logs)): #Iterate through each log string, split and strip each element of the log. Then grid each log element into their respective columns.
                self.logsplitted=self.logs[i].split("@")
                self.clearedlog=[]
                for j in self.logsplitted:
                    self.tempstrip=j.strip()
                    if self.tempstrip!="":
                        self.clearedlog.append(self.tempstrip)
                if self.clearedlog==[] or set(self.clearedlog)==set([""]) or set(self.clearedlog)==set(["\n"]):
                    print "Empty log"
                else:
                    self.timedisplay=Label(self.frame,text=self.clearedlog[0])
                    self.typedisplay=Label(self.frame,text=self.clearedlog[1])
                    self.USDdisplay=Label(self.frame,text=self.clearedlog[2])
                    self.currencydisplay=Label(self.frame,text=self.clearedlog[3])
                    self.valuedisplay=Label(self.frame,text=self.clearedlog[4])
                    self.timedisplay.grid(row=2+i,column=1)
                    self.typedisplay.grid(row=2+i,column=2)
                    self.USDdisplay.grid(row=2+i,column=3)
                    self.currencydisplay.grid(row=2+i,column=4)
                    self.valuedisplay.grid(row=2+i,column=5)


########################## HELP PAGE CLASS ############################

class Instructions(Toplevel): #Bunch of text for new users to read.
    def __init__(self):
        Toplevel.__init__(self)
        self.title("Instructions")
        self.frame=Frame(self)
        self.frame.pack(expand=True,fill=BOTH)
        self.Welcome=Label(self.frame,text="Welcome to the Currency Investment Adviser app, this application was initially made for a course project at CMU-Q.\nThis program was developed by Selmane Tabet, an amateur Bitcoin trader and a computer engineering student at HBKU.")
        self.Welcome.pack()

        self.disclaimer=Label(self.frame,text="\nDISCLAIMER:\nTHIS APPLICATION IS MEANT TO BE USED FOR THE SAKE OF SIMULATING THE REAL CRYPTOCURRENCY MARKET.\nALL THE DATA IS PROVIDED ARE FROM THE GDAX PLATFORM AND DUE TO THE VOLATILE NATURE OF DECENTRALIZED CURRENCIES USED THEREIN, THIS APP SHOULD NOT BE USED AS THE ONLY RELIABLE TOOL FOR MARKET PREDICTIONS.\nUNFORESEEN FLUCTUATIONS WILL HAPPEN AND THIS APP WILL NOT BE ABLE TO PREDICT THEM.\nINVEST AT YOUR OWN RISK, AND ONLY USE THIS APP'S DATA AS REFERENCE!\n\n")
        self.disclaimer.pack()

        self.howto=Label(self.frame,text="How to use:\nStart off by topping up your balance using the Top Up button located at the top window menu.\nThen use the USD balance available (displayed in the top right corner) to invest into your choice of currency.\nWhen opening the Investment window, fill in the amount and choose the currency, click on Analyze and see how much you could earn (or lose) within one week timeframe.\nYou can also withdraw your investment via the Cashout window, the procedure is pretty much the same as investment, refresh and see how much you are gonna get.\nYou could also check your progress through the Earnings Breakdown and Total profit/loss figures located at the right side of the graph.\nSpeaking of the graph; you could change the currency being viewed by selecting one of circular buttons located on top of the graph.\nThis application features auto-saving and it records every action in your personal Transaction Logs, the list is accessible via the Transaction Logs button.\nUse the exchange rates and trend values located below the graph to study the current trends of the market.\nRed colored ones indicate STEADILY FALLING currencies, while green colored ones indicate STEADILY INCREASING currencies.\nBlack ones on the other hand indicate the the currency has been going up and down, and not so steady.\n\n")
        self.howto.pack()

        self.tips=Label(self.frame,text="Tips:\nIt is recommended to invest on green indicated currencies in order to catch on the profit train, but ALWAYS KEEP TRACK OF THE CURRENCY VALUE!\nYou are advised to withdraw your investment as soon as you get close to resetting back to breakeven, or even when you think that you are losing too much for that matter.\nOn the other hand, red indicated ones are dangerous to invest in, they will keep going down until the indication turns black.\nFinally, in the case of black indicated ones, those are currencies you may invest, but may carry more risk than the green colored ones because the longer term trend is sort of unknown.\nOne improtant thing; Keep an eye on the news regarding the cryptocurrency you invest in, political actions among other things that are reported in the news directly affect your investment!\nKeep in mind that this app is all about building your confidence in the cryptocurrency market and is about training your own judgement on making the right investment decision given the available data.\n\n")
        self.tips.pack()
                
        


#########################################   LOGIN STEP CODE    #########################################

            
class LoginWindow(Tk): #Login Page, where the login process takes place.
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
        self.U.focus()
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

        self.U.bind('<Return>',lambda event: self.LOGIN(self.U.get(),self.P.get())) #Keybinds to make it easier for the user to navigate.
        self.P.bind('<Return>',lambda event: self.LOGIN(self.U.get(),self.P.get()))
        
    def LOGIN(self,username,password): #Takes the password, hashes it and checks if it is correct. If so, then it will load the user's data and transfer them to the Main Window.
        if os.path.exists(username+".txt"):
            f=open(username+".txt")
            tlist=f.readlines()
            for i in range(len(tlist)):
                tlist[i]=tlist[i].strip()
            salt=tlist[0] #Salt of the target password.
            target=tlist[1] #Target hashed string.
            hashedpw=bcrypt.hashpw(password+salt+"ROFLMAOXD",salt) #Attempt to hash the provided password with the salt of the target password.
            if hashedpw==target: #Compare if the hashed password matches the target hashed string.
                self.USDbalance=float(tlist[2][7:]) #Extract the numbers, they are placed starting from the 8th character of each line.
                self.BTCbalance=float(tlist[3][7:])
                self.ETHbalance=float(tlist[4][7:])
                self.LTCbalance=float(tlist[5][7:])
                if len(tlist)>6: #Anything after the 6th line (LTC balance in this case) is a log in the form of date@type@USD@cryptocurrency@cryptocurrencyvalue.
                    self.logunsplit=tlist[6:] #Take every remaining line and append each log into the self.logs list.
                    self.logs=[]
                    for i in range(len(self.logunsplit)):
                        self.logs.append(self.logunsplit[i].split("@")) #Split each log line by the @'s.
                else:
                    self.logs=[] #No logs detected otherwise.
                tkMessageBox.showinfo("Success!","Login successful! Welcome to the trading world!")
                self.loggedin=True #Set this in order to be able to proceed to the Main Window upon Login window destruction.
                self.userid=username #To make the auto-save feature in the Main Window object recall the username every time it autosaves.
                self.destroy()
            else:
                tkMessageBox.showinfo("Wrong credentials","Wrong password, please try again.")
            
        else:
            tkMessageBox.showinfo("Wrong credentials","Username incorrect or does not exist.\nIf you are a new user, create an account before logging in.")

    def newacc(self): #Account creation function.
        new=AccCreation() #Create Account Creation Toplevel object.
        
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
        self.U.focus()
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
        
        self.U.bind('<Return>',lambda event: self.Create(self.U.get(),self.P.get(),self.Pcon.get())) #Keybinds to make it easier for the user to navigate.
        self.P.bind('<Return>',lambda event: self.Create(self.U.get(),self.P.get(),self.Pcon.get()))
        self.Pcon.bind('<Return>',lambda event: self.Create(self.U.get(),self.P.get(),self.Pcon.get()))
        

    def Create(self,username,password,passconf):
        if os.path.exists(username+".txt"): #Check if the username exists.
            tkMessageBox.showinfo("Username taken","Username already exists, enter a different username.")
            self.lift() #Take the Account Creation window back to the top of the window stack.
        elif username=="" or password=="" or passconf=="": #Check for null input.
            tkMessageBox.showinfo("Invalid input!","Make sure you have filled in all the fields!")
            self.lift()
        elif password!=passconf: #Check if the passwords match.
            tkMessageBox.showinfo("Invalid input!","Passwords do not match!\nMake sure that you have typed the passwords correctly.")
            self.lift()
        
        else:
            f=open(username+".txt","w") #Create save data file. Write the salt, hashed string and default values (zeros in this case) into the save file.
            salt=bcrypt.gensalt()
            f.write(salt+"\n")
            f.write(bcrypt.hashpw(password+salt+"ROFLMAOXD", salt)+"\n")
            f.write("USDbal=0\n")
            f.write("BTCbal=0\n")
            f.write("ETHbal=0\n")
            f.write("LTCbal=0\n")
            f.close()
            tkMessageBox.showinfo("Creation success!","Account successfully created!\nYou may now login with your credentials.")
            self.destroy() #Back to login.

            
Logwin=LoginWindow() #Initialize and display the Login screen.
Logwin.mainloop()

if Logwin.loggedin==False:
    os._exit(0) #If the user destroyed the window, exit the whole program and do not initialize Main window.
else:
    AppWin=Mainw(usd=Logwin.USDbalance,btc=Logwin.BTCbalance,eth=Logwin.ETHbalance,ltc=Logwin.LTCbalance,logslist=Logwin.logs) #Initialize and display the Main window otherwise.
    AppWin.mainloop()
