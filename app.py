import json
import os
import matplotlib.pyplot as plt
from equilibrium import *

# ******** VARIAVEIS ENTRADA *********
Conc_Fe3 = 1 #em M -> alterar para ppm
Conc_Fe2 = 1 #em M -> alterar para ppm

pH = 7 #pH do sistema
potencial = 0 #potencial redox do sistema
# ************************************

list_dir = os.listdir('src/equilibrium')
print(list_dir)

#TEMPORÁRIO - INPUT DE FILE PARA CRIAR 
temp_input = input('Choose File to Load: ')
temp_input = temp_input + '.json'
if temp_input in list_dir:
    print('File exists.')
else:
    print('File does not exist.')

#open json file
f = open('src/equilibrium/{}'.format(temp_input))
json_info = json.load(f)

#CREATE DICTIONARY OF LOADED EQUILIBRIUM FILES
filesDictionary = []

#create a list of equilibriums for each file
exec('{} = []'.format(json_info['Info']))
#create an entry on a dictionary for the list of equilibriums for each file
exec('{}.append("{}":{})'.format(filesDictionary, json_info['Info'], json_info['Info']))

for i in range(0,len(json_info['Equilibrium'])):
    exec('{}.append({}.from_json_object({}))'.format(json_info['Info'], json_info['Equilibrium'][i]['ObjectType'], json_info['Equilibrium'][i]))
    
data = []
for i in range(len(water)):
    data.append(water[i].GetCurve(Conc_Fe2, Conc_Fe3))
plt.plot(data[0][0], data[0][1],json_info['Equilibrium'][i]['LineStyle'])
plt.plot(data[1][0], data[1][1],json_info['Equilibrium'][i]['LineStyle'])
plt.show()