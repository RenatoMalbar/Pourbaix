import equilibrium as eql
import logging
import matplotlib.pyplot as plt


#creating logger
formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


#app
file_path = (r'src\equilibrium\iron.json')

iron = eql.Pourbaix.from_json_file(file_path)

iron.set_equilibrium_variables()
iron.set_curves()

for key, equil in iron.eqDict.items():
    plt.plot(equil.Curve[0], equil.Curve[1])

plt.show()


