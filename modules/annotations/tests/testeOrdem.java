public class testeOrdem {
	int a, b, c;
	
	//@jfortes_getSequenceConstructor name = testeOrdem, args = (none), sequence = 1;
	testeOrdem(){			
		this.a = 1;
		this.b = 2;
		this.c = 3;
		this.soma();
		this.multiplicacao();
		this.resultado();
	}
	
	//@jfortes_getSequenceMethod name = resultado, args = (none), sequence = 4, sequencebyconstructor = 3;
	public int resultado(){
		int resultado;
		resultado = soma()+ multiplicacao();
		return resultado;
	}
	
	//@jfortes_getSequenceMethod name = soma, args = (none), sequence = 2, sequencebyconstructor = 1;
	public int soma(){
		int soma = a + b + c;
		return soma;
	}
	//@jfortes_getSequenceMethod name = multiplicacao, args = (none), sequence = 2, sequencebyconstructor = 2;
	public int multiplicacao(){
		int multiplicacao = a*b*c;
		return multiplicacao;
	}
	
}
