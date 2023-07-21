import sympy as sy

#BASE CLASS DESCRIBING THE EQUILIBRIUM OF TWO CHEM SPECIES  
class equilibrium:

    def __init__(self, func, description, variables, LowerBound, LBoundType, UpperBound, UBoundType, EquilibriumType) -> None:
        self.func = func
        self.descrp = description        
        self.variables = variables
        self.LBound = LowerBound
        self.LBoundType = LBoundType
        self.UBound = UpperBound
        self.UBoundType = UBoundType
        self.EquilType = EquilibriumType
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
        return (cls(dict['Equation'], dict['Reaction'], variables, dict['LowerBound'], dict['LowerBoundType'], dict['UpperBound'], dict['UpperBoundType'], dict['ObjectType'] ))
    
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
            bounds[0] = float(-2)

            #check if variables are set and create input for function_eval
            funcEval_input = dict()
            funcEval_input['ph'] = bounds[0]
            for var in self.variables:
                if var in inpt_variables:
                    funcEval_input[var] = inpt_variables[var]
                else:
                    print(var, 'is missing from input.')

            bounds[1] = self.func_eval_from_string(funcEval_input)
            #print('Debug - bounds:', bounds)
        elif BoundType == 'equilibrium_pot':
            return NotImplemented
        else:
            return NotImplemented        
    
        return bounds

    def GetCurve(self, input_variables):
        # **************** EQUILIBRIUM_PH ****************    
        if self.EquilType == 'equilibrium_ph':            
            #get boundaries
            #LOWER
            self.Curve[0][0], self.Curve[1][0] = self.getBounds(self.LBoundType, self.LBound, input_variables)
            
            #UPPER
            self.Curve[0][1], self.Curve[1][1] = self.getBounds(self.UBoundType, self.UBound, input_variables)
        
            return self.Curve

        else:
            return NotImplemented

    def func_eval_from_string(self, input_str):        
        result = self.function_eval(**input_str)
        #print('Debug - input_str, result:', input_str, result)
        return result