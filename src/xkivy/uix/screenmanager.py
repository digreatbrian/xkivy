#flexible screenmanager
'''This is a very flexible Screen Manager that auto manages switches to the new screens.
Whatever screen you visit its recorded and ,when the back or esc has been pressed the Screen Manager will switch to the previous screen automatically untill it reaches the last screen then it can now close the window when esc/back has been called.'''
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.properties import ListProperty ,NumericProperty ,OptionProperty
from kivy.core.window import Window
from .layouts import LayoutUIXEffect

class XScreen(LayoutUIXEffect ,Screen):
    pass

class XScreenManager(LayoutUIXEffect,ScreenManager):
    '''Just switch to any screen without worry,there is auto management of screen switches.This class is different from Ordinary Screen Manager because it has a flexibility of auto screen switch management.'''

    _ordered_screens=ListProperty([]) #the order of screens ,from the previous screens to the current screen
    duration = NumericProperty(1)
    direction =OptionProperty('left',options=['left','right'])
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.init_sm()
        
    def on_current_screen(self,*r):
        #this method manages the screen switches
        current_screen = self.current_screen
        if self._ordered_screens!=[]:
            if current_screen.name == self._ordered_screens[0].name:
                self._ordered_screens = [current_screen]
            else:self._ordered_screens.append(current_screen)
        else:
            self._ordered_screens.append(current_screen)
        
    def init_sm(self,*i):
        self._win = Window
        self._win.on_key_down=self.on_key_down_ev
        
    def on_key_down_ev(self,key,*args):
        if len(self._ordered_screens)>1:
            #there are other screens to switch to
            if key ==27:
                #ESC pressed
                #checking if any popup on the screen
                #respect the closing of popups on the screen rather than closing the current screen
                try:
                    for widget in self._win.children:
                        if hasattr(widget ,'_is_open'):\
                           #this is totally a popup
                           if widget._is_open:
                               widget.dismiss()
                               return True
                except AttributeError:
                    pass
                except TypeError:
                    pass
                previous_screen=self._ordered_screens.pop()
                screen=self._ordered_screens.pop() #target screen
                self.switch_to(screen,
                               transition=self.transition,
                               direction = self.direction,
                               duration = self.duration)
                Window.mainloop()
                return True
            
    def add_widget(self ,widget):
        super().add_widget(widget)
            
            
