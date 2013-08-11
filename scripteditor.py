import wx

from wx.stc import *

def GetText():
	global script_ctrl
	return script_ctrl.GetText()

def SetText(text):
	global script_ctrl
	
	text = text.replace("\n\n", "\n")
	
	script_ctrl.SetText(text)
	
def initialize():
	global script_ctrl
	
	luakeywords = "and break do else elseif end for function if local nil not or repeat return then until while"

	#Create script editor
	scriptedit = wx.Frame(None, wx.ID_ANY, "Script Editor", (10,10), (500,550))

	script_ctrl = StyledTextCtrl(scriptedit,  -1)

	script_ctrl.SetLexer(STC_LEX_LUA)

	script_ctrl.SetKeyWords(0, luakeywords)

	scriptedit.Show(True)
	
	#Load script template
	SetText( open("template.lua").read() )

	#From Yellow Brain Styling Example
	#http://www.yellowbrain.com/stc/styling.html#example

	faces = { 'times': 'Courier New',
			  'mono' : 'Courier New',
			  'helv' : 'Courier New',
			  'other': 'Courier New',
			  'size' : 12,
			  'size2': 10,
			 }
				 
	# Global default styles for all languages
	script_ctrl.StyleSetSpec(STC_STYLE_DEFAULT,     "face:%(helv)s,size:%(size)d" % faces)
	script_ctrl.StyleSetSpec(STC_STYLE_LINENUMBER,  "back:#C0C0C0,face:%(helv)s,size:%(size2)d" % faces)
	script_ctrl.StyleSetSpec(STC_STYLE_CONTROLCHAR, "face:%(other)s" % faces)
	script_ctrl.StyleSetSpec(STC_STYLE_BRACELIGHT,  "fore:#FFFFFF,back:#0000FF,bold")
	script_ctrl.StyleSetSpec(STC_STYLE_BRACEBAD,    "fore:#000000,back:#FF0000,bold")
	
	# Python styles
	# White space
	script_ctrl.StyleSetSpec(STC_LUA_DEFAULT, "fore:#808080,face:%(helv)s,size:%(size)d" % faces)
	
	# Comment
	script_ctrl.StyleSetSpec(STC_LUA_COMMENTLINE, "fore:#007F00,face:%(other)s,size:%(size)d" % faces)
	
	# Number
	script_ctrl.StyleSetSpec(STC_LUA_NUMBER, "fore:#007F7F,size:%(size)d" % faces)
	
	# String
	script_ctrl.StyleSetSpec(STC_LUA_STRING, "fore:#7F007F,italic,face:%(times)s,size:%(size)d" % faces)
	
	# Single quoted string
	script_ctrl.StyleSetSpec(STC_LUA_CHARACTER, "fore:#7F007F,italic,face:%(times)s,size:%(size)d" % faces)
	
	# Keyword
	script_ctrl.StyleSetSpec(STC_LUA_WORD, "fore:#00007F,bold,size:%(size)d" % faces)
	
	# Triple quotes
	script_ctrl.StyleSetSpec(STC_LUA_LITERALSTRING, "fore:#7F0000,size:%(size)d" % faces)
	
	# Operators
	script_ctrl.StyleSetSpec(STC_LUA_OPERATOR, "bold,size:%(size)d" % faces)
	
	# Identifiers
	script_ctrl.StyleSetSpec(STC_LUA_IDENTIFIER, "fore:#808080,face:%(helv)s,size:%(size)d" % faces)
	
	# Comment-blocks
	script_ctrl.StyleSetSpec(STC_LUA_COMMENTDOC, "fore:#7F7F7F,size:%(size)d" % faces)
	
	# Comment-blocks
	script_ctrl.StyleSetSpec(STC_LUA_COMMENT, "fore:#7F7F7F,size:%(size)d" % faces)
	
	# End of line where string is not closed
	script_ctrl.StyleSetSpec(STC_LUA_STRINGEOL, "fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % faces)