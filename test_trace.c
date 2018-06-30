#include <stdio.h>
#include <stdlib.h>


void print_hello(char *h)
{
	printf(h);
}

void print_world(char *w)
{
	printf(w);
}

void print_space(char *s)
{
	printf(s);
}

void print_line(char* l)
{
	printf(l);
}

void print_helloworld(char *a, char *b, char *c, char *d)
{
	printf("%s %s %s %s", a, b, c, d);
}


int main()
{
	print_hello("HELLO");
	print_space(" ");
	print_world("WORLD");
	print_line("\n");
	print_helloworld("Hello", " ", "World", "\n");
}

