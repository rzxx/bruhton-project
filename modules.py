class prinput():
    operators = ["<=", "=>"]
    def returnCode(input):
        if input[0] == "<=":
            return str('print!("{}", ' + input[1] + '); ')
        elif input[0] == "=>":
            return f"std::io::stdin().read_line(&mut {input[1]}); "
        else:
            return ""

def getModule(input):
    if input == "prinput":
        return prinput
    else:
        return ""