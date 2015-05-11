/**
 * >> No Bug found in compilation
 * 	  $ javac ObjStack_False.java -verbose
 * >> Bug found in execution
 **/

public class ObjStack_False {
  /*@ non_null */ Object [] a;  
  int n;  //@ invariant 0 <= n & n <= 10;  

  ObjStack_False() {
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

}
