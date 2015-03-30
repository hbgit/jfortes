/**
 * Running uncrustify
 * ./uncrustify -q -l C -c ben.cfg -f <program.java>
 * */

class Bag {
   // no relation
   //int[] a;
   //int n;

   //with relation
   //@ jfortes_attribute name = n, from_constructors = {Bag_0,Bag_1}, sequence = {0, 0}, line = 13;
   int n;
   //@ jfortes_attribute name = a, from_constructors = {Bag_0,Bag_1}, sequence = {1, 1}, line = 15;
   int[] a;

   //@ jfortes_constructor name = Bag, id = Bag_1, sequence = 0, line = 18;
   Bag(int[] input, String name)
   {
      System.out.println("In Bag: " + name);
      n = input.length;
      a = new int[n];
      System.arraycopy(input, 0, a, 0, n);
   }


   //@ jfortes_constructor name = Bag, id = Bag_0, sequence = 1, line = 26;
   Bag(int[] input2)
   {
      System.out.println("In default Bag");
      n = input2.length;
      a = new int[n];
      System.arraycopy(input2, 0, a, 0, n);
   }


   //@ jfortes_method name = extractMin, from_constructors = {Bag_0}, sequence = {0}, line = 34;
   public int extractMin()
   {
      int z, x, k;
      int m      = Integer.MAX_VALUE;
      int mindex = 0;

      for (int i = 1; i <= n; i++)
      {
         if (a[i] < m)
         {
            mindex = i;
            m      = a[i];
         }
      }
      n--;
      a[mindex] = a[n];
      return(m);
   }


   //@ jfortes_method name = printN, from_constructors = {Bag_0,Bag_1}, sequence = {1, 0}, line = 50;
   public void printN()
   {
      System.out.println(this.n);
   }
}