import llvmlite.ir as ll
import llvmlite.binding as llvm


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

   def codeGenerate(self, module):
       if self.is_array == False:
           ty = self.type.codeGenerate()
           gv = ll.GlobalVariable(module,ty,self.name)
           if self.value != None:
               gv.initializer = int32(self.value)
       else:
           ty = ll.ArrayType(ll.IntType(32), self.size)
           gv = ll.GlobalVariable(module, ty, self.name)
           
       return module  

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

   def codeGenerate(self, module):
      rtn_type = self.function_type.codeGenerate()
      ftype = ll.FunctionType(rtn_type, self.args_types)
      function = ll.Function(module, ftype, self.name)
      if self.args_names is not None:
         for idx in range(len(self.args_names)):
            function.args[idx].name = self.args_names[idx]
      self.compound_stmt.function = function
      self.compound_stmt.codeGenerate()
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

   def codeGenerate(self):
      builder = ll.IRBuilder(self.function.append_basic_block(self.name))
      for ast in self.ast_list:
         ast.codeGenerate(builder)

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
   
   def codeGenerate(self, builder):
      if self.value == None:
         builder.ret_void()
      else:
         const_1 = ll.Constant(ll.IntType(32),1);
         builder.ret(const_1)
   
class ProgramAST(MiniCBaseAST):
   def __init__(self):
      self.asts = []

   def codeGenerate(self):
      module = ll.Module()
      for ast in self.asts:
         module = ast.codeGenerate(module)
      strmod = str(module)
      return strmod;
