	.file	"dictionary.c"
	.text
	.globl	strip
	.type	strip, @function
strip:
.LFB2:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$48, %rsp
	movq	%rdi, -40(%rbp)
	movq	-40(%rbp), %rax
	movq	(%rax), %rax
	movq	%rax, -8(%rbp)
	movq	-8(%rbp), %rax
	movq	%rax, %rdi
	call	strlen
	movl	%eax, -20(%rbp)
	movl	-20(%rbp), %eax
	cltq
	leaq	-1(%rax), %rdx
	movq	-8(%rbp), %rax
	addq	%rdx, %rax
	movq	%rax, -16(%rbp)
	jmp	.L2
.L4:
	addq	$1, -8(%rbp)
.L2:
	movq	-8(%rbp), %rax
	cmpq	-16(%rbp), %rax
	jnb	.L5
	call	__ctype_b_loc
	movq	(%rax), %rdx
	movq	-8(%rbp), %rax
	movzbl	(%rax), %eax
	movsbq	%al, %rax
	addq	%rax, %rax
	addq	%rdx, %rax
	movzwl	(%rax), %eax
	movzwl	%ax, %eax
	andl	$1024, %eax
	testl	%eax, %eax
	je	.L4
	jmp	.L5
.L7:
	subq	$1, -16(%rbp)
.L5:
	movq	-16(%rbp), %rax
	cmpq	-8(%rbp), %rax
	jbe	.L6
	call	__ctype_b_loc
	movq	(%rax), %rdx
	movq	-16(%rbp), %rax
	movzbl	(%rax), %eax
	movsbq	%al, %rax
	addq	%rax, %rax
	addq	%rdx, %rax
	movzwl	(%rax), %eax
	movzwl	%ax, %eax
	andl	$1024, %eax
	testl	%eax, %eax
	je	.L7
.L6:
	movq	-8(%rbp), %rax
	cmpq	-16(%rbp), %rax
	jbe	.L8
	movl	$0, %eax
	jmp	.L9
.L8:
	movq	-16(%rbp), %rax
	addq	$1, %rax
	movb	$0, (%rax)
	movq	-40(%rbp), %rax
	movq	-8(%rbp), %rdx
	movq	%rdx, (%rax)
	movq	-8(%rbp), %rax
.L9:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE2:
	.size	strip, .-strip
	.globl	insert
	.type	insert, @function
insert:
.LFB3:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$48, %rsp
	movq	%rdi, -40(%rbp)
	movq	%rsi, -48(%rbp)
	cmpq	$0, -40(%rbp)
	je	.L18
	movq	-40(%rbp), %rax
	movq	(%rax), %rdx
	movq	-48(%rbp), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	strcmp
	movl	%eax, -4(%rbp)
	cmpl	$0, -4(%rbp)
	je	.L19
	cmpl	$0, -4(%rbp)
	jns	.L14
	movq	-40(%rbp), %rax
	movq	8(%rax), %rax
	testq	%rax, %rax
	je	.L15
	movq	-40(%rbp), %rax
	movq	8(%rax), %rax
	movq	-48(%rbp), %rdx
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	insert
	jmp	.L10
.L15:
	movl	$24, %edi
	call	malloc
	movq	%rax, -24(%rbp)
	movq	-48(%rbp), %rax
	movq	%rax, %rdi
	call	strdup
	movq	%rax, %rdx
	movq	-24(%rbp), %rax
	movq	%rdx, (%rax)
	movq	-24(%rbp), %rax
	movq	$0, 8(%rax)
	movq	-24(%rbp), %rax
	movq	$0, 16(%rax)
	movq	-40(%rbp), %rax
	movq	-24(%rbp), %rdx
	movq	%rdx, 8(%rax)
	jmp	.L10
.L14:
	movq	-40(%rbp), %rax
	movq	16(%rax), %rax
	testq	%rax, %rax
	je	.L17
	movq	-40(%rbp), %rax
	movq	16(%rax), %rax
	movq	-48(%rbp), %rdx
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	insert
	jmp	.L10
.L17:
	movl	$24, %edi
	call	malloc
	movq	%rax, -16(%rbp)
	movq	-48(%rbp), %rax
	movq	%rax, %rdi
	call	strdup
	movq	%rax, %rdx
	movq	-16(%rbp), %rax
	movq	%rdx, (%rax)
	movq	-16(%rbp), %rax
	movq	$0, 8(%rax)
	movq	-16(%rbp), %rax
	movq	$0, 16(%rax)
	movq	-40(%rbp), %rax
	movq	-16(%rbp), %rdx
	movq	%rdx, 16(%rax)
	jmp	.L10
.L18:
	nop
	jmp	.L10
.L19:
	nop
.L10:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE3:
	.size	insert, .-insert
	.section	.rodata
.LC0:
	.string	"r"
.LC1:
	.string	"%s"
	.text
	.globl	populate_dictionary
	.type	populate_dictionary, @function
populate_dictionary:
.LFB4:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$1072, %rsp
	movq	%rdi, -1064(%rbp)
	movq	%rsi, -1072(%rbp)
	movq	-1072(%rbp), %rax
	movl	$.LC0, %esi
	movq	%rax, %rdi
	call	fopen
	movq	%rax, -8(%rbp)
	cmpq	$0, -8(%rbp)
	je	.L26
	jmp	.L22
.L25:
	leaq	-1040(%rbp), %rax
	movq	%rax, %rdi
	call	strdup
	movq	%rax, -1048(%rbp)
	leaq	-1048(%rbp), %rax
	movq	%rax, %rdi
	call	strip
	movq	%rax, -1048(%rbp)
	movq	-1064(%rbp), %rax
	movq	(%rax), %rax
	testq	%rax, %rax
	jne	.L23
	movl	$24, %edi
	call	malloc
	movq	%rax, -16(%rbp)
	movq	-1048(%rbp), %rdx
	movq	-16(%rbp), %rax
	movq	%rdx, (%rax)
	movq	-16(%rbp), %rax
	movq	$0, 8(%rax)
	movq	-16(%rbp), %rax
	movq	$0, 16(%rax)
	movq	-1064(%rbp), %rax
	movq	-16(%rbp), %rdx
	movq	%rdx, (%rax)
	jmp	.L22
.L23:
	movq	-1048(%rbp), %rdx
	movq	-1064(%rbp), %rax
	movq	(%rax), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	insert
.L22:
	leaq	-1040(%rbp), %rdx
	movq	-8(%rbp), %rax
	movl	$.LC1, %esi
	movq	%rax, %rdi
	movl	$0, %eax
	call	__isoc99_fscanf
	cmpl	$1, %eax
	je	.L25
.L26:
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE4:
	.size	populate_dictionary, .-populate_dictionary
	.globl	find_word
	.type	find_word, @function
find_word:
.LFB5:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$32, %rsp
	movq	%rdi, -24(%rbp)
	movq	%rsi, -32(%rbp)
	cmpq	$0, -32(%rbp)
	je	.L28
	cmpq	$0, -24(%rbp)
	jne	.L29
.L28:
	movl	$0, %eax
	jmp	.L30
.L29:
	movq	-24(%rbp), %rax
	movq	(%rax), %rdx
	movq	-32(%rbp), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	strcmp
	movl	%eax, -4(%rbp)
	cmpl	$0, -4(%rbp)
	jne	.L31
	movl	$1, %eax
	jmp	.L30
.L31:
	cmpl	$0, -4(%rbp)
	jns	.L32
	movq	-24(%rbp), %rax
	movq	8(%rax), %rax
	movq	-32(%rbp), %rdx
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	find_word
	jmp	.L30
.L32:
	movq	-24(%rbp), %rax
	movq	16(%rax), %rax
	movq	-32(%rbp), %rdx
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	find_word
.L30:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE5:
	.size	find_word, .-find_word
	.globl	print_tree
	.type	print_tree, @function
print_tree:
.LFB6:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$16, %rsp
	movq	%rdi, -8(%rbp)
	cmpq	$0, -8(%rbp)
	je	.L37
	movq	-8(%rbp), %rax
	movq	8(%rax), %rax
	testq	%rax, %rax
	je	.L36
	movq	-8(%rbp), %rax
	movq	8(%rax), %rax
	movq	%rax, %rdi
	call	print_tree
.L36:
	movq	-8(%rbp), %rax
	movq	(%rax), %rax
	movq	%rax, %rdi
	call	puts
	movq	-8(%rbp), %rax
	movq	16(%rax), %rax
	testq	%rax, %rax
	je	.L33
	movq	-8(%rbp), %rax
	movq	16(%rax), %rax
	movq	%rax, %rdi
	call	print_tree
	jmp	.L33
.L37:
	nop
.L33:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE6:
	.size	print_tree, .-print_tree
	.section	.rodata
	.align 8
.LC2:
	.string	"Dictionary loaded.\nEnter search word: "
.LC3:
	.string	"Yes!\n"
.LC4:
	.string	"No!\n"
.LC5:
	.string	"Enter search word: "
	.text
	.globl	main
	.type	main, @function
main:
.LFB7:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$1088, %rsp
	movl	%edi, -1076(%rbp)
	movq	%rsi, -1088(%rbp)
	movq	$0, -40(%rbp)
	movl	$0, -16(%rbp)
	cmpl	$2, -1076(%rbp)
	jne	.L39
	movq	-1088(%rbp), %rax
	movq	8(%rax), %rax
	movq	%rax, -8(%rbp)
.L39:
	cmpq	$0, -8(%rbp)
	jne	.L40
	movl	$-1, %eax
	jmp	.L50
.L40:
	movq	-8(%rbp), %rdx
	leaq	-40(%rbp), %rax
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	populate_dictionary
	movq	stdout(%rip), %rax
	movq	%rax, %rcx
	movl	$38, %edx
	movl	$1, %esi
	movl	$.LC2, %edi
	call	fwrite
	jmp	.L42
.L49:
	leaq	-1072(%rbp), %rax
	movq	%rax, -24(%rbp)
	movq	-24(%rbp), %rax
	movq	%rax, %rdi
	call	strlen
	movl	%eax, -28(%rbp)
	movl	$0, -12(%rbp)
	jmp	.L43
.L44:
	movl	-12(%rbp), %eax
	movslq	%eax, %rdx
	movq	-24(%rbp), %rax
	addq	%rdx, %rax
	movzbl	(%rax), %eax
	movsbl	%al, %eax
	movl	%eax, %edi
	call	tolower
	movl	%eax, %ecx
	movl	-12(%rbp), %eax
	movslq	%eax, %rdx
	movq	-24(%rbp), %rax
	addq	%rdx, %rax
	movl	%ecx, %edx
	movb	%dl, (%rax)
	addl	$1, -12(%rbp)
.L43:
	movl	-12(%rbp), %eax
	cmpl	-28(%rbp), %eax
	jl	.L44
	cmpl	$0, -28(%rbp)
	jle	.L45
	movl	-28(%rbp), %eax
	cltq
	leaq	-1(%rax), %rdx
	movq	-24(%rbp), %rax
	addq	%rdx, %rax
	movzbl	(%rax), %eax
	cmpb	$10, %al
	jne	.L45
	movl	-28(%rbp), %eax
	cltq
	leaq	-1(%rax), %rdx
	movq	-24(%rbp), %rax
	addq	%rdx, %rax
	movb	$0, (%rax)
	subl	$1, -28(%rbp)
.L45:
	movq	-40(%rbp), %rax
	movq	-24(%rbp), %rdx
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	find_word
	testl	%eax, %eax
	je	.L46
	movq	stdout(%rip), %rax
	movq	%rax, %rcx
	movl	$5, %edx
	movl	$1, %esi
	movl	$.LC3, %edi
	call	fwrite
	jmp	.L47
.L46:
	movq	stdout(%rip), %rax
	movq	%rax, %rcx
	movl	$4, %edx
	movl	$1, %esi
	movl	$.LC4, %edi
	call	fwrite
.L47:
	movq	stdout(%rip), %rax
	movq	%rax, %rcx
	movl	$19, %edx
	movl	$1, %esi
	movl	$.LC5, %edi
	call	fwrite
.L42:
	cmpl	$0, -16(%rbp)
	jne	.L48
	movq	stdin(%rip), %rdx
	leaq	-1072(%rbp), %rax
	movl	$1024, %esi
	movq	%rax, %rdi
	call	fgets
	testq	%rax, %rax
	jne	.L49
.L48:
	movq	stdout(%rip), %rax
	movq	%rax, %rsi
	movl	$10, %edi
	call	fputc
	movl	$0, %eax
.L50:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE7:
	.size	main, .-main
	.ident	"GCC: (GNU) 7.3.0"
	.section	.note.GNU-stack,"",@progbits
