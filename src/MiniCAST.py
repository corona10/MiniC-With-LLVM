import llvmlite.ir as ll
import llvmlite.binding as llvm

class MiniCBaseAST(object):
   def __init__(self):
      pass

   def codeGenerate(self):
      pass

class GloabalAST(MiniCBaseAST):
   def __init__(self,**kwargs):
      self.name = kargs['name']
      self.type = kwargs['type']
      self.is_array = False
      if 'is_array' in kwargs:
          self.is_array = kwargs['is_array']
      if self.is_array == True:
          self.value = kwargs['value']
      else:
          self.value = kwargs['value']

   def codeGenerate(self, module):
       ty = self.type.codeGenerate()
       ll.GloabalVariable(module,ty,self.name)
       return module  
       #gv = ll.GloabalVariable(module,typ,self.name)
       #return gv
      

class FunctionAST(MiniCBaseAST):
   def __init__(self, **kwargs):
      self.name = kwargs['name']
      self.function_type = kwargs['function_type']
      self.args_types = kwargs['args_types']
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

      return module

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
      print self.param_type
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

class ProgramAST(MiniCBaseAST):
   def __init__(self):
      self.asts = []

   def codeGenerate(self):
      module = ll.Module()
      for ast in self.asts:
         module = ast.codeGenerate(module)
      strmod = str(module)
      return strmod;
