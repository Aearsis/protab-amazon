#!/usr/bin/env python3
from datetime import datetime, timedelta

from data import stock, inception, game_length
import matplotlib.pyplot as plt
import matplotlib.dates as dates

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

x_axis = dates.drange(inception, inception + len(stock[0]) * second, second)

for i in range(len(stock)):
    plt.plot_date(x_axis, stock[i], "-", linewidth=0.3, label=labels[i])

plt.legend(loc=3)

plt.savefig('plot.pdf')

idx_base = int(((now - window) - inception).total_seconds())
timestamp_base = int((now - window).timestamp())
for i in range(int(window.total_seconds())):
    print(timestamp_base + i, *(stock[k][idx_base + i] for k in range(5)))
