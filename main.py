import Lex_main
import Parse_main
import Extract_main
import symbol_table
import optimization



if __name__ == "__main__":

    l = Lex_main.Lexer(Extract_main.extract_main("test_program.c"))
   
    p = Parse_main.Parse(l.tokens)

    p.program()

    Parse_main.traverse(p.ast)
    

    s = symbol_table.semantics(p.ast)
    s.var_traverse(s.ir)

    print(s.scope.scope)
    