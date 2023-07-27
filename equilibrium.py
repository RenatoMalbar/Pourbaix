import sympy as sy
import logging
import json

#creating logger
formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)

#BASE CLASS DESCRIBING THE EQUILIBRIUM OF TWO CHEM SPECIES  
class equilibrium:

    def __init__(self, func, description, variables, LowerBound, LBoundType, UpperBound, UBoundType, ObjectType, EquilibriumType) -> None:
        self.func = func
        self.descrp = description        
        self.variables = variables
        self.LBound = LowerBound
        self.LBoundType = LBoundType
        self.UBound = UpperBound
        self.UBoundType = UBoundType
        self.Type = ObjectType
        self.PhaseType = EquilibriumType
        #initialize curve
        self.Curve = [[0,0],[0,0]]

    def __repr__(self) -> str:
        return ('equilibrium_base({},{})'.format(self.func, self.descrp))

    def __str__(self) -> str:
        return f"{self.descrp}"
    
    def function_eval(self, **kwargs):
        func_sy = sy.sympify(self.func)
        result = func_sy.evalf(subs=kwargs)
        return result
    
    @classmethod
    def from_json_object(cls, dict, variables):
        obj = (cls(dict['Equation'], dict['Reaction'], variables, dict['LowerBound'], dict['LowerBoundType'], dict['UpperBound'], dict['UpperBoundType'], dict['ObjectType'], dict['EquilibriumType'] ))
        logger.info('Created Equilibrium Obj - {}'.format(obj.descrp))
        return obj
    
    def __repr__(self) -> str:
        return ("equilibrium_ph('{}', '{}', {}, {}, {}, {})".format(self.func, self.descrp, self.LBound, self.LBoundType, self.UBound, self.UBoundType))
    
    def __str__(self) -> str:
        return f"{self.descrp}"

    def getBounds(self, BoundType, Bound, inpt_variables):
        #inicialize vector
        bounds = [0,0]        

        #BOUND TYPE FLOAT
        if BoundType == 'float':
            bounds[0]= float(Bound)
            bounds[1] = self.function_eval(ph=int(Bound))
                
        #BOUND TYPE EQUILIBRIUM_PH
        elif BoundType == 'equilibrium_ph':
            
            #debug
            logger.debug('Type and bound - {}, {}'.format(BoundType, Bound))

            bounds[0] = float(-2)

            #check if variables are set and create dictionar of variables for function_eval
            funcEval_input = dict()
            funcEval_input['ph'] = bounds[0]
            for var in self.variables:
                if var in inpt_variables:
                    funcEval_input[var] = inpt_variables[var]
                else:
                    logger.error('{} is missing from input.'.format(var))

            bounds[1] = self.func_eval_from_string(funcEval_input)
            #logger.debug('bounds: {}'.format(bounds))
        elif BoundType == 'equilibrium_pot':
            return NotImplemented
        else:
            return NotImplemented        
    
        return bounds

    def GetCurve(self, input_variables):
        # **************** EQUILIBRIUM_PH ****************    
        if self.Type == 'equilibrium_ph':            
            #get boundaries
            #LOWER
            self.Curve[0][0], self.Curve[1][0] = self.getBounds(self.LBoundType, self.LBound, input_variables)
            
            #UPPER
            self.Curve[0][1], self.Curve[1][1] = self.getBounds(self.UBoundType, self.UBound, input_variables)

            logger.debug('Updated curve property: {}'.format(self.Curve))

            return self.Curve

        else:
            return NotImplemented

    def func_eval_from_string(self, input_str):        
        result = self.function_eval(**input_str)
        return result

    def get_intersec(self, other):
        pass
    #encontrar inters de duas funções
    def find_root_ph(x, func1, func2, atividade_red, atividade_oxi):
        return func1(atividade_red, atividade_oxi, x) - func2(atividade_red, atividade_oxi, x)

#Private funciton
def __read_equilibrium_json_file(dict, aVariables):
    #merge variables files
    variables = aVariables
    #initialize a list of equilibriums for each file
    lst = []
    #Create all equilibrium objects from json file
    for i in range(0,len(dict['Equilibrium'])):
        eq = equilibrium.from_json_object(dict['Equilibrium'][i], variables)
        lst.append(eq)
        #(lst.append(Class.from_json_object(Equilibrium)))
    
    return lst

#Private function
def __input_var_method(var):
    inpt = float(input('Set {} value (must be numeric): '.format(var)))
    return inpt

#Private function
def __create_equilibrium_variables(neededVars):

    #create variable input
    input_variables = dict()
    for var in neededVars:
        try:
            temp_inputvar = __input_var_method(var)
            input_variables[var]=temp_inputvar
            #clear memory
            del temp_inputvar
        except ValueError:
            logger.error("Input must be numeric. Use . as decimal separator.")
            exit()        

    return input_variables

def from_json_file(file_path):
    
    #open json file
    file = open(file_path)
    file_info = json.load(file)        
    
    #create list of equilibriums (class) 
    temp_eqList_loaded = __read_equilibrium_json_file(file_info, file_info["AuxVariables"])
    logger.info('Created list of equilibriums for file - {}'.format(file_info['Info']))

    #CREATE DICTIONARY OF LOADED EQUILIBRIUM FILES
    filesDictionary = dict()
    #create an entry on a dictionary for the list of equilibriums for each file
    filesDictionary[file_info['Info']] = temp_eqList_loaded

    inpt_variables = __create_equilibrium_variables(file_info["AuxVariables"])

    return filesDictionary, inpt_variables