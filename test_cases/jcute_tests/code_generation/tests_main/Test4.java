import cute.Cute; // <- [JFORTES]

import java.util.Random;

public class Test4 {
   //@ jfortes_attribute name = array2d, from_constructors = {Test4_0}, sequence = {0}, line = 6;
   int[][] array2d;
   Random gerador = new Random();


   //@ jfortes_constructor name = Test4, id = Test4_0, sequence = 0, line = 11;
   Test4(int len)
   {
// IN ORIGINAL CODE AT LINE: < 12  >
// COMMENT:  Possible attempt to allocate array of negative length (NegSize)
      Cute.Assert(!(len < 0));
      this.array2d = new int[len][len];
      System.out.println("Test4 created");
   }

   //@ jfortes_method name = preencheMat, from_constructors = {Test4_0}, sequence = {0}, line = 17;
   public void preencheMat()
   {
// IN ORIGINAL CODE AT LINE: < 19  >
// COMMENT:  Possible null dereference (Null)
      Cute.Assert(array2d != null && array2d.length > 0);
      for (int lin = 0; lin < array2d.length; lin++)
      {
// IN ORIGINAL CODE AT LINE: < 21  >
// COMMENT:  Possible null dereference (Null)
         Cute.Assert(array2d[lin] != null && array2d[lin].length > 0);
         for (int col = 0; col < array2d[lin].length; col++)
         {
// IN ORIGINAL CODE AT LINE: < 23  >
// COMMENT:  Possible null dereference (Null)
//            Cute.Assert(gerador != null && gerador.length > 0);
            array2d[lin][col] = gerador.nextInt(100);
         }
      }
   }


   //@ jfortes_method name = printMat, from_constructors = {Test4_0}, sequence = {1}, line = 26;
   public void printMat()
   {
      for (int lin = 0; lin < array2d.length; lin++)
      {
         for (int col = 0; col < array2d[lin].length; col++)
         {
            System.out.print(array2d[lin][col] + " ");
         }
         System.out.println("");
      }
   }


   public static void main(String[] args)
   {
      Test4 runJFORTES1 = new Test4(Cute.input.Integer());

      runJFORTES1.array2d = new int[Cute.input.Integer()][Cute.input.Integer()];
      runJFORTES1.preencheMat();
      runJFORTES1.printMat();
   }
}

//@The following comments are auto-generated to save options for testing the current file
//@jcute.optionLogPath=true
//@jcute.optionLogTraceAndInput=true
//@jcute.optionGenerateJUnit=true
//@jcute.optionExtraOptions=
//@jcute.optionJUnitOutputFolderName=/home/glarissa/jCute/jcute
//@jcute.optionJUnitPkgName=
//@jcute.optionNumberOfPaths=10000
//@jcute.optionLogLevel=3
//@jcute.optionDepthForDFS=0
//@jcute.optionSearchStrategy=0
//@jcute.optionSequential=true
//@jcute.optionQuickSearchThreshold=100
//@jcute.optionLogRace=true
//@jcute.optionLogDeadlock=true
//@jcute.optionLogException=true
//@jcute.optionLogAssertion=true
//@jcute.optionUseRandomInputs=false
//@jcute.optionPrintOutput=true
