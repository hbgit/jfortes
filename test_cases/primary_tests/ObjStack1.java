class ObjStack {
  /*@ non_null */ Object [] a;  
  int n;  //@ invariant 0 <= n & n <= 10;  

  ObjStack() {
    n = 0;
    a = new Object[10];
  }

  //@ requires n < 10;
  void Push(Object o) {
    a[n++] = o;
  }

  //@ requires n > 0;
  Object Pop() {
    Object o = a[--n];
    a[n] = null;
    return o;
  }
  public static void main (String args[]){
	ObjStack x = new ObjStack();
    Object[] value = new Object[5];
    value[0] = value;
	x.Push(value);
	x.Pop();
  }

}
