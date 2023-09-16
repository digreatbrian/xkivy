
from .layouts import XBoxLayout,XFloatLayout
from ..colors import default
from kivy.uix.textinput import TextInput
from kivy.metrics import dp,sp
from kivy.properties import (
	ListProperty,
	NumericProperty,
	StringProperty,
	BooleanProperty,
	ObjectProperty,
	OptionProperty,
	ColorProperty
	)
from kivy.properties import VariableListProperty as VarProperty
from kivy.clock import Clock
from kivymd.uix.button import MDIconButton

from .popup import XPopup
from .icon import XImageIcon
from ..colors import (
	default,
	black,
	white,
	grey
)

#used to get default values to attach to our xtextfield
_input = TextInput()

#XTEXTFIELD
class XTextField(XFloatLayout):
	allow_copy = BooleanProperty(True)
	auto_indent = BooleanProperty(_input.auto_indent)
	
	bold = BooleanProperty(False)
	border = ListProperty([0,0,0,0])
	
	character_error=BooleanProperty(False)
	character_mode = OptionProperty('other',options=['numeric','other'])
	cursor_color = ColorProperty(white)
	cursor_height = NumericProperty(dp(3))
	cursor_width = NumericProperty(_input.cursor_width)
	
	error = BooleanProperty(False)
	error_outlined = BooleanProperty(False)
	error_color = ColorProperty([1,0,.1,.7])
	
	focus = BooleanProperty(_input.focus)
	font_context = StringProperty(_input.font_context)
	font_family = StringProperty(_input.font_family)
	fontname = StringProperty(None)
	font_size = NumericProperty(sp(13))
	
	hint_text = StringProperty("Text Here ")
	hint_text_color = ColorProperty(grey)
	
	input_type = StringProperty(_input.input_type)
	italic = BooleanProperty(False)
	
	keyboard = ObjectProperty(None,allownone=True)
	keyboard_mode = OptionProperty('auto',options=['auto','managed'])
	
	left_icons = ListProperty(None)
	line_height = NumericProperty(_input.line_height)
	line_spacing = NumericProperty(_input.line_spacing)
	
	multiline = BooleanProperty(False)
	
	padding = ListProperty([dp(4)]*4)
	password = BooleanProperty(False)
	password_mask = StringProperty('*')
	
	readonly = BooleanProperty(False)
	required = BooleanProperty(False)
	required_error = BooleanProperty(False)
	right_icons = ListProperty(None)
	
	scroll_x = NumericProperty(_input.scroll_x)
	scroll_y = NumericProperty(_input.scroll_y)
	selection_color = ColorProperty(_input.selection_color )
	size_hint = ListProperty([1, None])
	height = NumericProperty(dp(48))
	suggestion_text = StringProperty('')
	
	tab_width = NumericProperty(_input.tab_width)
	text = StringProperty('')
	text_color = ColorProperty(black)
	text_language = StringProperty(_input.text_language)
	
	use_bubble = BooleanProperty(_input.use_bubble)
	use_handles = BooleanProperty(_input.use_handles)
	
	xbg_color = ColorProperty(default)
	xradius = VarProperty([dp(30)]*4,length=4)

	xborder_radius = None
	
	def __init__(self,**kwargs):
		super(XTextField,self).__init__(**kwargs)
		self.bind(parent = self.init_textfield)
		self.fbind('on_touch_down',self.manage_touch_down)
		Clock.schedule_interval(self.manage_required, .1)
		
	def init_textfield(self,*a):
		'''Initialise the textfield ,the most important first step.'''
		#first step ,initialising the textfield, packing all the widgets
		if hasattr(self,'initialised'):
			#already initialised
			if self.initialised:
				return
		self._container = XBoxLayout(
			size_hint=[.96, 1],
			pos_hint = {"center_x":.5, 'center_y':.5},
			spacing = dp(2),
		)
		textfield = TextInput(size_hint = [1,1])
		textfield.background_color = [1, 1, 1, 1]
		self._textinput = textfield
		
		#creating event_handler for handling events when an attrib has changed/creating "on_" events eg on_text
		ev = [
			"cursor_height",
			'padding',
			'font_family',
			'text_color',
			"font_size",
			'cursor_color',
			'hint_text',
			'hint_text_color',
			'bold',
			'italic',
			'focus',
			'multiline',
			'password',
			'password_mask',
			'allow_copy',
			'border',
			'cursor_width',
			'cursor_height',
			'font_context',
			'input_type',
			'font_family',
			'line_height',
			'line_spacing',
			'readonly',
			'scroll_x',
			'scroll_y',
			'selection_color',
			'suggestion_text',
			'tab_width',
			'text',
			'text_language',
			'use_bubble',
			'use_handles',
			'auto_indent',
			'fontname',
			'keyboard_mode'
			]
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
		textfield.font_size = self.font_size
		textfield.cursor_color = self.cursor_color
		textfield.hint_text=self.hint_text
		textfield.hint_text_color = self.hint_text_color
		textfield.foreground_color = self.text_color
		textfield.bold = self.bold
		textfield.italic = self.italic
		textfield.multiline=self.multiline
		textfield.password = self.password
		textfield.allow_copy = self.allow_copy
		textfield.auto_indent = self.auto_indent
		textfield.background_color = [0,0,0,0]
		textfield.cursor_height = self.cursor_height
		textfield.password_mask = self.password_mask
		textfield.border = self.border
		textfield.cursor_width = self.cursor_width
		textfield.focus = self.focus
		textfield.font_context = self.font_context
		textfield.input_type = self.input_type
		textfield.font_family = self.font_family
		textfield.line_height = self.line_height
		textfield.line_spacing = self.line_spacing
		textfield.scroll_x = self.scroll_x
		textfield.scroll_y = self.scroll_y
		textfield.selection_color = self.selection_color
		textfield.suggestion_text = self.suggestion_text
		textfield.readonly = self.readonly
		textfield.tab_width = self.tab_width
		textfield.text = self.text
		textfield.text_language = self.text_language
		textfield.use_bubble = self.use_bubble
		textfield.use_handles = self.use_handles
		textfield.auto_indent = self.auto_indent
		textfield.fontname = self.fontname
		textfield.padding = self.padding
		textfield.keyboard_mode = self.keyboard_mode
		textfield.pos_hint = {'center_x':.5,'center_y':.5}
		
		#attribs that need to be updated every milisecond
		self.keyboard= textfield.keyboard
		
		#recording important attribs from _textinput and setting important attribs
		self._keyboard_on_textfield = textfield.keyboard_on_textinput
		self._keyboard_on_key_down = textfield.keyboard_on_key_down
		self._keyboard_on_key_up = textfield.keyboard_on_key_up
		
		self.register_event_type("on_keyboard_textfield")
		self.register_event_type("on_keyboard_key_down")
		self.register_event_type("on_keyboard_key_up")
		
		def keyboard_on_textfield(*args):
			self._keyboard_on_textfield(*args)
			self.dispatch('on_keyboard_textfield',*args)
		
		def keyboard_on_key_down(*args):
			self._keyboard_on_key_down(*args)
			self.dispatch('on_keyboard_key_down',*args)
		
		def keyboard_on_key_up(*args):
			self._keyboard_on_key_up(*args)
			self.dispatch('on_keyboard_key_up',*args)
			
		########################
		textfield.keyboard_on_textinput = keyboard_on_textfield
		textfield.keyboard_on_key_down = keyboard_on_key_down
		textfield.keyboard_on_key_up = keyboard_on_key_up
		#########################
		
		#########################
		rd = self.xradius[0]
		left_box = XBoxLayout()
		mid_right_box = XBoxLayout()
		right_box = XBoxLayout()
		
		left_box.size_hint = [None, 1]
		mid_right_box.size_hint = [None, 1]
		right_box.size_hint = [None, 1]

		left_box.width = 0
		mid_right_box.width = 0
		right_box.width = 0
		
		#packing/adding widgets
		self._container.add_widget(left_box)
		self._container.add_widget(textfield)
		self._container.add_widget(mid_right_box)
		self._container.add_widget(right_box)
		
		self._left_box = left_box
		self._mid_right_box = mid_right_box
		self._right_box = right_box
		
		self.initialised = True
		self.add_widget(self._container)
		Clock.schedule_interval(self.textfield_update, .1)
		
	def manage_touch_down(self ,inst ,touch):
		try:
			if self.collide_point(*touch.pos):
				#textfield is pressed ,user trying to input something
				if not self.focus:
					#faking position of touch ,pretending if we pressed textinput
					touch.pos = self._textinput.pos
					self._textinput.on_touch_down(touch)
		except:
			pass

	@property
	def real_textfield(self):
		'''Get the real textfield'''
		if not hasattr(self,'initialised'):
			def init():
				self.init_textfield()
				self.real_textfield
			Clock.schedule_once(lambda x : init())
			return
		return self._textinput
	
	def __getattribute__(self ,attr):
		try:
			return super(XTextField ,self).__getattribute__(attr)
		except Exception as e:
			raise AttributeError(str(e).capitalize() + ' ,maybe the attribute you are trying to get is on the real_textfield ,try using "self.real_textfield" ')
		           
	def manage_required(self ,*a):
		if self.required:
			#if an input is required
			if not self.text:self.required_error = True
			else:self.required_error=False
		else:self.required_error=False
		
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
		
	def on_character_error(self, inst, err):
		if err:
			self.error =  True
		else:
			self.error = False
		
	def on_character_mode(self,inst,md):
		'''On character_mode ,please use super().on_character_mode if you have overriden this method.'''
		self._on_character_mode(inst,md)
		
	def on_error(self,inst,err):
		'''On error ,please use super().on_error if you have overriden this method.'''
		self._on_error(inst,err)
		
	def _on_error(self,inst,error):
		#creating proper error bg color
		err_bg = list(self.error_color)
		err_bg.pop()
		err_bg.append(.4)
		#setting bg and textcolor

		if not self.error_outlined:
			#user does want the whole background color to change on error
			if self.xbg_color != err_bg:
				#if bg is not of error bg
				self._xbg_color=self.xbg_color
				self._text_color=self.text_color
			if error:
				self.xbg_color=err_bg
				self.text_color=self.error_color
			else:
				self.text_color=self._text_color
				self.xbg_color=self._xbg_color

		else:
			err_bg.pop()
			err_bg.append(1)
			if self.xborder_color != err_bg:
				#if xborder color is not of error color
				self._xborder_color = self.xborder_color
				self._text_color = self.text_color
			if error:
				self.xborder_color = err_bg
				self.text_color = self.error_color
			else:
				self.text_color = self._text_color
				self.xborder_color = self._xborder_color
		
	def check_chars(self,*_):
		text = self.text
		md = self.character_mode

		if md == 'numeric':
			
			if text.isdigit() or not text:
				self.character_error = False
			else:
				self.character_error = True
		else:
			self.character_error = False
		
	def _on_character_mode(self,inst,md):
		if not hasattr(self,"_chars_check"):
			self.fbind('text', self.check_chars)
		self._chars_check = self.check_chars
		
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
		
	def on_left_icons(self, inst, r):
		'''On left_icons ,please use super().on_left_icons if you have overriden this method.'''
		self._on_left_icons(inst,r)
		
	def _on_left_icons(self, inst, rd):
		if not hasattr(self,'initialised'):
			def redo():
				self.init_textfield()
				self._on_left_icons(inst ,rd)
			Clock.schedule_once(lambda x : redo())
			return

		if not rd:
			#empty list
			self._left_box.size_hint = [None ,1]
			self._left_box.width = 0
			return
		
		if len(rd) > 1:
			raise TypeError("Only 1 Icon can be added to the left of the XTextField.")
		
		# len(rd) = 1	
		icon = rd[-1]

		if not isinstance(icon, XImageIcon) and not isinstance(icon, MDIconButton):
			raise TypeError('Icon of left_icons should be of instance/type <XImageIcon> or <MDIconButton>')
		
		self._left_box.size_hint = [None ,1]
		self._left_box.width = icon.width
		self._left_box.clear_widgets()
		self._left_box.add_widget(icon)

		#setting some attributes for the icon
		icon.pos_hint = {"center_x":.5 ,"center_y":.5}
			
	def on_right_icons(self, inst, r):
		'''On right_icons ,please use super().on_right_icons if you have overriden this method.'''
		self._on_right_icons(inst,r)
			
	def _on_right_icons(self,inst,rd):
		if not hasattr(self,'initialised'):
			def redo():
				self.init_textfield()
				self._on_right_icons(inst ,rd)
			Clock.schedule_once(lambda x : redo())
			return
		
		if not rd:
			self._right_box.size_hint = [None ,1]
			self._mid_right_box.size_hint = [None ,1]
			self._right_box.width = 0
			self._mid_right_box.width = 0
			return
		
		if len(rd) > 2:
			raise TypeError("Only 2 Icons can be added to the right of the XTextField.")
		
		counter = 0
		for x in rd:
			if not isinstance(x, XImageIcon) and not isinstance(x ,MDIconButton):
				raise TypeError('Icon(s) of left_icons should be of instance/type <XImageIcon> or MDIconButton')
			counter += 1

		if counter == 1:
			icon = rd[0]
			icon.pos_hint = {'center_x': .5,'center_y': .5}
			self._right_box.size_hint = [None ,1]
			self._mid_right_box.size_hint = [None ,1]
			self._mid_right_box.width = 0
			self._right_box.width = icon.width
			self._right_box.clear_widgets()
			self._right_box.add_widget(icon)

		else:
			#counter = 2
			icon1 = rd[-1]
			icon2 = rd[0]

			icon1.pos_hint = {'center_x': .5,'center_y': .5}
			icon2.pos_hint = {'center_x': .5,'center_y': .5}

			self._right_box.size_hint = [None ,1]
			self._mid_right_box.size_hint = [None ,1]
			self._right_box.width = icon1.width
			self._mid_right_box.width = icon2.width
			
			self._right_box.clear_widgets()
			self._mid_right_box.clear_widgets()
			self._right_box.add_widget(icon1)
			self._mid_right_box.add_widget(icon2)
		
	
	def textfield_update(self,*_):
		'''Update the textfield'''
		#allocating space/size used by the mid right box/mid right container depending on the children of the widget
		self.keyboard = self._textinput.keyboard 
		self.text = self._textinput.text
		self.focus = self._textinput.focus
		