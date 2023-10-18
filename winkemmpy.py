from _io import TextIOWrapper 

MOD_SHORTHANDS = ["C","A","S"]

SPECIALCHARS_DESCRIPTIONS = {'{ADD}': 'Keypad add',
 '{BACKSPACE}': 'Backspace',
 '{BKSP}': 'Backspace',
 '{BREAK}': 'Break',
 '{BS}': 'Backspace',
 '{CAPSLOCK}': 'Caps lock',
 '{DELETE}': 'Del or delete',
 '{DEL}': 'Del or delete',
 '{DIVIDE}': 'Keypad divide',
 '{DOWN}': 'Down arrow',
 '{END}': 'End',
 '{ENTER}': 'Enter',
 '{ESC}': 'Esc',
 '{F10}': 'F10',
 '{F11}': 'F11',
 '{F12}': 'F12',
 '{F13}': 'F13',
 '{F14}': 'F14',
 '{F15}': 'F15',
 '{F16}': 'F16',
 '{F1}': 'F1',
 '{F2}': 'F2',
 '{F3}': 'F3',
 '{F4}': 'F4',
 '{F5}': 'F5',
 '{F6}': 'F6',
 '{F7}': 'F7',
 '{F8}': 'F8',
 '{F9}': 'F9',
 '{HELP}': 'Help',
 '{HOME}': 'Home',
 '{INSERT}': 'Ins or insert',
 '{INS}': 'Ins or insert',
 '{LEFTB}': 'Left bracket ( { )',
 '{LEFT}': 'Left arrow',
 '{MULTIPLY}': 'Keypad multiply',
 '{NUMLOCK}': 'Num lock',
 '{PGDN}': 'Page down',
 '{PGUP}': 'Page up',
 '{PRTSC}': 'Print screen (may not work)',
 '{RIGHTB}': 'Right bracket ( } )',
 '{RIGHT}': 'Right arrow',
 '{SCROLLLOCK}': 'Scroll lock', 
 '{SPACE}': 'Spacebar',             
 '{SUBTRACT}': 'Keypad subtract',
 '{TAB}': 'Tab',
 '{UP}': 'Up arrow',
 '{WIN}': 'Windows key (simulated by ctrl+esc)'}

SPECIALCHARS = SPECIALCHARS_DESCRIPTIONS.keys()

class KeyboardMacro():
    def __init__(self):
        self.actions = []
        self.read_str = self.read_string
    
    def read_txt(self,txt_file):
        arg_type = type(txt_file)
        if arg_type not in [TextIOWrapper,str]: 
            raise TypeError(f"argument should be _io.TextIOWrapper or str, not {arg_type}")
        if arg_type == TextIOWrapper:
            lines = txt_file.readlines()
            return self.__read_inner(lines)
        else:
            with open(txt_file,"r") as file:
                lines = file.readlines()
                return self.__read_inner(lines)
        
    def read_string(self,string):
        arg_type = type(string)
        if arg_type != str: raise TypeError(f"argument should be str, not {arg_type}")
        lines = string.split("\n")
        return self.__read_inner(lines)
    
    def __read_inner(self,lines):
        valid_cmds = ["WAIT","TYPE","HOLD","LIFT"]
        for i,line in enumerate(lines):
            line = line.replace("\n","")
            if len(line)<6: continue
            cmd = line[:4].upper()
            #ignore all lines with without a valid command
            if cmd not in valid_cmds: continue 
            arg = line[5:]
            if cmd in ['HOLD','LIFT']:
                if arg[0].upper() not in MOD_SHORTHANDS:
                    raise Exception(f"Invalid mod key entry found on line {i+1} of text input")
            if cmd=="WAIT":
                try: arg = float(arg)
                except: raise Exception(f"Invalid wait entry found on line {i+1} of text input")
            self.actions.append([cmd,arg])
            
    def type(self,text):
        if type(text) != str: raise TypeError(f"argument should be str, not {type(text)}")
        self.actions.append(["TYPE",text])
        
    def wait(self,seconds):
        seconds = float(seconds)
        self.actions.append(["WAIT",seconds])
        
    def hold(self,mod):
        mod_shorthand = mod[0].upper()
        if mod_shorthand not in MOD_SHORTHANDS: raise Exception(f"argument should be 'CTRL', 'ALT', or 'SHIFT', got {mod}")
        self.actions.append(["HOLD",mod_shorthand])
        
    def lift(self,mod):
        mod_shorthand = mod[0].upper()
        if mod_shorthand not in MOD_SHORTHANDS: raise Exception(f"argument should be 'CTRL', 'ALT', or 'SHIFT', got {mod}")
        self.actions.append(["LIFT",mod_shorthand])
    
    #apply a function to all "special character codes" in text
    def __apply_to_SPECIALCHARS(self, text, func):
        #split text based on { and } delimiters
        temp=[] 
        for chunk in text.split("{"): temp.extend(chunk.split("}"))
        out = ''
        for i in range(len(temp)):
            #the odd indices of temp are the substrings of text that were enveloped by { }
            if i%2==1: out += "{" + func(temp[i]) + "}"
            else: out += temp[i]
        return out
    
    #format the argument of TYPE commands
    def __format_TYPE_arg_inner(self,text):
        #capitalize all "special character codes"
        text = self.__apply_to_SPECIALCHARS(text,lambda x: x.upper())
        #use brackets to escape special chars
        for char in ["+","%","^","~",")","("]:
            text = text.replace(char,"{"+char+"}")
        #implement some new special character codes
        text = text.replace("{WIN}","^{ESC}") #CTRL+ESC acts like the windows key
        text = text.replace("{LEFTB}","{{}") #the { char
        text = text.replace("{RIGHTB}","{}}") #the } char
        text = text.replace("{SPACE}"," ")
        #text = text.replace("{S}","\\") #an alternative for backslash
        #escape double brackets (needed for passing through batch script)
        text = text.replace('"','""')
        return text
        
    def __to_powershell_inner(self):
        output = []
        output.append("Add-Type -AssemblyName System.Windows.Forms")
        modifier_dict = {"C":"^(", "S":"+(", "A":"%("} #ctrl, shift, and alt
        active_mods=[]
        for action in self.actions:
            cmd = action[0]
            arg = action[1]
            
            if cmd=="TYPE":
                text=''
                for modifer in active_mods: text += modifer
                text += self.__format_TYPE_arg_inner(arg)
                for _ in range(len(active_mods)): text += ")"
                output.append(f'''[System.Windows.Forms.SendKeys]::SendWait("{text}")''')

            elif cmd=="WAIT":
                seconds = float(arg)
                output.append(f'''Start-Sleep -Seconds {seconds}''')

            elif cmd=="HOLD":
                modifer = arg[0].upper()
                active_mods.append(modifier_dict[modifer])

            elif cmd=="LIFT":
                modifer = arg[0].upper()
                active_mods.reverse()
                active_mods.remove(modifier_dict[modifer])
                active_mods.reverse()
        return output
    
    def to_powershell(self):
        return "\n".join(self.__to_powershell_inner())
                
    def generate_bat_launcher(self):
        ps_code = self.__to_powershell_inner()
        bat = 'set file=%0.ps1\n'
        for line in ps_code:
            line = line.replace("%","%%")
            bat += "echo "+line+" >> %file%\n"
        bat += "Powershell.exe -ExecutionPolicy Bypass -File %file%\n"
        bat += "del %file%"
        return bat
        
    def export_bat(self,filename="macro.bat"):
        bat_code = self.generate_bat_launcher()
        with open(filename,"w") as file:
            file.write(bat_code)
            
