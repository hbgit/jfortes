public class Bank{
	
	//@jfortes_attribute name = nome, from_constructors = {Bank_0}, sequence = 0;
	String nome;
	//@jfortes_attribute name = saldo, from_constructors = {Bank_0}, sequence = 1;
	float saldo;
	//@jfortes_attribute name = codigo, from_constructors = {Bank_0}, sequence = 2;
	int codigo;
	
	//@ jfortes_constructor name = Bank, id = Bank_0, sequence = 0;
	Bank(){
		this.deposita(30);
	}
	
	//@ jfortes_constructor name = Bank, id = Bank_1, sequence = 0;
	Bank(String novoNome, float novoSaldo){
		this.setSaldo(novoSaldo);
		this.setNome(novoNome);
	}
	
	
	public String getNome(){
		return this.nome;
	}
	
	//@ jfortes_method name = setNome, from_constructors = {Bank_1}, sequence = 0;
	public void setNome(String novoNome){
		this.nome = novoNome;
	}
	
	public float getSaldo(){
		return this.saldo;
	}
	
	//@ jfortes_method name = setSaldo, from_constructors = {Bank_0, Bank_1}, sequence = 0;
	public void setSaldo(float novoSaldo){
		this.saldo = novoSaldo;
	}
	
	public void saca(float valor){
		float temp = this.getSaldo() - valor;
		this.setSaldo(temp);
	}
	
	//@ jfortes_method name = deposita, from_constructors = {Bank_0, Bank_1}, sequence = 1;
	public void deposita(float valor){
		float temp = this.getSaldo() + valor;
		this.setSaldo(temp);
	}
}
