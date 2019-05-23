from pyriot.wrapper import PyRiot, EUROPE_WEST

priot = PyRiot('RGAPI-620d547c-fbc8-4d93-ae43-0b7b385647a7')
datos = priot.summoner_get_by_name(EUROPE_WEST, 'kanuto1996')

print(datos)