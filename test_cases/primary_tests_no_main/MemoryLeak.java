/*
Se uma pilha cresce e encolhe, os objetos que foram tirados 
da pilha não vão ser lixo coletado, mesmo que o programa usando 
a pilha não tenha mais referências à eles. Isto é porque a pilha
mantém referências obsoletas para estes objetos. Uma referência 
obsoleta é simplesmente uma referência que nunca será desreferenciado novamente. 
Neste caso, as referências fora da "parte ativa" do elemento de matriz estão obsoletos. 
A parte ativa é constituída pelos elementos cujo índice é menor do que o tamanho.
 */
import java.io.*;
		
		public class MemoryLeak
		{
		    private static final int CAPACITY = 50;
		    private static final int HALF_CAPACITY = CAPACITY/2;
		
		    
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
