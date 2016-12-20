int x;
void foo(int n) {
  n = n + 1;
  return;
}
int main()
{
   int x;
   x = 5;
   foo(x);
   return 0;
}
