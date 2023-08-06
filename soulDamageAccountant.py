
from soulDamageDiversion import divertSoulDamageHarvesters
from parameters import harvester_age, harvester_list, getCorruptionLevel
from parameters import corruption_diversion_points
import numpy as np


HOURS_TO_REACH_CRYPTS_ENDTILES = 6


def drawTileArrivals():
    # simulate characters arriving on harvester tiles/destinations every period (few hours)
    bounds = [50, 200]
    return {
        'h1': np.random.randint(bounds[0], bounds[1]),
        'h2': np.random.randint(bounds[0], bounds[1]),
        'h3': np.random.randint(bounds[0], bounds[1]),
        'h4': np.random.randint(bounds[0], bounds[1]),
        'h5': np.random.randint(bounds[0], bounds[1]),
        'h6': np.random.randint(bounds[0], bounds[1]),
        'h7': np.random.randint(bounds[0], bounds[1]),
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


soul_damage_base_rate = 1000


class SoulDamageAccountant:
    """ Soul Damage accounting history object """

    def __init__(self):
        self.max_soul_damage = 1_000_000
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

        # Crypts num characters on the board/destinations
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


    def simulateCryptsArrivals(self, hour, hours_to_reset=24):

        if (hour % hours_to_reset) <= HOURS_TO_REACH_CRYPTS_ENDTILES:
            # 24 hours in, reset the round; assuming each Crypts round is 24hrs
            # assume first X hours, no legion makes it to destination under X hrs
            for h in self.harvesters:
                self.characters_on_end_tiles[h][hour] = 0
        else:
            # otherwise, draw random arrivals to end tiles and increment
            arrivals = drawTileArrivals()
            total_characters_in_crypts = 0
            for h in self.harvesters:
                total_characters_in_crypts += arrivals[h]
                self.total_characters_in_crypts[hour] = total_characters_in_crypts
                prev_count = self.characters_on_end_tiles[h][hour-1]
                self.characters_on_end_tiles[h][hour] = prev_count + arrivals[h]


    def _calculateSoulDmg(self, harvester, hour, harvester_corr_balances):

        ### TODO: incorporate diversion points
        total_corr_div_pts = self.total_characters_in_crypts[hour]
        corr_div_pts = self.characters_on_end_tiles[harvester][hour]

        if total_corr_div_pts == 0:
            ## no one playing Crypts
            return 0
        else:
            age = harvester_age[harvester] # number of months since birth
            c = getCorruptionLevel(harvester_corr_balances[harvester][-1]) # current corruption levels for each harvester

            m = age * 2 * (1 + c)
            # m = age * 2
            return soul_damage_base_rate * (corr_div_pts / total_corr_div_pts) * m


    def emitSoulDamage(self, hour, harvester_corr_balances):
        for h in self.harvesters:
            rate = self._calculateSoulDmg(h, hour, harvester_corr_balances)

            if hour == 0:
                self.y_soul_damage[h][hour] = 0
            else:
                prev_value = self.y_soul_damage[h][hour-1]
                self.y_soul_damage[h][hour] = prev_value + rate




s = SoulDamageAccountant()
corr = drawCorrLevel()

s.addAccountingEntriesForHour(1)
s.simulateCryptsArrivals(1)
s.emitSoulDamage(1, corr)
s.characters_on_end_tiles

s.addAccountingEntriesForHour(2)
s.simulateCryptsArrivals(2)
s.emitSoulDamage(2, corr)
s.characters_on_end_tiles

s.addAccountingEntriesForHour(3)
s.simulateCryptsArrivals(3)
s.emitSoulDamage(3, corr)
s.characters_on_end_tiles

s.addAccountingEntriesForHour(4)
s.simulateCryptsArrivals(4)
s.emitSoulDamage(4, corr)
s.characters_on_end_tiles

s.addAccountingEntriesForHour(5)
s.simulateCryptsArrivals(5)
s.emitSoulDamage(5, corr)
s.characters_on_end_tiles

# s.simulateCryptsArrivals(24)
# s.addAccountingEntriesForHour(24)
# s.emitSoulDamage(24)
# s.characters_on_end_tiles

s.total_characters_in_crypts
s.y_soul_damage