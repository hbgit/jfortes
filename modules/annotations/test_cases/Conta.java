public class Conta{
	String nome;
	double saldo;
	int codigo;
	
	//@jfortes_getSequenceConstructor name = Conta, args = (none), sequence = 1;
	Conta(){
		this.setSaldo(0);
	}

	//@jfortes_getSequenceConstructor name = Bag, args = (novoNome, novoSaldo), sequence = 2;
	Conta(String novoNome, double novoSaldo){
		this.setNome(novoNome);
		this.setSaldo(novoSaldo);
	}

	public String getNome(){
		return this.nome;
	}

	public void setNome(String novoNome){
		this.nome = novoNome;
	}
	
	public double getSaldo(){
		return this.saldo;
	}	

	//@jfortes_getSequenceMethod name = setSaldo, args = (novoSaldo), sequence = 2, sequencebyconstructor = 1; 
	public void setSaldo(double novoSaldo){
		this.saldo = novoSaldo;
	}
	
	public void saca(double valor){
		double temp = this.getSaldo() - valor;
		this.setSaldo(temp);
	}

	public void deposita(double valor){
		double temp = this.getSaldo() + valor;
		this.setSaldo(temp);
	}

}
