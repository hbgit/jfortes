class Bag {
	int[] a;
  	int n;

  	Bag(int[] input) {
    		n = input.length; a = new int[n];
    		System.arraycopy(input, 0, a, 0, n);
  	}

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
	public static void main(String[] args){
		// int[] b = new int [Cute.input.Integer()];
		Bag x = Bag(Cute.input.Object());
		//(Bag)Cute.input.Object(b);
		System.out.println(x.extractMin());
	}
 
}

