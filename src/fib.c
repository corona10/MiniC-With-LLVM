int foo(int n) {
  int k;
  n = n + 1;
  n = n - 1;
  k = n * 2;
  return n + k;
}
int main()
{
   int x;
   x = 5;
   foo(x);
   return 0;
}
