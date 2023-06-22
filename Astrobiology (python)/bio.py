import numpy as np
import matplotlib.pyplot as plt
import pandas
import math
from scipy import optimize
from astropy.modeling import models, fitting
from astropy.modeling.models import Sine1D
from astropy.stats import LombScargle
from scipy.signal import lombscargle

def mysin(time, amplitude, period, phase, vs):
    return amplitude * np.sin((2*np.pi/period)*(time + phase)) + vs

fajl = 'cnc55.txt'
period, velocity, error = np.genfromtxt(fajl, delimiter='\t', unpack=True, autostrip=True)
period = period - min(period)
G = 6.673e-11
Msol = 1.989e30
Mjup = 1.89813e27
Ms = 1.015 * 1.989e30
n = 3
name = ["b","d","c"]
P = np.zeros(n)
K = np.zeros(n)
phase = np.zeros(n)
vs = np.zeros(n)
Mp = np.zeros(n)
a = np.zeros(n)
e = np.zeros(n)

for i in range(n):
    plt.scatter(period, velocity)
    plt.title('Radial velocity of cnc55' + name[i])
    plt.xlabel('D[day]')
    plt.ylabel('Rv[m/s]')
    plt.show()

    frequency, power = LombScargle(period, velocity, error).autopower()
    time = 1/frequency
    plt.plot(time,power)
    plt.title('Periodogram')
    plt.xscale("log")
    plt.xlabel('Period')
    plt.ylabel('Power')
    plt.show()

    P[i] = time[np.argwhere(power == max(power))]
    best_frequency = frequency[np.argmax(power)]
    t_fit = np.linspace(0,2.1*P[i], 1000)
    y_fit = LombScargle(period,velocity,error).model(t_fit,best_frequency)
    K[i] = (np.max(y_fit)-np.min(y_fit))/2
    vs[i] = (np.max(y_fit)+np.min(y_fit))/2
    phase[i] = t_fit[np.max(np.argwhere(y_fit<0))]
    while(phase[i] >= P[i]):
        phase[i] = phase[i]-P[i]
    phase[i] = -phase[i]

    Mp[i] = ((P[i]/365.25)/12)**(1/3) * (K[i]/13)
    Ps = P[i] * 24 * 3600
    a[i] = ((G * ((Mp[i]*Mjup) + Ms) * Ps**2)/(4 * (np.pi**2)))**(1/3)
    a[i] = a[i]/1.496e11
    
    e[i] = np.sqrt(1-(((Mp[i]*Mjup)**2)*(   (Ps/(2*np.pi*G))**(-2/3) ) * (K[i]**(-2)) * ((Ms)**(-4/3)) ) )
    print(e[i])
    e[i] = np.sqrt(1-(1/(K[i]/((203*(P[i])**(-1/3)*Mp[i])/(((Ms/Msol)+9.548e-4*Mp[i])**(2/3))))**2))
    print(e[i])
    plt.plot(t_fit,y_fit)
    plt.title('Cnc55'+ name[i] + '\nP = ' + str(P[i]) + ' days K = ' + str(K[i]) + ' m/s e = ' + str(e[i]))
    plt.xlabel('Orbital phase')
    plt.ylabel('Velocity[m/s]')
    plt.show()

    print("Orbital period of " + fajl[:-4] + name[i] + ": " + str(P[i]) + " days")
    print("Semi-amplitude K of " + fajl[:-4] + name[i] + ": " + str(K[i]) + " m/s")
    print("Mass of " + fajl[:-4] + name[i] + ": " + str(Mp[i]) + " Mjup")
    print("Semi-major axis of " + fajl[:-4] + name[i] + ": " + str(a[i]) + " AU")
    print("Eccentricity of " + fajl[:-4] + name[i] + ": " + str(e[i]))
    print('----------------------------------------------------')

    for j in range(len(period)):
        velocity[j] = velocity[j]-mysin(period[j], K[i], P[i], phase[i], vs[i])
