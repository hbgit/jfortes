/**
 * >> No Bug found in compilation
 *    $ javac Division_False.java -Xlint:all
 * >> Bug found in execution
 **/
 
public class Division_False {
	public static void main (String args[]) {
	int numA=0,numB=0,numC=0,soma;
	soma = numA + numB + numC/numA;
	System.out.println (soma);
	}
}
