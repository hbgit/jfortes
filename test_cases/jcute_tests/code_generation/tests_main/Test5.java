import cute.Cute; // <- [JFORTES]

import java.util.Random;

public class Test5 {
   //@ jfortes_attribute name = array2d, from_constructors = {Test5_0}, sequence = {1}, line = 5;
   float[][] array2d;
   //@ jfortes_attribute name = n, from_constructors = {Test5_0}, sequence = {0}, line = 7;
   int    n;
   Random gerador = new Random();

   //@ jfortes_constructor name = Test5, id = Test5_0, sequence = 0, line = 10;
   Test5(float[][] input)
   {
      System.out.println("Test5 created");
// IN ORIGINAL CODE AT LINE: < 14  >
// COMMENT:  Possible null dereference (Null)
      Cute.Assert(input != null && input.length > 0);
      n       = input.length;
      array2d = new float[n][n];
   }

   //@ jfortes_method name = preencheMat, from_constructors = {Test5_0}, sequence = {0}, line = 18;
   public void preencheMat()
   {
// IN ORIGINAL CODE AT LINE: < 21  >
// COMMENT:  Possible null dereference (Null)
      Cute.Assert(array2d != null && array2d.length > 0);
      for (int lin = 0; lin < array2d.length; lin++)
      {
// IN ORIGINAL CODE AT LINE: < 23  >
// COMMENT:  Possible null dereference (Null)
         Cute.Assert(array2d[lin] != null && array2d[lin].length > 0);
         for (int col = 0; col < array2d[lin].length; col++)
         {
// IN ORIGINAL CODE AT LINE: < 25  >
// COMMENT:  Possible null dereference (Null)
//            Cute.Assert(gerador != null && gerador.length > 0);
            array2d[lin][col] = gerador.nextInt(100);
         }
      }
   }


   public static void main(String[] args)
   {
      float[][] arrJFORTES1 = new float [Cute.input.Integer()][Cute.input.Integer()];
      Test5 runJFORTES1 = new Test5(arrJFORTES1);

      runJFORTES1.n       = Cute.input.Integer();
      runJFORTES1.array2d = new float[Cute.input.Integer()][Cute.input.Integer()];
      runJFORTES1.preencheMat();
   }
}

