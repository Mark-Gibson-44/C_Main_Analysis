from Lex_main import LexTokens

class node:

    def __init__(self, lexeme, token = -1):
        self.token = token
        self.text = lexeme
        self.parent = None
        self.children = []

    def addNode(self, node):
        node.set_parent(self)
        self.children.append(node)
    
    def get_parent(self):
        return self.parent

    def set_parent(self, parent):
        self.parent = parent
    
    def remove(self, node):
        self.children.remove(node)

class Parse:

    def consume(self):
        
        self.current_token += 1
        self.lookahead_token += 1

    def match(self, x):
        if self.tokens[self.current_token][0] == x:
            child = node(self.tokens[self.current_token][1], self.tokens[self.current_token][0])
            self.traversal_ptr.addNode(child)

            self.consume()

    def __init__(self, token_stream):

        self.parse_tree = []
        self.current_token = 2
        self.lookahead_token = 3
        self.tokens = token_stream
        self.ast = node("Program")
        self.traversal_ptr = self.ast
        pass
    

    def expr(self):
        
        if self.tokens[self.current_token][0] == LexTokens.var_type:
            self.match(LexTokens.var_type)
            
            self.match(LexTokens.var_name)
            
            if self.tokens[self.current_token][0] == LexTokens.assignment:
                self.match(LexTokens.assignment)
                _rhs = node("RHS")
                self.traversal_ptr.addNode(_rhs)
                self.traversal_ptr = _rhs
                self.expr()
                self.traversal_ptr = self.traversal_ptr.get_parent()

                
        if self.tokens[self.current_token][0] == LexTokens.int_literal:
            
            self.match(LexTokens.int_literal)
        
        if self.tokens[self.current_token][0] == LexTokens.var_name and self.tokens[self.lookahead_token][0] == LexTokens.Equality:
            self.match(LexTokens.var_name)
            
            self.match(LexTokens.Equality)
            if self.tokens[self.current_token][0] == LexTokens.int_literal:
                self.match(LexTokens.int_literal)
            else:
                self.match(LexTokens.var_name)
            self.traversal_ptr = self.traversal_ptr.get_parent()
        if self.tokens[self.current_token][0] == LexTokens.var_name and self.tokens[self.lookahead_token][0] == LexTokens.Increment:
            self.match(LexTokens.var_name)
            self.match(LexTokens.Increment)
        pass
    
    def block(self):
        i = 0
        while self.tokens[self.current_token][0] is not LexTokens.right_brace:
            
            inner_s = node("nested_statement{}".format(i))
            self.traversal_ptr.addNode(inner_s)
            self.traversal_ptr = inner_s
            i += 1
            self.stmt()
        
        self.traversal_ptr = self.traversal_ptr.get_parent()

    def stmt(self):
        
        if self.tokens[self.current_token][0] == LexTokens.left_brace:
            
            
            self.match(LexTokens.left_brace)
            
            self.block()
            
            self.match(LexTokens.right_brace)
            self.traversal_ptr = self.traversal_ptr.get_parent()
            return
            


        if self.tokens[self.current_token][0] == LexTokens.if_key:
            

            self.match(LexTokens.if_key)
            _expr = node("EXPR")
            self.traversal_ptr.addNode(_expr)
            self.traversal_ptr = _expr
            self.expr()
            _block = node("BLOCK")
            self.traversal_ptr.addNode(_block)
            self.traversal_ptr = _block
            self.block()
            self.traversal_ptr = self.traversal_ptr.get_parent()
            return
        else:
            self.expr()



    def program(self):
        
        while self.lookahead_token < len(self.tokens):
            
            
            statm = node("Main_block")
            self.traversal_ptr.addNode(statm)
            self.traversal_ptr = statm
            self.stmt()
            self.traversal_ptr = self.traversal_ptr.get_parent()
            



def traverse(tree):
    if tree.get_parent() is None:
        print("Lex: {0} with Parent Root".format(tree.text))
    else:
        print("Lex: {0} with Parent {1}".format(tree.text, tree.get_parent().text))
    for leaves in tree.children:
        traverse(leaves)
        



