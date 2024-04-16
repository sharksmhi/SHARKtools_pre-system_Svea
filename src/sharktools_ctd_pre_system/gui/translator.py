

class Translator:
    names = {'depth': 'Maxdjup i plot (m)',
             'bin_size': 'Djupgrid (m)',
             'cruise': 'Expedition nr',
             'vessel': 'Fartyg',
             'series': 'Serie',
             'tail': 'Testkast',
             'station': 'Station',
             'distance': 'Avstånd till station (m)',
             'operator': 'CTD operatör',
             'position': 'Position',
             'event_id': 'EventID      ',
             'parent_event_id': 'ParentEventID',

             'mprog':   'Övervakningsprogram',
             'proj':    'Projekt',
             'orderer': 'Beställare',
             'slabo':   'Provtagande laboratorium',
             'alabo':   'Analyserande laboratorium',
             'refsk':   'Provtagningsmetod referens',

             'wadep_bot': 'Bottendjupet ska vara [m]',
             'wadep': 'Ekolodsdjup vid station [m]',
             'windir': 'Vindriktning',
             'winsp': 'Vindhastighet [m/s]',
             'airtemp': 'Lufttemperatur [grader C]',
             'airpres': 'Lufttryck [hPa]',
             'weath': 'Väder [kod]',
             'cloud': 'Moln [kod]',
             'waves': 'Vågor [kod]',
             'iceob': 'Is [kod]',
             'comment': 'CTD kommentar'}

    def __init__(self):
        self.reversed_names = {value: key for key, value in self.names.items()}

    def get_readable(self, item):
        return self.names.get(item, item)

    def get_id(self, item):
        return self.reversed_names.get(item, item)