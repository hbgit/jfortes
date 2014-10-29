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
         if (a[i] < m)
         {
            mindex = i;
            m      = a[i];
         }
      }
      n--;
      a[mindex] = a[n];
      System.out.print(aux);
      return(m);
   }
public static void main(String[] args){
int[] arrJFORTES = new int [Cute.input.Integer()];
Bag runJFORTES = new Bag( arrJFORTES );
runJFORTES.nome = Cute.input.String();
runJFORTES.a = new int [Cute.input.Integer()];
runJFORTES.n = Cute.input.Integer();
runJFORTES.teste = Cute.input.Float();
runJFORTES.extractMin();
}
}
