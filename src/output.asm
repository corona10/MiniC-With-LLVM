	.text
	.file	"<string>"
	.globl	foo
	.align	16, 0x90
	.type	foo,@function
foo:
	.cfi_startproc
	movabsq	$i, %rcx
	movl	$10, (%rcx)
	movl	-4(%rsp), %eax
	leal	1(%rax), %edx
	movl	%edx, -4(%rsp)
	movl	%eax, -4(%rsp)
	addl	%eax, %eax
	movl	%eax, -8(%rsp)
	addl	-4(%rsp), %eax
	addl	(%rcx), %eax
	retq
.Lfunc_end0:
	.size	foo, .Lfunc_end0-foo
	.cfi_endproc

	.globl	main
	.align	16, 0x90
	.type	main,@function
main:
	.cfi_startproc
	movl	$5, -4(%rsp)
	movabsq	$t, %rax
	movl	$2, 12(%rax)
	movl	$2, -4(%rsp)
	movl	$1, -8(%rsp)
	jmp	.LBB1_1
	.align	16, 0x90
.LBB1_2:
	decl	-4(%rsp)
.LBB1_1:
	cmpl	$0, -4(%rsp)
	jg	.LBB1_2
	xorl	%eax, %eax
	retq
.Lfunc_end1:
	.size	main, .Lfunc_end1-main
	.cfi_endproc

	.type	i,@object
	.bss
	.globl	i
	.align	4
i:
	.long	0
	.size	i, 4

	.type	t,@object
	.globl	t
	.align	16
t:
	.zero	20
	.size	t, 20


	.section	".note.GNU-stack","",@progbits
