import mercy.MercyApplication

db = mercy.MercyApplication.get_db()

class SimpleModel():
    def __init__(self, *args, **kwargs):
        db.Model.__init__(self, *args, **kwargs)
        for (k, v) in kwargs.iteritems():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                raise AttributeError("Invalid attribute {} => {}".format(k, v))

    def __repr__(self, *args, **kwargs):
        try:
            getattr(self.__class__, "__repr_keys__")
        except AttributeError, e:
            return db.Model.__repr__(self, *args, **kwargs)

        values = []
        for (name, otype) in self.__class__.__repr_keys__.iteritems():
            if otype == basestring:
                values += "'{}'".format(str(getattr(self.__class__, name)))
            else:
                values += str(getattr(self.__class__, name))
        return "<{}({})>".format(self.__class__.__name__, ', '.join(values))
