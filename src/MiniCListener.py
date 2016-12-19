# Generated from MiniC.g4 by ANTLR 4.5.1
from antlr4 import *
from ctypes import CFUNCTYPE, c_int, POINTER
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
        self.tm = llvm.Target.from_default_triple().create_target_machine()

    # Enter a parse tree produced by MiniCParser#program.
    def enterProgram(self, ctx):
        pass

    # Exit a parse tree produced by MiniCParser#program.
    def exitProgram(self, ctx):
        programAst = ProgramAST()
        for child in ctx.getChildren():
            child_ast = self.prop[child]
            programAst.asts.append(child_ast) 
        strmod = programAst.codeGenerate()
        print "=== Generated IR code ===\n"
        print strmod
        llmod = llvm.parse_assembly(strmod)
        llmod.verify()
        with llvm.create_mcjit_compiler(llmod, self.tm) as ee:
            ee.finalize_object()
            print "=== Generated assembly code ===\n"
            print(self.tm.emit_assembly(llmod))


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
        ty = ctx.getChild(0)
        name = ctx.getChild(1).getText()
        #value = ctx.getChild(3).getText()
        type_ast = self.prop[ty]
        global_ast = GloabalAST(name=name,type=type_ast,is_array=False,value=0)
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
        pass

    # Exit a parse tree produced by MiniCParser#fun_decl.
    def exitFun_decl(self, ctx):
        ftype = self.prop[ctx.getChild(0)]
        function_name = ctx.getChild(1).getText()
        if len(ctx.getChild(3).getText()) > 0:
           args_ast = self.prop[ctx.getChild(3)]
           args, args_names = args_ast.codeGenerate() 
           ast = FunctionAST(function_type= ftype, name=function_name, args_types = args, args_names = args_names)
           self.prop[ctx] = ast
        else:
           ast = FunctionAST(function_type= ftype, name=function_name, args_types = None)
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
                    paramAST = self.prop[ctx.getChild(i-1)]
                    ast.param_asts.append(paramAST)
            self.prop[ctx] = ast

    # Enter a parse tree produced by MiniCParser#param.
    def enterParam(self, ctx):
        pass

    # Exit a parse tree produced by MiniCParser#param.
    def exitParam(self, ctx):
        param_type = ctx.getChild(0).getText()
        param_name = ctx.getChild(1).getText()
        ast = ParamAST(type=param_type, name = param_name)
        self.prop[ctx] = ast


    # Enter a parse tree produced by MiniCParser#stmt.
    def enterStmt(self, ctx):
        pass

    # Exit a parse tree produced by MiniCParser#stmt.
    def exitStmt(self, ctx):
        #stmt = ""
        #if ctx.getChildCount > 0:
        #    if ctx.expr_stmt is not None:
        #        print ctx.getText()
        #        stmt += self.prop[ctx.expr_stmt()]
        #    elif ctx.compound_stmt is not None:
        #        stmt += self.prop[ctx.compound_stmt()]
        #    elif ctx.if_stmt is not None:
        #        stmt += self.prop[ctx.if_stmt]
        #    elif ctx.while_stmt is not None:
        #        stmt += self.prop[ctx.while_stmt]
        #    else:
        #        stmt += self.prop[ctx.return_stmt]
        #self.prop[ctx]=stmt
        pass


    # Enter a parse tree produced by MiniCParser#expr_stmt.
    def enterExpr_stmt(self, ctx):
        pass

    # Exit a parse tree produced by MiniCParser#expr_stmt.
    def exitExpr_stmt(self, ctx):
        #stmt = ""
        #if ctx.getChildCount() == 2:
        #    stmt +=" "
        #    stmt +=self.prop[ctx.expr()]
        #    stmt +=ctx.getChild(1).getText()
        #    stmt +="\n"
        #self.prop[ctx]=stmt
        pass


    # Enter a parse tree produced by MiniCParser#while_stmt.
    def enterWhile_stmt(self, ctx):
        pass

    # Exit a parse tree produced by MiniCParser#while_stmt.
    def exitWhile_stmt(self, ctx):
        pass


    # Enter a parse tree produced by MiniCParser#compound_stmt.
    def enterCompound_stmt(self, ctx):
        pass

    # Exit a parse tree produced by MiniCParser#compound_stmt.
    def exitCompound_stmt(self, ctx):
        pass


    # Enter a parse tree produced by MiniCParser#local_decl.
    def enterLocal_decl(self, ctx):
        pass

    # Exit a parse tree produced by MiniCParser#local_decl.
    def exitLocal_decl(self, ctx):
        pass


    # Enter a parse tree produced by MiniCParser#if_stmt.
    def enterIf_stmt(self, ctx):
        pass

    # Exit a parse tree produced by MiniCParser#if_stmt.
    def exitIf_stmt(self, ctx):
        pass


    # Enter a parse tree produced by MiniCParser#return_stmt.
    def enterReturn_stmt(self, ctx):
        pass

    # Exit a parse tree produced by MiniCParser#return_stmt.
    def exitReturn_stmt(self, ctx):
        pass


    # Enter a parse tree produced by MiniCParser#expr.
    def enterExpr(self, ctx):
        pass

    # Exit a parse tree produced by MiniCParser#expr.
    def exitExpr(self, ctx):
        #expr=""
        #print ctx.getText()
        #if ctx.getChildCount() > 0:
        #    if ctx.getChildCount() == 1:
        #        expr+=ctx.getChild(0).getText()
        #    elif ctx.getChildCount() == 2:
        #        expr+=ctx.getChild(0).getText()
        #        expr+=self.prop[ctx.expr(0)]
        #    elif ctx.getChildCount() == 3:
        #        if ctx.getChild(0).getText() == "(":
        #            expr+=ctx.getChild(0).getText()
        #            expr+=self.prop[ctx.expr(0)]
        #            expr+=ctx.getChild(2).getText()
        #        elif ctx.getChild(1).getText() == "=":
        #            expr+=ctx.getChild(0).getText()
        #            expr+=" "
        #            expr+=ctx.getChild(1).getText()
        #            expr+=" "
        #            expr+=self.prop[ctx.expr(0)]
        #        else: #binary
        #            expr+=self.prop[ctx.expr(0)]
        #            expr+=" "
        #            expr+=ctx.getChild(1).getText()
        #            expr+=" "
        #            expr+=self.prop[ctx.expr(1)]
        #    elif ctx.getChildCount() == 4:
        #        expr+=ctx.getChild(0).getText()
        #        if ctx.args() is not None:
        #            expr+=ctx.getChild(1).getText()
        #            expr+=self.prop[ctx.args()]
        #        else:
        #            expr+=ctx.getChild(1).getText
        #            expr+=self.prop[ctx.expr(0)]
        #        expr+=ctx.getChild(3).getText()
        #    else:
        #        expr+=ctx.getChild(0).getText()
        #        expr+=ctx.getChild(1).getText()
        #        expr+=self.prop[ctx.expr(0)]
        #        expr+=ctx.getChild(3).getText()
        #        expr+=" "
        #        expr+=ctx.getChild(4).getText()
        #        expr+=" "
        #        expr+=self.prop[ctx.expr(1)]
        #    self.prop[ctx]=expr
        pass


    # Enter a parse tree produced by MiniCParser#args.
    def enterArgs(self, ctx):
        pass

    # Exit a parse tree produced by MiniCParser#args.
    def exitArgs(self, ctx):
        #args=""
        #if ctx.getChildCount() >=0:
        #    for i in range(ctx.getChildCount()):
        #        if i%2==0:
        #            args+=self.prop[ctx.expr(i/2)]
        #        else:
        #            args+=ctx.getChild(i).getText()
        #            args+=" "
        #self.prop[ctx]=args
        pass


