public class Test3{
	
	//@ jfortes_attribute name = array, from_constructors = {Test3_0, Test3_1}, sequence = {0, 1}, line = 4;
	int[] array;
	
	float attr1;
	
	//@ jfortes_attribute name = attr2, from_constructors = {Test3_1}, sequence = {0}, line = 9;
	int attr2;
	
	//@ jfortes_constructor name = Test3, id = Test3_0, sequence = 0, line = 13;
	Test3(int len){
		this.array = new int[len];
	}
	
	//@ jfortes_constructor name = Test3, id = Test3_1, sequence = 1, line = 18;
	Test3(int[] input, String name) {
        System.out.println("In Test3: "+name);
		attr2 = input.length;
		array = new int[attr2];
		System.arraycopy(input, 0, array, 0, attr2);
	}
	
	//@ jfortes_method name = maior, from_constructors = {Test3_1}, sequence = {0}, line = 26;
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
