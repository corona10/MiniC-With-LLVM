import llvmlite.ir as ll
import llvmlite.binding as llvm

function_set = {}

def int32(value):
   return ll.Constant(ll.IntType(32),value)

class MiniCBaseAST(object):
   def __init__(self):
      pass

   def codeGenerate(self):
      pass

class GlobalAST(MiniCBaseAST):
   def __init__(self,**kwargs):
      self.name = kwargs['name']
      self.type = kwargs['type']
      self.is_array = False
      self.value = None
      if 'is_array' in kwargs:
          self.is_array = kwargs['is_array']
      if 'value' in kwargs:
          self.value = kwargs['value']
      if self.is_array == True:
          self.size = kwargs['size']

   def codeGenerate(self, module,var_ptr_symbolTBL):
       if self.is_array == False:
           ty = self.type.codeGenerate()
           gv = ll.GlobalVariable(module,ty,self.name)
           if self.value != None:
               gv.initializer = int32(self.value)
       else:
           ty = ll.ArrayType(ll.IntType(32), self.size)
           gv = ll.GlobalVariable(module, ty, self.name)
           gv.initializer = ll.Constant(ll.ArrayType(ll.IntType(32), self.size), None)
       var_ptr_symbolTBL[self.name] = gv
           
       return module  

class LocalDeclAST(MiniCBaseAST):
   def __init__(self,**kwargs):
      self.name = kwargs['name']
      self.type = kwargs['type']
      self.is_array = False
      self.value = None
      if 'is_array' in kwargs:
          self.is_array = kwargs['is_array']
      if 'value' in kwargs:
          self.value = kwargs['value']
      if self.is_array == True:
          self.size = kwargs['size']

   def codeGenerate(self, builder, var_ptr_symbolTBL):
       if self.is_array == False:
           ty = self.type.codeGenerate()
           decl = builder.alloca(ll.IntType(32), name=self.name)
           if self.value != None:
               builder.store(ll.Constant(decl.type.pointee, self.value), decl)
       else:
           ty = ll.ArrayType(ll.IntType(32), self.size)
           decl = builder.alloca(ty, name=self.name)
       var_ptr_symbolTBL[self.name] = decl
       return builder

class FunctionAST(MiniCBaseAST):
   def __init__(self, **kwargs):
      self.name = kwargs['name']
      self.function_type = kwargs['function_type']
      self.args_types = kwargs['args_types']
      self.compound_stmt = kwargs['compound_stmt']
      if 'args_names' in kwargs:
         self.args_names = kwargs['args_names']
      else:
         self.args_names = None

      if self.args_types is None: 
         self.args_types = []
      self.bb_lists = []

   def codeGenerate(self, module,var_ptr_symbolTBL):
      rtn_type = self.function_type.codeGenerate()
      ftype = ll.FunctionType(rtn_type, self.args_types)
      function = ll.Function(module, ftype, self.name)
      function_set[self.name] = function
      if self.args_names is not None:
         for idx in range(len(self.args_names)):
            function.args[idx].name = self.args_names[idx]
            function.args[idx].type = self.args_types[idx]
      self.compound_stmt.function = function
      self.compound_stmt.codeGenerate(var_ptr_symbolTBL)
      return module

   def pushAST(self, ast):
      ast.codeGenerate()

class ParamsAST(MiniCBaseAST):
   def __init__(self):
      self.param_asts = []

   def codeGenerate(self):
      llvm_asts = []
      param_names = []
      for param in self.param_asts:
         args_type, args_name = param.codeGenerate()
         llvm_asts.append(args_type)
         param_names.append(args_name)
      return llvm_asts, param_names

class ParamAST(MiniCBaseAST):
   def __init__(self, **kwargs):
      self.param_type = kwargs['type']
      self.name = kwargs['name']
      self.is_array = False
      if 'is_array' in kwargs:
         self.is_array = kwargs['is_array']

   def codeGenerate(self):
      if self.param_type == 'int':
         return ll.IntType(32), self.name

class TypeSpecAST(MiniCBaseAST):
   def __init__(self, **kwargs):
      self.type = kwargs['type_spec']
   
   def codeGenerate(self):
      if self.type == "int":
         return ll.IntType(32)
      if self.type == "void":
         return ll.VoidType()

class CompoundAST(MiniCBaseAST):
   def __init__(self, **kwargs):
      self.name = kwargs['name']
      self.ast_list = []
      self.hasRet = False

   def codeGenerate(self,var_ptr_symbolTBL):
      builder = ll.IRBuilder(self.function.append_basic_block(self.name))
      if self.function.args is not None:
         for idx in range(len(self.function.args)):
            ptr = builder.alloca(self.function.args[idx].type,name=self.function.args[idx].name)
            var_ptr_symbolTBL[self.function.args[idx].name] = ptr
      for ast in self.ast_list:
         ast.codeGenerate(builder,var_ptr_symbolTBL)

   def pushAST(self, ast):
      self.ast_list.append(ast)

   def sethasRet(self,hasRet):
      self.hasRet = hasRet

class ReturnAST(MiniCBaseAST):
   def __init__(self, **kwargs):
      if "value" in kwargs:
         self.value = kwargs['value']
      else:
         self.value = None
   
   def codeGenerate(self, builder,var_ptr_symbolTBL):
      if self.value == None:
         builder.ret_void()
      else:
         #const_1 = ll.Constant(ll.IntType(32),0);
         if super(type(self.value)) ==  MiniCBaseAST:
             load = self.value.codeGenerate(builder,var_ptr_symbolTBL)
         else:
             load = self.value.codeGenerate(builder,var_ptr_symbolTBL) 
         rvalue = load
         builder.ret(rvalue)
   
class ProgramAST(MiniCBaseAST):
   def __init__(self):
      self.asts = []

   def codeGenerate(self,var_ptr_symbolTBL):
      module = ll.Module()
      module.triple = llvm.get_default_triple()
      for ast in self.asts:
         module = ast.codeGenerate(module, var_ptr_symbolTBL)
      strmod = str(module)
      return strmod;

class AssignAST(MiniCBaseAST):
   def __init__(self, **kwargs):
      self.s1 = kwargs['s1']
      self.op = kwargs['op']
      self.s2 = kwargs['s2']

   def codeGenerate(self,builder,var_ptr_symbolTBL):
      if self.op == "=":
         s2_load = self.s2.codeGenerate(builder,var_ptr_symbolTBL)
         s1_ptr = var_ptr_symbolTBL[self.s1]
         A =  builder.store(s2_load,s1_ptr) 

class FunctionCallAST(MiniCBaseAST):

   def __init__(self, **kwargs):
      self.IDENT = kwargs['IDENT']
      self.args = kwargs['args']

   def codeGenerate(self,builder,var_symbolTBL):
      args = []
      for arg in self.args:
          args.append(arg.codeGenerate(builder, var_symbolTBL))
      return builder.call(function_set[self.IDENT], tuple(args))


class BinaryAST(MiniCBaseAST):

   def __init__(self, **kwargs):
      self.s1 = kwargs['s1']
      self.op = kwargs['op']
      self.s2 = kwargs['s2']

   def codeGenerate(self,builder,var_ptr_symbolTBL):
      s1_load = self.s1.codeGenerate(builder,var_ptr_symbolTBL)
      s2_load = self.s2.codeGenerate(builder,var_ptr_symbolTBL)
      if self.op == "+":
         return builder.add(s1_load,s2_load)
      elif self.op == "-":
         return builder.sub(s1_load,s2_load)
      elif self.op == "*":
         return builder.mul(s1_load,s2_load)
      elif self.op == "/":
         return builder.sdiv(s1_load,s2_load)
      elif self.op == "%":
         return builder.srem(s1_load,s2_load)
      elif self.op == "and":
         return builder.and_(s1_load,s2_load)
      elif self.op == "or":
         return builder.or_(s1_load,s2_load)
      else:
         return builder.icmp_signed(cmpop=self.op, lhs=s1_load, rhs=s2_load )
      


class UnaryAST(MiniCBaseAST):

   def __init__(self,**kwargs):
      self.op = kwargs['op']
      self.s1= kwargs['s1']

   def codeGenerate(self, builder,var_ptr_symbolTBL):
      s1 = self.s1.codeGenerate(builder, var_ptr_symbolTBL)
      s1_ptr = var_ptr_symbolTBL[self.s1.value]
      if self.op == '++':
         builder.store(builder.add(s1, ll.Constant(ll.IntType(32),1)),s1_ptr)
      elif self.op == '--':
         builder.store(builder.sub(s1, ll.Constant(ll.IntType(32),1)),s1_ptr)
      elif self.op == '+':
         builder.load(s1)
      elif self.op == '-':
         builder.neg(s1)
        
class LiteralAST(MiniCBaseAST):

   def __init__(self,**kwargs):
      self.value = kwargs['value']

   def codeGenerate(self, builder,var_ptr_symbolTBL):
      return int32(self.value)
        
class IdentAST(MiniCBaseAST):

   def __init__(self,**kwargs):
      self.value = kwargs['value']

   def codeGenerate(self, builder,var_ptr_symbolTBL):
      return builder.load(var_ptr_symbolTBL[self.value])


class ArrayAST(MiniCBaseAST):
   def __init__(self, **kwargs):
      self.IDENT = kwargs['IDENT']
      self.expr = kwargs['expr']

   def codeGenerate(self, builder, var_ptr_symbolTBL):
      s1_ptr = var_ptr_symbolTBL[self.IDENT]
      idx = self.expr.codeGenerate(builder,var_ptr_symbolTBL)
      bgep = builder.gep(s1_ptr, [ll.Constant(ll.IntType(32),0),idx], inbounds=False)
      return builder.load(bgep)
      #return builder.extract_value(s1_ptr,self.expr.value)

class ArrayAssignAST(MiniCBaseAST):

   def __init__(self, **kwargs):
      self.IDENT = kwargs['IDENT']
      self.idx= kwargs['idx']
      self.value = kwargs['value']

   def codeGenerate(self, builder, var_ptr_symbolTBL):
      s1_ptr = var_ptr_symbolTBL[self.IDENT]
      s1_load = self.value.codeGenerate(builder,var_ptr_symbolTBL)
      idx = self.idx.codeGenerate(builder,var_ptr_symbolTBL)
      bgep = builder.gep(s1_ptr, [ll.Constant(ll.IntType(32),0),idx], inbounds=False)
      builder.store(s1_load, bgep)


