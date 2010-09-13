class Singleton(object):
    __single = None # the one, true Singleton

    def __new__(classtype, *args, **kwargs):
        # Check to see if a __single exists already for this class
        # Compare class types instead of just looking for None so
        # that subclasses will create their own __single objects
        if classtype != type(classtype.__single):
            classtype.__single = object.__new__(classtype, *args, **kwargs)
            classtype.__single._runOnce()
        
        return classtype.__single

    def __getattr__(self, name):
        print "Attribute", name, "not assigned in", self
        return 0
        