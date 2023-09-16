'''Module for doing Kivy graphic operations outside th Main kivy Thread.This also depends on the kivy.clock module.'''

from kivy.clock import Clock

def xcall(callback ,args=[]):
    '''For calling kivy graphics callback outside the kivy thread.Calling functions/callables with kivy graphics operations safely without raising an issue.'''
    if not isinstance(args ,list):
        raise TypeError(f'Args Argument provided on "xcall" should be a list rather than "{args}"')
    def trig(none):
        callback(*args)
    trigger = Clock.create_trigger(trig)
    trigger()
            
def xsetattr(obj ,attrib ,value):
    '''For setting kivy attributes on objects outside the kivy thread eg Widget instance attributes.'''
    def xset():
        setattr(obj ,attrib ,value)
    xcall(xset)
    
    
