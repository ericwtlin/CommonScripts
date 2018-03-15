"""
Doc inheriter
这个方法没有另一种方法的多重继承的问题，但是，如果有类里面用到了metaclass了已经（例如ABCMeta），则会报错：
TypeError: metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases

另一个问题是meta class，Python 3才有。
"""
from functools import partial


# Replace this with actual implementation from
# http://code.activestate.com/recipes/577748-calculate-the-mro-of-a-class/
# (though this will work for simple cases)
def mro(*bases):
    return bases[0].__mro__


# This definition is only used to assist static code analyzers
def inherit_ancestor_docstring(fn):
    '''Copy docstring for method from superclass

    For this decorator to work, the class has to use the `InheritableDocstrings`
    metaclass.
    '''
    raise RuntimeError('Decorator can only be used in classes '
                       'using the `InheritableDocstrings` metaclass')


def _inherit_ancestor_docstring(mro, fn):
    '''Decorator to set docstring for *fn* from *mro*'''

    if fn.__doc__ is not None:      # if the class itself or its nearest ancestor has a docstring, return it
        #raise RuntimeError('Function already has docstring')
        return fn

    # Search for docstring in superclass
    for cls in mro:
        super_fn = getattr(cls, fn.__name__, None)
        if super_fn is None:
            continue
        fn.__doc__ = super_fn.__doc__
        break
    else:
        raise RuntimeError("Can't inherit docstring for %s: method does not "
                           "exist in superclass" % fn.__name__)

    return fn


class InheritableDocstrings(type):
    @classmethod
    def __prepare__(cls, name, bases, **kwds):
        classdict = super().__prepare__(name, bases, *kwds)

        # Inject decorators into class namespace
        classdict['inherit_ancestor_docstring'] = partial(_inherit_ancestor_docstring, mro(*bases))

        return classdict

    def __new__(cls, name, bases, classdict):

        # Decorator may not exist in class dict if the class (metaclass
        # instance) was constructed with an explicit call to `type`.
        # (cf http://bugs.python.org/issue18334)
        if 'inherit_ancestor_docstring' in classdict:

            # Make sure that class definition hasn't messed with decorators
            copy_impl = getattr(classdict['inherit_ancestor_docstring'], 'func', None)
            if copy_impl is not _inherit_ancestor_docstring:
                raise RuntimeError('No inherit_ancestor_docstring attribute may be created '
                                   'in classes using the InheritableDocstrings metaclass')

            # Delete decorators from class namespace
            del classdict['inherit_ancestor_docstring']

        return super().__new__(cls, name, bases, classdict)


class FooParent(object):
    def foo(self):
        """ Frobber parent
        """

class Foo(FooParent, metaclass=InheritableDocstrings):
    @inherit_ancestor_docstring
    def foo(self):
        """Frobber
        """
        pass

class Bar(Foo, metaclass=InheritableDocstrings):
    @inherit_ancestor_docstring
    def foo(self):
        pass

class Bar2(Foo, metaclass=InheritableDocstrings):
    @inherit_ancestor_docstring
    def foo(self):
        """Frobber of son
        """
        pass

if __name__ == "__main__":
    f = Foo()
    b = Bar()
    b2 = Bar2()
    print(f.foo.__doc__)    #Frobber
    print(b.foo.__doc__)    #Frobber
    print(b2.foo.__doc__)   #Frobber of son