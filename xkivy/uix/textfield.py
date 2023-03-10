from .layouts import XBoxLayout,XFloatLayout
from ..colors import default
from kivy.uix.textinput import TextInput
from kivy.metrics import dp,sp
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (ListProperty,
NumericProperty,DictProperty,
StringProperty,BooleanProperty,
ObjectProperty,OptionProperty,
ColorProperty)
from kivy.properties import VariableListProperty as VarProperty
#from kivy.core.window import Window
from kivy.clock import Clock

from .popup import XBoxPopup
from .image import XImage
from ..colors import (
default,
black,
white,
grey)

_input=TextInput()

#XICON
class XIcon(XImage):
	icon=StringProperty('')
	size_hint=[.8,.8]
	pos_hint={'center_x':.5,'center_y':.5}
	def on_icon(self,inst,ico):
		pass

#XTEXTFIELD
class XTextField(XFloatLayout):
	allow_copy = BooleanProperty(True)
	auto_indent = \
	BooleanProperty(_input.auto_indent)
	
	bold=BooleanProperty(False)
	border=ListProperty([0,0,0,0])
	
	character_error=BooleanProperty(False)
	character_mode =\
	OptionProperty('other',options=['numeric','other'])
	cursor_color = ColorProperty(white)
	cursor_height = NumericProperty(dp(3))
	cursor_width = \
	NumericProperty(_input.cursor_width)
	
	error = BooleanProperty(False)
	error_color = ColorProperty([1,0,0,.7])
	
	focus = BooleanProperty(_input.focus)
	font_context = \
	StringProperty(_input.font_context)
	font_family = \
	StringProperty(_input.font_family)
	fontname = StringProperty(None)
	font_size = NumericProperty(sp(13))
	
	hint_text = StringProperty("Text Here ")
	hint_text_color = ColorProperty(grey)
	
	input_type = \
	StringProperty(_input.input_type)
	italic = BooleanProperty(False)
	
	keyboard = \
	ObjectProperty(None,allownone=True)
	keyboard_mode = OptionProperty('auto',options=['auto','managed'])
	
	left_icons = ListProperty(None)
	line_height = \
	NumericProperty(_input.line_height)
	line_spacing = \
	NumericProperty(_input.line_spacing)
	
	multiline = BooleanProperty(False)
	
	padding = ListProperty([dp(4)]*4)
	password = BooleanProperty(False)
	password_mask = StringProperty('*')
	
	readonly = BooleanProperty(False)
	right_icons = ListProperty(None)
	
	scroll_x = \
	NumericProperty(_input.scroll_x)
	scroll_y = \
	NumericProperty(_input.scroll_y)
	selection_color = \
	ColorProperty(_input.selection_color )
	size_hint = ListProperty([1,.1])
	suggestion_text = \
	StringProperty(_input.suggestion_text )
	
	tab_width = \
	NumericProperty(_input.tab_width)
	text = StringProperty('')
	text_color = ColorProperty(black)
	text_language = \
	StringProperty(_input.text_language)
	
	use_bubble = \
	BooleanProperty(_input.use_bubble)
	use_handles = \
	BooleanProperty(_input.use_handles)
	
	xbg_color = ColorProperty(default)
	xradius = \
	VarProperty([dp(30)]*4,length=4)
	
	def __init__(self,**kwargs):
		super(XTextField,self).__init__(**kwargs) ;self.bind(parent=self.init_textfield)
		
	def copy(self):
		def g(*_):
			self.copy()
		if hasattr(self,'initialised'):
			self._textinput.copy()
		else:
			Clock.schedule_once(g)
		
	def cut(self):
		def g(*_):
			self.cut()
		if hasattr(self,'initialised'):
			self._textinput.cut()
		else:
			Clock.schedule_once(g)
		
	def paste(self,text):
		def g(*_):
			self.paste()
		if hasattr(self,'initialised'):
			self._textinput.paste(text)
		else:
			Clock.schedule_once(g)
		
	def select_all(self):
		def g(*_):
			self.select_all()
		if hasattr(self,'initialised'):
			self._textinput.select_all()
		else:
			Clock.schedule_once(g)
		
	def select_text(self ,start ,end):
		def g(*_):
			self.select_text()
		if hasattr(self,'initialised'):
			st=start
			self._textinput.select_text(st ,end)
		else:
			Clock.schedule_once(g)
		
	def insert_text(self,substring ,from_undo = False):
		def g(*_):
			self.insert_text(text)
		if hasattr(self,'initialised'):
			self._textinput.insert_text(substring ,from_undo)
		else:
			Clock.schedule_once(g)
		
	def show_keyboard(self):
		def g(*_):
			self.show_keyboard()
		if hasattr(self,'initialised'):
			self._textinput.show_keyboard()
		else:
			Clock.schedule_once(g)
			
	def on_text_color(self,inst,color):
		pass
		
	def on_character_error(self,inst,err):
		pass
		
	def on_character_mode(self,inst,md):
		'''On character_mode ,please use super().on_character_mode if you have overriden this method.'''
		self._on_character_mode(inst,md)
		
	def on_error(self,inst,err):
		'''On error ,please use super().on_error if you have overriden this method.'''
		self._on_error(inst,err)
		
	def _on_error(self,inst,error):
		#creating proper error bg color
		err_bg=list(self.error_color)
		err_bg.pop()
		err_bg.append(.4)
		#setting bg and textcolor
		if self.xbg_color!=err_bg:
			#if bg is not of error bg
			self._xbg_color=self.xbg_color
			self._text_color=self.text_color
		if error:
			self.xbg_color=err_bg
			self.text_color=self.error_color
		else:
			self.text_color=self._text_color
			self.xbg_color=self._xbg_color
		
	def _on_character_mode(self,inst,md):
		def check_chars(*_):
			text=self.text
			if md=='numeric':
				if not text.strip():self.character_error=False
				it=iter(list(text))
				ints=[0,1,2,3,4,5,6,7,8,9,0]
				for x in it:
					try:
						int(x)
					except ValueError:
						self.character_error=True
						break
					self.character_error=False
		if not hasattr(self,"check_chars"):
			Clock.schedule_interval(check_chars,.1)
		self.check_chars=check_chars
		
	def on_text_color(self,inst,color):
 		pass
 		
	def on_hint_text(self,inst,txt):
 		pass
 		
	def on_cursor_height(self,inst,h):
 		pass
		
	def on_font_size(self,inst,f):
 		pass
		
	def on_cursor_color(self,inst,cl):
 		pass
 		
	def on_hint_text_color(self,inst,color):
		pass
	
	def on_text(self,inst,txt):
		pass
			
	def on_focus(self,inst,f):
		pass
		
	def on_keyboard(self,inst,k):
		pass
		
	def on_keyboard_textfield(self, window ,k) : pass
		
	def on_keyboard_key_down(self,window, keycode, text, modifiers):
		'''Event called whenever a key is pressed on keyboard.'''
		
	def on_keyboard_key_up(self,window,keycode):
		'''Event called whenever a key is released on keyboard.'''
		
	def on_left_icons(self,inst,x):
		'''On left_icons ,please use super().on_left_icons if you have overriden this method.'''
		self._on_left_icons(inst,x)
		
	def _on_left_icons(self,inst,rd):
		if not rd:
			return
		
		if len(rd)>1:
			raise TypeError("Only 1 Icon can be added to the left of the XTextField.")
		for x in rd:
			if not isinstance(x,XIcon):
				raise TypeError('Icon of left_icons should be of instance/type <XIcon>')
		def init_and_add(*_):
			self.init_textfield()
			self._left_box.clear_widgets()
			self._left_box.add_widget(rd[0])
			
		if not hasattr(self,'initialised'):
			Clock.schedule_once(init_and_add)
		else:
			self._left_box.clear_widgets()
			self._left_box.add_widget(rd[0])
			
	def on_right_icons(self,inst,r):
		'''On right_icons ,please use super().on_right_icons if you have overriden this method.'''
		self._on_right_icons(inst,r)
			
	def _on_right_icons(self,inst,rd):
		if not rd:
			return
		if len(rd)>2:
			raise TypeError("Only 2 Icons can be added to the right of the XTextField.")
		for x in rd:
			if not isinstance(x,XIcon):
				raise TypeError('Icon(s) of left_icons should be of instance/type <XIcon>')
		
		def init_and_add(*_):
			self.init_textfield()
			self._mid_right_box.clear_widgets()
			self._right_box.clear_widgets()
			if len(rd)==2:
				self._mid_right_box.add_widget(rd[0])
			self._right_box.add_widget(rd[-1])
			
		if not hasattr(self,'initialised'):
			Clock.schedule_once(init_and_add)
		else:
			self._mid_right_box.clear_widgets()
			self._right_box.clear_widgets()
			if len(rd)==2:
				self._mid_right_box.add_widget(rd[0])
			self._right_box.add_widget(rd[-1])
	
	def textfield_update(self,*_):
		'''Update the textfield'''
		#allocating space/size used by the mid right box/mid right container depending on the children of the widget
		self.keyboard = \
		self._textinput.keyboard 
		self.text=self._textinput.text
		self.focus=self._textinput.focus
		if hasattr(self,"_mid_right_box"):
			if not self._mid_right_box.children:
				self._mid_right_box.size_hint = \
				[.01,.8]
			else:
				self._mid_right_box.size_hint = \
				[.1,.8]
	
	def init_textfield(self,*a):
		'''Initialise the textfield ,the most important first step.'''
		#first step ,initialising the textfield,packing all the widgets
		if hasattr(self,'initialised'):
			#already initialised
			if self.initialised:return
		self._container=BoxLayout(size_hint=[.9,.9],pos_hint={"center_x":.5,'center_y':.5},spacing=dp(5))
		
		textfield=TextInput(size_hint=[.5,.8])
		self._textinput=textfield
		
		#creating event_handler for handling events when an attrib has changed/creating "on_" events eg on_text
		ev=["cursor_height",'padding','font_family','text_color',"font_size",'cursor_color','hint_text','hint_text_color','bold','italic','focus','multiline','password','password_mask','allow_copy','border','cursor_width','cursor_height','font_context','input_type','font_family','line_height','line_spacing','password','password_mask','readonly','scroll_x','scroll_y','selection_color','suggestion_text','tab_width','text','text_language','use_bubble','use_handles','auto_indent','fontname','keyboard_mode']
		def create_ev(self,s):
			exec('''def on_{s}(inst,a):
				def g(*_):
					on_{s}(inst,a)
				if hasattr(inst,'initialised'):
					inst._textinput.{s}=a
					if "{s}"=="text_color":
						inst._textinput.foreground_color=a
				else:
					Clock.schedule_once(g)
					
			'''.format(s=s))
			exec('self.bind({s}=on_{s})'.format(s=s))
			
		for x in ev:
			create_ev(self,x)
		
		#setting useful attribs to _textinput from textfield/self 
		textfield.font_size=self.font_size
		textfield.cursor_color = \
		self.cursor_color
		textfield.hint_text=self.hint_text
		textfield.hint_text_color = \
		self.hint_text_color
		textfield.foreground_color = \
		self.text_color
		textfield.bold=self.bold
		textfield.italic=self.italic
		textfield.multiline=self.multiline
		textfield.password=self.password
		textfield.allow_copy=self.allow_copy
		textfield.auto_indent=self.auto_indent
		textfield.background_color=[0,0,0,0]
		textfield.cursor_height = \
		self.cursor_height
		textfield.password_mask = \
		self.password_mask
		textfield.border=self.border
		textfield.cursor_width = \
		self.cursor_width
		textfield.focus=self.focus
		textfield.font_context = \
		self.font_context
		textfield.input_type=self.input_type
		textfield.font_family=self.font_family
		textfield.line_height=self.line_height
		textfield.line_spacing = \
		self.line_spacing
		textfield.scroll_x=self.scroll_x
		textfield.scroll_y=self.scroll_y
		textfield.selection_color = \
		self.selection_color
		textfield.suggestion_text = \
		self.suggestion_text
		textfield.readonly = self.readonly
		textfield.tab_width=self.tab_width
		textfield.text=self.text
		textfield.text_language = \
		self.text_language
		textfield.use_bubble=self.use_bubble
		textfield.use_handles = \
		self.use_handles
		textfield.auto_indent=self.auto_indent
		textfield.fontname=self.fontname
		textfield.padding=self.padding
		textfield.keyboard_mode = \
		self.keyboard_mode
		textfield.pos_hint = \
		{'center_x':.5,'center_y':.5}
		
		
		#attribs that need to be updated every milisecond
		self.keyboard= textfield.keyboard
		
		#recording important attribs from _textinput and setting important attribs
		self._keyboard_on_textfield = \
		textfield.keyboard_on_textinput
		self._keyboard_on_key_down = \
		textfield.keyboard_on_key_down
		self._keyboard_on_key_up = \
		textfield.keyboard_on_key_up
		
		self.register_event_type(
		"on_keyboard_textfield")
		self.register_event_type(
		"on_keyboard_key_down")
		self.register_event_type(
		"on_keyboard_key_up")
		
		def keyboard_on_textfield(*args):
			self._keyboard_on_textfield(*args)
			self.dispatch(
			'on_keyboard_textfield',*args)
		
		def keyboard_on_key_down(*args):
			self._keyboard_on_key_down(
			*args)
			self.dispatch(
			'on_keyboard_key_down',*args)
		
		def keyboard_on_key_up(*args):
			self._keyboard_on_key_up(*args)
			self.dispatch(
			'on_keyboard_key_up',*args)
			
		########################
		textfield.keyboard_on_textinput = \
		keyboard_on_textfield
		textfield.keyboard_on_key_down=\
		keyboard_on_key_down
		textfield.keyboard_on_key_up = \
		keyboard_on_key_up
		#########################
		
		#########################
		
		rd=self.xradius[0]
		left_box=XBoxLayout()
		mid_right_box=XBoxLayout()
		right_box=XBoxLayout()
		
		left_box.pos_hint={'center_y':.5}
		mid_right_box.pos_hint={'center_y':.5}
		right_box.pos_hint={'center_y':.5}
		
		left_box.size_hint=[.1,.8]
		mid_right_box.size_hint=[.1,.8]
		right_box.size_hint=[.1,.8]
		
		#packing/adding widgets
		self._container.add_widget(left_box)
		self._container.add_widget(textfield)
		self._container.add_widget(
		mid_right_box)
		self._container.add_widget(right_box)
		self.add_widget(self._container)
		
		self._left_box=left_box
		self._mid_right_box=mid_right_box
		self._right_box=right_box
		
		Clock.schedule_interval(self.textfield_update,.1)
		
		self.initialised=True
		
#XWINDOWTEXTFIELD			
class XWindowTextField(XTextField):
	next_xbg_color=ListProperty(black)
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		self.init_wintextfield()
		
	def init_wintextfield(self):
		if not hasattr(self,'initialised_wintextfield') and not self.parent:
			self.initialised_wintextfield=True
			self._popup=XBoxPopup()
			self._popup.size_hint=self.size_hint
			self._popup.size=self.size
			self._popup.pos_hint={'center_x':.5,'center_y':.9}
			self._popup.overlay_color=self.next_xbg_color
			self._popup.opacity=2
			
			########################
			def on_pre_open():
				if not hasattr(self,'_parent'):
					self._parent=self.parent
				par=self._parent
				if self in par.children:
					self.textfield_index=par.children.index(self)
					par.remove_widget(self)
				self._phint=self.pos_hint 
				self.pos_hint={'center_y':.9}
				self._popup.add_widget(self)
			
			#########################
				
			def on_pre_dismiss():
				par=self._parent
				index=self.textfield_index
				self.pos_hint=self._phint
				if self not in par.children:
					try:par.add_widget(self) 
					except:
						self._popup.remove_widget(self)
						par.add_widget(self) 
					par.children.remove(self)
					par.children.insert(self.textfield_index,self)
					
			#########################
			
			self._popup.on_pre_open=on_pre_open
			self._popup.on_pre_dismiss=on_pre_dismiss
			
			#########################
			
	def on_next_xbg_color(self,inst,color):
		if not hasattr(self,'initialised_wintextfield'):
			def x(*_):
				self.on_next_xbg_color(inst,color)
			Clock.schedule_once(x)
			return
		#already initialised
		self._popup.overlay_color=color
		self._popup.opacity=2
			
	def on_focus(self,inst,f):
		super().on_focus(inst,f)
		if not hasattr(self,'initialised_wintextfield'):
			def on_focus_and_init(*_):
				self.init_wintextfield()
				self.on_focus(inst,f)
			Clock.schedule_once(on_focus_and_init)
		if f : #is focused
			#textfield is initialised
			if not self._popup.is_open:
				self._popup.open()
		