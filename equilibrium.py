import sympy as sy

#BASE CLASS DESCRIBING THE EQUILIBRIUM OF TWO CHEM SPECIES  
class equilibrium_base:

    def __init__(self, func, description, variables) -> None:
        self.func = func
        self.descrp = description        
        self.variables = variables

    def __repr__(self) -> str:
        return ('equilibrium_base({},{})'.format(self.func, self.descrp))

    def __str__(self) -> str:
        return f"{self.descrp}"
    
    def function_creator(self, **kwargs):
        func_sy = sy.sympify(self.func)
        return func_sy.evalf(subs=kwargs)
    
#CLASS DESCRIBING THE EQUILIBRIUM OF TWO CHEM SPECIES - pH AS INDEPENDENT VARIABLE
class equilibrium_ph(equilibrium_base):
    def __init__(self, func, description, variables, LowerBound, LBoundType, UpperBound, UBoundType) -> None:
        super().__init__(func, description, variables)
        self.LBound = LowerBound
        self.LBoundType = LBoundType
        self.UBound = UpperBound
        self.UBoundType = UBoundType
    
    @classmethod
    def from_json_object(cls, dic, variables):
        return (cls(dic['Equation'], dic['Reaction'], variables, dic['LowerBound'], dic['LowerBoundType'], dic['UpperBound'], dic['UpperBoundType']))
    
    def __repr__(self) -> str:
        return ("equilibrium_ph('{}', '{}', {}, {}, {}, {})".format(self.func, self.descrp, self.LBound, self.LBoundType, self.UBound, self.UBoundType))
    
    def __str__(self) -> str:
        return f"{self.descrp}"
    
    def GetCurve(self, CFe2, CFe3):
        #initialize boundaries
        Boundaries = [[0,0],[0,0]]
        
        #get boundaries
        #LOWER
        if self.LBoundType == 'int':
            Boundaries[0][0] = int(self.LBound)
            inpt_string  = ph=int(self.LBound)
            Boundaries[1][0] = self.function_creator(ph=int(self.LBound), CFe2 = CFe2, CFe3 = CFe3)
        else:
            return NotImplemented

        #UPPER
        if self.UBoundType == 'int':
            Boundaries[0][1] = int(self.UBound)
            Boundaries[1][1] = self.function_creator(ph=int(self.UBound), CFe2 = CFe2, CFe3 = CFe3)
        else:
            return NotImplemented
        
        return Boundaries
    
    def new_GetCurve(self, CFe2, CFe3):
        #initialize boundaries
        Boundaries = [[0,0],[0,0]]

        #set variables
        for var in self.variables:
            x=1

        #get boundaries
        #LOWER
        if self.LBoundType == 'int':
            Boundaries[0][0] = int(self.LBound)
            inpt_string  = ph=int(self.LBound)
            Boundaries[1][0] = self.function_creator(ph=int(self.LBound), CFe2 = CFe2, CFe3 = CFe3)
        else:
            return NotImplemented

        #UPPER
        if self.UBoundType == 'int':
            Boundaries[0][1] = int(self.UBound)
            Boundaries[1][1] = self.function_creator(ph=int(self.UBound), CFe2 = CFe2, CFe3 = CFe3)
        else:
            return NotImplemented
        
        return Boundaries

    
#CLASS DESCRIBING THE EQUILIBRIUM OF TWO CHEM SPECIES - REDUCTION POTENCIAL AS INDEPENDENT VARIABLE

