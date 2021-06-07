from Lex_main import LexTokens
import Parse_main as p



class symbol_table:

    def __init__(self, outer = None):
        
        self.scope = {}
        self.outer_scope = outer
    def add_assign(self, node, val = None):
        self.scope[node.text] = val
    
    def re_assign_var(self, var, val):
        if self.in_scope(var):
            self.scope[var] = val
        elif self.outer_scope is not None:
            self.outer_scope.re_assign_var(var, val)

    def in_scope(self, var):
        
        if var in self.scope:
            return True
        if self.outer_scope is None:
            return False
        return self.outer_scope.in_scope(var)
    def in_local_scope(self, var):
        return var in self.scope
    
    
        

    

class semantics:

    def __init__(self, ir):
        self.ir = ir
        self.scope = symbol_table()
        self.branches = []

    def eval_r_val(self, rhs):
        accum = 0
        for elements in rhs:
            if elements.token == LexTokens.var_name:
                accum += self.scope.scope[elements.text]
            else:
                accum += int(elements.text)
        return accum
    
    def inc_dec(self, var_node, inc_node):
        if inc_node.text == "++":
            self.scope.add_assign(var_node, self.scope.scope[var_node.text] + 1)
        else:
            self.scope.add_assign(var_node, self.scope.scope[var_node.text] - 1)

    def assign(self, expr):
        var_name = None
        for lex in expr:
            if lex.token == LexTokens.var_name:
                var_name = lex
            if lex.text == "RHS":
                
                self.scope.add_assign(var_name, self.eval_r_val(lex.children))
            if lex.token == LexTokens.Increment:
                self.inc_dec(var_name, lex)
                
        pass
    def expr_is_constant(self, expr):
        const = True
        for leaves in expr.children:
            if leaves.token == LexTokens.var_name:
                const &= self.scope.in_local_scope(leaves.text)
        return const

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
            if node.token == LexTokens.Increment:
                self.assign(expr)
        
        
    def var_traverse(self, leaf):
        
        if(leaf.text == "EXPR" or "statement" in leaf.text):
            
            self.eval_node(leaf.children)
        if (leaf.token == LexTokens.left_brace):
            pass#self.scope = symbol_table(self.scope)
        if (leaf.token == LexTokens.right_brace):
            #if self.scope.outer is not None:
            #   self.scope = self.scope.outer
            pass#self.scope = self.scope.outer
        if leaf.text == "Bool_Expr":
            print("BOOLEAN EXPRESSION IS CONSTANT? {}".format(self.expr_is_constant(leaf)))
        if leaf.text == "BLOCK":
            self.branches.append(leaf)
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
        
    