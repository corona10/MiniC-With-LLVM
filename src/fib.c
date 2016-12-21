int i;
int foo(int n) {
  int k;
  i = 10;
  n = n + 1;
  n = n - 1;
  k = n * 2;
  return n + k + i;
}
int main()
{
   int t[5];
   int x;
   x = 5;
   t[3] = 2;
   ++x;
   foo(x);
   return 0;
}
