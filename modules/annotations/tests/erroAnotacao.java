public class erroAnotacao{
	String nome;
	double saldo;
	int codigo;
	
	//@jfortes_getSequenceConstructor name = Conta, args = (noe), sequence = 1;
	erroAnotacao(){
		this.setSaldo(0);
	}

	//erro
	//@jfortes_getSequenceConstructor name = Bag, args = (novoNome, novoSaldo sequence = 2;
	erroAnotacao(String novoNome, double novoSaldo){
		this.setNome(novoNome);
		this.setSaldo(novoSaldo);
	}

	//erro
	//@fortes_getSequenceM name = setSaldo, args = none, sequence = 2, sequencebyconstructor = 1;
	public String getNome(){
		return this.nome;
	}

	//erro
	//jfortes_getSequenceMethod nome = setNome, args (novoNome), sequence = 3 sequencebyconstructor = 2;
	public void setNome(String novoNome){
		this.nome = novoNome;
	}
	
	//@jfortes_getSequenceMethod name = setSaldo, args = (none), sequence = 4, sequencebyconstructor = 3;
	public double getSaldo(){
		return this.saldo;
	}	

	//erro
	//@jfortes_getSequenceMethod name = setSaldo, args = (novoSaldo), seqnce = 5, sequencebyconstructor = 4; 
	public void setSaldo(double novoSaldo){
		this.saldo = novoSaldo;
	}
	
	
	//@jfortes_getSequenceMethod name = saca, args = (valor), sequence = 6, sequencebyconstructor = 5;
	public void saca(double valor){
		double temp = this.getSaldo() - valor;
		this.setSaldo(temp);
	}

	//@jfortes_getSequenceMethod name = deposita, args = (valor), sequence = 7, sequencebyconstructor = 6;
	public void deposita(double valor){
		double temp = this.getSaldo() + valor;
		this.setSaldo(temp);
	}

}
