public class Test2{
	
	//@ jfortes_attribute name = attr1, from_constructors = {Test2_0, Test2_1}, sequence = {0, 0}, line = 4;
	float[] attr1;
	
	//@ jfortes_attribute name = attr2, from_constructors = {Test2_0, Test2_1}, sequence = {1, 1}, line = 7;
	int attr2;
	
	//@ jfortes_constructor name = Test2, id = Test2_0, sequence = 0, line = 10;
	Test2(float[] input){
		System.out.println("object created");
		this.attr2 = input.length;
		this.attr1 = new float[attr2];	
	}
	
	//@ jfortes_constructor name = Test2, id = Test2_1, sequence = 1, line = 17;
	Test2(){
		System.out.println("object created");
		this.attr1 = new float[this.attr2];
	}
	
	//@ jfortes_method name = addition, from_constructors = {Test2_0}, sequence = {0}, line = 23; 
	public int addition(int num){
		int sum = attr2 + num;
		return sum;
	}
	
	//@ jfortes_method name = printAttr2, from_constructors = {Test2_0, Test2_1}, sequence = {1, 0}, line = 29; 
	public void printAttr2(){
		System.out.println(this.attr2);
	}

}
