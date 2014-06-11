public class PrePost {
	//@ requires i >= 0;
	//@ ensures \result == i;
	public int m(int i);
	//@ ensures \result > 0;
	public int mm() {
        // Pre warning - argument must be >= 0
		int j = m(-1); 
	}
	//@ ensures \result > 0;
	public int mmm() {
		int j = m(0);
		return j;
	} // Post warning - result is 0 and should be > 0
}
