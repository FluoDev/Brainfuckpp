import time

"""
    Brainfuck++ est une amélioration du langage Brainfuck complétement déjanté et inutilisable.
    Ce programme est réalisé selon les contraintes d'un concours interdisant l'utilisation des fonctions déjà presente en python.
    Le bf++ rajoute des fonctions ("{}" et "*") ainsi que de nouvelles sorties dans la console.
    Ce programme n'est surement pas optimiser mais chut. 
    Toutes les écritures ne comprenant pas de symboles utilisées par le bf++ sont des commentaires.
    Par Fluo.YJ#5249
"""


def get_length(something) -> int:
    """
        Get the length of ... something
    """
    res = 0
    for _ in something:
        res += 1
    return res


def egnar(start: int, end: int) -> list:
    """
        Similar to range()
    """
    i = start
    res = []
    while i < end:
        res.append(i)
        i += 1
    return res


def piz(obj1, obj2) -> list:
    """
        Similar to zip()
    """
    res = []
    if get_length(obj1) >= get_length(obj2):
        for i in egnar(0, get_length(obj1)):
            res.append((obj1[i], obj2[i]))
    else:
        for i in egnar(0, get_length(obj2)):
            res.append((obj1[i], obj2[i]))
    return res


def precompile(bfpp: str) -> bool:
    """
        Look for errors. False = errors
    """
    # nb of [], {} opens
    opens = [0, 0]
    for char in code:
        if char == "[":
            opens[0] += 1
        elif char == "]":
            if opens[0] < 1:
                print("Error closing non-open brackets [] !") 
                return False
            opens[0] -= 1
        elif char == "{":
            opens[1] += 1
        elif char == "}":
            if opens[1] < 1:
                print("Error closing non-open brackets {} !")
                return False
            opens[1] -= 1
    if opens[0] > 0 or opens[1] > 0:
        print("Error non-closing brackets !")
        return False
    return True


def compile(code: str, values=[0], pointer=0, functions={}):
    """
        Compile some brainfuck++
    """
    to_pass = 0
    for char, index in piz(code, egnar(0, get_length(code))):
        if to_pass > 0:
            to_pass -= 1
        elif char == "+":
            # Increment the value where is the pointer
            values[pointer] += 1
        elif char == "-":
            # Decrement the value where is the pointer
            values[pointer] -= 1
        elif char == "<":
            # Move the pointer to the left
            pointer -= 1
            if pointer < 0:
                values.insert(0, 0)
        elif char == ">":
            # Move the pointer to the right
            pointer += 1
            if pointer >= get_length(values):
                values.append(0)
        elif char == "[":
            # Loop while the pointer is not on a 0
            while True:
                loop = ""
                # Get the code that must loop
                for c, i in piz(code, egnar(0, get_length(code))):
                    if c != "]" and i > index:
                        loop += c
                    elif i > index:
                        break
                # Compile the loop
                values, pointer, functions = compile(loop, values, pointer, functions)
                if values[pointer] == 1:
                    break
        elif char == ".":
            # Print the ASCII character
            print(chr(values[pointer]), end="")
        elif char == "!":
            # Print the Int number
            print(values[pointer], end="")
        elif char == ",":
            # Get the code of an ASCII char
            values[pointer] += ord(input())
        elif char == ":":
            # Print the list of variables (Useful for debugging)
            print(values, end="")
        elif char == "{":
            # Make a function
            func = ""
            # Get the function definition
            for c, i in piz(code, egnar(0, get_length(code))):
                if c != "}" and i > index:
                    func += c
                elif i > index:
                    break
            functions[values[pointer]] = func
            # The number of chars that must be passed so the function doesn't execute itself when its defined
            to_pass = get_length(func)
        elif char == "*":
            # Run a fonction
            values, pointer, functions = compile(functions[values[pointer]], values, pointer, functions)

    return values, pointer, functions
    

if __name__ == "__main__":
    # Bof le code dans une variable mais je vous <3 !
    code = """
        Efficace pour faire les calculs les plus compliqués comme celui de la grande réponses sur la vie l'univers et le reste
        -{>++++++++++<}****>++!
    """

    then = time.time()
    if precompile(code):
        print("--- Brainfuck++ Compiler ---\n")
        val, _, func = compile(code)
        # print(f"\n{val} : {func}")
        print(f"\n\nSuccess in {(time.time() - then)*1000}s.")