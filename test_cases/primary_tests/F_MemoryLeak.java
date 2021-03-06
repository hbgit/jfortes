/*
Se uma pilha cresce e encolhe, os objetos que foram tirados 
da pilha n�o v�o ser lixo coletado, mesmo que o programa usando 
a pilha n�o tenha mais refer�ncias � eles. Isto � porque a pilha
mant�m refer�ncias obsoletas para estes objetos. Uma refer�ncia 
obsoleta � simplesmente uma refer�ncia que nunca ser� desreferenciado novamente. 
Neste caso, as refer�ncias fora da "parte ativa" do elemento de matriz est�o obsoletos. 
A parte ativa � constitu�da pelos elementos cujo �ndice � menor do que o tamanho.
 */
import java.io.*;
		
		public class MemoryLeak
		{
		    private static final int CAPACITY = 50;
		    private static final int HALF_CAPACITY = CAPACITY/2;
		
		    public static void main(String[] args) throws IOException
		    {
		        System.out.print("Press any key to start memory leak scenario... ");
		        InputStreamReader reader = new InputStreamReader(System.in);
		        reader.read();
		        System.out.println();
		        Stack stack = new Stack(CAPACITY);
		        for (int i = 0; i < CAPACITY; ++i)
		        {
		            stack.push(new Object());
		            System.out.println("Foi inserido um n�mero!");
		        }
		        for (int i = 0; i < HALF_CAPACITY; ++i)
		        {
		            stack.pop();
		        }
		        System.out.print("Press any key to stop memory leak scenario... ");
		        reader.read();
		        reader.read();
		    }
		}
		
		class Stack
		{
		    private Object[] elements;
		    private int size = 0;
		    public Stack(int initialCapacity)
		    {
		        this.elements = new Object[initialCapacity];
		    }
		
		    public void push(Object e)
		    {
		        ensureCapacity();
		        elements[size++] = e;
		    }
		
		    public Object pop()
		    {
		        if (size > 0)
		        {
		            return elements[--size]; // MEMORY LEAK
		        }
		        return null;
		    }
		
		    /**
		    * Ensure space for at least one more element, roughly
		    * doubling the capacity each time the array needs to grow.
		    */
		    private void ensureCapacity()
		    {
		        if (elements.length == size)
		        {
		            Object[] oldElements = elements;
		            elements = new Object[2 * elements.length + 1];
		            System.arraycopy(oldElements, 0, elements, 0, size);
		        }
		    }
		}