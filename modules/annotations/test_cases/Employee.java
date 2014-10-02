//sem anotações no construtor

class Employee {
	
  private String name;

  private double salary;
  
  public Employee(String n, double s) {
    name = n;
    salary = s;
  }

  //@jfortes_getSequenceMethod name = getName, args = (none), sequence = 2, sequencebyconstructor = 1;
  public String getName() {
    return name;
  }

  //@jfortes_getSequenceMethod name = getSalary, args = (none), sequence = 3, sequencebyconstructor = 2;
  public double getSalary() {
    return salary;
  }

  //@jfortes_getSequenceMethod name = raiseSalary, args = (byPercent), sequence = 4, sequencebyconstructor = 3;
  public void raiseSalary(double byPercent) {
    double raise = salary * byPercent / 100;
    salary += raise;
  }

}
