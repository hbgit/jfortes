/**
 * >> No Bug found in compilation
 * 	  $ javac ObjStack_False.java -verbose
 * >> Bug found in execution
 **/

public class ObjStack_False {
  /*@ non_null */ Object [] a;  
  int n;  //@ invariant 0 <= n & n <= 10;  

  //@ jfortes_constructor name = ObjStack_False, id = ObjStack_False_0, sequence = 0, line = 12;
  ObjStack_False() {
    n = 0;
    a = new Object[10];
  }

  //@ requires n < 10;
  	//@ jfortes_method name = Push, from_constructors = {ObjStack_False_0}, sequence = {0}, line = 19; 
  void Push(Object o) {
    a[n++] = o;
  }

  //@ requires n > 0;]
  //@ jfortes_method name = Pop, from_constructors = {ObjStack_False_0}, sequence = {1}, line = 25; 
  Object Pop() {
    Object o = a[--n];
    a[n] = null;
    return o;
  }

}
