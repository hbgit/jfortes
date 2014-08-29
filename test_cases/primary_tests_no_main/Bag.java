/**
 * Running uncrustify
 * ./uncrustify -q -l C -c ben.cfg -f <program.java>
 * */

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

 }
