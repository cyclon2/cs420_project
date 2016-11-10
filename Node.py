import tok as t

class Expr : pass

class Program(Expr):
	def __init__(self, first_list = None, second_list = None):
		self.type = "program"
		self.first_list = first_list
		self.second_list = second_list


class Decllist(Expr):
	def __init__(self, declaration, decllist = None):
		self.type = "decllist"
		self.declaration = declaration 
		self.decllist = decllist


class Funclist(Expr):
	def __init__(self, function, funclist = None):
		self.type = "funclist"
		self.funclist = funclist
		self.function = function


class Declaration(Expr):
	def __init__(self, dec_type ,identlist):
		self.type = "declaration"
		self.identlist = identlist
		self.dec_type = dec_type


class Identlist(Expr):
	def __init__(self, identifier, identlist = None):
		self.type = "identlist"
		self.identifier = identifier
		self.identlist = identlist


class identifier(Expr):
	def __init__(self, id ,intnum = None):
		self.type = "identifier"
		self.intnum = intnum
		self.id = id

class Function(Expr):
	def __init__(self, func_type, id ,compoundstmt, paramlist=None):
		self.type = "function"
		self.id = id
		self.func_type = func_type
		self.paramlist = paramlist
		self.compoundstmt = compoundstmt
	

class Paramlist(Expr):
	def __init__(self, param_type, identifier, paramlist = None):
		self.param_type = param_type 
		self.type = "paramlist"
		self.identifier = identifier
		self.paramlist = paramlist

class Type(Expr):
	def __init__(self, Type_type):
		self.type = "type"
		self.Type_type = Type_type
		
class Compoundstmt(Expr):
	def __init__(self, stmtlist, decllist = None):
		self.type = "compoundstmt"
		self.decllist = decllist
		self.stmtlist = stmtlist

class Stmtlist(Expr):
	def __init__(self, stmt = None, stmtlist = None):
		self.type = "stmtlist"
		self.stmt = stmt
		self.stmtlist = stmtlist

class Stmt(Expr):
	def __init__(self, stmt):
		self.type = "stmt"
		self.stmt = stmt

class Assignstmt(Expr):
	def __init__(self, assign):
		self.type = "assignstmt"
		self.assign = assign

class Assign(Expr):
	def __init__(self, id, expr1, expr2 = None):
		self.type = "assign"
		self.id = id
		self.expr1 = expr1
		self.expr2 = expr2

class Callstmt(Expr):	
	def __init__(self, call):
		self.type= "callstmt"
		self.call = call

class Call(Expr):
	def __init__(self, id, arglist = None):
		self.type = "call"
		self.id =id
		self.arglist = arglist

class Retstmt(Expr):
	def __init__(self, expr=None):
		self.type = "retstmt"
		self.expr = expr

class Whilestmt(Expr):
	def __init__(self, expr, stmt, isDowhile = False):
		self.type = "whilestmt"
		self.expr =expr
		self.stmt = stmt
		self.isDowhile = isDowhile

class Forstmt(Expr):
	def __init__(self, assign1, expr, assign2, stmt):
		self.type = "forstmt"
		self.assign1 = assign1
		self.assign2 = assign2
		self.expr = expr
		self.stmt =stmt

class Ifstmt(Expr):
	def __init__(self, expr, ifstmt, elsestmt =None):
		self.type="ifstmt"
		self.expr = expr
		self.ifstmt = ifstmt
		self.elsestmt = elsestmt

class Switchstmt(Expr):	
	def __init__(self, identifier, caselist):
		self.type = "switchstmt"
		self.identifier = identifier
		self.caselist= caselist

class Caselist(Expr):	
	def __init__(self, casestmt = None, caselist = None, defaultstmt = None):
		self.type = "caselist"
		self.casestmt = casestmt
		self.caselist = caselist
		self.defaultstmt = defaultstmt

class Casestmt(Expr):
	def __init__(self, intnum, stmtlist, isbreak = True):
		self.type = "caselist"
		self.intnum = intnum
		self.stmtlist = stmtlist
		self.isbreak = isbreak

class DefaultStmt(Expr):
	def __init__(self, stmtlist, isbreak = True):
		self.type= "defaultstmt"
		self.stmtlist = stmtlist
		self.isbreak = isbreak

class Expression(Expr):	
	def __init__(self, expr, id_expr = None, isPAREN = False):
		self.type = "expression"
		self.expr = expr
		self.id_expr = id_expr
		self.isPAREN = isPAREN

class Binop(Expr):
	def __init__(self, left, right, op):
		self.type = "bioperaion"
		self.left = left
		self.right = right
		self.op = op

class Unop(Expr):
	def __init__(self, value):
		self.type = "unop"
		self.value = value

class Arglist(Expr):
	def __init__(self, expr, arglist = None):
		self.type = "arglist"
		self.expr = expr
		self.arglist = arglist


