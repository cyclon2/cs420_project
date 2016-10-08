tokens = (
	'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
	'LT', 'GT', 'LE', 'GE', 'EQ', 'NE', 'COMMA', 'SEMICOLON', 'COLON',
	'ID', 'LPAREN', 'RPAREN', 'LBRK', 'RBRK', 'LBRACE', 'RBRACE',
	'INTNUM', 'FLOATNUM',
	'INT', 'FLOAT','RETURN', 'WHILE', 'DO', 'FOR', 'IF', 'ELSE', 'SWITCH', 'CASE', 'BREAK', 'DEFAULT', 
	)


## bi operation ##
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='
t_COMMA = r'\,'
t_SEMICOLON = r';'
t_COLON = r':'

##	closure		##

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRK = r'\['
t_RBRK = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

##		num		##

t_INTNUM = r'[0-9]+'
t_FLOATNUM = r'[0-9]+.[0-9]+'

##	keyword		##

t_INT = r'int'
t_FLOAT = r'float'
t_RETURN = r'return'
t_WHILE = r'while'
t_DO = r'do'
t_FOR = r'for'
t_IF = r'if'
t_ELSE = r'else'
t_SWITCH = r'switch'
t_CASE = r'case'
t_DEFAULT = r'default'
t_BREAK = r'break'




t_ignore = " \t"

def t_ID(t):
	r'[A-Za-z][A-Za-z0-9_]*'
	if t.value == 'int':
		t.type = 'INT'
	
	elif t.value == 'float':
		t.type = 'FLOAT'
	
	elif t.value == 'return':
		t.type = 'RETURN'
	
	elif t.value == 'while':
		t.type = 'WHILE'
	
	elif t.value == 'do':
		t.type = 'DO'
	
	elif t.value == 'for':
		t.type = 'FOR'

	elif t.value == 'if':
		t.type = 'IF'
	
	elif t.value == 'else':
		t.type = 'ELSE'

	elif t.value == 'switch':
		t.type = 'SWITCH'
	
	elif t.value == 'case':
		t.type = 'CASE'
	
	elif t.value == 'default':
		t.type = 'DEFAULT'
	
	elif t.value == 'break':
		t.type = 'BREAK'	

	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += t.value.count("\n")

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

precedence = (
	('left', 'EQ', 'NE'),
	('left', 'GT', 'GE', 'LT', 'LE'),
	('left', 'PLUS', 'MINUS'),
	('left', 'TIMES', 'DIVIDE'),
	('right','UMINUS'),
	('right', 'EQUALS'),
)

# dictionary of names


def p_Program(t):
	'''Program : DeclList FuncList
			| DeclList
			| FuncList 
			|  '''
	print("program" )

def p_DeclList(t):
	'''DeclList : Declaration 
			| DeclList Declaration'''
	print("DeclList")

def p_FuncList(t):
	'''FuncList : Function
			| FuncList Function'''
	print("FucnList")

def p_Declaration(t):
	'Declaration : Type IdentList SEMICOLON'
	print("Declaration")

def p_IdentList(t):
	'''IdentList : identifier 
			| IdentList COMMA identifier'''
	print("IdentList")

def p_identifier(t):
	'''identifier : ID 
				| ID LBRK INTNUM RBRK '''
	print("identifier : ", t[1])

def p_Function(t):
	'''Function : Type ID LPAREN RPAREN CompoundStmt
			| Type ID LPAREN ParamList RPAREN CompoundStmt'''
	print("Function :", t[1], t[2])

def p_ParamList(t):
	'''ParamList : Type identifier
			| ParamList COMMA Type identifier'''
	print("paramList", t[1], t[2])

def p_Type(t):
	'''Type : INT
			| FLOAT'''
	print("type : ", t[1])

def p_CompoundStmt(t):
	'''CompoundStmt : LBRACE DeclList StmtList RBRACE
			| LBRACE StmtList RBRACE'''
	print("CompoundStmt")

def p_StmtList(t):
	'''StmtList : Stmt StmtList
			| '''
def p_Stmt(t):
	'''Stmt : AssignStmt
			| CallStmt
			| RetStmt
			| WhileStmt
			| ForStmt
			| IfStmt
			| SwitchStmt
			| CompoundStmt 
			| SEMICOLON'''
	print("Stmt")

def p_AssignStmt(t):
	'AssignStmt : Assign SEMICOLON'
	print("AssignStmt")

def p_Assign(t):
	'''Assign : ID EQUALS Expr
			| ID LBRK Expr RBRK EQUALS Expr'''
	print("Assign")

def p_CallStmt(t):
	'CallStmt : Call SEMICOLON'
	print("CallStmt")

def p_Call(t):
	'''Call : ID LPAREN ArgList RPAREN
			| ID LPAREN RPAREN'''
	print("CAll : ", t[1])

def p_RetStmt(t):
	'''RetStmt : RETURN SEMICOLON
			| RETURN Expr SEMICOLON'''
	print("RetStmt")

def p_WhileStmt(t):
	'''WhileStmt : WHILE LPAREN Expr RPAREN Stmt
			| DO Stmt WHILE LPAREN Expr RPAREN'''
	print("Whilestmt")

def p_ForStmt(t):
	'ForStmt : FOR LPAREN Assign SEMICOLON Expr SEMICOLON Assign RPAREN Stmt'
	print("for")

def p_IfStmt(t):
	'''IfStmt : IF LPAREN Expr RPAREN Stmt
			| IF LPAREN Expr RPAREN Stmt ELSE Stmt'''
	print("IF else")

def p_SwitchStmt(t):
	'''SwitchStmt : SWITCH LPAREN identifier RPAREN LBRACE CaseList RBRACE'''
	print("switch")

def p_CaseList(t):
	'''CaseList : CaseList CASE INTNUM COLON StmtList BREAK SEMICOLON DEFAULT COLON StmtList BREAK SEMICOLON
			| CaseList CASE INTNUM COLON StmtList BREAK SEMICOLON DEFAULT COLON StmtList
			| CaseList CASE INTNUM COLON StmtList DEFAULT COLON StmtList BREAK SEMICOLON
			| CaseList CASE INTNUM COLON StmtList DEFAULT COLON StmtList
			| CaseList CASE INTNUM COLON StmtList BREAK SEMICOLON
			| CaseList CASE INTNUM COLON StmtList
			| CASE INTNUM COLON StmtList BREAK SEMICOLON DEFAULT COLON StmtList BREAK SEMICOLON
			| CASE INTNUM COLON StmtList BREAK SEMICOLON DEFAULT COLON StmtList
			| CASE INTNUM COLON StmtList DEFAULT COLON StmtList BREAK SEMICOLON
			| CASE INTNUM COLON StmtList DEFAULT COLON StmtList
			| CASE INTNUM COLON StmtList BREAK SEMICOLON
			| CASE INTNUM COLON StmtList'''
	print("case")

def p_Expr(t):
	'''Expr : Unop
			| Bioperation
			| Call 
			| INTNUM 
			| FLOATNUM 
			| ID 
			| ID LBRK Expr RBRK 
			| LPAREN Expr RPAREN'''
	print("expr : ", t[1])

def p_unop(t):
	'Unop : MINUS Expr %prec UMINUS'
	print("unop : ",t[1])

def p_Bioperation(t):
	'''Bioperation : Expr PLUS Expr
			| Expr MINUS Expr
			| Expr TIMES Expr
			| Expr DIVIDE Expr
			| Expr GT Expr
			| Expr LT Expr
			| Expr GE Expr
			| Expr LE Expr
			| Expr EQ Expr
			| Expr NE Expr'''

def p_ArgList(t):
	'''ArgList : Expr
			| ArgList COMMA Expr'''


def p_error(t):
	print("Syntax error at '%s'" % t.value)



import ply.yacc as yacc
parser = yacc.yacc()

while True:
	try:
		s = input('calc > ')
	except EOFError:
		break
	parser.parse(s)

