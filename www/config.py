config_default={
    'debug':True,
    'db':{
        'host':'127.0.0.1',
        'port':3306,
        'user':'www-data',
        'password':'www-data',
        'db':'awesome'
    },
    'session':{
        'secret':'AwEsOmE'
    }
}

config_override={
    'db':{
        'host':'127.0.0.1'
    }
}

def merge(default:dict,override:dict)->dict:
    result={}
    for key,value in default.items():
        if key in override:
            result[key]=merge(value,override[key]) if isinstance(value,dict) else override[key]
        else:
            result[key]=value
    return result

configs=merge(config_default,config_override)

class Dict(dict):
    '''
    Simple dict but support access as x.y style.
    '''
    def __init__(self,names=(),values=(),**kw):
        super(Dict,self).__init__(**kw)
        for key,value in zip(names, values):
            self[key]=value

    def __getattr__(self,key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'"%key)

    def __setattr__(self,key,value):
        self[key]=value

def toDict(d:dict)->Dict:
    D=Dict()
    for key,value in d.items():
        D[key]=toDict(value) if isinstance(value,dict) else value
    return D

configs=toDict(configs)

if __name__ == '__main__':
    print(configs)