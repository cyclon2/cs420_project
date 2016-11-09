class leaf : pass

class Float(leaf):
	def __init__(self, value):
		self.type = "float"
		self.value = value
		print(value)

class Int(leaf):
	def __init__(self, value):
		self.type = "int"
		self.value = value
		print(value)

class Plus(leaf):
	def __init__(self):
		self.type = "plus"
		self.value = "+"
		print(self.value)

class Minus(leaf):
	def __init__(self):
		self.type = "minus"
		self.value = "-"
		print(self.value)

class Times(leaf):
	def __init__(self):
		self.type = "time"
		self.value = "*"
		print(self.value)

class Divide(leaf):
	def __init__(self):
		self.type = "divide"
		self.value = "/"
		print(self.value)

class Eq(leaf):
	def __init__(self):
		self.type = "eq"
		self.value = "=="
		print(self.value)

class Le(leaf):
	def __init__(self):
		self.type = "le"
		self.value = "<="
		print(self.value)

class Ge(leaf):
	def __init__(self):
		self.type = "ge"
		self.value = ">="
		print(self.value)

class Ne(leaf):
	def __init__(self):
		self.type = "ne"
		self.value = "!="
		print(self.value)

class Equals(leaf):
	def __init__(self):
		self.type = "equals"
		self.value = "="
		print(self.value)

class Lt(leaf):
	def __init__(self):
		self.type = "lt"
		self.value = "<"
		print(self.value)

class Gt(leaf):
	def __init__(self):
		self.type = "gt"
		self.value = ">"
		print(self.value)

class Comma(leaf):
	def __init__(self):
		self.type = "comma"
		self.value = ","
		print(self.value)

class Semicolon(leaf):
	def __init__(self):
		self.type = "semicolon"
		self.value = ";"
		print(self.value)

class Colon(leaf):
	def __init__(self):
		self.type = "colon"
		self.value = ":"
		print(self.value)

class Lparen(leaf):
	def __init__(self):
		self.type = "lparen"
		self.value = "("
		print(self.value)

class Rparen(leaf):
	def __init__(self):
		self.type = "rparen"
		self.value = ")"
		print(self.value)

class Lbrk(leaf):
	def __init__(self):
		self.type = "lbrk"
		self.value = "["
		print(self.value)

class Rbrk(leaf):
	def __init__(self):
		self.type = "Rbrk"
		self.value = "]"
		print(self.value)

class Rbrace(leaf):
	def __init__(self):
		self.type = "rbrace"
		self.value = "}"
		print(self.value)

class Lbrace(leaf):
	def __init__(self):
		self.type = "Lbrace"
		self.value = "{"
		print(self.value)

class ID(leaf):
	def __init__(self, type,value):
		self.type = type
		self.value = value
		print(self.value)
