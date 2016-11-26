import sys
name_table = {}

## function name and frequnecy
def lookup_fname(function_name):
	try:
		name_table[function_name] = name_table[function_name]+1
		return name_table[function_name]
	except KeyError:
		name_table[function_name] = 1
		return 1


class symbol:
	def __init__(self,id="", type="", array=None, role=""):
		self.id = id
		self.type = type
		self.array = array
		self.role = role


class scope:
	def __init__(self, function_name="0global", symbols=[], function_type = "", isfunction = False):
		self.function_name =function_name
		self.isfunction = isfunction
		self.function_type = function_type
		self.paramNum = 0
		self.symbols =[]
		


symbol_table = []

def Program_dfs(node, pw):
	global p
	p = pw
	name_table.clear()
	if node.second_list is not None and node.first_list is not None:
		symbol_table.append(scope())
		Decllist_dfs(node.first_list)
		Funclist_dfs(node.second_list)
	elif node.first_list is not None:
		if node.first_list.type == "decllist":
			symbol_table.append(scope())
			Decllist_dfs(node.first_list)
		else :
			Funclist_dfs(node.first_list)
	else:
		pass


def Decllist_dfs(node):
	if node.decllist is not None:
		Decllist_dfs(node.decllist)
		Declaration_dfs(node.declaration)
	else:
		Declaration_dfs(node.declaration)


def Funclist_dfs(node):
	if node.funclist is not None:
		Funclist_dfs(node.funclist)
		Function_dfs(node.function)
	else:
		Function_dfs(node.function)


def Declaration_dfs(node):
	dec_type = Type_dfs(node.dec_type)
	Identlist_dfs(node.identlist, dec_type)
	if p == "-p": print(";")


def Identlist_dfs(node, dec_type):
	if node.identlist is not None:
		Identlist_dfs(node.identlist, dec_type)
		if p == "-p": print(", ", end ="")
		identifier_dfs(node.identifier, dec_type, False)
	else:
		identifier_dfs(node.identifier, dec_type, False)

def identifier_dfs(node, dec_type, isparam):
	if dec_type != None:
		lookup_st(node.id, True, False)
		symbol_table[-1].symbols.append(symbol(type =dec_type))
		if node.intnum is not None:
			if isparam :
				symbol_table[-1].symbols[-1].id = node.id
				symbol_table[-1].symbols[-1].array = node.intnum
				symbol_table[-1].symbols[-1].role = "parameter"
			else :
				symbol_table[-1].symbols[-1].id = node.id
				symbol_table[-1].symbols[-1].array = node.intnum
				symbol_table[-1].symbols[-1].role = "variable"
			if p == "-p": print(node.id+ "["+ node.intnum+ "]", end ="")
		else:
			if isparam:
				symbol_table[-1].symbols[-1].id = node.id
				symbol_table[-1].symbols[-1].role = "parameter"
			else :
				symbol_table[-1].symbols[-1].id = node.id
				symbol_table[-1].symbols[-1].role = "variable"

			if p == "-p": print(node.id, end = "")

def Function_dfs(node):
	dec_type = Type_dfs(node.func_type)
	if node.paramlist is not None:
		if p == "-p": print(node.id+ "(", end="")
		symbol_table.append(scope(function_name = node.id, isfunction = True))
		symbol_table[-1].function_type = dec_type
		Paramlist_dfs(node.paramlist)
		if p == "-p": print(")", end="")
		Compoundstmt_dfs(node.compoundstmt, node.id, False)
	else:
		if p == "-p": print(node.id+ "()")
		symbol_table.append(scope(function_name = node.id, isfunction = True))
		symbol_table[-1].function_type = dec_type
		Compoundstmt_dfs(node.compoundstmt, node.id, False)

def Paramlist_dfs(node):
	symbol_table[-1].paramNum = symbol_table[-1].paramNum+1
	if node.paramlist is not None:
		Paramlist_dfs(node.paramlist)
		if p == "-p": print(",", end = "")
	dec_type = Type_dfs(node.param_type)
	isparam = True
	identifier_dfs(node.identifier, dec_type, isparam)


def Type_dfs(node):
	if node.Type_type == "int":
		if p == "-p": print("int ", end = "")
		return "int"
	elif node.Type_type == "float":
		if p == "-p": print("float ", end = "")
		return "float"
	else:
		pass

def Compoundstmt_dfs(node, function_name, beforecmpd):
	function_name2 = function_name
	if(beforecmpd):
		fd = lookup_fname(function_name+" compound")
		symbol_table.append(scope(function_name = function_name+ " compound(%d)"%(fd)))
		function_name2 = function_name+ " compound(%d)"%(fd)
	if node.decllist is not None:
		if p == "-p": print("{")
		Decllist_dfs(node.decllist)
		Stmtlist_dfs(node.stmtlist, function_name2, True)
		if p == "-p": print("}")
	else:
		if p == "-p": print("{")
		Stmtlist_dfs(node.stmtlist, function_name2, True)
		if p == "-p": print("}")

def Stmtlist_dfs(node, function_name, beforecmpd):
	if node.stmt is not None and node.stmtlist is not None:
		Stmt_dfs(node.stmt, function_name, beforecmpd)
		Stmtlist_dfs(node.stmtlist, function_name, beforecmpd)
	elif node.stmt is None and node.stmtlist is None:
		pass

def Stmt_dfs(node, function_name, beforecmpd):
	if type (node.stmt) == str:
		if p == "-p": print(";")
	elif node.stmt.type == "assignstmt":
		Assignstmt_dfs(node.stmt)
	elif node.stmt.type == "callstmt":
		Callstmt_dfs(node.stmt)
	elif node.stmt.type == "retstmt":
		Retstmt_dfs(node.stmt)
	elif node.stmt.type == "whilestmt":
		Whilestmt_dfs(node.stmt, function_name)
	elif node.stmt.type == "forstmt":
		Forstmt_dfs(node.stmt, function_name)
	elif node.stmt.type == "ifstmt":
		Ifstmt_dfs(node.stmt, function_name)
	elif node.stmt.type == "switchstmt":
		Switchstmt_dfs(node.stmt, function_name)
	elif node.stmt.type == "compoundstmt":
		Compoundstmt_dfs(node.stmt, function_name, beforecmpd)
	else:
		if p == "-p": print(";")
		pass

def Assignstmt_dfs(node):
	Assign_dfs(node.assign)
	if p == "-p": print(";")

def Assign_dfs(node):
	if node.expr2 is None:
		id_type = lookup_st(node.id,False, False)
		if p == "-p": print(node.id+ "=", end = " ")
		ret = Expr_dfs(node.expr1)
		if ret != id_type and id_type != "id" and ret != None:
			print("warning: implicit conversion from '%s' to '%s' changes value"%(id_type, ret))
	else:	
		if p == "-p": print(node.id+ "[", end = " ")
		id_type = lookup_st(node.id,False, True)
		Expr_dfs(node.expr1)
		if p == "-p": print("]=", end = " ")
		ret = Expr_dfs(node.expr2)
		if ret != id_type and id_type !="id" and ret != None:
			print("warning: implicit conversion from '%s' to '%s' changes value"%(id_type, ret))

def Callstmt_dfs(node):
	Call_dfs(node.call)
	if p == "-p": print(";")

def Call_dfs(node):
	if node.arglist is None:
		lookup_call(node.id,0)	
		if p == "-p": print(node.id+"()", end ="")
		pass
	else:
		if p == "-p": print(node.id+ "(", end="")
		argNum = Arglist_dfs(node.arglist, 0)
		lookup_call(node.id, argNum)
		if p == "-p": print(")", end="")

def Retstmt_dfs(node):
	if node.expr is None:
		if symbol_table[-1].function_type != None:
			print("non-void function '%s' should return a value"%(symbol_table[-1].function_name))
			exit()
		if p == "-p": print("return;")
		pass
	else:
		if p == "-p": print("return", end =" ")
		ret = Expr_dfs(node.expr)
		if ret != "id" and symbol_table[-1].function_type != ret:
			print("warning implicit conversion from '%s' to '%s' changes value"%(symbol_table[-1].function_type, ret))
		if p == "-p": print(";")

def Whilestmt_dfs(node, function_name):
	function_name = function_name + " while"
	fd = lookup_fname(function_name)
	symbol_table.append(scope(function_name = function_name+ "(%d)"%(fd)))

	if node.isDowhile is True:
		if p == "-p": print("do ", end ="")
		Stmt_dfs(node.stmt, function_name+"(%d)"%(fd), False)
		if p == "-p": print("while (", end = "")
		Expr_dfs(node.expr)
		if p == "-p": print(");")
	else:
		if p == "-p": print("while (", end = "")
		Expr_dfs(node.expr)
		if p == "-p": print(") ", end= "")
		Stmt_dfs(node.stmt, function_name+"(%d)"%(fd), False)

def Forstmt_dfs(node, function_name):
	if p == "-p": print("for( ", end ="")
	Assign_dfs(node.assign1)
	if p == "-p": print("; ", end="")
	Expr_dfs(node.expr)
	if p == "-p": print("; ", end="")
	Assign_dfs(node.assign2)
	if p == "-p": print(")")
	function_name = function_name + " for"
	fd = lookup_fname(function_name)
	symbol_table.append(scope(function_name = function_name+ "(%d)"%(fd)))

	Stmt_dfs(node.stmt, function_name+"(%d)"%(fd), False)

def Ifstmt_dfs(node, function_name):
	if p == "-p": print("if ( ", end ="")
	Expr_dfs(node.expr)
	if p == "-p": print(")")
	function_name2 = function_name+ " if"
	fd = lookup_fname(function_name2)
	symbol_table.append(scope(function_name = function_name2+ "(%d)"%(fd)))

	Stmt_dfs(node.ifstmt, function_name2+"(%d)"%(fd), False)
	if node.elsestmt is not None:
		function_name3 = function_name+ " else"
		fd = lookup_fname(function_name3)
		symbol_table.append(scope(function_name = function_name3+ "(%d)"%(fd)))

		Stmt_dfs(node.elsestmt, function_name3+"(%d)"%(fd), False)

def Switchstmt_dfs(node, function_name):
	if p == "-p": print("swtich (", end ="")
	identifier_dfs(node.identifier, None,False)
	if p == "-p": print("){", end="")
	Caselist_dfs(node.caselist, function_name)
	if p == "-p": print("}")

def Caselist_dfs(node, function_name):
	if node.casestmt is not None and node.caselist is not None:
		Casestmt_dfs(node.casestmt, function_name)
		Caselist_dfs(node.caselist, function_name)
	if node.defaultstmt is not None:
		Defaultstmt_dfs(node.defaultstmt, function_name)

def Casestmt_dfs(node, function_name):
	if p == "-p": print("case ", node.intnum, ":", end =" ")
	function_name = function_name+" case"+ node.intnum
	fd = lookup_fname(function_name)
	symbol_table.append(scope(function_name = function_name+ "(%d)"%(fd)))
	Stmtlist_dfs(node.stmtlist, function_name+"(%d)"%(fd), True)
	if node.isbreak:
		if p == "-p": print("break;")
		pass
	else:
		pass

def Defaultstmt_dfs(node, function_name):
	if p == "-p": print("default :", end ="")
	function_name = function_name + " default"
	fd = lookup_fname(function_name)
	symbol_table.append(scope(function_name = function_name+ "(%d)"%(fd)))
	Stmtlist_dfs(node.stmtlist, function_name+"(%d)"%(fd),False)
	if node.isbreak:
		if p == "-p": print("break;")
		pass
	else:
		pass

def Expr_dfs(node, isArray = False):
	if type(node) == str:
		if p == "-p": print(node, end =" ")
		return lookup_st(node, False, isArray)
	elif type(node.expr) == str:
		 return Expr_dfs(node.expr)
	else:
		if node.id_expr is None:
			if node.expr.type == "unop":
				return Unop_dfs(node.expr)
			elif node.expr.type == "bioperaion":
				Binop_dfs(node.expr)
			elif node.expr.type == "call":
				Call_dfs(node.expr)
			elif node.isPAREN:
				if p == "-p": print("(", end ="")
				Expr_dfs(node.expr)
				if p == "-p": print(")", end="")
		else:
			Expr_dfs(node.id_expr, True)
			if p == "-p": print("[", end ="")
			Expr_dfs(node.expr)
			if p == "-p": print("]", end="")


def Unop_dfs(node):
	if p == "-p": print("-", end="")
	return Expr_dfs(node.value)
	pass

def Binop_dfs(node):
	Expr_dfs(node.left)
	if p == "-p": print(node.op, end =" ")
	Expr_dfs(node.right)

def Arglist_dfs(node, argNum):
	argNum = argNum +1
	if node.arglist is None:
		Expr_dfs(node.expr)
	else:
		argNum = Arglist_dfs(node.arglist, argNum)
		if p == "-p": print(",", end=" ")
		Expr_dfs(node.expr)
	return argNum


def lookup_funcName(s):
	super_funcName = s.rsplit(" ",1)[0]
	for scope in symbol_table:
		if scope.function_name == super_funcName:
			return scope

def lookup_st(p, isRedecla, isArray):
	try:
		try:
			int(p)
			return "int"
		except:
			float(p)
			return "float"
	except:
		if isRedecla == False:
			func_scope = symbol_table[-1]
			while(func_scope.isfunction == False):
				l = func_scope.symbols
				for i in l:
					if p == i.id:
						if isArray ==True and i.array !=None:
							if i.type == "int":
								return "int"
							elif i.type == "float":
								return "float"
							return "id"
						elif isArray == False and i.array == None:
							if i.type == "int":
								return "int"
							elif i.type == "float":
								return "float"
							return "id"
						else:
							print("%s subscripted value is not an array, pointer, or vector"%(p))
							exit()
				func_scope = lookup_funcName(func_scope.function_name)

			if func_scope.isfunction == True:
				l = func_scope.symbols
				for i in l:
					if p == i.id:
						if isArray ==True and i.array !=None:
							if i.type == "int":
								return "int"
							elif i.type == "float":
								return "float"
							return "id"
						elif isArray == False and i.array == None:
							if i.type == "int":
								return "int"
							elif i.type == "float":
								return "float"
							return "id"
						else:
							print("%s subscripted value is not an array, pointer, or vector"%(p))
							exit()	
			if symbol_table[0].function_name == "0global":
				func_scope = symbol_table[0]
				l = func_scope.symbols
				for i in l:
					if p == i.id:
						if isArray==True and i.array !=None:
							if i.type == "int":
								return "int"
							elif i.type == "float":
								return "float"
							return "id"
						elif isArray == False and i.array == None:
							if i.type == "int":
								return "int"
							elif i.type == "float":
								return "float"
							return "id"
						else:
							print("%s subscripted value is not an array, pointer, or vector"%(p))
							exit()

			print('%s no declaration in any scope\n'%(p))
			exit()
		else:
			l = symbol_table[-1].symbols
			for i in l:
				if p == i.id:
					print('redefinitio of %s n\n'%(p))
					exit()
			else:
				return "id"


def lookup_call(p, argNum):
	for i in symbol_table:
		if i.function_name == p:
			if i.paramNum == argNum:
				return
			elif i.paramNum < argNum:
				print("too many arguments to function call, expected %d, have %d"%(i.paramNum, argNum))
				exit()
			else:
				print("too few arguments to function call, expected %d, have %d"%(i.paramNum, argNum))
				exit()
	print('%s no function declaration\n'%(p))
	exit()

def print_st():
	for s in symbol_table:
		print("func name : %s // func type : %s // is_func : %s // paramNum %d "%(s.function_name, s.function_type, s.isfunction, s.paramNum))
		for l in s.symbols:
			print(l.type,"\t",l.id,"\t",l.array,"\t",l.role)
		print()
