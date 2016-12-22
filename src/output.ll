; ModuleID = ""
target triple = "x86_64-unknown-linux-gnu"
target datalayout = ""

@"i" = global i32 0
@"t" = global [5 x i32] zeroinitializer
define i32 @"foo"(i32 %"n") 
{
foo:
  %"n.1" = alloca i32
  %"k" = alloca i32
  store i32 10, i32* @"i"
  %".4" = load i32, i32* %"n.1"
  %".5" = add i32 %".4", 1
  store i32 %".5", i32* %"n.1"
  %".7" = load i32, i32* %"n.1"
  %".8" = sub i32 %".7", 1
  store i32 %".8", i32* %"n.1"
  %".10" = load i32, i32* %"n.1"
  %".11" = mul i32 %".10", 2
  store i32 %".11", i32* %"k"
  %".13" = load i32, i32* %"n.1"
  %".14" = load i32, i32* %"k"
  %".15" = add i32 %".13", %".14"
  %".16" = load i32, i32* @"i"
  %".17" = add i32 %".15", %".16"
  ret i32 %".17"
}

define i32 @"main"() 
{
main:
  %"x" = alloca i32
  %"y" = alloca i32
  store i32 5, i32* %"x"
  %".3" = getelementptr [5 x i32], [5 x i32]* @"t", i32 0, i32 3
  store i32 2, i32* %".3"
  %".5" = getelementptr [5 x i32], [5 x i32]* @"t", i32 0, i32 3
  %".6" = load i32, i32* %".5"
  store i32 %".6", i32* %"x"
  store i32 1, i32* %"y"
  br label %"loop.header"
loop.header:
  %".10" = load i32, i32* %"x"
  %".11" = icmp sgt i32 %".10", 0
  br i1 %".11", label %"loop.body", label %"loop.end"
loop.body:
  %".13" = load i32, i32* %"x"
  %".14" = sub i32 %".13", 1
  store i32 %".14", i32* %"x"
  br label %"loop.header"
loop.end:
  ret i32 0
}
