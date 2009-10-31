#!/usr/bin/env python

import time
try:
    from hashlib import md5
except ImportError:
    from md5 import md5

def sid(seed=""):
    """The hash of the server time + seed makes an unique SID for each session.
    """
    sid = md5()
    sid.update(repr(time.time()))
    if seed:
        sid.update(seed)
    return sid.hexdigest()

def make_vals(val, klass, klass_inst=None, prop=None, part=False):
    """
    Creates a class instance with a specified value, the specified
    class instance are a value on a property in a defined class instance.
    
    :param klass_inst: The class instance which has a property on which 
        what this function returns is a value.
    :param val: The value
    :param prop: The property which the value should be assigned to.
    :param klass: The value class
    :param part: If the value is one of a possible list of values it should be
        handled slightly different compared to if it isn't.
    :return: Value class instance
    """
    ci = None
    #print "_make_val: %s %s (%s)" % (prop,val,klass)
    if isinstance(val, bool):
        ci = klass(text="%s" % val)
    elif isinstance(val, int):
        ci = klass(text="%d" % val)
    elif isinstance(val, basestring):
        ci = klass(text=val)
    elif val == None:
        ci = klass()
    elif isinstance(val, dict):
        ci = make_instance(klass, val)
    elif not part:
        cis = [make_vals(sval, klass, klass_inst, prop, True) for sval in val]
        setattr(klass_inst, prop, cis)
    else:
        raise ValueError("strange instance type: %s on %s" % (type(val),val))
        
    if part:
        return ci
    else:        
        if ci:
            cis = [ci]
        setattr(klass_inst, prop, cis)
    
def make_instance(klass, spec):
    """
    Constructs a class instance containing the specified information
    
    :param klass: The class
    :param spec: Information to be placed in the instance
    :return: The instance
    """
    klass_inst = klass()
    for prop in klass.c_attributes.values():
        if prop in spec:
            if isinstance(spec[prop],bool):
                setattr(klass_inst,prop,"%s" % spec[prop])
            elif isinstance(spec[prop], int):
                setattr(klass_inst,prop,"%d" % spec[prop])
            else:
                setattr(klass_inst,prop,spec[prop])
    if "text" in spec:
        setattr(klass_inst,"text",spec["text"])
        
    for prop, klass in klass.c_children.values():
        if prop in spec:
            if isinstance(klass, list): # means there can be a list of values
                make_vals(spec[prop], klass[0], klass_inst, prop)
            else:
                ci = make_vals(spec[prop], klass, klass_inst, prop, True)
                setattr(klass_inst, prop, ci)
    return klass_inst