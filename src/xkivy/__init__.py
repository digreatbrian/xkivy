

"""
A kivy and kivymd extension module for easy accessibility, creation of new widgets and also adding more functionality. 

This module containing new advanced widgets that are readily available to suit your needs.

You may use this module with kivymd module for the best experience.This module was built to incorporate new widgets to kivy and kivymd ,to provide flexibility with widgets ,to add functionality and to fix some problems with kivymd.

To use this module, you just have to do the same procedure when creating a kivy/kivymd App. 

Example ::
    from kivy.app import App
    from xkivy.uix.button import XRectangularButton as XButton

    class TestApp(App):
        def build(self):
            return XButton(text='Test Button') 

    app=TestApp() 
    app.run()

"""

import kivy
import kivymd


