name_table = {}

## function name and frequnecy
def lookup_fname(function_name):
	try:
		name_table[function_name] = name_table[function_name]+1
		return name_table[function_name]
	except KeyError:
		name_table[function_name] = 1
		return 1

def Program_dfs(node, pw):
	global p
	p = pw
	name_table.clear()
	if node.second_list is not None and node.first_list is not None:
		if p == "-s" : print("Function name : Global")
		Decllist_dfs(node.first_list)
		Funclist_dfs(node.second_list)
	elif node.first_list is not None:
		if node.first_list.type == "decllist":
			if p == "-s" :  print("Function name : Global")
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
		if p == "-s" :  print(dec_type, "\t", end="")
		if node.intnum is not None:
			if p == "-s" :  print(node.id, "\t", node.intnum,"\t", "parameter" if isparam else "variable")
			if p == "-p": print(node.id+ "["+ node.intnum+ "]", end ="")
		else:
			if p == "-s" : print(node.id, "\t", "\t",  "parameter" if isparam else "variable")
			if p == "-p": print(node.id, end = "")

def Function_dfs(node):
	if node.paramlist is not None:
		Type_dfs(node.func_type)
		if p == "-p": print(node.id+ "(", end="")
		if p == "-s" : print("Function name :", node.id)
		Paramlist_dfs(node.paramlist)
		if p == "-p": print(")", end="")
		Compoundstmt_dfs(node.compoundstmt, node.id, False)
	else:
		Type_dfs(node.func_type)
		if p == "-p": print(node.id+ "()")
		if p == "-s" : print("Function name :", node.id)
		Compoundstmt_dfs(node.compoundstmt, node.id, False)

def Paramlist_dfs(node):
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
		if p == "-s" : print("Function name :", function_name+ " compound(%d)"%(fd))
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
		if p == "-p": print(node.id+ "=", end = " ")
		Expr_dfs(node.expr1)
	else:
		if p == "-p": print(node.id+ "[", end = " ")
		Expr_dfs(node.expr1)
		if p == "-p": print("]=", end = " ")
		Expr_dfs(node.expr2)

def Callstmt_dfs(node):
	Call_dfs(node.call)
	if p == "-p": print(";")

def Call_dfs(node):
	if node.arglist is None:
		if p == "-p": print(node.id+"()", end ="")
		pass
	else:
		if p == "-p": print(node.id+ "(", end="")
		Arglist_dfs(node.arglist)
		if p == "-p": print(")", end="")

def Retstmt_dfs(node):
	if node.expr is None:
		if p == "-p": print("return;")
		pass
	else:
		if p == "-p": print("return", end =" ")
		Expr_dfs(node.expr)
		if p == "-p": print(";")

def Whilestmt_dfs(node, function_name):
	function_name = function_name + " while"
	fd = lookup_fname(function_name)
	if p == "-s" : print("Function name :", function_name+"(%d)"%(fd))
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
	if p == "-s" : print("Function name :", function_name+"(%d)"%(fd))
	Stmt_dfs(node.stmt, function_name+"(%d)"%(fd), False)

def Ifstmt_dfs(node, function_name):
	if p == "-p": print("if ( ", end ="")
	Expr_dfs(node.expr)
	if p == "-p": print(")")
	function_name2 = function_name+ " if"
	fd = lookup_fname(function_name2)
	if p == "-s" : print("Function name :", function_name2+"(%d)"%(fd))
	Stmt_dfs(node.ifstmt, function_name2+"(%d)"%(fd), False)
	if node.elsestmt is not None:
		function_name3 = function_name+ " else"
		fd = lookup_fname(function_name3)
		if p == "-s" : print("Function name :", function_name3+"(%d)"%(fd))
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
	if p == "-s" : print("Function name :", function_name+"(%d)"%(fd))
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
	if p == "-s" : print("Function name :", function_name+"(%d)"%(fd))
	Stmtlist_dfs(node.stmtlist, function_name+"(%d)"%(fd),False)
	if node.isbreak:
		if p == "-p": print("break;")
		pass
	else:
		pass

def Expr_dfs(node):
	if type(node) == str:
		if p == "-p": print(node, end =" ")
		pass
	elif type(node.expr) == str:
		Expr_dfs(node.expr)
	else:
		if node.id_expr is None:
			if node.expr.type == "unop":
				Unop_dfs(node.expr)
			elif node.expr.type == "bioperaion":
				Binop_dfs(node.expr)
			elif node.expr.type == "call":
				Call_dfs(node.expr)
			elif node.isPAREN:
				if p == "-p": print("(", end ="")
				Expr_dfs(node.expr)
				if p == "-p": print(")", end="")
		else:
			Expr_dfs(node.id_expr)
			if p == "-p": print("[", end ="") 
			Expr_dfs(node.expr)
			if p == "-p": print("]")

def Unop_dfs(node):
	if p == "-p": print("-", end="")
	Expr_dfs(node.value)
	pass

def Binop_dfs(node):
	Expr_dfs(node.left)
	if p == "-p": print(node.op, end =" ")
	Expr_dfs(node.right)

def Arglist_dfs(node):
	if node.arglist is None:
		Expr_dfs(node.expr)
	else:
		Arglist_dfs(node.arglist)
		if p == "-p": print(",", end=" ")
		Expr_dfs(node.expr)
