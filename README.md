# WinKeMMPy: Windows Keyboard Macro Maker in Python

## Description

A pythonic way to make self-contained low-dependency keyboard macro programs.

In essence, WinKeMMPy allows you to write a keyboard macro in Python and export it as a batch file that can be run on desktop Windows with (virtually) no dependencies.

Caveat: The exported bat file uses Powershell to implement the keyboard simulation. All Windows versions since Windows 7 have Powershell installed by default. So as long as Powershell is not disabled or uninstalled on the system, the bat file should run correctly.

## Usage Examples
### Basic
An example using all four basic action functions: `type`, `wait`, `hold`, and `lift`.
```python
import winkemmpy as kemm

# Create a keyboard macro object
km = kemm.KeyboardMacro()

# Give the macro some instructions
km.type("hello Alice{enter}") # The macro will type 'hello Alice' and then press the enter key
km.wait(5) # The macro will wait 5 seconds
km.hold("shift") # The macro will hold down the shift key
km.type("hi Bob") # Since the shift key is held, the macro will type 'HI BOB'
km.lift("shift") # The macro will let go of the shift key

# Export the macro as a bat file
km.export_bat("my_macro.bat")
```

### Reading instructions from strings
Instead of using the action functions, you can have the macro read a set of instructions from a string.
```python
#Let's have the macro write a sentence, highlight it, cut it, and paste it twice
instructions='''
WAIT 2
TYPE This sentence was written by a bot.{SPACE}
HOLD shift
TYPE {HOME}
LIFT shift
HOLD ctrl
TYPE xvv
LIFT ctrl
'''

km = kemm.KeyboardMacro()
km.read_string(instructions)
km.export_bat()
```


### Reading instructions from .txt files
Alternatively, you can also read instructions from a .txt file. The formatting is the same as for strings.
```text
### ./instructions.txt ###
# Comments can be added but must be written on separate lines from instruction lines
# Let's have the macro open the notepad program using the Windows start menu
TYPE {win}
WAIT 2
TYPE notepad{enter}
WAIT 3

# Now let's have the macro type a few lines of text
# And let's try to include as many unusual characters as possible
TYPE The atmosphere is 78% nitrogen{enter}
TYPE In English, we say "Good day!"{enter}
TYPE But in French, they say << Bonjour! >>{enter}
TYPE Last week, I visited a nice b&b{enter}
TYPE Pipes, carets and an underscore can make an emoji: |^_^|

# Now we'll save the file
# Note, for HOLD and LIFT, only the first letter of the key is necessary (c=CTRL,a=ALT,s=SHIFT)
HOLD c
TYPE s
LIFT c
WAIT 0.5
TYPE winkemmpy_demo.txt
WAIT 0.5
TYPE {enter}
'''
```
Generate the macro in Python from the .txt file.
```python
km = kemm.KeyboardMacro()
km.read_txt("instructions.txt")
km.export_bat("write_a_winkemmpy_demo.bat")
```

## Special Characters

| Special Character | Description |
| --- | --- |
| {ADD} | Keypad add |
| {BACKSPACE} | Backspace |
| {BKSP} | Backspace |
| {BREAK} | Break |
| {BS} | Backspace |
| {CAPSLOCK} | Caps lock |
| {DELETE} | Del or delete |
| {DEL} | Del or delete |
| {DIVIDE} | Keypad divide |
| {DOWN} | Down arrow |
| {END} | End |
| {ENTER} | Enter |
| {ESC} | Esc |
| {F10} | F10 |
| {F11} | F11 |
| {F12} | F12 |
| {F13} | F13 |
| {F14} | F14 |
| {F15} | F15 |
| {F16} | F16 |
| {F1} | F1 |
| {F2} | F2 |
| {F3} | F3 |
| {F4} | F4 |
| {F5} | F5 |
| {F6} | F6 |
| {F7} | F7 |
| {F8} | F8 |
| {F9} | F9 |
| {HELP} | Help |
| {HOME} | Home |
| {INSERT} | Ins or insert |
| {INS} | Ins or insert |
| {LEFTB} | Left bracket ( { ) |
| {LEFT} | Left arrow |
| {MULTIPLY} | Keypad multiply |
| {NUMLOCK} | Num lock |
| {PGDN} | Page down |
| {PGUP} | Page up |
| {PRTSC} | Print screen (may not work) |
| {RIGHTB} | Right bracket ( } ) |
| {RIGHT} | Right arrow |
| {SCROLLLOCK} | Scroll lock |
| {SPACE} | Spacebar |
| {SUBTRACT} | Keypad subtract |
| {TAB} | Tab |
| {UP} | Up arrow |
| {WIN} | Windows key (simulated by ctrl+esc) |
