import cute.Cute; // <- [JFORTES]

//attributes values in constructors
//no annots for attributes

public class Test {
   int[] a;
   int n;


   //@ jfortes_constructor name = Test, id = Test_0, sequence = {0}, line = 18;
   Test(int[] input, boolean name)
   {
      System.out.println("In Test: " + name);
// IN ORIGINAL CODE AT LINE: < 13  >
// COMMENT:  Possible null dereference (Null)
      Cute.Assert(input != null && input.length > 0);
      n = input.length;
      a = new int[n];
      System.arraycopy(input, 0, a, 0, n);
   }


   //@ jfortes_constructor name = Test, id = Test_1, sequence = {1}, line = 26;
   Test(int[] input2)
   {
      System.out.println("In default Test");
// IN ORIGINAL CODE AT LINE: < 23  >
// COMMENT:  Possible null dereference (Null)
      Cute.Assert(input2 != null && input2.length > 0);
      n = input2.length;
      a = new int[n];
      System.arraycopy(input2, 0, a, 0, n);
   }


   //@ jfortes_method name = extractMin, from_constructors = {Test_0}, sequence = {0}, line = 34;
   public int extractMin()
   {
      int z, x, k;
      int m      = Integer.MAX_VALUE;
      int mindex = 0;

      for (int i = 1; i <= n; i++)
      {
// IN ORIGINAL CODE AT LINE: < 38  >
// COMMENT:  Possible null dereference (Null)
         Cute.Assert(a != null && a.length > 0);
// IN ORIGINAL CODE AT LINE: < 38  >
// COMMENT:  Array index possibly too large (IndexTooBig)
         Cute.Assert(i < a.length);
         if (a[i] < m)
         {
            mindex = i;
            m      = a[i];
         }
      }
      n--;
// IN ORIGINAL CODE AT LINE: < 45  >
// COMMENT:  Possible null dereference (Null)
      Cute.Assert(a != null && a.length > 0);
// IN ORIGINAL CODE AT LINE: < 45  >
// COMMENT:  Possible negative array index (IndexNegative)
      Cute.Assert(n >= 0);
      a[mindex] = a[n];
      return(m);
   }


   //@ jfortes_method name = printN, from_constructors = {Test_0,Test_1}, sequence = {1, 0}, line = 50;
   public void printN()
   {
      System.out.println(this.n);
   }


   public static void main(String[] args)
   {
      int[] arrJFORTES1 = new int [Cute.input.Integer()];
      Test runJFORTES1 = new Test(arrJFORTES1, Cute.input.Boolean());

      runJFORTES1.extractMin();
      runJFORTES1.printN();
      int[] arrJFORTES2 = new int [Cute.input.Integer()];
      Test runJFORTES2 = new Test(arrJFORTES2);

      runJFORTES2.printN();
   }
}