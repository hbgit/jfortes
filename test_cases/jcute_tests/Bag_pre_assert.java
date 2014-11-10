import cute.Cute; // <- [JFORTES]

/**
 * Running uncrustify
 * ./uncrustify -q -l C -c ben.cfg -f <program.java>
 * */

class Bag {
   // no relation
   int[] a;
   int n;

   //with relation
   // jfortes_attribute name = n, from_constructors = {Bag_0}, sequence = 0;
   //int n;
   // jfortes_attribute name = a, from_constructors = {Bag_0}, sequence = 1;
   //int[] a;

   //@ jfortes_constructor name = Bag, id = Bag_0, sequence = 0;
   Bag(int[] input)
   {
      System.out.println("In default Bag");
// IN ORIGINAL CODE AT LINE: < 21  > 
// COMMENT:  Possible null dereference (Null)
Cute.Assert(  input != null && input.length > 0 ); 
      n = input.length;
      a = new int[n];
      System.arraycopy(input, 0, a, 0, n);
   }

   //@ jfortes_constructor name = Bag, id = Bag_1, sequence = 1;
   Bag(int[] input, String name)
   {
      System.out.println("In Bag: " + name);
// IN ORIGINAL CODE AT LINE: < 30  > 
// COMMENT:  Possible null dereference (Null)
Cute.Assert(  input != null && input.length > 0 ); 
      n = input.length;
      a = new int[n];
      System.arraycopy(input, 0, a, 0, n);
   }

   //@ jfortes_method name = extractMin, from_constructors = {Bag_0}, sequence = 0;
   public int extractMin()
   {
      int z, x, k;
      int m      = Integer.MAX_VALUE;
      int mindex = 0;

      for (int i = 1; i <= n; i++)
      {
// IN ORIGINAL CODE AT LINE: < 44  > 
// COMMENT:  Possible null dereference (Null)
Cute.Assert(  a != null && a.length > 0 ); 
// IN ORIGINAL CODE AT LINE: < 44  > 
// COMMENT:  Array index possibly too large (IndexTooBig)
Cute.Assert(  i < a.length ); 
         if (a[i] < m)
         {
            mindex = i;
            m      = a[i];
         }
      }
      n--;
// IN ORIGINAL CODE AT LINE: < 51  > 
// COMMENT:  Possible null dereference (Null)
Cute.Assert(  a != null && a.length > 0 ); 
// IN ORIGINAL CODE AT LINE: < 51  > 
// COMMENT:  Possible negative array index (IndexNegative)
Cute.Assert(  n >= 0 ); 
      a[mindex] = a[n];
      return(m);
   }


   //@ jfortes_method name = printN, from_constructors = {Bag_0,Bag_1}, sequence = 1;
   public void printN()
   {
      System.out.println(this.n);
   }
public static void main(String[] args){
int[] arrJFORTES = new int [Cute.input.Integer()];
Bag runJFORTES_0 = new Bag( arrJFORTES );
int[] arrJFORTES = new int [Cute.input.Integer()];
Bag runJFORTES_1 = new Bag( arrJFORTES, Cute.input.String(".") );
}
}
