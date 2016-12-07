# Generated from MiniC.g4 by ANTLR 4.5.1
from antlr4 import *

# This class defines a complete listener for a parse tree produced by MiniCParser.
class MiniCListener(ParseTreeListener):
    def __init__(self):
        self.prop={}

    # Enter a parse tree produced by MiniCParser#program.
    def enterProgram(self, ctx):
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
        stmt = ""
        if ctx.getChildCount > 0:
            if ctx.expr_stmt is not None:
                print ctx.getText()
                stmt += self.prop[ctx.expr_stmt()]
            elif ctx.compound_stmt is not None:
                stmt += self.prop[ctx.compound_stmt()]
            elif ctx.if_stmt is not None:
                stmt += self.prop[ctx.if_stmt]
            elif ctx.while_stmt is not None:
                stmt += self.prop[ctx.while_stmt]
            else:
                stmt += self.prop[ctx.return_stmt]
        self.prop[ctx]=stmt
        pass


    # Enter a parse tree produced by MiniCParser#expr_stmt.
    def enterExpr_stmt(self, ctx):
        pass

    # Exit a parse tree produced by MiniCParser#expr_stmt.
    def exitExpr_stmt(self, ctx):
        stmt = ""
        if ctx.getChildCount() == 2:
            stmt +=" "
            stmt +=self.prop[ctx.expr()]
            stmt +=ctx.getChild(1).getText()
            stmt +="\n"
        self.prop[ctx]=stmt
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
        expr=""
        print ctx.getText()
        if ctx.getChildCount() > 0:
            if ctx.getChildCount() == 1:
                expr+=ctx.getChild(0).getText()
            elif ctx.getChildCount() == 2:
                expr+=ctx.getChild(0).getText()
                expr+=self.prop[ctx.expr(0)]
            elif ctx.getChildCount() == 3:
                if ctx.getChild(0).getText() == "(":
                    expr+=ctx.getChild(0).getText()
                    expr+=self.prop[ctx.expr(0)]
                    expr+=ctx.getChild(2).getText()
                elif ctx.getChild(1).getText() == "=":
                    expr+=ctx.getChild(0).getText()
                    expr+=" "
                    expr+=ctx.getChild(1).getText()
                    expr+=" "
                    expr+=self.prop[ctx.expr(0)]
                else: #binary
                    expr+=self.prop[ctx.expr(0)]
                    expr+=" "
                    expr+=ctx.getChild(1).getText()
                    expr+=" "
                    expr+=self.prop[ctx.expr(1)]
            elif ctx.getChildCount() == 4:
                expr+=ctx.getChild(0).getText()
                if ctx.args() is not None:
                    expr+=ctx.getChild(1).getText()
                    expr+=self.prop[ctx.args()]
                else:
                    expr+=ctx.getChild(1).getText
                    expr+=self.prop[ctx.expr(0)]
                expr+=ctx.getChild(3).getText()
            else:
                expr+=ctx.getChild(0).getText()
                expr+=ctx.getChild(1).getText()
                expr+=self.prop[ctx.expr(0)]
                expr+=ctx.getChild(3).getText()
                expr+=" "
                expr+=ctx.getChild(4).getText()
                expr+=" "
                expr+=self.prop[ctx.expr(1)]
            self.prop[ctx]=expr

             
            
	print self.prop[ctx]
        pass


    # Enter a parse tree produced by MiniCParser#args.
    def enterArgs(self, ctx):
        pass

    # Exit a parse tree produced by MiniCParser#args.
    def exitArgs(self, ctx):
        args=""
        if ctx.getChildCount() >=0:
            for i in range(ctx.getChildCount()):
                if i%2==0:
                    args+=self.prop[ctx.expr(i/2)]
                else:
                    args+=ctx.getChild(i).getText()
                    args+=" "
        self.prop[ctx]=args
        pass


