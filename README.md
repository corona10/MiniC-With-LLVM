# MiniC With LLVM
A compiler term project for item03  as CompilerCS302 of Chungnam National University.

We made a Mini C compiler which works with LLVM Lite for back end and antlr for front end.
This comiler generates LLVM IR Codes, assembly codes for target machine and CFG Graph.

## Pre-install
We tesed on Ubuntu 16.04 and python2.

* sudo apt-get install antlr4
* pip install antlr4-python2-runtime 
* conda install llvmlite
* pip install graphviz

## How to execute
`python main.py sourcecode.c`

## Example with fibonacci.c

### MiniC code
``` c
int fib(int n)
{
  if (n < 2)
     return n;
  return fib(n-1) + fib(n-2);
}

int main()
{
  int k = 10;
  int result;
  k = fib(k);
  return k;
}
```

### LLVM IR code
```
; ModuleID = '<string>'
target triple = "x86_64-pc-linux-gnu"

; Function Attrs: nounwind readnone
define i32 @fib(i32 %n) #0 {
fib:
  %.5 = icmp slt i32 %n, 2
  br i1 %.5, label %fib.if, label %fib.endif

fib.if:                                           ; preds = %fib
  ret i32 %n

fib.endif:                                        ; preds = %fib
  %.10 = add i32 %n, -1
  %.11 = tail call i32 @fib(i32 %.10)
  %.13 = add i32 %n, -2
  %.14 = tail call i32 @fib(i32 %.13)
  %.15 = add i32 %.14, %.11
  ret i32 %.15
}

; Function Attrs: nounwind readnone
define i32 @main() #0 {
main:
  %.4 = tail call i32 @fib(i32 10)
  ret i32 %.4
}

attributes #0 = { nounwind readnone }
```

### Assembly  code
``` assembly
	.text
	.file	"<string>"
	.globl	fib
	.align	16, 0x90
	.type	fib,@function
fib:
	pushq	%rbp
	pushq	%r14
	pushq	%rbx
	movl	%edi, %ebx
	cmpl	$1, %ebx
	jg	.LBB0_3
	movl	%ebx, %eax
	jmp	.LBB0_2
.LBB0_3:
	leal	-1(%rbx), %edi
	movabsq	$fib, %r14
	callq	*%r14
	movl	%eax, %ebp
	addl	$-2, %ebx
	movl	%ebx, %edi
	callq	*%r14
	addl	%ebp, %eax
.LBB0_2:
	popq	%rbx
	popq	%r14
	popq	%rbp
	retq
.Lfunc_end0:
	.size	fib, .Lfunc_end0-fib

	.globl	main
	.align	16, 0x90
	.type	main,@function
main:
	movabsq	$fib, %rax
	movl	$10, %edi
	jmpq	*%rax
.Lfunc_end1:
	.size	main, .Lfunc_end1-main


	.section	".note.GNU-stack","",@progbits
```
