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
