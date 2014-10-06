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

	//@jfortes_getSequenceMethod name = setSaldo, args = (none), sequence = 3, sequencebyconstructor = 1;
	public String getNome(){
		return this.nome;
	}

	//@jfortes_getSequenceMethod name = setNome, args = (novoNome), sequence = 4, sequencebyconstructor = 2;
	public void setNome(String novoNome){
		this.nome = novoNome;
	}
	
	//@jfortes_getSequenceMethod name = setSaldo, args = (none), sequence = 5, sequencebyconstructor = 3;
	public double getSaldo(){
		return this.saldo;
	}	

	//@jfortes_getSequenceMethod name = getSaldo, args = (novoSaldo), sequence = 6, sequencebyconstructor = 4; 
	public void setSaldo(double novoSaldo){
		this.saldo = novoSaldo;
	}
	
	
	//@jfortes_getSequenceMethod name = saca, args = (valor), sequence = 7, sequencebyconstructor = 5;
	public void saca(double valor){
		double temp = this.getSaldo() - valor;
		this.setSaldo(temp);
	}

	//@jfortes_getSequenceMethod name = deposita, args = (valor), sequence = 8, sequencebyconstructor = 6;
	public void deposita(double valor){
		double temp = this.getSaldo() + valor;
		this.setSaldo(temp);
	}

}
