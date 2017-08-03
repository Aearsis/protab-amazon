#!/usr/bin/env python3

from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import matplotlib.dates as dates

import pickle

inception = datetime.today().replace(hour=13, minute=30, second=0, microsecond=0)
destruction = datetime.today().replace(hour=19, minute=30, second=0, microsecond=0)
eternity_sec = int((destruction - inception).total_seconds())

# The time in which data will be normalized
game_start = datetime.today().replace(hour=15, minute=00)
game_end = datetime.today().replace(hour=17, minute=00)
game_length = game_end - game_start

game_sec = int(game_length.total_seconds())

second = timedelta(seconds=1)

#output = open('/home/pi/protab-academy/data.pkl', 'rb')
output = open('data.pkl', 'rb')

stock = pickle.load(output)

now = datetime.now()
window = game_length / 5
second = timedelta(seconds=1)

labels = [
    "Větráček",
    "Stahovací pásky na kabely",
    "RTC baterie",
    "BIOS čip",
    "Záslepka disketové mechaniky"
]

plt.style.use(['bmh'])
fig, ax = plt.subplots(1)
fig.suptitle("Vývoj cen", fontsize=16)
ax.set_xlabel('Čas')
ax.set_xlim(now - window, now)
ax.set_ylabel('Cena')
ax.set_ylim(0, 30)

fmt = dates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(fmt)

offset = int(((now - window) - inception).total_seconds())
size = int(window.total_seconds())
x_axis = dates.drange(inception, destruction, second)

for i in range(len(stock)):
    plt.plot_date(x_axis, stock[i], "-", linewidth=0.3, label=labels[i])

plt.legend(loc=3)

#plt.savefig('plot.pdf')
plt.show()

#timestamp_base = int((now - window).timestamp())
#for i in range(len(stock[0])):
#    print(timestamp_base + i, *(stock[k][offset + i] for k in range(5)))
