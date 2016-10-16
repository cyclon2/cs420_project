tokens = (
	'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
	'LT', 'GT', 'LE', 'GE', 'EQ', 'NE', 'COMMA', 'SEMICOLON', 'COLON',
	'ID', 'LPAREN', 'RPAREN', 'LBRK', 'RBRK', 'LBRACE', 'RBRACE',
	'INTNUM', 'FLOATNUM',
	'INT', 'FLOAT','RETURN', 'WHILE', 'DO', 'FOR', 'IF', 'ELSE', 'SWITCH', 'CASE', 'BREAK', 'DEFAULT', 
	)




t_ignore = " \t"


def t_FLOATNUM(t):
	r'[0-9]+\.[0-9]+'
	if p == "-p": print(t.value, end="")
	return t

def t_INTNUM(t):
	r'[0-9]+'
	if p == "-p":print(t.value, end="")
	return t

def t_PLUS(t):
	r'\+'
	if p == "-p":print(t.value, end=" ")
	return t

def t_MINUS(t):
	r'-'
	if p == "-p":print(t.value, end=" ")
	return t

def t_TIMES(t):
	r'\*'
	if p == "-p":print(t.value, end=" ")
	return t

def t_DIVIDE(t):
	r'/'
	if p == "-p": print(t.value, end=" ")
	return t

def t_EQ(t):
	r'=='
	if p == "-p": print(t.value, end=" ")
	return t

def t_LE(t):
	r'<='
	if p == "-p": print(t.value, end=" ")
	return t

def t_GE(t):
	r'>='
	if p == "-p": print(t.value, end=" ")
	return t

def t_NE(t):
	r'!='
	if p == "-p": print(t.value, end=" ")
	return t
def t_EQUALS(t):
	r'='
	if p == "-p": print(t.value, end=" ")
	return t

def t_LT(t):
	r'<'
	if p == "-p": print(t.value, end=" ")
	return t

def t_GT(t):
	r'>'
	if p == "-p": print(t.value, end=" ")
	return t


def t_COMMA(t):
	r','
	if p == "-p": print(t.value, end =" ")
	return t

def t_SEMICOLON(t):
	r';'
	if p == "-p": print(t.value, end=" ")
	return t

def t_COLON(t):
	r':'
	if p == "-p": print(t.value, end=" ")
	return t

def t_LPAREN(t):
	r'\('
	if p == "-p": print(t.value, end="")
	return t

def t_RPAREN(t):
	r'\)'
	if p == "-p": print(t.value, end="")
	return t

def t_LBRK(t):
	r'\['
	if p == "-p": print(t.value, end="")
	return t

def t_RBRK(t):
	r'\]'
	if p == "-p": print(t.value, end="")
	return t

def t_LBRACE(t):
	r'\{'
	if p == "-p": print(t.value, end="")
	return t

def t_RBRACE(t):
	r'\}'
	if p == "-p": print(t.value, end="")
	return t

def t_ID(t):
	r'[A-Za-z][A-Za-z0-9_]*'
	a = 0;
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
		if p == "-p": print(t.value, end = "")
		a = 1;
	else:
		if p == "-p": print(t.value, end = "")
		a = 1;
	if a == 0 : 
		if p == "-p":
			print(t.value, end= " ")
	return t

def t_newline(t):
	r'\n+'
	if p == "-p": print()
	t.lexer.lineno += t.value.count("\n")

def t_error(t):
	print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

precedence = (
	('nonassoc', 'IFX'),
	('nonassoc', 'ELSE'),
	('right', 'EQUALS'),
	('left', 'EQ', 'NE'),
	('left', 'GT', 'GE', 'LT', 'LE'),
	('left', 'PLUS', 'MINUS'),
	('left', 'TIMES', 'DIVIDE'),
	('right','UMINUS'),
	('left', 'LPAREN', 'RPAREN'),
)
# dictionary of names
def p_Program(t):
	'''Program : DeclList FuncList
			| DeclList
			| FuncList 
			|  '''

def p_DeclList(t):
	'''DeclList : Declaration 
			| DeclList Declaration'''

def p_FuncList(t):
	'''FuncList : Function
			| FuncList Function'''

def p_Declaration(t):
	'Declaration : Type IdentList SEMICOLON'

def p_IdentList(t):
	'''IdentList : identifier 
			| IdentList COMMA identifier'''

def p_identifier(t):
	'''identifier : ID 
				| ID LBRK INTNUM RBRK'''

def p_Function(t):
	'''Function : Type ID LPAREN RPAREN CompoundStmt
			| Type ID LPAREN ParamList RPAREN CompoundStmt'''

def p_ParamList(t):
	'''ParamList : Type identifier
			| ParamList COMMA Type identifier'''

def p_Type(t):
	'''Type : INT
			| FLOAT'''

def p_CompoundStmt(t):
	'''CompoundStmt : LBRACE DeclList StmtList RBRACE
			| LBRACE StmtList RBRACE'''

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

def p_AssignStmt(t):
	'AssignStmt : Assign SEMICOLON'

def p_Assign(t):
	'''Assign : ID EQUALS Expr
			| ID LBRK Expr RBRK EQUALS Expr'''

def p_CallStmt(t):
	'CallStmt : Call SEMICOLON'

def p_Call(t):
	'''Call : ID LPAREN ArgList RPAREN
			| ID LPAREN RPAREN'''

def p_RetStmt(t):
	'''RetStmt : RETURN SEMICOLON
			| RETURN Expr SEMICOLON'''

def p_WhileStmt(t):
	'''WhileStmt : WHILE LPAREN Expr RPAREN Stmt
			| DO Stmt WHILE LPAREN Expr RPAREN SEMICOLON'''

def p_ForStmt(t):
	'ForStmt : FOR LPAREN Assign SEMICOLON Expr SEMICOLON Assign RPAREN Stmt'

def p_IfStmt(t):
	'''IfStmt : IF LPAREN Expr RPAREN Stmt %prec IFX
			| IF LPAREN Expr RPAREN Stmt ELSE Stmt'''

def p_SwitchStmt(t):
	'''SwitchStmt : SWITCH LPAREN identifier RPAREN LBRACE CaseList RBRACE'''

def p_CaseList(t):
	'''CaseList : CaseStmt CaseList
			| DefaultStmt
			| '''
def p_CaseStmt(t):
	'''CaseStmt : CASE INTNUM COLON StmtList BREAK SEMICOLON
			| CASE INTNUM COLON StmtList'''

def p_DefaultStmt(t):
	'''DefaultStmt : DEFAULT COLON StmtList BREAK SEMICOLON
			| DEFAULT COLON StmtList'''

def p_Expr(t):
	'''Expr : Unop
			| Bioperation
			| Call 
			| INTNUM 
			| FLOATNUM 
			| ID 
			| ID LBRK Expr RBRK 
			| LPAREN Expr RPAREN'''

def p_unop(t):
	'Unop : MINUS Expr %prec UMINUS'

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
	print()
	print("Syntax error at '%s'" % t.value)



import ply.yacc as yacc
parser = yacc.yacc()
'''
while True:
	try:
		s = input('>> ')
	except EOFError:
		break
	parser.parse(s)
'''
while True:
	try:
		global p
		p = None
		cmd = input(">> ")
		s = cmd.split(" ")[0].strip()
		if(len(cmd.split(" ")) == 2):
			p = cmd.split(" ")[1]
		if s == "exit":
			break
		f = open(s)
		l = f.read()
	except:
		print("There is no such file")
		break;
	parser.parse(l)
