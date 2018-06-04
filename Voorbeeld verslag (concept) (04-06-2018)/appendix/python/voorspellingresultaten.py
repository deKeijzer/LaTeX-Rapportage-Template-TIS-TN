
# coding: utf-8

# In[71]:


import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress
#%matplotlib notebook
import TISTNplot as tn

# Nodig voor latex rendering
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

U_H = '-'
I = '-'
B = '-'
d = 5*10**-5
#n = 6.6*10**28
e = 1.60217662*10**-19

def f(I, n):
    B = 0.3
    d = 5*10**-5
    #n = 6.6*10**28
    e = 1.60217662*10**-19

    return (B*I)*10**6/(n*e*d*10**28)

n_list = [4.7, 2.65, 1.4, 1.15, 0.91, 8.47, 5.86]
B = []
U1 = []
U2 = []
U3 = []
U4 = []
U5 = []

for b in range(1, 30):
    B.append(b)
    U1.append(f(1, b)*10**0)
    U2.append(f(5, b)*10**0)
    U3.append(f(10, b)*10**0)
    U4.append(f(15, b)*10**0)
    U5.append(f(20, b)*10**0)


# In[109]:


plt.plot(B, U1, '.', label='1 A')
plt.plot(B, U2, 'v', label="5 A")
plt.plot(B, U3, 'x', label="10 A")
plt.plot(B, U4, '+', label="15 A")
plt.plot(B, U5, '*', label="20 A")


#fill plot
plt.fill_between(B, U1, U5, color='pink', alpha='0.3')

plt.xlabel('Charge carrier density $n$ \quad \cdot 10^{28} \quad [m^{-3}]')
plt.ylabel('Hall voltage $U_H$ \mathrm{[\mu V]}}')

#correcte opmaak
tn.PRECISION_X = 3
tn.PRECISION_Y = 3
tn.fix_axis(plt.gca())

plt.legend()
plt.grid()
#plt.xlim(1**26, 1**27)

props = dict(boxstyle='square', facecolor='wheat', alpha=0.75)
plt.text(10, 70, '$d$=5 \cdot 10^{-5} \quad \mathrm{[m]} \n $B$=0.30 \quad \quad \mathrm{[T]}', verticalalignment='top', bbox=props)

plt.text(4.7, 90, 'Li', verticalalignment='top', bbox=None) #
plt.text(2.65, 90, 'Na', verticalalignment='top', bbox=None) #
plt.text(1.4, 90, 'K', verticalalignment='top', bbox=None) #
plt.text(1.15, 95, 'Rb', verticalalignment='top', bbox=None) #
plt.text(0.91, 85, 'Cs', verticalalignment='top', bbox=None) #
plt.text(8.47, 90, 'Cu', verticalalignment='top', bbox=None) #
plt.text(5.86, 90, 'Ag', verticalalignment='top', bbox=None) #
plt.text(5.9, 85, 'Au', verticalalignment='top', bbox=None) #
plt.text(24.7, 85, 'Be', verticalalignment='top', bbox=None) #
plt.text(8.61, 95, 'Mg', verticalalignment='top', bbox=None) #
plt.text(4.61, 95, 'Ca', verticalalignment='top', bbox=None) #
plt.text(3.55, 100, 'Sr', verticalalignment='top', bbox=None) #
plt.text(3.15, 85, 'Ba', verticalalignment='top', bbox=None) #
plt.text(13.2, 90, 'Zn', verticalalignment='top', bbox=None)
plt.text(9.27, 85, 'Cd', verticalalignment='top', bbox=None)
plt.text(18.1, 85, 'Al', verticalalignment='top', bbox=None) #
plt.text(15.4, 90, 'Ga', verticalalignment='top', bbox=None)
plt.text(11.5, 85, 'In', verticalalignment='top', bbox=None) #
plt.text(10.5, 90, 'Ti', verticalalignment='top', bbox=None)#
plt.text(14.8, 85, 'Sn', verticalalignment='top', bbox=None)
plt.text(13.2, 85, 'Pb', verticalalignment='top', bbox=None)

plt.savefig('output\\simulatie\\n.png', dpi=300)

