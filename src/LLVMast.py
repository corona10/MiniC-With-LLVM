

class AST(object):

   def codegen(self):
      pass


class ProgramAST(self):
   
   def __init__(self):
      self.ast_list = []

   def codegen(self):
      moudle = llvm_modue()
      for ast in ast_list:
         ir = ast.codegen()
         module.append(ir)
      strmod = str(module)
      llmod = llvm.parse_assembly(strmod) # ir
      pmb = llvm.create_pass_manager_builder()
      pmb.opt_level = 2
      pm = llvm.create_module_pass_manager()
      pmb.populate(pm)  # asm
      pm.run(llmod)

class IdentAST(AST):

   def __init_(self, tp, value):
       if tp is "int":
         self.ir_val = builder.phi(ll.IntType(32))
   def codegen(self):
     return self.ir_val

class ExprAST(AST):
   def __init__(self, lhs, rhs):
      self.lhs = lhs;
      self.rhs = rhs;
   def codegen(self):
      if self.type == "binary":
        l = lhs.codegen(); # llvm value
        r = rhs.codegen();
        return builder.add(l, r)

class Function(AST):
   
    def __init__(self):
       self.bb_list = []

    def push_bb(self, bb):
       self.bb_list.append(bb)

    def codgen(self):
       for bb in bb_list:
          builder.position_at_end(bb)
      
       return 


