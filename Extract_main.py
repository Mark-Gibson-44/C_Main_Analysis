import re



types = ["int", "char", "bool", "float", "double"]

def extract_main(filename):
    f = open(filename, "r")

    main = False
    braces = 0
    main_code = ""
    for lines in f:
        if "{" in lines:
            braces += 1
        if "}" in lines:
            braces -= 1

        if "int main(" in lines:
            main = True
        if main:
            main_code += lines
        
        if main and braces == 0:
            main = False
    
    print(main_code)
    return main_code

def count_variables(main_code):
    var_count = 0
    for lines in main_code.splitlines():
        print(lines)
        for t in types:
            if t in lines:
                var_count += 1

    print(var_count)


if __name__ == "__main__":
    count_variables(extract_main("test_program.c"))



