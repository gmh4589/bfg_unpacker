import math
import os
import configparser

from datetime import datetime
from tkinter import filedialog as fd


def getMass(i):
    r = float(List['radius'][i])
    if r < 0.1666667:
        m = r * 5
    elif 0.1666667 < r < 0.33333:
        m = r
    elif 0.33333 < r < 0.75:
        m = r / 0.67
    else:
        m = 1

    return str(m)


def getRadius(i):
    m = float(List['mass'][i])
    if m < 0.1666667:
        r = m * 5
    elif 0.1666667 < m < 0.33333:
        r = m
    elif 0.33333 < m < 0.75:
        r = m / 0.67
    else:
        r = 1

    return str(r * 70000)


def getPeriod(i):
    semi_major_axis = float(List['semi_major_axis'][i])
    orbital_period = semi_major_axis * 365 if str(semi_major_axis) != 'nan' else 1

    return str(orbital_period)


def getSemiMajorAxis(i):
    orbitalPeriod = float(List['orbital_period'][i])
    semiAxis = math.sqrt(orbitalPeriod) / 365 if str(orbitalPeriod) != 'nan' else 1

    return str(semiAxis)


def celestia():

    with open(f'{path}\\exoplanets.ssc', 'w') as planets:
        planets.write(f"# {tl[117][:-1]} {now}\n")
        planets.write(f"# {tl[118][:-1]}{len(List) - 1}{tl[119]}")
        planets.write(f"# {tl[120][:-1]}: Extrasolar planet encyclopedia http://exoplanet.eu/catalog/\n")
        planets.write(f"# {tl[121][:-1]} BFG Unpacker\n\n")

        for line in range(len(List)):

            if str(List["star_name"][line]) != 'nan':
                print(f'{tl[228][:-1]} {List["# name"][line]}...')

                radius = List['radius'][line] if str(List['radius'][line]) != 'nan' else getRadius(line)
                mass = List['mass'][line] if str(List['mass'][line]) != 'nan' else getMass(line)
                period = List['orbital_period'][line] if str(List['orbital_period'][line]) != 'nan' else getPeriod(line)
                semiMajorAxis = List['semi_major_axis'][line] if str(
                    List['semi_major_axis'][line]) != 'nan' else getSemiMajorAxis(line)
                eccentricity = List['eccentricity'][line] if str(List['eccentricity'][line]) != 'nan' else '0'
                inclination = List['inclination'][line] if str(List['inclination'][line]) != 'nan' else '0'
                omega = List['omega'][line] if str(List['omega'][line]) != 'nan' else '90'

                planets.write(f'"{List["# name"][line]}" "{List["star_name"][line]}" ')
                planets.write('{\n')
                planets.write(f'\tMass {mass}\n')
                planets.write(f'\tRadius {radius}\n\n')
                planets.write('\tEllipticalOrbit {\n')
                planets.write(f'\t\tPeriod {period}\n')
                planets.write(f'\t\tSemiMajorAxis {semiMajorAxis}\n')
                planets.write(f'\t\tEccentricity {eccentricity}\n')
                planets.write(f'\t\tInclination {inclination}\n')
                planets.write(f'\t\tMeanLongitude {omega}\n')
                planets.write('\t}\n\n')
                planets.write('\tUniformRotation {\n')
                planets.write(f'\t\tPeriod 10\n')
                planets.write(f'\t\tInclination 90\n')
                planets.write(f'\t\tAscendingNode 0\n')
                planets.write(f'\t\tMeridianAngle 0\n')
                planets.write('\t}\n}\n\n')

    with open(f'{path}\\exoplanets.stc', 'w') as stars:

        stars.write(f"# {tl[117][:-1]} {now}\n")
        stars.write(f"# {tl[118][:-1]}{len(List) - 1}{tl[119]}")
        stars.write(f"# {tl[120][:-1]}: Extrasolar planet encyclopedia http://exoplanet.eu/catalog/\n")
        stars.write(f"# {tl[121][:-1]} BFG Unpacker\n\n")

        starList = ['Sun']

        for line in range(len(List)):

            starName = str(List["star_name"][line])

            if starName != 'nan' and starName not in starList:
                print(f'{tl[228][:-1]} {List["star_name"][line]}...')

                starList.append(starName)

                mag = List["mag_v"][line] if str(List['mag_v'][line]) != 'nan' else '1'
                radius = float(List["star_radius"][line]) * 695_700 if str(
                    List['star_radius'][line]) != 'nan' else 695_700
                specType = List["star_sp_type"][line].replace(' ', '') if str(
                    List['star_sp_type'][line]) != 'nan' else 'M'
                dist = List["star_distance"][line] if str(List['star_distance'][line]) != 'nan' else '1000'

                stars.write(f'Modify "{List["star_name"][line]}"')
                stars.write(' {\n')
                stars.write(f'\tRA {List["ra"][line]}\n')
                stars.write(f'\tDec {List["dec"][line]}\n')
                stars.write(f'\tDistance {dist}\n')
                stars.write(f'\tRadius {str(int(radius))}\n')
                stars.write(f'\tAbsMag {mag}\n')
                stars.write(f'\tSpectralType "{specType}"\n')
                stars.write('}\n\n')


try:

    import pandas

    filetypes = (('Exoplanet Catalog File', 'exoplanet.eu_catalog.csv'), ('All files', '*.*'))
    filePath = fd.askopenfilename(title = 'Select Catalog File', filetypes = filetypes)

    now = datetime.now().strftime("%d.%m.%Y")
    thisPath = os.path.dirname(os.path.realpath(__file__)).replace('data\\python_script', '')

    setting = configparser.ConfigParser()
    setting.read(f'{thisPath}/unpacker.ini')
    lang = setting['Main']['Language']
    path = setting['Main']['Path'].replace('\\', '\\\\')

    with open(f'{thisPath}data\\local\\{lang}.loc') as t:
        tl = t.readlines()

    e = False

    try:
        List = pandas.read_csv(filePath, delimiter=',')

    except (pandas.errors.ParserError, UnicodeDecodeError):
        # TODO: Localized text
        print('Please, select valid file')
        e = True

    if not e:

        if __name__ == '__main__': celestia()

except ModuleNotFoundError:

    os.system('pip3 install pandas')

    # TODO: Localized text
    print('Please, rerun this tool')
