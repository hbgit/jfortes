public class ModifiesWarning {
	int i;
	
	//@ assignable i;
	void m(/*non_null */ ModifiesWarning o) {
		i = 1;
		o.1 = 2; // Modifies warning
	}	
}
