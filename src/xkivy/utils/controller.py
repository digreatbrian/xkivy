'''Get to controll other widget's attributes from another widget/main widget in a simpler way.Type help(Controller) for more help.'''
from kivy.properties import ObjectProperty,DictProperty
__all__=["Controller"]


class Controller:
	'''For controlling the widgets from the main widget.
	
	All you need to do is to set the main attribute to the main widget will controll the widget and then set attribs attribute as dict ,key = value ,where key is the attribute of main that will be used to change attribute of the widget and value is the target attribute that will be changed when attribute *key* changes.
	Full Example ::
		
		from xkivy.uix.layouts import XBoxLayout
		from xkivy.utils.controller import Controller
		from kivy.app import App
		
		class Main(XBoxLayout):
			cont_radius=ListProperty([0]*4)
			
		class Container(Controller,XBoxLayout):
			pass
			
	class MyApp(App):
		def build(self):
			main=Main()
			cont=Container()
			main.add_widget(container)
			
			cont.main=main
			cont.attribs={'cont_radius':'xradius'}
			
			#whenever main.cont_radius changes ,the main.cont_radius value will be set to cont.xradius.
		
		MyApp().run()
	'''
	main=ObjectProperty()
	attribs=DictProperty({" ":" "}) #attribute of the main app : attribute to change to the widget.The key of the dict is the attribute within the main that we will set to the attribute of the widget which is the value .
	#eg {'bg_color'' : "md_bg_color"} the bg_color will be set to the widget md_bg_color attribute
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		
	def on_main(self,inst,main):
		if not isinstance(main,Widget):
			raise TypeError(f"Controller main attribute should be a Widget instance not {type(main)} .")
		self.on_attribs(inst,self.attribs)
		
	def on_attribs(self,inst,attribs):
		if not self.main:
			return
		main=self.main
		for x in attribs.keys():
			if not hasattr(main,f"{x}"):
				#raise ValueError(f"Controller main doesnt have attribute {x} .")
				return
			if x.strip():
				code_a="main.fbind('{}',partial(self.controller_set_attr,attribs.get('{}')))".format(x,x) 
				code_b="self.controller_set_attr(attribs.get('{}') ,inst,main.{})".format(x,x)
				exec(code_a)
				exec(code_b)
	
	def controller_set_attr(self,attr,inst,val):
		#setting attrib <attr> with value <val>
		exec("self.{}=val".format(attr))



