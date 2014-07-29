
public class TesteBO {
	int numA, numB;	
	public static void main (String args[]){
		TesteBO x = new TesteBO();		
		System.out.println(x.soma(2147483647, 2147483647));
	}
	
	public int soma(int numA, int numB){
		int soma = numA + numB;
		return soma;
	};
	
	
}
