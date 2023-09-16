from ..effects.clickeffect import CircularRippleEffect ,TouchEffect
from .image import XImage
from kivy.metrics import dp
from kivy.properties import StringProperty ,ListProperty

#XIMAGEICON
class XImageIcon(CircularRippleEffect ,TouchEffect ,XImage):
    icon = StringProperty('')
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = [None ,None]
        self.size = [dp(35) ,dp(35)]

    def on_icon(self, inst ,ico):
        pass

