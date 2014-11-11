public class Employee {
	
  //@jfortes_attribute name = nome, from_constructors = {Employee_0}, sequence = 0;
  private String name;
  
  //@jfortes_attribute name = salary, from_constructors = {Employee_0}, sequence = 1;
  private float salary;
  
  //@ jfortes_constructor name = Employee, id = Employee_0, sequence = 0;
  public Employee(String n, float s) {
    this.setName(n);
    this.setSalary(s);
  }

  
  public String getName() {
    return name;
  }
  
  //@ jfortes_method name = setName, from_constructors = {Employee_0}, sequence = 0;
  public void setName(String newName){
	  this.name = newName;
  }

  public float getSalary() {
    return salary;
  }
  
  //@ jfortes_method name = setSalary, from_constructors = {Employee_0}, sequence = 1;
  public void setSalary(float newSalary){
	  this.salary = newSalary;
  }

  //@ jfortes_method name = raiseSalary, from_constructors = {Employee_0}, sequence = 2;
  public void raiseSalary(float byPercent) {
    float raise = salary * byPercent / 100;
    salary += raise;
  }

}
