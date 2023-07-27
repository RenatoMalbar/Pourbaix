import json
import os
import matplotlib.pyplot as plt
import equilibrium as eql
import logging

#creating logger
formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


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
    logger.info('Chosen file exists.')
else:
    logger.error('File does not exist.')
    exit()

#open json file
#f = open('src/equilibrium/{}'.format(temp_input_json +'.json'))
filesDictionary, inpt_variables = eql.from_json_file('src/equilibrium/{}'.format(temp_input_json +'.json'))

#get file with linestyles
f = open('src\styles\equilibriumStyles.json')
eqStyle = json.load(f)

#initialize data storage
data = []
#generate data and plot
for i in range(len(filesDictionary[input_jsonFile])):
    curve = filesDictionary[input_jsonFile][i].GetCurve(inpt_variables)

    #LoadStyles
    styles = eqStyle[filesDictionary[input_jsonFile][i].PhaseType]
    plt.plot(curve[0], curve[1], linestyle = styles['linestyle'], color = styles['color'], linewidth = styles['linewidth'])
    data.append(curve)

#X AXIS
plt.xlabel('pH')
plt.xlim((-2,16))
plt.ylabel('Potencial Redox [mV]')
plt.tight_layout()
plt.show()