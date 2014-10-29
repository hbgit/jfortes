class Pessoa{
	String nome, sexo, sobrenome;
	int idade;
	double altura, peso;
	
	//@jfortes_getSequenceConstructor name = Pessoa, args = (none), sequence = 1;
	public Pessoa(){
		nome = "";
		idade = 0;
		altura = 0.0;
		peso = 0.0;
	}
	
	//@jfortes_getSequenceConstructor name = Pessoa, args = (nome, idade), sequence = 2;
	public Pessoa(String nome, int idade){
		this.nome = nome;
		this.idade= idade;
	}
	
	//@jfortes_getSequenceConstructor name = Pessoa, args = (altura, peso), sequence = 3;
	public Pessoa(double altura, double peso){
		this.altura = altura;
		this.peso = peso;
	}

}
