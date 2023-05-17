#xkivy dialog
from .popup import XBoxPopup
from kivy.metrics import dp

class XDialog(XBoxPopup):
    '''XDialog ,add widgets to XDialog but consider setting widgets' size_hints to [None,None] and set the sizes manually if encounting any problems.
    Please parse in the xbg_color argument for the background_color and this will fix a little error with the canvas.'''
    xradius=[dp(90),dp(20),dp(90),dp(20)]
        

