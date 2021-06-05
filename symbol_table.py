from Lex_main import LexTokens
import Parse_main as p



class symbol_table:

    def __init__(self, outer = None):
        
        self.scope = {}
        self.outer_scope = outer
    def add_assign(self, node, val = None):
        self.scope[node.text] = val
    
    

    def in_scope(self, var):
        
        if var in self.scope:
            return True
        if self.outer_scope is None:
            return False
        return self.outer_scope.in_scope(var)
    
    
        

    

class semantics:

    def __init__(self, ir):
        self.ir = ir
        self.scope = symbol_table()
    def assign(self, expr):
        var_name = None
        for lex in expr:
            if lex.token == LexTokens.var_name:
                var_name = lex
            if lex.text == "RHS":
                print("RHIGHT")
                #self.scope.add_assign(var_name, int(lex.text))    
        pass
    
    def init_var(self, expr):
        
        for lex in expr:
            if lex.token == LexTokens.var_name:
                self.scope.add_assign(lex)
        pass

    def eval_node(self, expr):
        for node in expr:
            
            if node.token == LexTokens.var_type:
                self.init_var(expr)
            if node.token == LexTokens.assignment :
                self.assign(expr)
        
        
    def var_traverse(self, leaf):
        
        if(leaf.text == "EXPR" or "statement" in leaf.text):
            
            self.eval_node(leaf.children)
            
        for leaves in leaf.children:
            
            self.var_traverse(leaves)
    
    def type_check(self, expr):
        pass

    def type_traverse(self, leaf):
        if(leaf.text == "EXPR"):
            self.type_check(leaf.children)
            return
        for leaves in leaf.children:
            self.type_traverse(leaf)
        
    