import argparse
import csv
import math
import numpy
import polyscope
import IPython


COMMON_NAMES = {
    'alp2cen': 'Toliman',
    'gl406': 'Wolf 359',
    'gl65a': 'Luyten 726-8 [A] (BL Ceti)',
    'gl65b': 'Luyten 726-8 [B] (UV Ceti)',
    'gl244b': 'Sirius [B]',
    'gl729': 'Ross 154',
    'gl905': 'Ross 248 (HH Andromedae)',
    '18epseri': 'Epsilon Eridani',
    'gl447': 'Ross 128',
    'gl866a': 'EZ Aquarii',
    '173740': 'Struve 2398 [B]',
    '61cyg3.486': '61 Cygni [A]',
    '61cyg3.498': '61 Cygni [B]',
    'gl280b': 'Procyon [B]',
    '10alpcmi': 'Procyon [A]',
    'gl15b': 'Groombridge 34 [B] (GQ And)',
    '173739': 'Struve 2398 [A]',
    '1326': 'Groombridge 34 [A] (GX And)',
    'epsind': 'Epsilon Indi',
    'gj1111': 'DX Cancri',
    '52taucet': 'Tau Ceti',
    'gj1061': 'Gliese 1061',
    'gl54.1': 'YZ Ceti',
    'gl860b': 'Kruger 60 [B]',
    'gl234a': 'Ross 614 [A]',
    'gl234b': 'Ross 614 [B]',
    'gl628': 'Wolf 1061',
    'gl473a': 'Wolf 424 [A]',
    'gl473b': 'Wolf 424 [B]',
    '225213': 'Gliese 1',
    'gl83.1': 'L 1159-16',
    'nn3618': 'LHS 288',
    'nn3622': 'LHS 292',
}

PLANETS = {
    '70666': { # Proxima Centauri
        'd': {
            'confirmed': False,
            'mass': '0.29 +/-0.08',
            'semimajor': '0.02895 +/-0.00022',
            'orbit': '5.168 +0.051 -0.069',
        },
        'b': {
            'confirmed': True,
            'habitable': True,
            'mass': '1.60 +0.46 -0.36',
            'semimajor': '0.04857 +/-0.00029',
            'orbit': '11.18418 +0.00068 -0.00074',
            'eccentricity': '0.109 +0.076 -0.068',
            'radius': '1.30 +1.20 -0.62',
        },
        'c': {
            'confirmed': True,
            'mass': '7 +/-1',
            'semimajor': '1.489 +/-0.049',
            'orbit': '1928 +/-20',
            'eccentricity': '0.04 +/-0.01',
            'inclination': '133 +/-1'
        }
    },
    '71456': { # Rigil Kentaurus
        'b': {
            'confirmed': False,
            'mass': '9 +35 -0',
            'semimajor': '1.1',
            'orbit': '360',
            'inclination': '65 +/-25',
            'radius': '3 +0.7 -0',
        }
    },
    '87665': { # Barnard's Star
    },
    '118720': { # Wolf 359
    }
}

CORRECTIONS = {
    '118236': {'dist': '3.6743'}
}

ADDITIONS = [
    {
        'id': '1000001',
        'proper': 'Teegarden\'s Star',
        'ci': '2.150',
        'dist': '3.382',
        'ra': '2.88680925',
        'dec': '17.755035',
    },
    {
        'id': '1000002',
        'proper': 'SCR 1845-6357 [A]',
        'ci': '2.295',
        'dist': '4.001',
        'ra': '18.765',
        'dec': '-63.963278',
    },
    {
        'id': '1000003',
        'proper': 'SCR 1845-6357 [B]',
        'ci': '2.295',
        'dist': '4.01',
        'ra': '18.765',
        'dec': '-63.963278',
    },
    {
        'id': '1000004',
        'proper': 'LHS 1723',
        'ci': '1.72',
        'dist': '5.375',
        'ra': '5.03261836',
        'dec': '-6.94621438',
    }
]


def get_stars_within(distance):
    """
    """
    DISTANCE_PARSECS = distance / 3.262
    with open('HYG-Database/hygdata_v3.csv', newline='') as csvfile:
        spamreader = csv.DictReader(csvfile)
        i = 0
        within = []
        for d in spamreader:
            if d['id'] in CORRECTIONS:
                for key in CORRECTIONS[d['id']]:
                    d[key] = CORRECTIONS[d['id']][key]
            if float(d['dist']) < DISTANCE_PARSECS:
                within.append(d)
        within.extend(ADDITIONS)
    return sorted(within, key=lambda d: float(d['dist']))

def get_habitable_zone_boundaries(star):
    # https://www.planetarybiology.com/calculating_habitable_zone.html
    pass


def get_coords_for_star(star):
    return (float(star['x']), float(star['y']), float(star['z']))

def print_coords_for_star(star):
    print('coords: \t{}\ncomputed: \t{}\ncomputed (deg):\t{}'.format(
        get_coords_for_star(star),
        compute_coords_for_star(star),
        compute_coords_for_star_deg(star),
    ))

def compute_coords_for_star(star):
    if 'rarad' in star  and 'decrad' in star:
        return compute_coords(float(star['dist']), float(star['rarad']), float(star['decrad']))
    return compute_coords_for_star_deg(star)

def compute_coords_for_star_deg(star):
    return compute_coords(
        float(star['dist']),
        math.radians(float(star['ra']) * 15),
        math.radians(float(star['dec'])),
    )

def compute_coords(distance, right_ascension, declination):
    return (
        distance * math.cos(declination) * math.cos(right_ascension),
        distance * math.sin(right_ascension) * math.cos(declination),
        distance * math.sin(declination)
    )

def bv2rgb(bv):
    if bv < -0.4: bv = -0.4
    if bv > 2.0: bv = 2.0
    if bv >= -0.40 and bv < 0.00:
        t = (bv + 0.40) / (0.00 + 0.40)
        r = 0.61 + 0.11 * t + 0.1 * t * t
        g = 0.70 + 0.07 * t + 0.1 * t * t
        b = 1.0
    elif bv >= 0.00 and bv < 0.40:
        t = (bv - 0.00) / (0.40 - 0.00)
        r = 0.83 + (0.17 * t)
        g = 0.87 + (0.11 * t)
        b = 1.0
    elif bv >= 0.40 and bv < 1.60:
        t = (bv - 0.40) / (1.60 - 0.40)
        r = 1.0
        g = 0.98 - 0.16 * t
    else:
        t = (bv - 1.60) / (2.00 - 1.60)
        r = 1.0
        g = 0.82 - 0.5 * t * t
    if bv >= 0.40 and bv < 1.50:
        t = (bv - 0.40) / (1.50 - 0.40)
        b = 1.00 - 0.47 * t + 0.1 * t * t
    elif bv >= 1.50 and bv < 1.951:
        t = (bv - 1.50) / (1.94 - 1.50)
        b = 0.63 - 0.6 * t * t
    else:
        b = 0.0
    return (r, g, b)


def get_star_name(star):
    if 'proper' in star and star['proper']:
        return star['proper']
    name = (
        star['bf']
        or star['hr']
        or star['hd']
        or star['gl']
        or star['hip']
    )
    return (
        # Handle cases where binary stars have the same designation
        COMMON_NAMES.get(name.lower().replace(' ', '') + str(round(float(star['dist'] or 0), 3)))
        or COMMON_NAMES.get(name.lower().replace(' ', ''))
        or name
    )


def print_stars(distance):
    """Prints stars within distance in ly.
    """
    within = get_stars_within(distance)
    print('{} entries within {} ly'.format(len(within), distance))
    print('\n'.join([
        str(i) + ' ' + str(y) for i, y in enumerate(sorted([(
                round(float(x['dist']) * 3.262, 3),
                get_star_name(x),
                x['id'],
                [round(z) for z in compute_coords_for_star(x)],
                bv2rgb(float(x['ci'] or 0.0))
            ) for x in within]))
    ]))

def get_rand_color():
    pass

def compute_connectivity_graph(stars, home=0):
    length = numpy.array(numpy.array([[0 for x in stars] for y in stars]))
    for i, star in enumerate(stars):
        name = get_star_name(star)
        coords = numpy.array(compute_coords_for_star(star))
        for j, other_star in enumerate(stars):
            other_coords = numpy.array(compute_coords_for_star(other_star))
            length_between = numpy.linalg.norm(coords - other_coords)
            length[i][j] = numpy.linalg.norm(coords - other_coords)

    dist = [math.inf for x in stars]
    prev = [None for x in stars]
    dist[home] = 0
    unvisited = list(range(len(stars)))

    while unvisited:
        min_dist, min_index, position = min([(dist[index], index, list_position) for list_position, index in enumerate(unvisited)])
        del unvisited[position]
        for neighbor in unvisited:
            new_dist = min_dist + length[min_index][neighbor]
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = min_index

    return dist, prev

def print_connectivity_graph(stars):
    dist, prev = compute_connectivity_graph(stars)
    for i, star in enumerate(stars):
        path = []
        curr = prev[i]
        while curr is not None:
            path.insert(0, curr)
            curr = prev[curr]
        print(f"{get_star_name(stars[i]):<30} {dist[i]:<5} \t {path}")

def show_stars(distance):

    # Initialize polyscope
    polyscope.init()

    ### Register a point cloud
    # `my_points` is a Nx3 numpy array
    within = get_stars_within(distance)
    star_points = numpy.array([compute_coords_for_star(star) for star in within])
    polyscope.register_point_cloud('stars', star_points)
    stars = polyscope.get_point_cloud('stars')
    stars.add_color_quantity('_Color Index', numpy.array([bv2rgb(float(d['ci'] or 0)) for d in within]))
    for i, star in enumerate(within):
        colors = [(0, 0, 0)] * len(within)
        colors[i] = (1.0, 0, 0)
        stars.add_color_quantity(get_star_name(star) or 'no name {}'.format(i), numpy.array(colors))

    # View the point cloud and mesh we just registered in the 3D UI
    polyscope.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='return list of closest stars')
    parser.add_argument('ly', type=float, help='Distance from Earth in light years')
    parser.add_argument('--show', action='store_true', help='Show stars in 3D')
    parser.add_argument('--console', action='store_true', help='Open interactive session')

    args = parser.parse_args()
    print_stars(args.ly)
    if args.console:
        stars = get_stars_within(args.ly)
        IPython.embed()
    if args.show:
        show_stars(args.ly)