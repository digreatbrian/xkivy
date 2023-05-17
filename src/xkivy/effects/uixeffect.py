#UIXEffect
from kivy.uix.widget import Widget
from kivy.graphics.vertex_instructions import RoundedRectangle
from kivy.graphics.context_instructions import Color
from kivy.clock import Clock
from kivy.properties import( VariableListProperty,
ColorProperty)

from ..colors import default

class UIXEffect(Widget):
    '''UIX Effect to add effects to any widget such as:
        xradius :: Rounding widget corners
        xbg_color :: Changing background color
        
        '''
    xradius=\
    VariableListProperty([0,0,0,0],length=4)

    xbg_color=ColorProperty(default)

    md_bg_color=ColorProperty([0,0,0,0])

    background_color=\
    ColorProperty([0,0,0,0])

    def __init__(self,xradius=None,xbg_color=None,**kwargs):
        super().__init__(**kwargs)
        if xradius:self.xradius=xradius;self.radius=xradius
        if xbg_color:self.xbg_color=xbg_color
        self.bind(parent=self.prepare_uix)
        
    def on_background_color(self,inst,bg):
        if bg!=[0,0,0,0]:
            raise TypeError('Cant use "background_color" attribute,use "xbg_color" instead.')
            
    def on_md_bg_color(self,inst,bg):
        if bg!=[0,0,0,0]:
            raise TypeError('Cant use "md_bg_color" attribute,use "xbg_color" instead.')
            
    def disable_default_colors(self):
        #disable default colors
        self.background_color=[0,0,0,0]
        self.md_bg_color=[0,0,0,0]
        
    def prepare_uix(self,*a):
        if hasattr(self,'_uix_ready'):
            #canvas already loaded 
            return
        self.fbind("size",self.on_xsize)
        self.fbind("pos",self.on_xpos)
        self.disable_default_colors()
        self.color_instruction=Color()
        self.rect_instruction=RoundedRectangle()
        
        self.color_instruction.rgba=self.xbg_color
        self.rect_instruction.pos=self.pos
        self.rect_instruction.size=self.size
        self.rect_instruction.radius=self.xradius
        if not self.canvas:
            Clock.schedule_once(self.prepare_uix)
            return
        canvas=self.canvas.before
        canvas.add(self.color_instruction)
        canvas.add(self.rect_instruction)
        
        def update_radii(*_):self.radius=self.xradius ;#we assign self radius even if its useless to us .This is for the other widgets which uses this value to be able to update their state using updated radius value matching our self.xradius value.
        Clock.schedule_interval(update_radii,.1)
        self._uix_ready=True
        
    def update_uix(self,target,value):
        targets=['pos','size',
        'xbg_color',"xradius"]
        target=target.lower()
        if target not in targets:
            return
        if not hasattr(self,'_uix_ready'):
            self.prepare_uix()
        if target == 'pos':
            self.rect_instruction.pos=value
        elif target == 'size':
            self.rect_instruction.size=value
        elif target == 'xbg_color':
            self.color_instruction.rgba=value
        else:
            self.rect_instruction.radius=value
            self.radius=value
            #this is useless as radius is already being updated every milisecond
            #we assign self radius even if its useless to us .This is for the other widgets which uses this value to be able to update their state using updated radius value matching our self.xradius value.
            
    def on_size(self,*a):
        try:self.on_xsize(*a)
        except:pass
        
    def on_pos(self,*a):
        try:self.on_xpos(*a)
        except:pass
            
    def on_xsize(self,inst,size):
        #update size
        self.update_uix('size',size)
        
    def on_xpos(self,inst,pos):
        #update pos
        self.update_uix('pos',pos)
        
    #different from two methods above
    #because those methods are called for
    # properties that were already there eg
    #property size and pos and the below 
    #2 methods were created within this cls
    def on_xbg_color(self,inst,color):
        #update color
        self.update_uix('xbg_color',color)
        
    def on_xradius(self,inst,radius):
        #update radius
        self.update_uix('xradius',radius)

#AFTERCANVASUIXEFFECT
class CanvasAfterUIXEffect(Widget):
    '''CanvasAfterUIX Effect to add effects to any widget such as:
        Use this effect if UIXEffect is not working as expected.
        xradius :: Rounding widget corners
        xbg_color :: Changing background color
        
        '''
    xradius=\
    VariableListProperty([0,0,0,0],length=4)

    xbg_color=ColorProperty(default)

    md_bg_color=ColorProperty([0,0,0,0])

    background_color=\
    ColorProperty([0,0,0,0])

    def __init__(self,xradius=None,xbg_color=None,**kwargs):
        super().__init__(**kwargs)
        if xradius:self.xradius=xradius;self.radius=xradius
        if xbg_color:self.xbg_color=xbg_color
        self.bind(parent=self.prepare_uix)
        
    def on_background_color(self,inst,bg):
        if bg!=[0,0,0,0]:
            raise TypeError('Cant use "background_color" attribute,use "xbg_color" instead.')
            
    def on_md_bg_color(self,inst,bg):
        if bg!=[0,0,0,0]:
            raise TypeError('Cant use "md_bg_color" attribute,use "xbg_color" instead.')
            
    def disable_default_colors(self):
        #disable default colors
        self.background_color=[0,0,0,0]
        self.md_bg_color=[0,0,0,0]
        
    def prepare_uix(self,*a):
        if hasattr(self,'_uix_ready'):
            #canvas already loaded 
            return
        self.fbind("size",self.on_xsize)
        self.fbind("pos",self.on_xpos)
        self.disable_default_colors()
        self.color_instruction=Color()
        self.rect_instruction=RoundedRectangle()
        
        self.color_instruction.rgba=self.xbg_color
        self.rect_instruction.pos=self.pos
        self.rect_instruction.size=self.size
        self.rect_instruction.radius=self.xradius
        if not self.canvas:
            Clock.schedule_once(self.prepare_uix)
            return
        canvas=self.canvas
        canvas.add(self.color_instruction)
        canvas.add(self.rect_instruction)
        def update_radii(*_):self.radius=self.xradius ;#we assign self radius even if its useless to us .This is for the other widgets which uses this value to be able to update their state using updated radius value matching our self.xradius value.
        Clock.schedule_interval(update_radii,.1)
        self._uix_ready=True
        
    def update_uix(self,target,value):
        targets=['pos','size',
        'xbg_color',"xradius"]
        target=target.lower()
        if target not in targets:
            return
        if not hasattr(self,'_uix_ready'):
            self.prepare_uix()
        if target == 'pos':
            self.rect_instruction.pos=value
        elif target == 'size':
            self.rect_instruction.size=value
        elif target == 'xbg_color':
            self.color_instruction.rgba=value
        else:
            self.rect_instruction.radius=value
            self.radius=value
            #this is useless as radius is already being updated every milisecond
            #we assign self radius even if its useless to us .This is for the other widgets which uses this value to be able to update their state using updated radius value matching our self.xradius value.
            
    def on_size(self,*a):
        try:self.on_xsize(*a)
        except:pass
        
    def on_pos(self,*a):
        try:self.on_xpos(*a)
        except:pass
            
    def on_xsize(self,inst,size):
        #update size
        self.update_uix('size',size)
        
    def on_xpos(self,inst,pos):
        #update pos
        self.update_uix('pos',pos)
        
    #different from two methods above
    #because those methods are called for
    # properties that were already there eg
    #property size and pos and the below 
    #2 methods were created within this cls
    def on_xbg_color(self,inst,color):
        #update color
        self.update_uix('xbg_color',color)
            
    def on_xradius(self,inst,radius):
        #update radius
        self.update_uix('xradius',radius)
        




