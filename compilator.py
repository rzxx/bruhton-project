filename = "1.bhtn"

import subprocess
with open(filename) as F:
    file = F.read()
    file = file.replace("\n", " ")

def writeRustCode(source):
    with open("src/main.rs","w") as F:
        F.write(source)
        F.close()

import modules as bruhtonModules
import tags as bruhtonTags
languageWords = [
    "Computer",
    "work",
    "born",
    "do",
    "chill",
    "intBruh-16",
    "intBruh-32",
    "intBruh-64",
    "floBruh-32",
    "floBruh-64",
    "Bruhing",
    "named",
    "think",
    "sorry",
    "and",
    "or",
    "prinput",
    "->",
    "<-",
    "=>",
    "&",
    "bigboy",
    "smallboy",
    "sameboy",
    "notsameboy",
]
varTypes = [
    "intBruh-16",
    "intBruh-32",
    "intBruh-64",
    "floBruh-32",
    "floBruh-64",
    "Bruhing",
]
modules = [
    "Computer",
]


#used in compilation variables:
variables = {}
output = ""
state = 0
words = []
x = ""

def createVariable(type, name):
    if type == "intBruh-16":
        variables[name] = type
        return f"let mut {name}: i16 = 0; "
    elif type == "intBruh-32":
        variables[name] = type
        return f"let mut {name}: i32 = 0; "
    elif type == "intBruh-64":
        variables[name] = type
        return f"let mut {name}: i64 = 0; "
    elif type == "floBruh-32":
        variables[name] = type
        return f"let mut {name}: f32 = 0.0; "
    elif type == "floBruh-64":
        variables[name] = type
        return f"let mut {name}: f64 = 0.0; "
    elif type == "Bruhing":
        variables[name] = type
        return f'let mut {name}: String = "".to_string(); '
    else:
        printCompilationError(f"wrong variable type on createVariable step, used: {name} -> {type}")
        return ""

def createVariableWithValue(type, name, value):
    if type == "intBruh-16":
        variables[name] = type
        return f"let mut {name}: i16 = {value}; "
    elif type == "intBruh-32":
        variables[name] = type
        return f"let mut {name}: i32 = {value}; "
    elif type == "intBruh-64":
        variables[name] = type
        return f"let mut {name}: i64 = {value}; "
    elif type == "floBruh-32":
        variables[name] = type
        return f"let mut {name}: f32 = {value}; "
    elif type == "floBruh-64":
        variables[name] = type
        return f"let mut {name}: f64 = {value}; "
    elif type == "Bruhing":
        variables[name] = type
        return f'let mut {name}: String = "{value}".to_string(); '
    else:
        printCompilationError(f"wrong variable type on createVariableWithValue step, used: {name} -> {type}")
        return ""

def printCompilationError(text):
    print(f"// Compilation Error: {text}")

for i in file:
    if state == 0:
        if x == "" and i == " ":
            continue
        elif i == '"':
            state = 2
            x += i
        else:
            state = 1
            x += i
 
    elif state == 1:
        if i == " " or i == ";":
            state = 0
            words.append(x)
            x = ""
        else:
            x += i
    elif state == 2:
        if i == '"':
            x += i
            state = 0
            words.append(bruhtonTags.checkForTags(x))
            x = ""
        else:            
            x += i
if x != "":
    words.append(x)
 
 
#print(words)
context = []
for i in words:
    #print(i, context)
    if "Computer" in context:
        if i == "work":
            output += "fn main() { "
            context = []
        elif i == "chill":
            output += "}"
            context = []
            state = 99
        elif i == "born":
            context = ["born"]
        elif i == "do":
            context = ["do"]
        else:
            printCompilationError(f"waited for function, got: {i}")
            break
 
    elif "born" in context:
        if len(context) == 1:
            if i in varTypes:
                context.append(i)
            elif i in modules:
                context = [i]
            else:
                printCompilationError(f"waited for variable type, got: {i}")
                break
        elif len(context) == 2:
            if i == "named":
                context.append("named")
            else:
                printCompilationError(f'waited for keyword "named", got: {i}')
                break
        elif len(context) == 3:
            if i in languageWords:
                printCompilationError(
                    f"use of restricted variable name, please change: {i}"
                )
                break
            else:
                context.append(i)
        elif len(context) == 4:
            if i == "=>":
                context.append(i)
            else:
                output += createVariable(context[1], context[3])
                if i in varTypes:
                    context = ["born", i]
                else:
                    if i in modules:
                        context = [i]
                    else:
                        printCompilationError(f'Waited for variable or module, check for typos or "Computer" keyword, context: {context}, got: {i}')
                        break
        elif len(context) == 5:
            context.append(i)
            output += createVariableWithValue(context[1], context[3], context[5])
            context = ["born"]
        else:
            if i in modules:
                context = [i]
            else:
                printCompilationError(f'Waited for variable or module, check for typos or "Computer" keyword, context: {context}, got: {i}')
                break

    elif "do" in context:
        if len(context) == 1:
            if bruhtonModules.getModule(i) != "":
                context.append(i)
            elif i in modules:
                context = [i]
            else:
                printCompilationError(f"module not found, maybe there's a typo? context: {context}, got: {i}")
                break
        elif len(context) == 2:
            if i in bruhtonModules.getModule(context[1]).operators:
                context.append(i)
            else:
                printCompilationError(f"operator not found, module can: {bruhtonModules.getModule(context[1]).operators}, got: {i}")
                break
        elif len(context) == 3:
            output += (bruhtonModules.getModule(context[1])).returnCode([context[2],i])
            context = ["do"]
        else:
            printCompilationError(f"something's wrong. context: {context}, got: {i}")
            break
    else:
        if i in modules:
            context = [i]
        else:
            printCompilationError(f"word doesn't found in Bruhton, maybe there's a typo? context: {context}, got: {i}")
            break
if state == 99:
    writeRustCode(output)
    print('compilation done! code in "src/main.rs"')
    subprocess.Popen('cargo run', shell=True)