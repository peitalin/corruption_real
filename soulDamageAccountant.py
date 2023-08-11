
from parameters import harvester_age, harvester_list, getCorruptionLevel
from parameters import corruption_diversion_points
import numpy as np
from functools import reduce


DEATH_THRESHOLD = 1_000_000
TARGET_NUM_HARVESTERS = 4

HOURS_TO_REACH_CRYPTS_ENDTILES = 12
SOUL_DAMAGE_BASE_RATE = 9999


def drawTileArrivals(hDead):
    # simulate characters arriving on harvester tiles/destinations every period (1 hours)
    bounds = [20, 40]
    return {
        'h1': 0 if hDead['h1'] else np.random.randint(bounds[0]*4, bounds[1]*4),
        'h2': 0 if hDead['h2'] else np.random.randint(bounds[0], bounds[1]),
        'h3': 0 if hDead['h3'] else np.random.randint(bounds[0], bounds[1]),
        'h4': 0 if hDead['h4'] else np.random.randint(bounds[0]*4, bounds[1]*4),
        'h5': 0 if hDead['h5'] else np.random.randint(bounds[0], bounds[1]),
        'h6': 0 if hDead['h6'] else np.random.randint(bounds[0], bounds[1]),
        'h7': 0 if hDead['h7'] else np.random.randint(bounds[0], bounds[1]),
    }

def drawCorrLevel():
    bounds = [0, 7]
    return {
        'h1': np.random.randint(bounds[0], bounds[1]),
        'h2': np.random.randint(bounds[0], bounds[1]),
        'h3': np.random.randint(bounds[0], bounds[1]),
        'h4': np.random.randint(bounds[0], bounds[1]),
        'h5': np.random.randint(bounds[0], bounds[1]),
        'h6': np.random.randint(bounds[0], bounds[1]),
        'h7': np.random.randint(bounds[0], bounds[1]),
    }




class SoulDamageAccountant:
    """ Soul Damage accounting history object """

    def __init__(self):
        self.harvesters = harvester_list
        self.y_soul_damage = {
            'h1': { 0: 0 },
            'h2': { 0: 0 },
            'h3': { 0: 0 },
            'h4': { 0: 0 },
            'h5': { 0: 0 },
            'h6': { 0: 0 },
            'h7': { 0: 0 },
        }
        self.characters_on_end_tiles = {
            'h1': { 0: 0 },
            'h2': { 0: 0 },
            'h3': { 0: 0 },
            'h4': { 0: 0 },
            'h5': { 0: 0 },
            'h6': { 0: 0 },
            'h7': { 0: 0 },
        }
        self.soul_damage_rates = {
            'h1': { 0: 0 },
            'h2': { 0: 0 },
            'h3': { 0: 0 },
            'h4': { 0: 0 },
            'h5': { 0: 0 },
            'h6': { 0: 0 },
            'h7': { 0: 0 },
        }
        self.harvester_age = harvester_age
        self.death_time = {
            'h1': np.nan,
            'h2': np.nan,
            'h3': np.nan,
            'h4': np.nan,
            'h5': np.nan,
            'h6': np.nan,
            'h7': np.nan,
        }
        self.death = {
            'h1': False,
            'h2': False,
            'h3': False,
            'h4': False,
            'h5': False,
            'h6': False,
            'h7': False,
        }
        self.total_characters_in_crypts = { 0: 0 }


    def addAccountingEntriesForHour(self, hour):
        """Check time-series entry exists, add if need be """
        # soul damage balance for each harvester (cumulative)
        for h in self.harvesters:
            if h not in self.y_soul_damage.keys():
                continue
            if hour not in self.y_soul_damage[h].keys():
                if hour == 0:
                    # initial value for time-series
                    self.y_soul_damage[h][hour] = 0
                else:
                    self.y_soul_damage[h][hour] = self.y_soul_damage[h][hour-1]

        # Soul Damage Rates per hour
        for h in self.harvesters:
            if h not in self.soul_damage_rates.keys():
                continue
            if hour not in self.soul_damage_rates[h].keys():
                if hour == 0:
                    self.soul_damage_rates[h][hour] = 0
                else:
                    self.soul_damage_rates[h][hour] = self.soul_damage_rates[h][hour-1]

        for h in self.harvesters:
            if h not in self.characters_on_end_tiles.keys():
                continue
            if hour not in self.characters_on_end_tiles[h].keys():
                if hour == 0:
                    self.characters_on_end_tiles[h][hour] = 0
                else:
                    self.characters_on_end_tiles[h][hour] = self.characters_on_end_tiles[h][hour-1]

        if hour not in self.total_characters_in_crypts.keys():
            if hour == 0:
                self.total_characters_in_crypts[hour] = 0
            else:
                self.total_characters_in_crypts[hour] = self.total_characters_in_crypts[hour-1]


    def simulateCryptsArrivals(self, hour, hours_to_reset=48):

        if (hour % hours_to_reset) <= HOURS_TO_REACH_CRYPTS_ENDTILES:
            # assume it takes this much time to create the end of Crypts
            # assume first X hours, no legion makes it to destination under X hrs
            for h in self.harvesters:
                self.characters_on_end_tiles[h][hour] = 0

            self.total_characters_in_crypts[hour] = 0
        else:
            # otherwise, draw random arrivals to end tiles and increment
            arrivals = drawTileArrivals(self.death)
            for h in self.harvesters:
                self.total_characters_in_crypts[hour] += arrivals[h]
                prev_count = self.characters_on_end_tiles[h][hour-1]
                self.characters_on_end_tiles[h][hour] = prev_count + arrivals[h]


    def _calculateSoulDmg(self, harvester, hour, harvester_corr_balances):

        ### TODO: incorporate diversion points
        total_corr_div_pts = self.total_characters_in_crypts[hour]
        corr_div_pts = self.characters_on_end_tiles[harvester][hour]
        # number of months since birth
        age = harvester_age[harvester]
        # current corruption levels for each harvester
        # corr_level = getCorruptionLevel(harvester_corr_balances[harvester][-1])

        num_active_harvesters = 0
        for x in self.death.values():
            if x == False:
                num_active_harvesters += 1

        if self.death[harvester]:
            soul_damage_share = 0
        else:
            soul_damage_share = (corr_div_pts) / (1 + total_corr_div_pts)

        # if age < 3:
        #     m = 0
        # else:
        #     # m = (age + corr_level)
        #     m = age * age / 9

        n = num_active_harvesters / TARGET_NUM_HARVESTERS
        # soul_damage_share range: 1 ~ 4
        # age term range: 1 ~ 3+
        # corr term range: 1 ~ 3

        soul_damage = SOUL_DAMAGE_BASE_RATE * soul_damage_share * n
        self.soul_damage_rates[harvester][hour] = soul_damage
        return soul_damage


    def emitSoulDamage(self, hour, harvester_corr_balances):
        for h in self.harvesters:
            rate = self._calculateSoulDmg(h, hour, harvester_corr_balances)

            if hour == 0:
                self.y_soul_damage[h][hour] = 0
            else:
                prev_value = self.y_soul_damage[h][hour-1]
                soul_dmg_balance = prev_value + rate
                if soul_dmg_balance >= DEATH_THRESHOLD:
                    self.death[h] = True
                    self.death_time[h] = hour
                    self.y_soul_damage[h][hour] = 0
                else:
                    if self.death[h] == True:
                        self.y_soul_damage[h][hour] = 0
                    else:
                        self.y_soul_damage[h][hour] = prev_value + rate



