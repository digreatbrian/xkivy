#UIXEffect
from kivy.uix.widget import NumericProperty, Widget
from kivy.graphics.vertex_instructions import RoundedRectangle ,Line
from kivy.graphics.context_instructions import Color
from kivy.clock import Clock
from kivy.properties import(
    VariableListProperty,
    ColorProperty
    )

from ..colors import default

class UIXEffect:
    '''UIX Effect to add effects to any widget such as:
        xradius :: Rounding widget corners
        xbg_color :: Changing background color
        xborder_color :: Changing border color
        xborder_width :: Changing border width
        
        '''
    xradius = VariableListProperty([0,0,0,0],length=4)
    xbg_color = ColorProperty(default)
    xborder_color = ColorProperty([0,0,0,0])
    xborder_width = NumericProperty(.25)
    xborder_radius = VariableListProperty([0] * 4, length = 4)
    md_bg_color = ColorProperty([0,0,0,0])
    background_color = ColorProperty([0,0,0,0])
    def __init__(self,xradius = None, xbg_color = None, **kwargs):
        super().__init__(**kwargs)
        if xradius:
            self.xradius=xradius
            self.radius=xradius
        if xbg_color:
            self.xbg_color=xbg_color

        self.bind(parent = Clock.schedule_once(self.prepare_uix))  
    
    def on_background_color(self, inst, bg):
        if bg != [0, 0, 0, 0]:
            raise TypeError('Cant use "background_color" attribute, use "xbg_color" instead.')
            
    def on_md_bg_color(self, inst, bg):
        if bg != [0,0,0,0]:
            raise TypeError('Cant use "md_bg_color" attribute,use "xbg_color" instead.')
            
    def disable_default_colors(self):
        #disable default colors
        self.background_color = [0, 0, 0, 0]
        self.md_bg_color = [0, 0, 0, 0]
        
    def prepare_uix(self,*a):
        if hasattr(self,'_uix_ready'):
            #canvas already loaded 
            return
        self.disable_default_colors()
        self.color_instruction = Color()
        self.rect_instruction = RoundedRectangle()
        self.border_color_instruction = Color()
        self.border_instruction = Line(
            cap = 'none',
            joint = 'round',
            close = True,
            )
        
        self.fbind("size",self.on_xsize)
        self.fbind("pos",self.on_xpos)

        self.color_instruction.rgba = self.xbg_color
        self.rect_instruction.pos = self.pos
        self.rect_instruction.size = self.size
        self.rect_instruction.radius = self.xradius
        
        self.border_color_instruction.rgba = self.xborder_color
        self.border_instruction.width = self.xborder_width

        if not self.xborder_radius:
            xborder_radius = self.xradius
        else:
            xborder_radius = self.xborder_radius
            
        self.border_instruction.rounded_rectangle = [
            self.x -1 ,
            self.y - 1 ,
            self.width + 2 ,
            self.height + 2 ,
            *xborder_radius,
            100,
        ]

        if not self.canvas:
            Clock.schedule_once(self.prepare_uix)
            return
        
        canvas = self.canvas.before
        canvas.add(self.color_instruction)
        canvas.add(self.rect_instruction)

        canvas.add(self.border_color_instruction)
        canvas.add(self.border_instruction)
        
        def update_radii(*_):
            # we assign self radius even if its useless to us .
            # This is for the other widgets which uses this value to be able
            # to update their state using updated radius value matching our self.xradius value.
            self.radius = self.xradius
        
        Clock.schedule_interval(update_radii,.1)
        self._uix_ready=True

    def on_size(self,*a):
        try:self.on_xsize(*a)
        except:pass
        
    def on_pos(self,*a):
        try:self.on_xpos(*a)
        except:pass
        
    def update_uix(self,target,value):
        targets = [
            'pos',
            'size',
            'xbg_color',
            "xradius",
            'xborder_color',
            'xborder_width',
            'xborder_radius',
            ]
        target = target.lower()
        if target not in targets:
            return
        
        if not hasattr(self,'_uix_ready'):
            self.prepare_uix()

        if target == 'pos':
            self.rect_instruction.pos = value
            if not self.xborder_radius:
                self.border_instruction.rounded_rectangle = [
                    self.x -1 ,
                    self.y - 1 ,
                    self.width + 2 ,
                    self.height + 2 ,
                    *self.xradius,
                    100,
            ]
            else:
                self.border_instruction.rounded_rectangle = [
                    self.x -1 ,
                    self.y - 1 ,
                    self.width + 2 ,
                    self.height + 2 ,
                    *self.xborder_radius,
                    100,
                ]
        

        elif target == 'size':
            self.rect_instruction.size = value
            if not self.xborder_radius:
                self.border_instruction.rounded_rectangle = [
                    self.x -1 ,
                    self.y - 1 ,
                    self.width + 2 ,
                    self.height + 2 ,
                    *self.xradius,
                    100,
            ]
            else:
                self.border_instruction.rounded_rectangle = [
                    self.x -1 ,
                    self.y - 1 ,
                    self.width + 2 ,
                    self.height + 2 ,
                    *self.xborder_radius,
                    100,
                ]

        elif target == 'xbg_color':
            self.color_instruction.rgba = value

        elif target == 'xborder_color':
            self.border_color_instruction.rgba = value
        
        elif target == 'xborder_width':
            self.border_instruction.width = value

        elif target == 'xborder_radius':
            if not value:
                self.border_instruction.rounded_rectangle = [
                    self.x -1 ,
                    self.y - 1 ,
                    self.width + 2 ,
                    self.height + 2 ,
                    *self.xradius,
                    100,
            ]
            else:
                self.border_instruction.rounded_rectangle = [
                    self.x -1 ,
                    self.y - 1 ,
                    self.width + 2 ,
                    self.height + 2 ,
                    *value,
                    100,
                ]

        else:
            #xradius
            self.rect_instruction.radius = value
            if not self.xborder_radius:
                self.border_instruction.rounded_rectangle = [
                    self.x -1 ,
                    self.y - 1 ,
                    self.width + 2 ,
                    self.height + 2 ,
                    *value,
                    100,
            ]
            self.radius = value
            # this is useless as radius is already being updated every milisecond
            #we assign self radius even if its useless to us .
            # This is for the other widgets which uses this value to be able
            #  to update their state using updated radius value matching our self.xradius value.
       
    def on_xsize(self,inst,size):
        #update size
        self.update_uix('size',size)
        
    def on_xpos(self,inst,pos):
        #update pos
        self.update_uix('pos',pos)
        
    # different from two methods above
    # because those methods are called for
    # properties that were already there eg
    # property size and pos and the below 
    # 2 methods were created within this cls
    def on_xbg_color(self,inst,color):
        #update color
        self.update_uix('xbg_color',color)
        
    def on_xradius(self,inst,radius):
        #update radius
        self.update_uix('xradius',radius)

    def on_xborder_color(self,inst, color):
        #update border color
        self.update_uix('xborder_color',color)

    def on_xborder_width(self,inst, w):
        #update border witdth
        self.update_uix('xborder_width',w)

    def on_xborder_radius(self,inst, r):
        #update border radius
        self.update_uix('xborder_radius',r)

#AFTERCANVASUIXEFFECT
class CanvasAfterUIXEffect(Widget):
    '''CanvasAfterUIX Effect to add effects to any widget such as:
        xradius :: Rounding widget corners
        xbg_color :: Changing background color
        xborder_color :: Changing border color
        xborder_width :: Changing border width
        
        '''
    xradius = VariableListProperty([0,0,0,0],length=4)
    xbg_color = ColorProperty(default)
    xborder_color = ColorProperty([0,0,0,0])
    xborder_width = NumericProperty(.25)
    xborder_radius = VariableListProperty([0] * 4, length = 4)
    md_bg_color = ColorProperty([0,0,0,0])
    background_color = ColorProperty([0,0,0,0])
    def __init__(self,xradius = None, xbg_color = None, **kwargs):
        super().__init__(**kwargs)
        if xradius:
            self.xradius=xradius
            self.radius=xradius
        if xbg_color:
            self.xbg_color=xbg_color

        self.bind(parent = Clock.schedule_once(self.prepare_uix))  
    
    def on_background_color(self, inst, bg):
        if bg != [0, 0, 0, 0]:
            raise TypeError('Cant use "background_color" attribute, use "xbg_color" instead.')
            
    def on_md_bg_color(self, inst, bg):
        if bg != [0,0,0,0]:
            raise TypeError('Cant use "md_bg_color" attribute,use "xbg_color" instead.')
            
    def disable_default_colors(self):
        #disable default colors
        self.background_color = [0, 0, 0, 0]
        self.md_bg_color = [0, 0, 0, 0]
        
    def prepare_uix(self,*a):
        if hasattr(self,'_uix_ready'):
            #canvas already loaded 
            return
        self.disable_default_colors()
        self.color_instruction = Color()
        self.rect_instruction = RoundedRectangle()
        self.border_color_instruction = Color()
        self.border_instruction = Line(
            cap = 'none',
            joint = 'round',
            close = True,
            )
        
        self.fbind("size",self.on_xsize)
        self.fbind("pos",self.on_xpos)

        self.color_instruction.rgba = self.xbg_color
        self.rect_instruction.pos = self.pos
        self.rect_instruction.size = self.size
        self.rect_instruction.radius = self.xradius
        
        self.border_color_instruction.rgba = self.xborder_color
        self.border_instruction.width = self.xborder_width

        if not self.xborder_radius:
            xborder_radius = self.xradius
        else:
            xborder_radius = self.xborder_radius
            
        self.border_instruction.rounded_rectangle = [
            self.x -1 ,
            self.y - 1 ,
            self.width + 2 ,
            self.height + 2 ,
            *xborder_radius,
            100,
        ]

        if not self.canvas:
            Clock.schedule_once(self.prepare_uix)
            return
        
        canvas = self.canvas.after
        canvas.add(self.color_instruction)
        canvas.add(self.rect_instruction)

        canvas.add(self.border_color_instruction)
        canvas.add(self.border_instruction)
        
        def update_radii(*_):
            # we assign self radius even if its useless to us .
            # This is for the other widgets which uses this value to be able
            # to update their state using updated radius value matching our self.xradius value.
            self.radius = self.xradius
        
        Clock.schedule_interval(update_radii,.1)
        self._uix_ready=True

    def on_size(self,*a):
        try:self.on_xsize(*a)
        except:pass
        
    def on_pos(self,*a):
        try:self.on_xpos(*a)
        except:pass
        
    def update_uix(self,target,value):
        targets = [
            'pos',
            'size',
            'xbg_color',
            "xradius",
            'xborder_color',
            'xborder_width',
            'xborder_radius',
            ]
        target = target.lower()
        if target not in targets:
            return
        
        if not hasattr(self,'_uix_ready'):
            self.prepare_uix()

        if target == 'pos':
            self.rect_instruction.pos = value
            if not self.xborder_radius:
                self.border_instruction.rounded_rectangle = [
                    self.x -1 ,
                    self.y - 1 ,
                    self.width + 2 ,
                    self.height + 2 ,
                    *self.xradius,
                    100,
            ]
            else:
                self.border_instruction.rounded_rectangle = [
                    self.x -1 ,
                    self.y - 1 ,
                    self.width + 2 ,
                    self.height + 2 ,
                    *self.xborder_radius,
                    100,
                ]
        

        elif target == 'size':
            self.rect_instruction.size = value
            if not self.xborder_radius:
                self.border_instruction.rounded_rectangle = [
                    self.x -1 ,
                    self.y - 1 ,
                    self.width + 2 ,
                    self.height + 2 ,
                    *self.xradius,
                    100,
            ]
            else:
                self.border_instruction.rounded_rectangle = [
                    self.x -1 ,
                    self.y - 1 ,
                    self.width + 2 ,
                    self.height + 2 ,
                    *self.xborder_radius,
                    100,
                ]

        elif target == 'xbg_color':
            self.color_instruction.rgba = value

        elif target == 'xborder_color':
            self.border_color_instruction.rgba = value
        
        elif target == 'xborder_width':
            self.border_instruction.width = value

        elif target == 'xborder_radius':
            if not value:
                self.border_instruction.rounded_rectangle = [
                    self.x -1 ,
                    self.y - 1 ,
                    self.width + 2 ,
                    self.height + 2 ,
                    *self.xradius,
                    100,
            ]
            else:
                self.border_instruction.rounded_rectangle = [
                    self.x -1 ,
                    self.y - 1 ,
                    self.width + 2 ,
                    self.height + 2 ,
                    *value,
                    100,
                ]

        else:
            #xradius
            self.rect_instruction.radius = value
            if not self.xborder_radius:
                self.border_instruction.rounded_rectangle = [
                    self.x -1 ,
                    self.y - 1 ,
                    self.width + 2 ,
                    self.height + 2 ,
                    *value,
                    100,
            ]
            self.radius = value
            # this is useless as radius is already being updated every milisecond
            #we assign self radius even if its useless to us .
            # This is for the other widgets which uses this value to be able
            #  to update their state using updated radius value matching our self.xradius value.
       
    def on_xsize(self,inst,size):
        #update size
        self.update_uix('size',size)
        
    def on_xpos(self,inst,pos):
        #update pos
        self.update_uix('pos',pos)
        
    # different from two methods above
    # because those methods are called for
    # properties that were already there eg
    # property size and pos and the below 
    # 2 methods were created within this cls
    def on_xbg_color(self,inst,color):
        #update color
        self.update_uix('xbg_color',color)
        
    def on_xradius(self,inst,radius):
        #update radius
        self.update_uix('xradius',radius)

    def on_xborder_color(self,inst, color):
        #update border color
        self.update_uix('xborder_color',color)

    def on_xborder_width(self,inst, w):
        #update border witdth
        self.update_uix('xborder_width',w)

    def on_xborder_radius(self,inst, r):
        #update border radius
        self.update_uix('xborder_radius',r)