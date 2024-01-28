import math
import pandas
from icecream import ic

from datetime import datetime
from source.reaper import Reaper, file_reaper
from source.ui import localize


class Celestia(Reaper):

    def __init__(self):
        super().__init__()
        self.list = None

    def getMass(self, i):
        r = float(self.list['radius'][i])

        if r < 0.1666667:
            m = r * 5
        elif 0.1666667 < r < 0.33333:
            m = r
        elif 0.33333 < r < 0.75:
            m = r / 0.67
        else:
            m = 1

        return str(m)

    def getRadius(self, i):
        m = float(self.list['mass'][i])

        if m < 0.1666667:
            r = m * 5
        elif 0.1666667 < m < 0.33333:
            r = m
        elif 0.33333 < m < 0.75:
            r = m / 0.67
        else:
            r = 1

        return str(r * 70000)

    def getPeriod(self, i):
        semi_major_axis = float(self.list['semi_major_axis'][i])
        orbital_period = semi_major_axis * 365 if str(semi_major_axis) != 'nan' else 1

        return str(orbital_period)

    def getSemiMajorAxis(self, i):
        orbitalPeriod = float(self.list['orbital_period'][i])
        semiAxis = math.sqrt(orbitalPeriod) / 365 if str(orbitalPeriod) != 'nan' else 1

        return str(semiAxis)

    @file_reaper
    def run(self):
        self.list = pandas.read_csv(self.file_name, delimiter=',')
        now = datetime.now().strftime("%d.%m.%Y")
        all_planets = len(self.list)
        header = (f"# {localize.exo_catalog} {now}\n"
                  f"# {localize.data_about} {all_planets - 1} {localize.planets}\n"
                  f"# {localize.source}: Extrasolar planet encyclopedia http://exoplanet.eu/catalog/\n"
                  f"# {localize.make_with} BFG Unpacker\n\n")

        with open(f'{self.output_folder}\\exoplanets.ssc', 'w') as planets:
            planets.write(header)

            for line in range(all_planets):

                if str(self.list["star_name"][line]) != 'nan':
                    ic(self.list["# name"][line])
                    print(f'{localize.planet_added}: {self.list["# name"][line]}...')
                    self.update_signal.emit(int(100 / all_planets * (line + 1)), f'{line + 1}/{all_planets}',
                                            f'{localize.planet_added} - {self.list["# name"][line]}...', False)

                    radius = self.list['radius'][line] if str(self.list['radius'][line]) != 'nan' else self.getRadius(
                        line)
                    mass = self.list['mass'][line] if str(self.list['mass'][line]) != 'nan' else self.getMass(line)
                    period = self.list['orbital_period'][line] if str(
                        self.list['orbital_period'][line]) != 'nan' else self.getPeriod(line)
                    semiMajorAxis = self.list['semi_major_axis'][line] if str(
                        self.list['semi_major_axis'][line]) != 'nan' else self.getSemiMajorAxis(line)
                    eccentricity = self.list['eccentricity'][line] if str(
                        self.list['eccentricity'][line]) != 'nan' else '0'
                    inclination = self.list['inclination'][line] if str(
                        self.list['inclination'][line]) != 'nan' else '0'
                    omega = self.list['omega'][line] if str(self.list['omega'][line]) != 'nan' else '90'

                    planets.write(f'"{self.list["# name"][line]}" "{self.list["star_name"][line]}" ')
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

        with open(f'{self.output_folder}\\exoplanets.stc', 'w') as stars:
            stars.write(header)
            starList = ['Sun']

            for line in range(len(self.list)):

                starName = str(self.list["star_name"][line])

                if starName != 'nan' and starName not in starList:
                    print(f'{localize.star_added}: {self.list["star_name"][line]}...')
                    ic(self.list["star_name"][line])
                    self.update_signal.emit(int(100 / all_planets * (line + 1)), f'{line + 1}/{all_planets}',
                                            f'{localize.star_added}- {self.list["star_name"][line]}...', False)

                    starList.append(starName)

                    mag = self.list["mag_v"][line] if str(self.list['mag_v'][line]) != 'nan' else '1'
                    radius = float(self.list["star_radius"][line]) * 695_700 if str(
                        self.list['star_radius'][line]) != 'nan' else 695_700
                    specType = self.list["star_sp_type"][line].replace(' ', '') if str(
                        self.list['star_sp_type'][line]) != 'nan' else 'M'
                    dist = self.list["star_distance"][line] if str(
                        self.list['star_distance'][line]) != 'nan' else '1000'

                    stars.write(f'Modify "{self.list["star_name"][line]}"')
                    stars.write(' {\n')
                    stars.write(f'\tRA {self.list["ra"][line]}\n')
                    stars.write(f'\tDec {self.list["dec"][line]}\n')
                    stars.write(f'\tDistance {dist}\n')
                    stars.write(f'\tRadius {str(int(radius))}\n')
                    stars.write(f'\tAbsMag {mag}\n')
                    stars.write(f'\tSpectralType "{specType}"\n')
                    stars.write('}\n\n')

        self.update_signal.emit(100, f'{all_planets}/{all_planets}', localize.done, True)
