from ..effects.clickeffect import CircularRippleEffect
from .image import XImage
from kivy.properties import StringProperty ,ListProperty

#XIMAGEICON
class XImageIcon(CircularRippleEffect ,XImage):
    icon=StringProperty('')
    size_hint=ListProperty([.5,.5])
    pos_hint={'center_x':.5,'center_y':.5}
    def on_icon(self,inst,ico):
        pass

