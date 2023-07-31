import sympy as sy
import logging
import json

#creating logger
formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)

#BASE CLASS DESCRIBING THE EQUILIBRIUM OF TWO CHEM SPECIES  
class equilibrium:

    def __init__(self, func, description, variables, LowerBound, LBoundType, UpperBound, UBoundType, ObjectType, EquilibriumType) -> None:
        self.func = func
        self.func_sy = sy.sympify(self.func)
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
        result = self.func_sy.evalf(subs=kwargs)
        logger.debug('(function_eval) function and args: {} <- {}'.format(self.func, kwargs))
        logger.debug('(function_eval) result: f(args) -> {}'.format(result))
        return result
    
    @classmethod
    def from_json_object(cls, dict, variables):
        obj = (cls(dict['Equation'], dict['Reaction'], variables, dict['LowerBound'], dict['LowerBoundType'], dict['UpperBound'], dict['UpperBoundType'], dict['ObjectType'], dict['EquilibriumType'] ))
        logger.info('(from_json_object) Created Equilibrium Obj - {}'.format(obj.descrp))
        return obj
    
    def __repr__(self) -> str:
        return ("equilibrium_ph('{}', '{}', {}, {}, {}, {})".format(self.func, self.descrp, self.LBound, self.LBoundType, self.UBound, self.UBoundType))
    
    def __str__(self) -> str:
        return f"{self.descrp}"

    def func_eval_from_dictionary(self, input_dict):    
        result = self.function_eval(**input_dict)  
        logger.debug('(func_eval_from_dictionary) Input to function: {}. Result: {}'.format(input_dict, result))      
        return result


#POURBAIX DIAGRAM CLASS - HOLDS ALL EQUILIBRIA, SET GLOBAL VARIABLES AND SET CURVES FOR EACH EQUILIBRIUM
class Pourbaix:

    def __init__(self, name, equilibria, input_variables) -> None:
        self.name = name
        self.eqDict = equilibria[self.name] #list of equilibria objects
        self.inpt_vars = input_variables #list of input variables

    def __str__(self) -> str:
        return ('Pourbaix equilibria for {}.'.format(self.name))

    #Set medium variables. Must be iniciated before getting curve.
    def set_equilibrium_variables(self) -> None:

        for key, value in self.inpt_vars.items():
            self.inpt_vars[key] = self.__input_var_method(key)

    #Set curves for all equilibria
    def set_curves(self):
        
        #Check is global varibles are set
        for value in self.inpt_vars.values():
            if value == NotImplemented:
                logger.error('Must set global variables first. Call method set_equilibrium_variables() before set_curves() or set inpt_vars manually.')
                return ValueError

        for name, equil in self.eqDict.items():
            self.SetCurve(equil, self.inpt_vars)

    @classmethod
    def from_json_file(cls, file_path):
        
        #open json file
        file = open(file_path)
        file_info = json.load(file)        
        
        #create list of equilibriums (class) 
        temp_eqList_loaded = cls.__read_equilibrium_json_file(file_info, file_info["AuxVariables"])
        logger.info('(from_json_file) Created list of equilibriums for file - {}'.format(file_info['Info']))

        #CREATE DICTIONARY OF LOADED EQUILIBRIUM FILES
        filesDictionary = dict()
        #create an entry on a dictionary for the list of equilibriums for each file
        filesDictionary[file_info['Info']] = temp_eqList_loaded

        #iniciate input var dictionary        
        inpt_variables = dict()
        for var in file_info["AuxVariables"]:
            inpt_variables[var] = NotImplemented

        prbx = cls(file_info['Info'], filesDictionary, inpt_variables)

        return prbx

    #Private method
    def SetCurve(self, equilib, input_variables):
        # **************** EQUILIBRIUM_PH ****************    
        if equilib.Type == 'equilibrium_ph':            
            #get boundaries
            #LOWER
            equilib.Curve[0][0], equilib.Curve[1][0] = self.__getBounds(equilib, equilib.LBoundType, equilib.LBound, input_variables)
            
            #UPPER
            equilib.Curve[0][1], equilib.Curve[1][1] = self.__getBounds(equilib, equilib.UBoundType, equilib.UBound, input_variables)

            logger.debug('(SetCurve) Updated curve property: {}'.format(equilib.Curve))

        else:
            return NotImplemented

    #Private method
    def __getBounds(self, equil, BoundType, Bound, inpt_variables):
        #inicialize vector
        bounds = [0,0]        

        #debug
        logger.debug('(__getBounds) Type and bound - {}, {}'.format(BoundType, Bound))

        #BOUND TYPE FLOAT
        if BoundType == 'float':
            bounds[0]= float(Bound)

            inpt_var_dict = (self.inpt_vars).copy()
            inpt_var_dict['ph'] = bounds[0]
            logger.debug('(__getBounds) inpt_var_dict: {}'.format(inpt_var_dict))
            bounds[1] = equil.function_eval(**inpt_var_dict)
            #bounds[1] = equil.function_eval(ph=int(Bound))
                
        #BOUND TYPE EQUILIBRIUM_PH
        elif BoundType == 'equilibrium_ph':   

            #gets intersection of curve with limit curve
            bounds[0] =  (self.__get_intersec_phDep(equil, self.eqDict[Bound], self.inpt_vars))
                
            #check if variables are set and create dictionary of variables for function_eval
            inpt_var_dict = dict()
            inpt_var_dict['ph'] = bounds[0]
            for var in equil.variables:
                if var in inpt_variables:
                    inpt_var_dict[var] = inpt_variables[var]
                else:
                    logger.error('{} is missing from input.'.format(var))

            logger.debug('(__getBounds) inpt_var_dict: {}'.format(inpt_var_dict))
            bounds[1] = equil.func_eval_from_dictionary(inpt_var_dict)
        
        #BOUND TYPE EQUILIBRIUM_POT
        elif BoundType == 'equilibrium_pot':
            logger.error('Limit type {} not implemented'.format(BoundType))
            return NotImplemented
        
        else:
            logger.error('Limit type {} not implemented'.format(BoundType))
            return NotImplemented        
    
        return bounds

    #Private method
    #Get intersection of two curves (ph dependent variable)
    @staticmethod
    def __get_intersec_phDep(equilib, other, variables_dict):
        
        logger.debug('(__get_intersec_phDep) variables input: {}'.format(variables_dict))
        
        ph = sy.symbols('ph')
        func1 = equilib.function_eval(**variables_dict)
        func2 = other.function_eval(**variables_dict)

        intersec = sy.solve(func1 - func2, ph)

        logger.debug('(__get_intersec_phDep) Intersection of ({}) and ({}) -> pH = {}'.format(func1, func2, intersec))

        return float(intersec[0])

    #Private method
    @staticmethod
    def __read_equilibrium_json_file(dictionary, aVariables):
        #merge variables files
        variables = aVariables
        #initialize a list of equilibriums for each file
        equilibria = dict() 
        #Create all equilibrium objects from json file
        for i in range(0,len(dictionary['Equilibrium'])):
            equilibria[dictionary['Equilibrium'][i]['Name']] = equilibrium.from_json_object(dictionary['Equilibrium'][i], variables)
        
        return equilibria

    #Private method
    @staticmethod
    def __input_var_method(var):
        inpt = float(input('Set {} value (must be numeric): '.format(var)))
        return inpt
    