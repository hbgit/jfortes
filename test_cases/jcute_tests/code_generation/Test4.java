import java.util.Random;  

public class Test4{
	int[][] array2d;
	Random gerador = new Random();

	
	Test4(int len){
		this.array2d = new int[len][len];
		System.out.println("Test4 created");
	}
	
	public void preencheMat(){
		for (int lin = 0; lin < array2d.length; lin++){  
			for (int col = 0; col < array2d[lin].length; col++){  
				array2d[lin][col] = gerador.nextInt(100);
			}
		}
	}
	
	public void printMat(){
		for (int lin = 0; lin < array2d.length; lin++){  
			for (int col = 0; col < array2d[lin].length; col++){
				System.out.print(array2d[lin][col] + " ");
			}
			System.out.println("");
		}
	}
	
	
	public static void main(String[] args){
		Test4 obj = new Test4(3);
		obj.preencheMat();
		obj.printMat();
	
	}
}
