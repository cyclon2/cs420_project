import sys

import Node as n
import dfs_search as dfs
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
	return t

def t_INTNUM(t):
	r'[0-9]+'
	return t

def t_PLUS(t):
	r'\+'
	return t

def t_MINUS(t):
	r'-'
	return t

def t_TIMES(t):
	r'\*'
	return t

def t_DIVIDE(t):
	r'/'
	return t

def t_EQ(t):
	r'=='
	return t

def t_LE(t):
	r'<='
	return t

def t_GE(t):
	r'>='
	return t

def t_NE(t):
	r'!='
	return t
def t_EQUALS(t):
	r'='
	return t

def t_LT(t):
	r'<'
	return t

def t_GT(t):
	r'>'
	return t


def t_COMMA(t):
	r','
	return t

def t_SEMICOLON(t):
	r';'
	return t

def t_COLON(t):
	r':'
	return t

def t_LPAREN(t):
	r'\('
	return t

def t_RPAREN(t):
	r'\)'
	return t

def t_LBRK(t):
	r'\['
	return t

def t_RBRK(t):
	r'\]'
	return t

def t_LBRACE(t):
	r'\{'
	return t

def t_RBRACE(t):
	r'\}'
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
			| '''
	if len(t) == 1 :
		t[0] = n.Program()
	elif len(t) == 2 :
		t[0] = n.Program(t[1])
	elif len(t) == 3 :
		t[0] = n.Program(t[1], t[2])
	else:
		print("program error!")
	
	dfs.Program_dfs(t[0], option)

def p_DeclList(t):
	'''DeclList : Declaration 
			| DeclList Declaration'''
	if len(t) == 2 :
		t[0] = n.Decllist(declaration = t[1])
	elif len(t) == 3 :
		t[0] = n.Decllist(t[2],t[1])
	else:
		print("declist error!")

def p_FuncList(t):
	'''FuncList : Function
			| FuncList Function'''
	if len(t) ==2:
		t[0] = n.Funclist(t[1])
	elif len(t) ==3:
		t[0] = n.Funclist(t[2], t[1])
	else:
		print("funclist error!")

def p_Declaration(t):
	'Declaration : Type IdentList SEMICOLON'
	t[0] = n.Declaration(t[1], t[2])

def p_IdentList(t):
	'''IdentList : identifier 
			| IdentList COMMA identifier'''
	if len(t) ==2:
		t[0] = n.Identlist(t[1])
	elif len(t) ==4:
		t[0] = n.Identlist(t[3], t[1])
	else :
		print("identlist error!")

def p_identifier(t):
	'''identifier : ID 
				| ID LBRK INTNUM RBRK'''
	if len(t) == 2:
		t[0] = n.identifier(id = t[1])
	else :
		t[0] = n.identifier(t[1], t[3])
	

def p_Function(t):
	'''Function : Type ID LPAREN RPAREN CompoundStmt
			| Type ID LPAREN ParamList RPAREN CompoundStmt'''
	if len(t) == 6:
		t[0] = n.Function(t[1], t[2], t[5])
	elif len(t) == 7:
		t[0] = n.Function(t[1], t[2], t[6], t[4])
	else:
		print("function error!")

def p_ParamList(t):
	'''ParamList : Type identifier
			| ParamList COMMA Type identifier'''
	if len(t) == 3:
		t[0] = n.Paramlist(t[1], t[2])
	elif len(t) == 5:
		t[0] = n.Paramlist(t[3], t[4], t[1])
	else:
		print("paramlist error!")
	
def p_Type(t):
	'''Type : INT
			| FLOAT'''
	t[0] = n.Type(t[1])

def p_CompoundStmt(t):
	'''CompoundStmt : LBRACE DeclList StmtList RBRACE
			| LBRACE StmtList RBRACE'''
	if len(t) == 5 :
		t[0] = n.Compoundstmt(t[3], t[2])
	else :
		t[0] = n.Compoundstmt(t[2])

def p_StmtList(t):
	'''StmtList : Stmt StmtList
			| '''
	if len(t) == 3:
		t[0] = n.Stmtlist(t[1], t[2])
	else:
		t[0] = n.Stmtlist()
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
	t[0] = n.Stmt(t[1])

def p_AssignStmt(t):
	'AssignStmt : Assign SEMICOLON'
	t[0] = n.Assignstmt(t[1])

def p_Assign(t):
	'''Assign : ID EQUALS Expr
			| ID LBRK Expr RBRK EQUALS Expr'''
	if len(t) == 4:
		t[0] = n.Assign(t[1], t[3])
	else:
		t[0] = n.Assign(t[1], t[3], t[6])

def p_CallStmt(t):
	'CallStmt : Call SEMICOLON'
	t[0] = n.Callstmt(t[1])

def p_Call(t):
	'''Call : ID LPAREN ArgList RPAREN
			| ID LPAREN RPAREN'''
	if len(t) == 5 :
		t[0] = n.Call(t[1], t[3])
	else:
		t[0] = n.Call(t[1])

def p_RetStmt(t):
	'''RetStmt : RETURN SEMICOLON
			| RETURN Expr SEMICOLON'''
	if len(t) == 3 :
		t[0] = n.Retstmt()
	else:
		t[0] = n.Retstmt(t[2])

def p_WhileStmt(t):
	'''WhileStmt : WHILE LPAREN Expr RPAREN Stmt
			| DO Stmt WHILE LPAREN Expr RPAREN SEMICOLON'''
	if len(t) == 6:
		t[0] = n.Whilestmt(t[3], t[5])
	else:
		t[0] = n.Whilestmt(t[5], t[2], True)

def p_ForStmt(t):
	'ForStmt : FOR LPAREN Assign SEMICOLON Expr SEMICOLON Assign RPAREN Stmt'
	t[0] = n.Forstmt(t[3], t[5], t[7], t[9])

def p_IfStmt(t):
	'''IfStmt : IF LPAREN Expr RPAREN Stmt %prec IFX
			| IF LPAREN Expr RPAREN Stmt ELSE Stmt'''
	if len(t) ==6 :
		t[0] = n.Ifstmt(t[3], t[5])
	else:
		t[0] = n.Ifstmt(t[3], t[5], t[7])

def p_SwitchStmt(t):
	'''SwitchStmt : SWITCH LPAREN identifier RPAREN LBRACE CaseList RBRACE'''
	t[0] = n.Switchstmt(t[3], t[6])

def p_CaseList(t):
	'''CaseList : CaseStmt CaseList
			| DefaultStmt
			| '''
	if len(t)==3:
		t[0] = n.Caselist(t[1], t[2])
	elif len(t) == 2:
		t[0] = n.Caselist(None,None,t[1])
	elif len(t) ==1:
		t[0] = n.Caselist()
	else:
		print("caselist error!")

def p_CaseStmt(t):
	'''CaseStmt : CASE INTNUM COLON StmtList BREAK SEMICOLON
				| CASE INTNUM COLON StmtList'''
	if len(t)== 7:
		t[0] = n.Casestmt(t[2], t[4])
	else:
		t[0] = n.Casestmt(t[2], t[4], False)

def p_DefaultStmt(t):
	'''DefaultStmt : DEFAULT COLON StmtList BREAK SEMICOLON
				| DEFAULT COLON StmtList'''
	if len(t) == 6:
		t[0] = n.DefaultStmt(t[3])
	else:
		t[0] = n.DefaultStmt(t[3], False)

def p_Expr(t):
	'''Expr : Unop
			| Bioperation
			| Call 
			| INTNUM 
			| FLOATNUM 
			| ID 
			| ID LBRK Expr RBRK 
			| LPAREN Expr RPAREN'''
	if len(t) == 2 :
		t[0] = n.Expression(t[1])
	elif len(t) == 5:
		t[0] = n.Expression(t[3], t[1])
	else: 
		t[0] = n.Expression(t[2], isPAREN = True)

def p_unop(t):
	'Unop : MINUS Expr %prec UMINUS'
	t[0] = n.Unop(t[2])

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
	t[0] = n.Binop(t[1], t[3], t[2])

def p_ArgList(t):
	'''ArgList : Expr
			| ArgList COMMA Expr'''
	if len(t) == 2 : 
		t[0] = n.Arglist(t[1])
	elif len(t) == 4 :
		t[0] = n.Arglist(t[3], t[1])
	else:
		print("arglist error!")

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

try:
	global option
	if len(sys.argv) == 3:
		option = sys.argv[1]	
		file_name = sys.argv[2]
	elif len(sys.argv) == 2:
		option = None
		file_name= sys.argv[1]
	else:
		print(len(sys.argv))
	f = open(file_name)
	l = f.read()
except:
	print("There is no such file")
parser.parse(l)
#dfs.print_st()
