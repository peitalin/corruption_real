
from parameters import corruption_rate

characters_on_tiles = {
    'h1': 10_000,
    'h2': 10_000,
    'h3': 10_000,
    'h4': 0,
    'h5': 0,
    'h6': 0,
    'h7': 0,
}


def divertCorruptionHarvesters(c=characters_on_tiles):

    # legions who ended up in each destination
    ldestination_h1 = c['h1']
    ldestination_h2 = c['h2']
    ldestination_h3 = c['h3']
    ldestination_h4 = c['h4']
    ldestination_h5 = c['h5']
    ldestination_h6 = c['h6']
    ldestination_h7 = c['h7']

    total_legions = ldestination_h1 \
        + ldestination_h2 \
        + ldestination_h3 \
        + ldestination_h4 \
        + ldestination_h5 \
        + ldestination_h6 \
        + ldestination_h7

    print("total_legions: {}".format(total_legions))

    l_h1 = ldestination_h1 / total_legions
    l_h2 = ldestination_h2 / total_legions
    l_h3 = ldestination_h3 / total_legions
    l_h4 = ldestination_h4 / total_legions
    l_h5 = ldestination_h5 / total_legions
    l_h6 = ldestination_h6 / total_legions
    l_h7 = ldestination_h7 / total_legions

    crypts_altered_corruption_rate = {
        'h1': corruption_rate['h1'] * (1 + l_h1),
        'h2': corruption_rate['h2'] * (1 + l_h2),
        'h3': corruption_rate['h3'] * (1 + l_h3),
        'h4': corruption_rate['h4'] * (1 + l_h4),
        'h5': corruption_rate['h5'] * (1 + l_h5),
        'h6': corruption_rate['h6'] * (1 + l_h6),
        'h7': corruption_rate['h7'] * (1 + l_h7),
    }
    return crypts_altered_corruption_rate

c = divertCorruptionHarvesters()


