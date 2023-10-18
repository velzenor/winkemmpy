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
# Let's have the macro write a sentence, highlight it, cut it, and paste it twice
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
# Let's have the macro open the Notepad program using the Windows start menu
TYPE {win}
WAIT 2.0
TYPE notepad{enter}
WAIT 3.0

# Now let's have the macro type a few lines of text
# And let's try to include as many unusual characters as possible
TYPE Last week, I visited a nice b&b in France{enter}
TYPE In English, we say "Good day!"{enter}
TYPE But in French, they say << Bonjour! >>{enter}
TYPE The atmosphere is 78% nitrogen{enter}
TYPE Pipes, carets and an underscore can make an emoji: |^_^|

# Now we'll have the macro save the text it wrote
# Note, for HOLD and LIFT, only the first letter of the key is necessary (c=CTRL,a=ALT,s=SHIFT)
HOLD c
TYPE s
LIFT c
WAIT 0.5
TYPE winkemmpy_demo.txt
WAIT 0.5
TYPE {enter}
```
Generate the macro in Python from the .txt file.
```python
km = kemm.KeyboardMacro()
km.read_txt("instructions.txt")
km.export_bat("write_a_winkemmpy_demo.bat")
```

## Special Characters
Certain keyboard keys have special character codes that can be used to type them. A character code is always enveloped by a pair of braces { }. For example, `{ENTER}` corresponds to the enter key. 

Note that if you need to type a brace, you can use `{RIGHTB}` for a right brace and `{LEFTB}` for a left brace. 

A list of all accepted special characters can be found [here](SPECIALCHARS.md).

## Live Demo
Try out WinKeMMPy in a live notebook environment using Google Colab. Link [here](https://colab.research.google.com/drive/1EjgqKhPgE26ISjTpGgwZZ4rSH4lCnvjl?usp=sharing).

