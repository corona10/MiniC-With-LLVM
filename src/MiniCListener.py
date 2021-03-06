# Generated from MiniC.g4 by ANTLR 4.5.1
from antlr4 import *
from ctypes import CFUNCTYPE, c_int, POINTER
import copy
import sys
import llvmlite.ir as ll
import llvmlite.binding as llvm
from MiniCAST import *
# This class defines a complete listener for a parse tree produced by MiniCParser.
class MiniCListener(ParseTreeListener):
    def __init__(self):
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()
        self.prop={}
        self.function_name_table = {}
        self.function_symbol_table = {}
        self.var_symbolTBL = {}
        self.var_ptr_symbolTBL = {}
        self.var_ptr_symbolTBL['var_symbolTBL'] = self.var_symbolTBL

        self.tm = llvm.Target.from_default_triple().create_target_machine()

    # Enter a parse tree produced by MiniCParser#program.
    def enterProgram(self, ctx):
        pass

    # Exit a parse tree produced by MiniCParser#program.
    def exitProgram(self, ctx):
        print "* Target cpu: " + llvm.get_host_cpu_name()
        programAst = ProgramAST()
        for child in ctx.getChildren():
            child_ast = self.prop[child]
            programAst.asts.append(child_ast) 
        mod, cfg_list  = programAst.codeGenerate(self.var_ptr_symbolTBL)
        strmod = str(mod)
        print "=== Generated IR code ===\n"
        print strmod
        with open("output.ll", 'w') as f:
            f.write(strmod)
 
        llmod = llvm.parse_assembly(strmod)
        answer = raw_input('* Optimizing this code? (y/n): ')
        if answer.lower() == "y":
            opt = True
        else:
            opt = False

        if opt:
            pm = llvm.create_module_pass_manager()
            pmb = llvm.create_pass_manager_builder()
            pmb.opt_level = 3  # -O3
            pmb.populate(pm)
            # optimize
            pm.run(llmod)
            print "=== Generated optimized IR code ===\n"
            print llmod
            with open("output_opt.ll", 'w') as f:
                f.write(str(llmod))


        llmod.verify()
        with llvm.create_mcjit_compiler(llmod, self.tm) as ee:
            ee.finalize_object()
            print "=== Generated assembly code ===\n"
            print(self.tm.emit_assembly(llmod))
            with open("output.asm", 'w') as f:
                f.write(self.tm.emit_assembly(llmod))
        answer = raw_input('Do you want to create CFG Graph? (y/n) : ')
        if answer.lower() == 'y': 
            for cfg in cfg_list:
                dot = llvm.get_function_cfg(cfg)
                llvm.view_dot_graph(dot ,filename=cfg.name,view = True)

    # Enter a parse tree produced by MiniCParser#decl.
    def enterDecl(self, ctx):
        pass

    # Exit a parse tree produced by MiniCParser#decl.
    def exitDecl(self, ctx):
        ast = self.prop[ctx.getChild(0)]
        if ast is not None:
           self.prop[ctx] = ast

    # Enter a parse tree produced by MiniCParser#var_decl.
    def enterVar_decl(self, ctx):
        pass

    # Exit a parse tree produced by MiniCParser#var_decl.
    def exitVar_decl(self, ctx):
        if ctx.getChildCount() == 3:
            ty = ctx.getChild(0)
            name = ctx.getChild(1).getText()
            type_ast = self.prop[ty]
            global_ast = GlobalAST(name=name,type=type_ast,is_array=False,value=0)
        if ctx.getChildCount() == 5:
            ty = ctx.getChild(0)
            name = ctx.getChild(1).getText()
            type_ast = self.prop[ty]
            value = int(ctx.getChild(3).getText())
            global_ast = GlobalAST(name=name, type=type_ast, is_array=False, value = value)

        if ctx.getChildCount() == 6:
            ty = ctx.getChild(0)
            name = ctx.getChild(1).getText()
            type_ast = self.prop[ty]
            size = int(ctx.getChild(3).getText())
            global_ast = GlobalAST(name=name, type=type_ast, is_array=True, size = size)

        self.prop[ctx] = global_ast

    # Enter a parse tree produced by MiniCParser#type_spec.
    def enterType_spec(self, ctx):
        pass

    # Exit a parse tree produced by MiniCParser#type_spec.
    def exitType_spec(self, ctx):
        type_spec = ctx.getChild(0).getText()
        ast = TypeSpecAST(type_spec= type_spec)
        self.prop[ctx] = ast


    # Enter a parse tree produced by MiniCParser#fun_decl.
    def enterFun_decl(self, ctx):
        func_name = ctx.getChild(1).getText()
        self.function_symbol_table[func_name] = {}
        self.function_name_table[ctx.getChild(3)] = func_name
        self.function_name_table[ctx.getChild(5)] = func_name

    # Exit a parse tree produced by MiniCParser#fun_decl.
    def exitFun_decl(self, ctx):
        ftype = self.prop[ctx.getChild(0)]
        function_name = ctx.getChild(1).getText()
        compound = self.prop[ctx.getChild(5)]
        if len(ctx.getChild(3).getText()) > 0:
           args_ast = self.prop[ctx.getChild(3)]
           args, args_names = args_ast.codeGenerate() 
           ast = FunctionAST(function_type= ftype, name=function_name, args_types = args, args_names = args_names, compound_stmt = compound)
        else:
           ast = FunctionAST(function_type= ftype, name=function_name, args_types = None, compound_stmt = compound)

        if compound.hasRet == False:
           r_ast = ReturnAST()
           ast.pushAST(r_ast)
        self.prop[ctx] = ast


    # Enter a parse tree produced by MiniCParser#params.
    def enterParams(self, ctx):
        pass

    # Exit a parse tree produced by MiniCParser#params.
    def exitParams(self, ctx):
        if ctx.getChildCount() >= 1:
            ast = ParamsAST()
            for i in range(ctx.getChildCount()):
                if (i+1) % 2 != 0:
                    paramAST = self.prop[ctx.getChild(i)]
                    ast.param_asts.append(paramAST)
            self.prop[ctx] = ast

    # Enter a parse tree produced by MiniCParser#param.
    def enterParam(self, ctx):
        pass

    # Exit a parse tree produced by MiniCParser#param.
    def exitParam(self, ctx):
        param_type = ctx.getChild(0).getText()
        param_name = ctx.getChild(1).getText()
        if ctx.getChildCount() == 2:
           ast = ParamAST(type=param_type, name = param_name)
        else:
           ast = ParamAST(type=param_type, name = param_name, is_array=True)
        self.add_var(param_name,ast)
        self.prop[ctx] = ast


    # Enter a parse tree produced by MiniCParser#stmt.
    def enterStmt(self, ctx):
        func_name = self.function_name_table[ctx]
        if ctx.getChildCount() > 0:
            for pt in ctx.children:
                self.function_name_table[pt] = func_name

    # Exit a parse tree produced by MiniCParser#stmt.
    def exitStmt(self, ctx):
        
        if ctx.getChild(0) in self.prop:
           ast = self.prop[ctx.getChild(0)]
           self.prop[ctx] = ast


    # Enter a parse tree produced by MiniCParser#expr_stmt.
    def enterExpr_stmt(self, ctx):
        func_name = self.function_name_table[ctx]
        if ctx.getChildCount() > 0:
            for pt in ctx.children:
                self.function_name_table[pt] = func_name


    # Exit a parse tree produced by MiniCParser#expr_stmt.
    def exitExpr_stmt(self, ctx):  
        ast=""
        if ctx.getChildCount() == 2 :
           ast = self.prop[ctx.expr()]
           self.prop[ctx]=ast


    # Enter a parse tree produced by MiniCParser#while_stmt.
    def enterWhile_stmt(self, ctx):
        func_name = self.function_name_table[ctx]
        if ctx.getChildCount() > 0:
            for pt in ctx.children:
                self.function_name_table[pt] = func_name

    # Exit a parse tree produced by MiniCParser#while_stmt.
    def exitWhile_stmt(self, ctx):
        func_name = self.function_name_table[ctx]
        cond = self.prop[ctx.getChild(2)]
        stmt = self.prop[ctx.getChild(4).getChild(0).getChild(1)]
        ast = WhileAST(function_name = func_name , cond=cond, stmt=stmt)
        self.prop[ctx] = ast


    # Enter a parse tree produced by MiniCParser#return_stmt.
    def enterReturn_stmt(self, ctx):
        func_name = self.function_name_table[ctx]
        if ctx.getChildCount() > 0:
            for pt in ctx.children:
                self.function_name_table[pt] = func_name

    # Enter a parse tree produced by MiniCParser#compound_stmt.
    def enterCompound_stmt(self, ctx):
        func_name = self.function_name_table[ctx]
        if ctx.getChildCount() > 0:
            for pt in ctx.children:
                self.function_name_table[pt] = func_name

    # Exit a parse tree produced by MiniCParser#compound_stmt.
    def exitCompound_stmt(self, ctx):
        func_name = self.function_name_table[ctx]
        compoundAST = CompoundAST(name="entry", function_name = func_name)
        self.prop[ctx] = compoundAST
        for stmt in ctx.getChildren():
           if stmt in self.prop:
              compoundAST.pushAST(self.prop[stmt])
        size = ctx.getChildCount()
        ast = self.prop[ctx.getChild(size-2)]
        if type(ast) == ReturnAST:
            compoundAST.sethasRet(True)
       

    # Enter a parse tree produced by MiniCParser#local_decl.
    def enterLocal_decl(self, ctx):
        pass

    def add_var(self,name, ast):
        if name in self.var_symbolTBL.keys():
           self.var_symbolTBL[name].append(ast)
        else:
           self.var_symbolTBL[name] = []
           self.var_symbolTBL[name].append(ast)

    # Exit a parse tree produced by MiniCParser#local_decl.
    def exitLocal_decl(self, ctx):
        if ctx.getChildCount() == 3:
            ty = self.prop[ctx.getChild(0)]
            name = ctx.getChild(1).getText()
            ast = LocalDeclAST(type = ty, name = name)
        if ctx.getChildCount() == 5:
            ty = self.prop[ctx.getChild(0)]
            name = ctx.getChild(1).getText()
            value = int(ctx.getChild(3).getText())
            ast = LocalDeclAST(type=ty, name = name, value = value)
        if ctx.getChildCount() == 6:
            ty = self.prop[ctx.getChild(0)]
            name = ctx.getChild(1).getText()
            size = int(ctx.getChild(3).getText())
            ast = LocalDeclAST(type = ty, name= name, is_array= True, size = size)
        self.add_var(name,ast)
        self.prop[ctx] = ast
        self.function_symbol_table[name] = ast


    # Enter a parse tree produced by MiniCParser#if_stmt.
    def enterIf_stmt(self, ctx):
        func_name = self.function_name_table[ctx]
        if ctx.getChildCount() > 0:
            for pt in ctx.children:
                self.function_name_table[pt] = func_name

    # Exit a parse tree produced by MiniCParser#if_stmt.
    def exitIf_stmt(self, ctx):
        if ctx.getChildCount() == 5:
            func_name = self.function_name_table[ctx]
            cond = self.prop[ctx.getChild(2)]
            stmt = self.prop[ctx.getChild(4)]
            ast = IfAST(function_name = func_name, cond=cond, stmt = stmt)
        else:
            func_name = self.function_name_table[ctx]
            cond = self.prop[ctx.getChild(2)]
            stmt = self.prop[ctx.getChild(4)]
            elstmt = self.prop[ctx.getChild(6)]
            ast = IfAST(function_name = func_name , cond=cond, stmt=stmt, else_stmt = elstmt)
        self.prop[ctx] = ast


    # Enter a parse tree produced by MiniCParser#return_stmt.
    def enterReturn_stmt(self, ctx):
        func_name = self.function_name_table[ctx]
        if ctx.getChildCount() > 0:
            for pt in ctx.children:
                self.function_name_table[pt] = func_name


    # Exit a parse tree produced by MiniCParser#return_stmt.
    def exitReturn_stmt(self, ctx):
        if ctx.getChildCount() == 2:
            rtn_ast = ReturnAST()
        else:
            rtn_ast = ReturnAST(value=self.prop[ctx.getChild(1)])
        self.prop[ctx] = rtn_ast

    # Enter a parse tree produced by MiniCParser#expr.
    def enterExpr(self, ctx):
        func_name = self.function_name_table[ctx]
        if ctx.getChildCount() > 0:
            for pt in ctx.children:
                self.function_name_table[pt] = func_name

    # Exit a parse tree produced by MiniCParser#expr.
    def exitExpr(self, ctx):
        if ctx.getChildCount() > 0:
            if ctx.getChildCount() == 1:
                if ctx.getChild(0) == ctx.LITERAL():
                   expr=ctx.getChild(0).getText()
                   ast=LiteralAST(value = expr)
                elif ctx.getChild(0) == ctx.IDENT():
                   expr=ctx.getChild(0).getText()
                   ast=IdentAST(value=expr)
            elif ctx.getChildCount() == 2:
                op = ctx.getChild(0).getText()
                s1=self.prop[ctx.expr(0)]
                ast= UnaryAST(op=op,s1=s1)
            elif ctx.getChildCount() == 3:
                if ctx.getChild(0).getText() == "(":
                    expr=self.prop[ctx.expr(0)]
                    ast = expr
                elif ctx.getChild(1).getText() == "=":
                    s1 = ctx.getChild(0).getText()
                    op = ctx.getChild(1).getText()
                    s2 = self.prop[ctx.expr(0)]
                    ast = AssignAST(s1=s1,op=op,s2=s2)
                    self.add_var(s1,s2)
                else: #Binary
                    s1 = self.prop[ctx.expr(0)]
                    op = ctx.getChild(1).getText()
                    s2 = self.prop[ctx.expr(1)]
                    ast = BinaryAST(s1=s1,op=op,s2=s2)
                                 
            elif ctx.getChildCount() == 4:
                #IDNET(args) or IDENT[args]
                IDENT=ctx.getChild(0).getText()
                if ctx.args() is not None:
                    f=ctx.getChild(1).getText()
                    kwargs={}
                    if f == "(":
                        args=self.prop[ctx.args()]
                        ast = FunctionCallAST(IDENT=IDENT, args=args) 
                    if f == "[":
                        expr = self.prop[ctx.args()]
                        ast = ArrayAST(IDENT=IDENT,expr=expr) 
                else:
                    expr=self.prop[ctx.expr(0)]
		    ast = ArrayAST(IDENT=IDENT,expr=expr) 
            else:
                #IDENT[expr] = expr
                IDENT = ctx.getChild(0).getText()
                lb = ctx.getChild(1).getText()
                idx = self.prop[ctx.expr(0)]
                rb = ctx.getChild(3).getText()
                assign = ctx.getChild(4).getText()
                value = self.prop[ctx.expr(1)]
                if lb == "[" and assign == "=":
                   ast = ArrayAssignAST(IDENT=IDENT,idx=idx,value=value)
                
            self.prop[ctx]=ast


    # Enter a parse tree produced by MiniCParser#args.
    def enterArgs(self, ctx):
        func_name = self.function_name_table[ctx]
        if ctx.getChildCount() > 0:
            for pt in ctx.children:
                self.function_name_table[pt] = func_name

    # Exit a parse tree produced by MiniCParser#args.
    def exitArgs(self, ctx):
        args=[]
        if ctx.getChildCount() >=0:
            for i in range(ctx.getChildCount()):
                if i%2==0:
                    args.append(self.prop[ctx.expr(i/2)])
                else:
                    continue
        self.prop[ctx]=args

