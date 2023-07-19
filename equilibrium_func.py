from equilibrium import *

def read_equilibrium_json_file(dict, mVariables, aVariables):
    #merge variables files
    variables = mVariables+aVariables
    #initialize a list of equilibriums for each file
    lst = []
    #Create all equilibrium objects from json file
    for i in range(0,len(dict['Equilibrium'])):
        exec('{}.append({}.from_json_object({},{}))'.format('lst', dict['Equilibrium'][i]['ObjectType'], dict['Equilibrium'][i], variables))
        #(lst.append(Class.from_json_object(Equilibrium)))
    
    return lst