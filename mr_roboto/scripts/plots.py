#!/usr/bin/env python3

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv


def plot1():
    x = []
    y = []

    with open('adc.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=';')

        for row in plots:
            y.append(float(row[0]))
            x.append(float(row[1]))

    plt.xlabel("Time (s)")
    plt.ylabel("Tactile sensor")

    plt.xticks(np.linspace(0, 130, num=10))
    plt.plot(x, y)
    plt.savefig('tactile')

def plot2():
    x, y1, y2, y3 = [], [], [], []

    with open('acc.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=';')

        for row in plots:
            y1.append(float(row[0]))
            y2.append(float(row[1]))
            y3.append(float(row[2]))
            x.append(float(row[3]))

    plt.xlabel("Time (s)")
    plt.ylabel("Acceleration (m/s^2 ?)")

    plt.xticks(np.linspace(0, 130, num=10))

    plt.plot(x, y1, color="red", linewidth=0.2, alpha=0.7, label="x-axis")
    plt.plot(x, y2, color="green", linewidth=0.2, alpha=0.7, label="y-axis")
    plt.plot(x, y3, color="blue", linewidth=0.2, alpha=0.7, label="z-axis")

    plt.legend()

    plt.savefig('acceleration')


def find_nearest(value, array):
    arg = (np.abs(array - value)).argmin()
    return arg

def export_shortened_adc():
    t, x, y, z, adc, adc_t = [], [], [], [], [], []

    with open('acc.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=';')

        for row in plots:
            x.append(float(row[0]))
            y.append(float(row[1]))
            z.append(float(row[2]))
            t.append(float(row[3]))

    with open('adc.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=';')

        for row in plots:
            adc.append(float(row[0]))
            adc_t.append(float(row[1]))



    shortened_adc = []

    for timestamp in t:
        arg = find_nearest(timestamp, np.array(adc_t))
        shortened_adc.append(adc[arg])

    np.savetxt('./shortened_acc.csv', shortened_adc, fmt='%d')
def plot3():
    t, x, y, z, adc, adc_t = [], [], [], [], [], []

    with open('acc.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=';')

        for row in plots:
            x.append(float(row[0]))
            y.append(float(row[1]))
            z.append(float(row[2]))
            t.append(float(row[3]))

    with open('shortened_acc.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=';')

        for row in plots:
            adc.append(float(row[0]))

    plt.xlabel("x-Acceleration (m/s^2 ?)")
    plt.ylabel("Tactile force")

    plt.ylim(0, 1023)
    plt.xlim(-20, 20)

    #tijdelijk alleen met acc_x om te zien of dit iets opleverd
    plt.scatter(x, adc, color="red", s=0.1, marker='.')


    plt.savefig('all3')


def plot4():
    t, x, y, z, adc, adc_t = [], [], [], [], [], []

    with open('acc.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=';')

        for row in plots:
            x.append(float(row[0]))
            y.append(float(row[1]))
            z.append(float(row[2]))
            t.append(float(row[3]))

    with open('shortened_acc.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=';')

        for row in plots:
            adc.append(float(row[0]))

    plt.xlabel("x-Acceleration (m/s^2 ?)")
    plt.ylabel("Tactile force")

    plt.ylim(0, 1023)
    plt.xlim(-20, 20)

    adc = (np.array(adc))[2666: 8300]
    x = (np.array(x))[2666:8300]

    plt.title("Cardboard")

    #tijdelijk alleen met acc_x om te zien of dit iets opleverd
    plt.scatter(x, adc, color="red", s=0.1, marker='.')

    plt.savefig('cardboard')

def plot5():
    t, x, y, z, adc, adc_t = [], [], [], [], [], []

    with open('acc.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=';')

        for row in plots:
            x.append(float(row[0]))
            y.append(float(row[1]))
            z.append(float(row[2]))
            t.append(float(row[3]))

    with open('shortened_acc.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=';')

        for row in plots:
            adc.append(float(row[0]))

    plt.xlabel("x-Acceleration (m/s^2 ?)")
    plt.ylabel("Tactile force")

    plt.ylim(0, 1023)
    plt.xlim(-20, 20)

    adc = (np.array(adc))[10900:14500]
    x = (np.array(x))[10900:14500]

    #tijdelijk alleen met acc_x om te zien of dit iets opleverd
    plt.scatter(x, adc, color="red", s=0.1, marker='.')

    plt.title("Plushie")

    plt.savefig('plushie')

def plot6():
    t, x, y, z, adc, adc_t = [], [], [], [], [], []

    with open('acc.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=';')

        for row in plots:
            x.append(float(row[0]))
            y.append(float(row[1]))
            z.append(float(row[2]))
            t.append(float(row[3]))

    with open('shortened_acc.csv', 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=';')

        for row in plots:
            adc.append(float(row[0]))

    plt.xlabel("x-Acceleration (m/s^2 ?)")
    plt.ylabel("Tactile force")

    plt.ylim(0, 1023)
    plt.xlim(-20, 20)

    adc = (np.array(adc))[17400:22000]
    x = (np.array(x))[17400:22000]

    #tijdelijk alleen met acc_x om te zien of dit iets opleverd
    plt.scatter(x, adc, color="red", s=0.1, marker='.')

    plt.title("Hard Metal Speaker")

    plt.savefig('speaker')

if __name__ == '__main__':
    plot6()
