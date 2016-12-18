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
      self.bb_lists = []

   def codeGenerate(self, module):
      rtn_type = self.function_type.codeGenerate()
      ftype = ll.FunctionType(rtn_type, [])
      function = ll.Function(module, ftype, self.name)
      return module

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
