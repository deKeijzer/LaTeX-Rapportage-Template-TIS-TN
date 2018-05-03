import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
from appJar import gui
import matplotlib.axes as ax
import matplotlib.ticker as mtick
import TISTNplot as TN
import tkinter as tk
from tkinter import filedialog
from tkinter import *

#Variabelen aanduiding
rawbestandDT = ""
Afstand = 0.376
vtext = "De gemiddelde snelheid in c = "
DTtext = "De gemiddelde delta time ongeacht van richting (ns) = "

def uitvoeren():
    rawdataDT = pd.read_csv(rawbestandDT,sep='\t',header=1,names=['Time','Counts'])
    CountsDT = rawdataDT['Counts']
    TimeDT = rawdataDT['Time']
    CountsSum = 0

    for n in range (0,len(TimeDT)):
        if CountsDT[n] > 0:
            CountsSum = CountsSum + CountsDT[n] * abs(TimeDT[n])

    hits = np.sum(CountsDT)
    DTavg = CountsSum/hits
    v = Afstand/(DTavg*10**(-9))
    global DTtext
    DTtext = "De gemmidelde delta time ongeacht van richting (ns) = %s" %DTavg
    vlight = v/(2.998*10**8)
    global vtext
    vtext = "De gemiddelde snelheid in c = %s" %vlight

    TimeDTplot = []
    CountsDTplot = []

    def sliceDT(linkergrens, rechtergrens):
        for n in range (0, len(TimeDT)):
            if TimeDT[n] >= linkergrens and TimeDT[n] <= rechtergrens:
                TimeDTplot.append(TimeDT[n])
                CountsDTplot.append(CountsDT[n])
        return TimeDTplot, CountsDTplot

    width = 1 / 2
    sliceDT(-10,10)
    x = np.array(TimeDTplot)
    y = np.array(CountsDTplot)

    n = len(x)
    mean = sum(x * y) / sum(y)
    sigma = np.sqrt(sum(y * (x - mean)**2) / sum(y))

    def gaus(x,a,x0,sigma):
        return a*np.exp(-(x-x0)**2/(2*sigma**2))

    popt, pcov = curve_fit(gaus,x,y,p0=[1,mean,sigma])

    plt.xlabel("Delta time (ns)")
    plt.ylabel("Counts")
    plt.xlim(-10,10)
    #TN.PRECISION_Y = 3         #
    #TN.PRECISION_X = 2         #Significantie
    #TN.fix_axis(plt.gca())
    #plt.ticklabel_format(style='sci',scilimits=(0,3),axis='both',useLocale='true')
    MuSigmaText = r'$\mu=%s\ ns, \sigma=%s$ ns' % (round(mean, 2), round(sigma,2))
    MuText = r'$\mu=%s$ ns' % (round(mean, 2))
    SigmaText = r'$\sigma=%s$ ns' % (round(sigma, 2))
    DTabsavgText = r'$\overline{|Delta Time|}=%s$' % round(DTavg, 2)
    plt.text((-0.95*max(TimeDTplot)), (max(CountsDTplot)), MuText)
    plt.text((-0.95*max(TimeDTplot)), 0.95*(max(CountsDTplot)), SigmaText)
    #plt.text((0.45*max(TimeDTplot)), (0.93*max(CountsDTplot)), DTabsavgText)

    plt.bar(TimeDTplot, CountsDTplot, width, color="blue", edgecolor="black",)
    plt.plot(x, gaus(x,*popt),'r:',label='fit', linewidth=2.5)
    global rawbestandDTplotnaam
    rawbestandDTplotnaam = rawbestandDT.replace(".txt",".png")
    plt.savefig(rawbestandDTplotnaam)
    #plt.show()

#GUI Buttons werking
def press(button):
    if button == "Stoppen":
        app.stop()
    if button == "Bestand kiezen":
        root = Tk()
        root.filename = filedialog.askopenfilename(initialdir="/", title="Kies het delta time bestand",
                                                   filetypes=(("txt bestanden", "*.txt"), ("all files", "*.*")))
        global rawbestandDT
        rawbestandDT = root.filename
        root.withdraw()
        app.setLabel("bestandinput", rawbestandDT)
    if button == "Verwerk":
        app.startLabelFrame("Delta time verdeling")
        uitvoeren()
        app.addImage("DTplot", rawbestandDTplotnaam)
        app.stopLabelFrame()
        app.setLabel("v",vtext)
        app.setLabel("DT",DTtext)
    if button == "Afstand instellen":
        global Afstand
        Afstand = app.getEntry("Afstand")

#GUI
app = gui("Data analysis Muonlab", "600x800")
app.addLabel("title", "Welkom in muonlab delta time data analyse")
app.setBg("white")
app.addNumericEntry("Afstand")
app.setEntryDefault("Afstand", "Afstand tussen de muonenbalken (m), default = 0.376 m")
app.addButtons(["Bestand kiezen", "Afstand instellen"], press)
app.addButtons(["Verwerk", "Stoppen"], press)
app.addLabel("bestandinputtext", "Huidig gekozen bestand:")
app.addLabel("bestandinput", "")
app.addLabel("v", vtext)
app.addLabel("DT", DTtext)
app.go()
#Einde GUI


