classes={}

def register(klass):
    classes[klass.__name__]=klass

def get(name):
    return classes[name]()
