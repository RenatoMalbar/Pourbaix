import json
import os
import matplotlib.pyplot as plt
from equilibrium import *
import equilibrium_func as eqF

# ********* INPUT VARIABLES **********
Conc_Fe3 = 1 #em M -> alterar para ppm
Conc_Fe2 = 1 #em M -> alterar para ppm

pH = 7 #pH do sistema
potencial = 0 #potencial redox do sistema
# ************************************

#LIST ALL AVAILABLE JSON FILES FOR EQUILIBRIUMS
list_dir = os.listdir('src/equilibrium')
lst_avl_data = [x[:-5] for x in list_dir]
print('Available Files:', lst_avl_data)

#INPUT DE FILE PARA CRIAR 
input_jsonFile = input('Choose File to Load: ')
temp_input_json = input_jsonFile
if temp_input_json in lst_avl_data:
    print('File exists.')
else:
    print('File does not exist.')
    exit()

#memory release list_dir
del list_dir

#open json file
f = open('src/equilibrium/{}'.format(temp_input_json +'.json'))
json_info = json.load(f)
#clear memory of input
del temp_input_json

#CREATE DICTIONARY OF LOADED EQUILIBRIUM FILES
filesDictionary = dict()

#create list of equilibriums (class) 
temp_eqList_loaded = eqF.read_equilibrium_json_file(json_info)

#create an entry on a dictionary for the list of equilibriums for each file
exec("{}['{}']={}".format('filesDictionary', json_info['Info'], "temp_eqList_loaded"))
#clear memory of temp list o equilibriums
del temp_eqList_loaded


#initialize data storage
data = []
#generate data and plot
for i in range(len(filesDictionary[input_jsonFile])):
    curve = filesDictionary[input_jsonFile][i].GetCurve(Conc_Fe2, Conc_Fe3)
    plt.plot(curve[0], curve[1], json_info['Equilibrium'][i]['LineStyle'])
    data.append(curve)

plt.show()