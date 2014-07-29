
public class Division {
	int numA,numB,numC;
	double soma;
	public static void main (String args[]) {
		Division calc = new Division();
		System.out.println(calc.soma(0, 0, 0));
	}

	public double soma (int numA, int numB, int numC){
		soma = numA + numB + numC/numA;
		return soma;		
	}
}
