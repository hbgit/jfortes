/**
 * >> No Bug found in compilation
 *    $ javac Overflow_False.java -Xlint:all
 * >> Bug found in execution
 **/
 
public class Overflow_False {
	public static void main (String args[]){
		int a = 2147483647; int b = 2147483647;
		int soma = a + b;
		System.out.println(soma);
	}
	
	
}
