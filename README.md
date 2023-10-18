# WinKeMMPy: Windows Keyboard Macro Maker in Python

## Description

A pythonic way to make self-contained no-dependency keyboard macro programs.

In essence, WinKeMMPy allows you to write a keyboard macro in Python and export it as a batch file that can be run on desktop Windows with (essentially) no dependencies.

Caveat: The exported bat file uses Powershell to implement the keyboard simulation. All Windows versions since Windows 7 have Powershell installed by default. So as long as Powershell is not be disabled or uninstalled on the system, the macro should work.

## Usage Examples
### Basic
```python

```

### Reading instructions from strings

### Reading instructions from .txt files

```text
```
Generated the macro in python from the .txt file.
```python

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
