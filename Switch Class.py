#Switch class that holds Case objects
class Switch():

    def __init__(self, cases, else_case=None):
        #create a dictionary 
        self.cases = {case.i:case for case in cases}
        self.else_case = else_case
        
    def __get__(self):
        return self.cases
    
    #add method
    def add(self, i, function, params=None):
        self.cases[i] = Case(i, function, params)
    
    #get method
    def get(self, key):
        if key in self.cases:
            return self.cases[key]
        else:
            #throw exception if else_case not set
            if self.else_case==None:
                raise KeyError('Key error. Else Case not set')
            return self.else_case
        
    #pop method
    def pop(self, key):
        """removes key and returns function"""
        temp = self.cases[key]
        del(self.cases[key])
        return temp
        
    #add subscript notation
    def __getitem__(self, key):
        return self.get(key)

    #make object callable
    def __call__(self, key):
        return self.cases[key]
    
    #define len function output
    def __len__(self):
        return len(self.cases)
    
    #define membership operator
    def __contains__(self, key):
        return key in self.cases
    
    #define how printing switch object looks
    def __str__(self):
        sb = []
        for key in self.cases:
            sb.append("{value}".format(key=key, value=self.cases[key]))
        text = '{' + ', '.join(sb) + '}'
        if self.else_case != None:
            name = self.else_case.function.__name__ if callable(self.else_case.function) else self.else_case.function
            params = self.else_case.parameters
            text += f' Else:{name}{params}'
        return text
    
    def __repr__(self):
        return self.__str__()
    
#Case class that holds a function and parameters
class Case:
    def __init__(self, i, function, params=None):
        self.i = i
        self.function = function
        self.parameters = params
    
    def __get__(self):
        return self.function
    
    def __call__(self, *params):
        #use new parameters if given
        if len(params)>0: return self.function(*params)
        #use no parameters if no defaults or new parameters
        if self.parameters==None: return self.function()
        #make sure string params aren't unpacked
        if type(self.parameters)==str:return self.function(self.parameters)
        #else use default parameters
        return self.function(*self.parameters)
    
    #define how printing case object looks
    def __str__(self):
        name = self.function.__name__ if callable(self.function) else self.function
        params = self.parameters
        if type(params)==str: params = f"'{params}'"
        if params==None:params=''
        return f"{self.i}:{name}({params})"
    def __repr__(self):
        return self.__str__()
        
#Else object to store a case object to run if i has no case
class Else(Case):
    def __init__(self, function, params=None):
        self.function = function
        self.parameters = params        


def main():
    #Attempt to make switch statement look like C++
    ns = Switch({
        Case(1, print, ('one')),
        Case(2, print),
        Case(3, print, ('three')),
        Case(4, print, ('four')),
        Case(5, print, ('five')),
        Case(6, print, ('six')),
        },
        Else(print, ('99','problems'))
    )
    
    #add method overrided old case object if i matches
    ns[2]()
    ns.add(2, print, ('two'))
    ns[2]()
    
    #or makes new case if i is new
    ns[7]()
    ns.add(7, print, ('seven'))
    ns[7]()
    
    #need () in order to call function
    ns[10]() 
    
    #pass no parameters in order to use default parameters
    #passing parameters in call overrides defaults
    ns[1]('whatever we want overrides default')
    
    f = ns[3] #returns just the function
    f()
    
    ns[1]()
    #pop method causes next call to use else_case
    ns.pop(1)
    ns[1]()
    
    print(ns)

if __name__ == '__main__':
    main()