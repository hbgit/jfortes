public class Test2{
	float[] attr1;
	int attr2;
	
	Test2(float[] input){
		System.out.println("object created");
		this.attr2 = input.length;
		this.attr1 = new float[attr2];	
	}
	
	Test2(){
		System.out.println("object created");
		this.attr1 = new float[this.attr2];
	}
	
	public int addition(int num){
		int sum = attr2 + num;
		return sum;
	}
	
	public void printAttr2(){
		System.out.println(this.attr2);
	}

}
