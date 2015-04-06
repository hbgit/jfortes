import java.util.Random;

public class Test5 {
	//@ jfortes_attribute name = array2d, from_constructors = {Test5_0}, sequence = {1}, line = 5;
	float[][] array2d;
	//@ jfortes_attribute name = n, from_constructors = {Test5_0}, sequence = {0}, line = 7;
	int n;
	Random gerador = new Random();
		
	//@ jfortes_constructor name = Test5, id = Test5_0, sequence = 0, line = 10;
	Test5(float[][] input){
		System.out.println("Test5 created");
		n = input.length;
		array2d = new float[n][n];
		
	}
	
	//@ jfortes_method name = preencheMat, from_constructors = {Test5_0}, sequence = {0}, line = 18;
	public void preencheMat(){
		for (int lin = 0; lin < array2d.length; lin++){  
			for (int col = 0; col < array2d[lin].length; col++){  
				array2d[lin][col] = gerador.nextInt(100);
			}
		}
	}
	
	

}
