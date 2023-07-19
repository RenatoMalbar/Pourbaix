from equilibrium import *

def read_equilibrium_json_file(dict, aVariables):
    #merge variables files
    variables = aVariables
    #initialize a list of equilibriums for each file
    lst = []
    #Create all equilibrium objects from json file
    for i in range(0,len(dict['Equilibrium'])):
        exec('{}.append({}.from_json_object({},{}))'.format('lst', dict['Equilibrium'][i]['ObjectType'], dict['Equilibrium'][i], variables))
        #(lst.append(Class.from_json_object(Equilibrium)))
    
    return lst


def create_equilibrium_variables(neededVars):

    #create variable input
    input_variables = dict()
    for var in neededVars:
        try:
            temp_inputvar = float(input('Set {} value (must be numeric): '.format(var)))
            input_variables[var]=temp_inputvar
            #clear memory
            del temp_inputvar
        except ValueError:
            print("Input must be numeric. Use . as decimal separator.")
            exit()
        

    return input_variables