/**
 * >> No Bug found in compilation
 *    $ javac UpperBound_False.java -Xlint:all
 * >> Bug found in execution
 **/

public class UpperBound_False {
	
  public static void main(String[] args) {    
    metodo1();    
  }

  static void metodo1() {    
    metodo2();    
  }

  static void metodo2() {    
    int[] array = new int[10];
    for (int i = 0; i <= 15; i++) {
      array[i] = i;      
      System.out.println(i);
    }    
  }
}
