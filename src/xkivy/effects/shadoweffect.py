from kivymd.uix.behaviors.elevation import CommonElevationBehavior as CommonElevation
from kivy.clock import Clock
from kivy.properties import (ListProperty,NumericProperty,BooleanProperty)

class ShadowEffect(CommonElevation):
    shadow_size=NumericProperty(3)
    auto_shadow_radius = BooleanProperty(True)
    def __init__(self,shadow_size=None,**kwargs):
        super().__init__(**kwargs)
        if shadow_size!=None:
            self.on_shadow_size(self,shadow_size)
        else:
            self.on_shadow_size(self,self.shadow_size)
        self.manage_radius()
    
    def manage_radius(self,*_):
        def manage(*a):
            if not self.auto_shadow_radius:
                return
            if hasattr(self,'xradius'):
                radii=self.xradius
                bottom_right,top_left,top_right,bottom_left=radii
                new_radius=[top_left,top_right,bottom_right,bottom_left]
                #xradius and shadow_radius are a bit different ,the order to set the corners are different
                self.shadow_radius=new_radius
        Clock.schedule_interval(manage,.1)
        
    def on_shadow_size(self,inst,size):
        self.elevation=size
    
    def on_shadow_radius(self,inst,radii):
        self._shadow_radius=radii
        super().on_shadow_radius(inst,radii)
    
    def on_shadow_color(self,inst,color):
        self._shadow_color=color
        super().on_shadow_color(inst,color)
