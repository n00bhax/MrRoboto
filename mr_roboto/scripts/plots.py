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


if __name__ == '__main__':
    plot2()
