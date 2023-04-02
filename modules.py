class prinput():
    operators = ["<=", "=>"]
    def returnCode(input):
        if input[0] == "<=":
            return str('print!("{}", ' + input[1] + '); ')
        elif input[0] == "=>":
            return "!"
        else:
            return ""

def getModule(input):
    if input == "prinput":
        return prinput
    else:
        return ""