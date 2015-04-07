//attributes values in constructors
//no annots for attributes

public class Test {
	int[] a;
	int n;
    
    
    //@ jfortes_constructor name = Test, id = Test_0, sequence = {0}, line = 18;     
	Test (int[] input, boolean name) {
        System.out.println("In Test: "+name);
		n = input.length;
		a = new int[n];
		System.arraycopy(input, 0, a, 0, n);
	}
	

	//@ jfortes_constructor name = Test, id = Test_1, sequence = {1}, line = 26; 
	Test (int[] input2) {
        System.out.println("In default Test");
		n = input2.length;
		a = new int[n];
		System.arraycopy(input2, 0, a, 0, n);
	}    
    

	//@ jfortes_method name = extractMin, from_constructors = {Test_0}, sequence = {0}, line = 34; 
	public int extractMin() {
		int z, x, k;
		int m = Integer.MAX_VALUE;
		int mindex = 0;
		for (int i = 1; i <= n; i++) {
			if (a[i] < m) {
				mindex = i;
				m = a[i];
			}
		}
		n--;
		a[mindex] = a[n];
		return m;
	}
    
    //@ jfortes_method name = printN, from_constructors = {Test_0,Test_1}, sequence = {1, 0}, line = 50; 
    public void printN(){
        System.out.println(this.n);
    }
	
}
