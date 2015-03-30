import java.util.Random;

public class Test5 {
	float[][] array2d;
	int n;
	
	Test5(float[][] input){
		System.out.println("Test5 created");
		n = input.length;
		array2d = new float[n][n];
		
	}
	
	public void preencheMat(){
		for (int lin = 0; lin < array2d.length; lin++){  
			for (int col = 0; col < array2d[lin].length; col++){  
				array2d[lin][col] = gerador.nextInt(100);
			}
		}
	}
	
	

}
