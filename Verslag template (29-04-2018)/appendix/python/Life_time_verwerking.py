import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.axes as ax
import matplotlib.ticker as mtick
import TISTNplot as TN
import glob
import os
from tkinter import filedialog
from tkinter import *
from appJar import gui

#Variablen
rawbestandLT = ""
n = 50

def uitvoeren():
    #rawbestandLT = 'data/Datalog_LT_3Days_Treshold_150_PMT_1250.txt'
    rawdataLT = pd.read_csv(rawbestandLT,sep='\t',header=1,names=['Time','Counts'])
    CountsLT = rawdataLT['Counts']
    TimeLT = rawdataLT['Time']
    hits = np.sum(CountsLT)
    '''
    TimeLTmovingavg = np.zeros(len(TimeLT)/5)
    interval = 10
    for n in range (len(TimeLT)):
        nmin = n
        nmax = n + interval
        TimeLTmovingavg[n] = TimeLT[nmin:nmax].sum()/interval
    '''
    def summed_data(a):
        data = np.zeros(len(a)/n)
        for d in range(0,(len(data))):
            dmin = n*d
            dmax = n*d + n
            data[d] = a[dmin:dmax].sum()
        return data

    SummedCountsLT = summed_data(CountsLT)
    SummedTimeLT = TimeLT[0:(len(SummedCountsLT))]*n

    def func(x, a, b, c):
        return a * np.exp(-b * x) + c

    popt, pcov = curve_fit(func,SummedTimeLT,SummedCountsLT)
    plt.xlabel("Life time (ns)")
    plt.ylabel("Counts")
    plt.grid(True)
    plt.ylim(-0.3,70)
    plt.xlim(0.5,20)
    #plt.semilogx(10, np.sin(2*np.pi*3*10))
    #TN.PRECISION_Y = 3         #
    #TN.PRECISION_X = 2         #Significantie
    #TN.fix_axis(plt.gca())
    #plt.ticklabel_format(style='sci',scilimits=(0,3),axis='both',useLocale='true')
    #MuSigmaText = r'$\mu=%s,\ \sigma=%s$' % (round(mean, 2), round(sigma,2))
    #DTabsavgText = r'$\overline{|Delta Time|}=%s$' % round(DTavg, 2)
    #plt.text((0.45*max(TimeDTplot)), (max(CountsDTplot)), MuSigmaText)
    #plt.text((0.45*max(TimeDTplot)), (0.93*max(CountsDTplot)), DTabsavgText)

    #plt.bar(TimeDTplot, CountsDTplot, width, color="blue", edgecolor="black",)
    plt.plot(TimeLT, func(TimeLT, *popt), 'r--')
    plt.plot(SummedTimeLT, SummedCountsLT,'bo', linewidth=2.5)
    global rawbestandLTplotnaam
    rawbestandLTplotnaam = rawbestandLT.replace(".txt",".png")
    plt.savefig(rawbestandLTplotnaam)

#GUI Buttons werking
def press(button):
    if button == "Stoppen":
        app.stop()
    if button == "Bestand kiezen":
        root = Tk()
        root.filename = filedialog.askopenfilename(initialdir="/", title="Kies het delta time bestand",
                                                   filetypes=(("txt bestanden", "*.txt"), ("all files", "*.*")))
        global rawbestandLT
        rawbestandLT = root.filename
        root.withdraw()
        app.setLabel("bestandinput", rawbestandLT)
    if button == "Verwerk":
        app.startLabelFrame("Life time verdeling")
        uitvoeren()
        app.addImage("LTplot", rawbestandLTplotnaam)
        app.stopLabelFrame()
        #app.setLabel("")
    if button == "Instellen":
        global n
        n = app.getEntry("n")

#GUI
app = gui("Data analysis Muonlab", "600x800")
app.addLabel("title", "Welkom in Muonlab lifetime data analyse")
app.setBg("white")
app.addButtons(["Bestand kiezen", "Instellen"], press)
app.addNumericEntry("n")
app.setEntryDefault("n", "Aantal datapunten die samengevoegd worden, default = 50")
app.addButtons(["Stoppen", "Verwerk"], press)
app.addLabel("bestandinputtext", "Huidig gekozen bestand:")
app.addLabel("bestandinput", "")
app.go()
#Einde GUI
