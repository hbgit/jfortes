import cute.Cute; // <- [JFORTES]

public class Test3 {
   //@ jfortes_attribute name = array, from_constructors = {Test3_0, Test3_1}, sequence = {0, 1}, line = 4;
   int[] array;

   float attr1;

   //@ jfortes_attribute name = attr2, from_constructors = {Test3_1}, sequence = {0}, line = 9;
   int attr2;

   //@ jfortes_constructor name = Test3, id = Test3_0, sequence = 0, line = 13;
   Test3(int len)
   {
// IN ORIGINAL CODE AT LINE: < 13  >
// COMMENT:  Possible attempt to allocate array of negative length (NegSize)
      Cute.Assert(!(len < 0));
      this.array = new int[len];
   }

   //@ jfortes_constructor name = Test3, id = Test3_1, sequence = 1, line = 18;
   Test3(int[] input, String name)
   {
      System.out.println("In Test3: " + name);
// IN ORIGINAL CODE AT LINE: < 20  >
// COMMENT:  Possible null dereference (Null)
      Cute.Assert(input != null && input.length > 0);
      attr2 = input.length;
      array = new int[attr2];
      System.arraycopy(input, 0, array, 0, attr2);
   }

   //@ jfortes_method name = maior, from_constructors = {Test3_1}, sequence = {0}, line = 26;
   public static int maior(int[] a)
   {
// IN ORIGINAL CODE AT LINE: < 28  >
// COMMENT:  Possible null dereference (Null)
      Cute.Assert(a != null && a.length > 0);
// IN ORIGINAL CODE AT LINE: < 28  >
// COMMENT:  Array index possibly too large (IndexTooBig)
      Cute.Assert(0 < a.length);
      int max = a[0];

      for (int i = 1; i < a.length; i++)
      {
         if (a[i] > max)
         {
            max = a[i];
         }
      }

      return(max);
   }


   public static void main(String[] args)
   {
      Test3 runJFORTES1 = new Test3(Cute.input.Integer());

      runJFORTES1.array = new int[Cute.input.Integer()];
      int[] arrJFORTES1 = new int [Cute.input.Integer()];
      Test3 runJFORTES2 = new Test3(arrJFORTES1, Cute.input.Object("."));

      runJFORTES2.attr2 = Cute.input.Integer();
      runJFORTES2.array = new int[Cute.input.Integer()];
      int[] arrJFORTES2 = new int [Cute.input.Integer()];
      runJFORTES2.maior(arrJFORTES2);
   }
}
