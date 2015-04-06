import java.util.Random;  

public class Test4{
	
	//@ jfortes_attribute name = array2d, from_constructors = {Test4_0}, sequence = {0}, line = 6;
	int[][] array2d;
	Random gerador = new Random();

	
	//@ jfortes_constructor name = Test4, id = Test4_0, sequence = 0, line = 11;	
	Test4(int len){
		this.array2d = new int[len][len];
		System.out.println("Test4 created");
	}
	
	//@ jfortes_method name = preencheMat, from_constructors = {Test4_0}, sequence = {0}, line = 17;
	public void preencheMat(){
		for (int lin = 0; lin < array2d.length; lin++){  
			for (int col = 0; col < array2d[lin].length; col++){  
				array2d[lin][col] = gerador.nextInt(100);
			}
		}
	}
	
	//@ jfortes_method name = printMat, from_constructors = {Test4_0}, sequence = {1}, line = 26;
	public void printMat(){
		for (int lin = 0; lin < array2d.length; lin++){  
			for (int col = 0; col < array2d[lin].length; col++){
				System.out.print(array2d[lin][col] + " ");
			}
			System.out.println("");
		}
	}
	
}
