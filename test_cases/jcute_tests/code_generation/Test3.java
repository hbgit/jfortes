public class Test3{
	int[] array;
	float attr1
	int attr2;
	
	Test3(int len){
		this.array = new int[len];
	}
	
	Test3(int[] input, String name) {
        System.out.println("In Test3: "+name);
		attr2 = input.length;
		array = new int[attr2];
		System.arraycopy(input, 0, a, 0, n);
	}
	
	public static int maior(int[] a){
		int max = a[0];
		for(int i = 1; i < a.length; i++){
		  if(a[i] > max){
			max = a[i];
		  }
		}
		
		return max;
	}
	
	

}
