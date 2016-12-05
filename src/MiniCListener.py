# Generated from MiniC.g4 by ANTLR 4.5.1
from antlr4 import *

# This class defines a complete listener for a parse tree produced by MiniCParser.
class MiniCListener(ParseTreeListener):

    # Enter a parse tree produced by MiniCParser#program.
    def enterProgram(self, ctx):
	print ctx.getText()
        pass

    # Exit a parse tree produced by MiniCParser#program.
    def exitProgram(self, ctx):
        pass


    # Enter a parse tree produced by MiniCParser#decl.
    def enterDecl(self, ctx):
        pass

    # Exit a parse tree produced by MiniCParser#decl.
    def exitDecl(self, ctx):
        pass


    # Enter a parse tree produced by MiniCParser#var_decl.
    def enterVar_decl(self, ctx):
        pass

    # Exit a parse tree produced by MiniCParser#var_decl.
    def exitVar_decl(self, ctx):
        pass


    # Enter a parse tree produced by MiniCParser#type_spec.
    def enterType_spec(self, ctx):
        pass

    # Exit a parse tree produced by MiniCParser#type_spec.
    def exitType_spec(self, ctx):
        pass


    # Enter a parse tree produced by MiniCParser#fun_decl.
    def enterFun_decl(self, ctx):
        pass

    # Exit a parse tree produced by MiniCParser#fun_decl.
    def exitFun_decl(self, ctx):
        pass


    # Enter a parse tree produced by MiniCParser#params.
    def enterParams(self, ctx):
        pass

    # Exit a parse tree produced by MiniCParser#params.
    def exitParams(self, ctx):
        pass


    # Enter a parse tree produced by MiniCParser#param.
    def enterParam(self, ctx):
        pass

    # Exit a parse tree produced by MiniCParser#param.
    def exitParam(self, ctx):
        pass


    # Enter a parse tree produced by MiniCParser#stmt.
    def enterStmt(self, ctx):
        pass

    # Exit a parse tree produced by MiniCParser#stmt.
    def exitStmt(self, ctx):
        pass


    # Enter a parse tree produced by MiniCParser#expr_stmt.
    def enterExpr_stmt(self, ctx):
        pass

    # Exit a parse tree produced by MiniCParser#expr_stmt.
    def exitExpr_stmt(self, ctx):
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
        pass


    # Enter a parse tree produced by MiniCParser#args.
    def enterArgs(self, ctx):
        pass

    # Exit a parse tree produced by MiniCParser#args.
    def exitArgs(self, ctx):
        pass


