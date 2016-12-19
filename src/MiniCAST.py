import llvmlite.ir as ll
import llvmlite.binding as llvm

class MiniCBaseAST(object):
   def __init__(self):
      pass

   def codeGenerate(self):
      pass

class FunctionAST(MiniCBaseAST):
   def __init__(self, **kwargs):
      self.name = kwargs['name']
      self.function_type = kwargs['function_type']
      self.args_types = kwargs['args_types']
      if self.args_types is None: 
         self.args_types = []
      self.bb_lists = []

   def codeGenerate(self, module):
      rtn_type = self.function_type.codeGenerate()
      ftype = ll.FunctionType(rtn_type, self.args_types)
      function = ll.Function(module, ftype, self.name)
      return module

class ParamsAST(MiniCBaseAST):
   def __init__(self):
      self.param_asts = []

   def codeGenerate(self):
      llvm_asts = []
      for param in self.param_asts:
         llvm_asts.append(param.codeGenerate())
      return llvm_asts
class ParamAST(MiniCBaseAST):
   def __init__(self, **kwargs):
      self.param_type = kwargs['type']
      self.name = kwargs['name']
      self.is_array = False
      if 'is_array' in kwargs:
         self.is_array = kwargs['is_array']

   def codeGenerate(self):
      print self.param_type
      if self.param_type == 'int':
         return ll.IntType(32)

class TypeSpecAST(MiniCBaseAST):
   def __init__(self, **kwargs):
      self.type = kwargs['type_spec']
   
   def codeGenerate(self):
      if self.type == "int":
         return ll.IntType(32)
      if self.type == "void":
         return ll.VoidType()

class ProgramAST(MiniCBaseAST):
   def __init__(self):
      self.asts = []

   def codeGenerate(self):
      module = ll.Module()
      for ast in self.asts:
         module = ast.codeGenerate(module)
      strmod = str(module)
      return strmod;
