import cute.Cute; // <- [JFORTES]

/**
 * Running uncrustify
 * ./uncrustify -q -l C -c ben.cfg -f <program.java>
 * */

class Bag {
   String nome;
   int[] a;
   int   n;
   float teste;
   public Bag(int[] input)
   {
// IN ORIGINAL CODE AT LINE: < 13  > 
// COMMENT:  Possible null dereference (Null)
Cute.Assert(  input != null && input.length > 0 ); 
      n = input.length;
      a = new int[n];
      System.arraycopy(input, 0, a, 0, n);
   }

   public int extractMin()
   {
      int z, x, k;
      int m      = Integer.MAX_VALUE;
      int mindex = 0;

      for (int i = 1; i <= n; i++)
      {
// IN ORIGINAL CODE AT LINE: < 26  > 
// COMMENT:  Possible null dereference (Null)
Cute.Assert(  a != null && a.length > 0 ); 
// IN ORIGINAL CODE AT LINE: < 26  > 
// COMMENT:  Array index possibly too large (IndexTooBig)
Cute.Assert(  i < a.length ); 
         if (a[i] < m)
         {
            mindex = i;
            m      = a[i];
         }
      }
      n--;
// IN ORIGINAL CODE AT LINE: < 33  > 
// COMMENT:  Possible null dereference (Null)
Cute.Assert(  a != null && a.length > 0 ); 
// IN ORIGINAL CODE AT LINE: < 33  > 
// COMMENT:  Possible negative array index (IndexNegative)
Cute.Assert(  n >= 0 ); 
      a[mindex] = a[n];
      return(m);
   }
}
