import Lex_main
import Parse_main
import Extract_main




if __name__ == "__main__":

    l = Lex_main.Lexer(Extract_main.extract_main("test_program.c"))

    p = Parse_main.Parse(l.tokens)

    p.program()

    Parse_main.traverse(p.ast)
