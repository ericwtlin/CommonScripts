"""
Doc inheriter
这个方法有个问题：
如果有多重继承的话，子类有DocInherit装饰，父类也有DocInherit装饰，则会在overridden = getattr(super(cls, obj), self.name, None)时陷入无限循环之中。
"""


from functools import wraps

class DocInherit(object):
    """
    Docstring inheriting method descriptor
    The class itself is also used as a decorator doc_inherit decorator

        if the function of son class has its own doc:
            use the son's own doc
        else:
            use its parent's doc
    """

    def __init__(self, mthd):
        self.mthd = mthd
        self.name = mthd.__name__

    def __get__(self, obj, cls):
        if obj:
            return self.get_with_inst(obj, cls)
        else:
            return self.get_no_inst(cls)

    def get_with_inst(self, obj, cls):
        overridden = getattr(super(cls, obj), self.name, None)

        @wraps(self.mthd, assigned=('__name__', '__module__', '__doc__'))
        def f(*args, **kwargs):
            return self.mthd(obj, *args, **kwargs)

        return self.use_parent_doc(f, overridden)

    def get_no_inst(self, cls):
        for parent in cls.__mro__[1:]:
            overridden = getattr(parent, self.name, None)
            if overridden:
                break

        @wraps(self.mthd, assigned=('__name__', '__module__', '__doc__'))
        def f(*args, **kwargs):
            return self.mthd(*args, **kwargs)

        return self.use_parent_doc(f, overridden)

    def use_parent_doc(self, func, source):
        if source is None:
            raise NameError("Can't find '%s' in parents" % self.name)
        if func.__doc__ is None:    # if func doesn't have its own doc, use its parents'.
            func.__doc__ = source.__doc__
        return func

doc_inherit = DocInherit
class FooParent(object):
    def foo(self):
        """ Frobber parent

        Returns:

        """

class Foo(FooParent):
    @DocInherit
    def foo(self):
        """Frobber
        """
        pass

class Bar(Foo):
    @DocInherit
    def foo(self):
        pass

class Bar2(Foo):
    @DocInherit
    def foo(self):
        """Frobber of son
        """
        pass

if __name__ == "__main__":
    f = Foo()
    b = Bar()
    b2 = Bar2()
    #print(f.foo.__doc__)
    print(b.foo.__doc__)    #Frobber
    #print(b2.foo.__doc__)   #Frobber of son