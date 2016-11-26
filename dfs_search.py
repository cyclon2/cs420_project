name_table = {}
print_ast = ""
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
		self.isused = False


class scope:
	def __init__(self, function_name="0global", symbols=[], function_type = "", isfunction = False):
		self.function_name =function_name
		self.isfunction = isfunction
		self.function_type = function_type
		self.paramNum = 0
		self.symbols =[]
		

symbol_table = []

def Program_dfs(node, pw):	
	global print_ast
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
	print_unused()
	print()
	print(print_ast)

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
	global print_ast
	dec_type = Type_dfs(node.dec_type)
	Identlist_dfs(node.identlist, dec_type)
	#if p == "-p": print(";")
	print_ast += ";\n"


def Identlist_dfs(node, dec_type):
	global print_ast
	if node.identlist is not None:
		Identlist_dfs(node.identlist, dec_type)
		#if p == "-p": print(", ", end ="")
		print_ast += ", "
		identifier_dfs(node.identifier, dec_type, False)
	else:
		identifier_dfs(node.identifier, dec_type, False)


def identifier_dfs(node, dec_type, isparam, isarray = False):
	global print_ast
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
			#if p == "-p": print(node.id+ "["+ node.intnum+ "]", end ="")
			print_ast += node.id+"["+node.intnum+"]"
		else:
			if isparam:
				symbol_table[-1].symbols[-1].id = node.id
				symbol_table[-1].symbols[-1].role = "parameter"
			else :
				symbol_table[-1].symbols[-1].id = node.id
				symbol_table[-1].symbols[-1].role = "variable"

			#if p == "-p": print(node.id, end = "")
			print_ast += node.id
	else:
		if isarray:
			lookup_st(node.id, False, True)
			#if p == "-p": print(node.id+ "["+ node.intnum+ "]", end ="")
			print_ast += node.id+"["+str(node.intnum)+"]"
		else:
			lookup_st(node.id, False, False)
			#if p == "-p": print(node.id, end = "")
			print_ast += node.id+""



def Function_dfs(node):
	global print_ast
	dec_type = Type_dfs(node.func_type)
	if node.paramlist is not None:
		#if p == "-p": print(node.id+ "(", end="")
		print_ast += node.id+"("
		for func in symbol_table:
			if func.function_name == node.id:
				print("error: redefinition of '%s'"%(node.id))
				exit()
		symbol_table.append(scope(function_name = node.id, isfunction = True))
		symbol_table[-1].function_type = dec_type
		Paramlist_dfs(node.paramlist)
		#if p == "-p": print(")", end="")
		print_ast += ")"
		Compoundstmt_dfs(node.compoundstmt, node.id, False)
	else:
		#if p == "-p": print(node.id+ "()")
		print_ast += node.id+"()\n"
		for func in symbol_table:
			if func.function_name == node.id:
				print("error: redefinition of '%s'"%(node.id))
				exit()
		symbol_table.append(scope(function_name = node.id, isfunction = True))
		symbol_table[-1].function_type = dec_type
		Compoundstmt_dfs(node.compoundstmt, node.id, False)

def Paramlist_dfs(node):
	global print_ast
	symbol_table[-1].paramNum = symbol_table[-1].paramNum+1
	if node.paramlist is not None:
		Paramlist_dfs(node.paramlist)
		#if p == "-p": print(",", end = "")
		print_ast += ","
	dec_type = Type_dfs(node.param_type)
	isparam = True
	identifier_dfs(node.identifier, dec_type, isparam)


def Type_dfs(node):
	global print_ast
	if node.Type_type == "int":
		#if p == "-p": print("int ", end = "")
		print_ast += "int "
		return "int"
	elif node.Type_type == "float":
		#if p == "-p": print("float ", end = "")
		print_ast += "float "
		return "float"
	else:
		pass

def Compoundstmt_dfs(node, function_name, beforecmpd):
	global print_ast
	function_name2 = function_name
	if(beforecmpd):
		fd = lookup_fname(function_name+" compound")
		symbol_table.append(scope(function_name = function_name+ " compound(%d)"%(fd)))
		function_name2 = function_name+ " compound(%d)"%(fd)
	if node.decllist is not None:
		#if p == "-p": print("{")
		print_ast += "{\n"
		Decllist_dfs(node.decllist)
		Stmtlist_dfs(node.stmtlist, function_name2, True)
		#if p == "-p": print("}")
		print_ast += "}\n"
	else:
		#if p == "-p": print("{")
		print_ast += "{\n"
		Stmtlist_dfs(node.stmtlist, function_name2, True)
		#if p == "-p": print("}")
		print_ast += "}\n"

def Stmtlist_dfs(node, function_name, beforecmpd):
	global print_ast
	if node.stmt is not None and node.stmtlist is not None:
		Stmt_dfs(node.stmt, function_name, beforecmpd)
		Stmtlist_dfs(node.stmtlist, function_name, beforecmpd)
	elif node.stmt is None and node.stmtlist is None:
		pass

def Stmt_dfs(node, function_name, beforecmpd):
	global print_ast
	if type (node.stmt) == str:
		#if p == "-p": print(";")
		print_ast += ";\n"
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
		#if p == "-p": print(";")
		print_ast += ";\n"
		pass

def Assignstmt_dfs(node):
	global print_ast
	Assign_dfs(node.assign)
	#if p == "-p": print(";")
	print_ast += ";\n"

def Assign_dfs(node):
	global print_ast
	if node.expr2 is None:
		#if p == "-p": print(node.id+ "=", end = " ")
		print_ast += node.id+"= "
		sym = lookup_st(node.id,False, False)
		id_type = sym.type
		ret = Expr_dfs(node.expr1, assign = sym) 
			
	else:	
		#if p == "-p": print(node.id+ "[", end = " ")
		print_ast += node.id+"["
		sym = lookup_st(node.id,False, True)
		id_type = sym.type
		id_num = sym.array
		idx_num = Expr_dfs(node.expr1)
		if type(idx_num) == symbol:
			pass
		elif idx_num > int(sym.array):
			print("warning: array index %d is past the end of the array"%(idx_num))	
		elif type(idx_num) == int and idx_num < 0:
			print("warning: array index %d is before the beginning of the array"%(idx_num))
		#if p == "-p": print("]=", end = " ")
		print_ast += "]= "
		ret = Expr_dfs(node.expr2, assign = sym)

def Callstmt_dfs(node):
	global print_ast
	Call_dfs(node.call)
	#if p == "-p": print(";")
	print_ast += ";\n"

def Call_dfs(node):
	global print_ast
	if node.arglist is None:
		lookup_call(node.id,0)	
		#if p == "-p": print(node.id+"()", end ="")
		print_ast += node.id+"()"	
		pass
	else:
		#if p == "-p": print(node.id+ "(", end="")
		print_ast += node.id+"("
		argNum = Arglist_dfs(node.arglist, 0)
		lookup_call(node.id, argNum)
		#if p == "-p": print(")", end="")
		print_ast += ")"

def Retstmt_dfs(node):
	global print_ast
	idx= -1
	while(symbol_table[idx].isfunction == False):
		idx = idx -1
	if node.expr is None:
		if symbol_table[idx].function_type != None:
			print("non-void function '%s' should return a value"%(symbol_table[idx].function_name))
			exit()
		#if p == "-p": print("return;")
		print_ast += "return \n"
		pass
	else:
		#if p == "-p": print("return", end =" ")
		print_ast += "return "
		ret = Expr_dfs(node.expr, ret = symbol_table[idx])
		#if p == "-p": print(";")
		print_ast += ";\n "

def Whilestmt_dfs(node, function_name):
	global print_ast
	function_name = function_name + " while"
	fd = lookup_fname(function_name)
	symbol_table.append(scope(function_name = function_name+ "(%d)"%(fd)))

	if node.isDowhile is True:
		#if p == "-p": print("do ", end ="")
		print_ast += "do "
		Stmt_dfs(node.stmt, function_name+"(%d)"%(fd), False)
		#if p == "-p": print("while (", end = "")
		print_ast += "while ("
		Expr_dfs(node.expr)
		#if p == "-p": print(");")
		print_ast += ");\n "
	else:
		#if p == "-p": print("while (", end = "")
		print_ast += "while ("
		Expr_dfs(node.expr)
		#if p == "-p": print(") ", end= "")
		print_ast += ") "
		Stmt_dfs(node.stmt, function_name+"(%d)"%(fd), False)

def Forstmt_dfs(node, function_name):
	global print_ast
	#if p == "-p": print("for( ", end ="")
	print_ast += "for( "
	Assign_dfs(node.assign1)
	#if p == "-p": print("; ", end="")
	print_ast += "; "
	Expr_dfs(node.expr)
	#if p == "-p": print("; ", end="")
	print_ast += "; "
	Assign_dfs(node.assign2)
	#if p == "-p": print(")")
	print_ast += ")\n"
	function_name = function_name + " for"
	fd = lookup_fname(function_name)
	symbol_table.append(scope(function_name = function_name+ "(%d)"%(fd)))

	Stmt_dfs(node.stmt, function_name+"(%d)"%(fd), False)

def Ifstmt_dfs(node, function_name):
	global print_ast
	#if p == "-p": print("if ( ", end ="")
	print_ast += "if ( "
	Expr_dfs(node.expr)
	#if p == "-p": print(")")
	print_ast += ")\n"
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
	global print_ast
	#if p == "-p": print("swtich (", end ="")
	print_ast += "switch ("
	if node.identifier.intnum == None:
		identifier_dfs(node.identifier, None,False)
	else:
		identifier_dfs(node.identifier, None,False, True)
	#if p == "-p": print("){", end="")
	print_ast += "){"
	Caselist_dfs(node.caselist, function_name)
	#if p == "-p": print("}")
	print_ast += "}\n"

def Caselist_dfs(node, function_name):
	global print_ast
	if node.casestmt is not None and node.caselist is not None:
		Casestmt_dfs(node.casestmt, function_name)
		Caselist_dfs(node.caselist, function_name)
	if node.defaultstmt is not None:
		Defaultstmt_dfs(node.defaultstmt, function_name)

def Casestmt_dfs(node, function_name):
	global print_ast
	#if p == "-p": print("case ", node.intnum, ":", end =" ")
	print_ast += "case "+node.intnum+" : "
	function_name = function_name+" case"+ node.intnum
	fd = lookup_fname(function_name)
	symbol_table.append(scope(function_name = function_name+ "(%d)"%(fd)))
	Stmtlist_dfs(node.stmtlist, function_name+"(%d)"%(fd), True)
	if node.isbreak:
		#if p == "-p": print("break;")
		print_ast += "break;\n "
		pass
	else:
		pass

def Defaultstmt_dfs(node, function_name):
	global print_ast
	#if p == "-p": print("default :", end ="")
	print_ast += "default :"
	function_name = function_name + " default"
	fd = lookup_fname(function_name)
	symbol_table.append(scope(function_name = function_name+ "(%d)"%(fd)))
	Stmtlist_dfs(node.stmtlist, function_name+"(%d)"%(fd),False)
	if node.isbreak:
		#if p == "-p": print("break;")
		print_ast += "break;\n "
		pass
	else:
		pass

def Expr_dfs(node, isArray = False, isNegative = False, assign = None, ret = None):
	global print_ast
	if type(node) == str:
		if assign != None:
			if assign.type == "int" and type(lookup_st(node, False,isArray)) ==float:
				print("warning: implicit conversion from '%s' to '%s' changes value in '%s'"%("int", "float", assign.id))
				node = node.split(".")[0]
		if ret != None:
			if ret.function_type == "int" and type(lookup_st(node, False,isArray)) ==float:
				print("warning: implicit conversion from '%s' to '%s' changes value in '%s'"%("int", "float", ret.function_name))
				node = node.split(".")[0]	
		#if p == "-p": print(node, end =" ")
		print_ast += node
		#check_type = type(lookup_st(node, False,isArray))
		return lookup_st(node, False,isArray)
	elif type(node.expr) == str:
		check = Expr_dfs(node.expr, isArray,isNegative,assign, ret)
		if isNegative and (type(check) ==int or type(check) == float) :
			return check *(-1)
		else:
			return check
	else:
		if node.id_expr is None:
			if node.expr.type == "unop":
				return Unop_dfs(node.expr, True, assign, ret)
			elif node.expr.type == "bioperaion":
				Binop_dfs(node.expr)
			elif node.expr.type == "call":
				Call_dfs(node.expr)
			elif node.isPAREN:
				#if p == "-p": print("(", end ="")
				print_ast += "("
				Expr_dfs(node.expr)
				#if p == "-p": print(")", end="")
				print_ast += ")"
		else:
			Expr_dfs(node.id_expr, True)
			#if p == "-p": print("[", end ="")
			print_ast += "["
			Expr_dfs(node.expr)
			#if p == "-p": print("]", end="")
			print_ast += "]"


def Unop_dfs(node, isNegative = True, assign = None, ret = None):
	global print_ast
	#if p == "-p": print("-", end="")
	print_ast += "-"
	return Expr_dfs(node.value, isNegative = True, assign = assign, ret = ret)

def Binop_dfs(node):
	global print_ast
	Expr_dfs(node.left)
	#if p == "-p": print(node.op, end =" ")
	print_ast += node.op + " "
	Expr_dfs(node.right)

def Arglist_dfs(node, argNum):
	global print_ast
	argNum = argNum +1
	if node.arglist is None:
		Expr_dfs(node.expr)
	else:
		argNum = Arglist_dfs(node.arglist, argNum)
		#if p == "-p": print(",", end=" ")
		print_ast += ","
		Expr_dfs(node.expr)
	return argNum


def lookup_funcName(s):
	super_funcName = s.rsplit(" ",1)[0]
	for scope in symbol_table:
		if scope.function_name == super_funcName:
			return scope

def lookup_st(p, isRedecla, isArray=False):
	try:
		try:
			int(p)
			return int(p)
		except:
			float(p)
			return float(p)
	except:
		if isRedecla == False:
			func_scope = symbol_table[-1]
			while(func_scope.isfunction == False):
				l = func_scope.symbols
				for i in l:
					if p == i.id:
						if (isArray ==True and i.array !=None) or (isArray == False and i.array == None):
							i.isused = True
							return i
						else:
							print("error: '%s' subscripted value is not an array, pointer, or vector"%(p))
							exit()
				func_scope = lookup_funcName(func_scope.function_name)

			if func_scope.isfunction == True:
				l = func_scope.symbols
				for i in l:
					if p == i.id:
						if (isArray ==True and i.array !=None) or (isArray == False and i.array == None):
							i.isused = True
							return i
						else:
							print("error: '%s' subscripted value is not an array, pointer, or vector"%(p))
							exit()	
			if symbol_table[0].function_name == "0global":
				func_scope = symbol_table[0]
				l = func_scope.symbols
				for i in l:
					if p == i.id:
						if (isArray==True and i.array !=None) or (isArray == False and i.array == None):
							i.isused = True
							return i
						else:
							print("error: '%s' subscripted value is not an array, pointer, or vector"%(p))
							exit()

			print("error: '%s' no declaration in any scope\n"%(p))
			exit()
		else:
			l = symbol_table[-1].symbols
			for i in l:
				if p == i.id:
					print("error: redefinitio of '%s' \n"%(p))
					exit()
			else:
				return "id"


def lookup_call(p, argNum):
	for i in symbol_table:
		if i.function_name == p:
			if i.paramNum == argNum:
				return
			elif i.paramNum < argNum:
				print("error: too many arguments to function call, expected %d, have %d"%(i.paramNum, argNum))
				exit()
			else:
				print("error: too few arguments to function call, expected %d, have %d"%(i.paramNum, argNum))
				exit()
	print("error: '%s' no function declaration"%(p))
	exit()
def print_unused():
	for s in symbol_table:
		for sym in s.symbols:
			if sym.isused == False:
				print("warning: '%s' expression result unused in function '%s'"%(sym.id, s.function_name))

def print_st():
	for s in symbol_table:
		print("func name : %s // func type : %s // is_func : %s // paramNum %d "%(s.function_name, s.function_type, s.isfunction, s.paramNum))
		for l in s.symbols:
			print(l.type,"\t",l.id,"\t",l.array,"\t",l.role)
		print()

	
