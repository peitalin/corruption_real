
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot
from matplotlib.animation import FuncAnimation

from soulDamageAccountant import SoulDamageAccountant
from corruptionAccountant import CorruptionAccountant, isHarvester
from parameters import harvester_age

from styles import brown, offwhite, grey, gold, darkblue, lightblue
from styles import line_styles, line_colors, harvester_linestyles


# initialize plot variables, overwritten on 1st pass of simulation
ax1 = 1
ax2 = 1
ax3 = 1
ax4 = 1
## x-axis is hours
hours = []
# each frame is 1 hr
FRAMES = 2000



def init_plot(i=0):
    # do nothing, prevents FuncAnim calling initialization twice
    return


c = corrAccountant = CorruptionAccountant()
s = soulDamageAccountant = SoulDamageAccountant()


def simulation_fn(i):

    hour = i # each i-frame is 1 hr
    hours.append(hour)

    # clear plots to redraw
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()

    corrAccountant.addAccountingEntriesForHour(hour)
    corrAccountant.emitCorruption(hour)
    corrAccountant.emitForgeableCorruption(hour)

    soulDamageAccountant.addAccountingEntriesForHour(hour)
    soulDamageAccountant.simulateCryptsArrivals(hour)
    soulDamageAccountant.emitSoulDamage(hour, corrAccountant.y_corruption)

    ### Plot 1 - Corruption in each BW structure
    for h in corrAccountant.y_structures:
        corrAccountant.maybeRemoveCorruptionNTimes(hour, h)
        ax1.plot(
            hours,
            corrAccountant.y_corruption[h],
            alpha=0.5,
            label="{structure}".format(structure=h),
            color=line_colors[h],
            linestyle=harvester_linestyles[h],
        )
        ax1.set(xlabel='', ylabel='Corruption level')
        ax1.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.5)

    #### Plot 2 - Amount of Circulating Corruption
    ax2.plot(
        hours,
        corrAccountant.y_forgeable_corruption.values(),
        label="Total Forgeable Corruption ",
        color='royalblue',
        linestyle=":",
    )
    ax2.plot(
        hours,
        corrAccountant.y_total_circulating_corruption.values(),
        label="Circulating Crafted Corruption",
        color='purple',
        linestyle="-",
    )
    ax2.set(xlabel='', ylabel='Corruption Crafted')
    ax2.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.5)

    #### Plot 3 - Crypts Characters at Destinations
    for h in soulDamageAccountant.harvesters:
        ax3.plot(
            hours,
            soulDamageAccountant.characters_on_end_tiles[h].values(),
            alpha=0.5,
            label="{h}: {n} characters".format(h=h, n=soulDamageAccountant.characters_on_end_tiles[h][hour]),
            color=line_colors["crypts_{}".format(h)],
        )
        ax3.set(xlabel='', ylabel='Characters on Crypts End Tiles')
        ax3.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.5)


    ### Plot 4 - Harvester Soul Damage
    for h in soulDamageAccountant.harvesters:

        ax4.plot(
            hours,
            soulDamageAccountant.y_soul_damage[h].values(),
            label="{} Damage".format(h),
            color="black" if h == 'h1' else "crimson",
            linestyle=harvester_linestyles[h],
            alpha=0.4,
        )
        ax4.set(xlabel='hours', ylabel='Harvester Soul Damage')
        ax4.grid(color='grey', linestyle='-', linewidth=0.5, alpha=0.5)


    ax1.set_title('Corruption Balances', size=10, color=gold)
    ax2.set_title('Circulating Corruption', size=10, color=gold)
    ax3.set_title('#Legions Finished Crypts', size=10, color=gold)
    ax4.set_title('Harvester Soul Damage Accumulated', size=10, color=gold)

    ax1.legend(bbox_to_anchor=(1.20, 1.1), loc="upper right")
    ax2.legend(bbox_to_anchor=(1.21, 0.2), loc="lower center")
    ax3.legend(bbox_to_anchor=(1.16, 0), loc="lower center")
    ax4.legend(bbox_to_anchor=(1.13, 0), loc="lower center")








def run_soul_damage_simulation():

    global fig
    global ax1
    global ax2
    global ax3
    global ax4

    # fig, (ax1, ax2, ax3) = plt.subplots(3, facecolor=darkblue)
    # fig.suptitle(''.format(), color=gold)

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)
    fig.suptitle(''.format())
    fig.set_size_inches(12, 9)

    ani = FuncAnimation(
        fig,
        simulation_fn,
        frames=FRAMES,
        interval=100,
        repeat=False,
        init_func=init_plot,
    )

    plt.subplots_adjust(left=0.08, right=0.7, top=0.9, bottom=0.1, hspace=0.3)
    # ax2.set_facecolor(lightblue)
    # ax3.set_facecolor(lightblue)

    plt.show()


run_soul_damage_simulation()






