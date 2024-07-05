#from Check import Error
#from Check import errors
class Error:
    pass
errors = []

class Context:

    def __init__(self, general = None, father = None):
        if general == None:
            general = {}
        self.general = general
        self.father = father

    def __getitem__(self, key):
        try:
            a = self.general[key]
            return a
        except:
            try:
                a = self.father[key]
                return a
            except:
                
                #raise KeyError(f'Invalid key: \'{key}\'')
                if type(key) == type('sdf') and len(key) > 1 and key[-2:] == '#@':
                    return
                errors.append(f'Invalid key: \'{key}\'')
                return Error()
                #raise KeyError(f'Invalid key: \'{key}\'')
    
    def __setitem__(self, key, value):
        self.general[key] = value

    def check_key(self, key, value):
        if key in self.general:
            errors.append(f'Invalid key: \'{key}\'')
            return Error()
            #raise KeyError(f'\'{key}\' is defined ')
        self.general[key] = value
    def rev(self, key):
        try:
            a = self.general[key]
            return a
        except:
            try:
                a = self.father[key]
                return a
            except:
                return 'None'