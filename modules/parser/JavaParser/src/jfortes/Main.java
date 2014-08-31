package jfortes;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import org.eclipse.jdt.core.dom.AST;
import org.eclipse.jdt.core.dom.ASTParser;
import org.eclipse.jdt.core.dom.ASTVisitor;
import org.eclipse.jdt.core.dom.ChildListPropertyDescriptor;
import org.eclipse.jdt.core.dom.ChildPropertyDescriptor;
import org.eclipse.jdt.core.dom.CompilationUnit;
import org.eclipse.jdt.core.dom.FieldDeclaration;
import org.eclipse.jdt.core.dom.MethodDeclaration;
import org.eclipse.jdt.core.dom.MethodRef;
import org.eclipse.jdt.core.dom.SimpleName;
import org.eclipse.jdt.core.dom.SingleVariableDeclaration;
import org.eclipse.jdt.core.dom.VariableDeclaration;
import org.eclipse.jdt.core.dom.VariableDeclarationFragment;
import org.eclipse.jdt.core.dom.VariableDeclarationStatement;
import org.eclipse.jdt.internal.core.util.MethodInfo;
 

/**
 * 
 * This program aims to identify the attributes of the class, 
 * as well as, the method with its input args 
 * 
 * Output: CSV file
 * 
 * @author Herbert Oliveira Rocha
 *
 */


public class Main {
 
	//use ASTParse to parse string
	public static void parse(String str) {
		ASTParser parser = ASTParser.newParser(AST.JLS3);
		parser.setSource(str.toCharArray());
		parser.setKind(ASTParser.K_COMPILATION_UNIT);
 
		final CompilationUnit cu = (CompilationUnit) parser.createAST(null);
 
		cu.accept(new ASTVisitor() {
 
			Set names = new HashSet();
			Boolean isAnMethod = false; 
 
			public boolean visit(VariableDeclarationFragment node) {				
				
				SimpleName name = node.getName();
				
				if(this.isAnMethod == false){
					this.names.add(name.getIdentifier());
					//System.out.println("\t\tDeclaration of '" + name + "' at line"
					//		+ cu.getLineNumber(name.getStartPosition()));
					
					//System.out.println(">>> "+node.getParent().getClass());					
					FieldDeclaration fldDecl = (FieldDeclaration) node.getParent();
					//System.out.println(">>> "+ fldDecl.getType());
					
					System.out.println(cu.getLineNumber(name.getStartPosition()) + ";"
							          + name + ";" + "attribute" + ";" + "class" + ";" + fldDecl.getType());
					this.isAnMethod = false;
				}
				
				return false; // do not continue 
			}			
			
			
			public boolean visit(MethodDeclaration node){			
				
				//Identify if is a method
				this.isAnMethod = true;
				
//				System.out.println("Declaring method { " + node.getName() 
//						+ " } that returns [ " + node.getReturnType2()
//						+ " ] at line < "+ cu.getLineNumber(node.getStartPosition())+" >");
				
				if(node.parameters().isEmpty()){
					
					System.out.println(cu.getLineNumber(node.getStartPosition()) + ";"
					          + "0NONE" + ";" + "method" 
                  		  + ";" + node.getName() + ";" + "0NONE");
					
				}else{
					//List<String> parameters = new ArrayList<String>();
	                for (Object parameter : node.parameters()) {
	                    VariableDeclaration variableDeclaration = (VariableDeclaration) parameter;
	                    String type = variableDeclaration.getStructuralProperty(SingleVariableDeclaration.TYPE_PROPERTY)
	                            .toString();
	                    for (int i = 0; i < variableDeclaration.getExtraDimensions(); i++) {
	                        type += "[]";
	                    }
	                    
	                    System.out.println(cu.getLineNumber(node.getStartPosition()) + ";"
						          + variableDeclaration.getName().toString() + ";" + "method" 
	                    		  + ";" + node.getName() + ";" + type);
	                    
	                    //parameters.add(type);
	                }
				}

                //System.out.println("Input args from method: "+parameters);
                
				
//				SimpleName name = node.getName();
//				this.names.add(name.getIdentifier());
//				System.out.println("Method: '" + name + "' at line"
//						+ cu.getLineNumber(name.getStartPosition()));
				return true;
			}			
			
 
//			public boolean visit(SimpleName node) {
//				
//				if (this.names.contains(node.getIdentifier())) {
//					System.out.println("Usage of '" + node + "' at line "
//							+ cu.getLineNumber(node.getStartPosition()));
//				}
//				return true;
//			}
		});
 
	}
 
	//read file content into a string
	public static String readFileToString(String filePath) throws IOException {
		StringBuilder fileData = new StringBuilder(1000);
		BufferedReader reader = new BufferedReader(new FileReader(filePath));
 
		char[] buf = new char[10];
		int numRead = 0;
		while ((numRead = reader.read(buf)) != -1) {
			//System.out.println(numRead);
			String readData = String.valueOf(buf, 0, numRead);
			fileData.append(readData);
			buf = new char[1024];
		}
 
		reader.close();
 
		return  fileData.toString();	
	}
 
	//loop directory to get file list
	public static void ParseFilesInDir() throws IOException{
		File dirs = new File(".");
		String dirPath = dirs.getCanonicalPath() + File.separator+"src"+File.separator;
 
		File root = new File(dirPath);
		//System.out.println(rootDir.listFiles());
		File[] files = root.listFiles ( );
		String filePath = null;
 
		 for (File f : files ) {
			 filePath = f.getAbsolutePath();
			 if(f.isFile()){
				 parse(readFileToString(filePath));
			 }
		 }
	}
 
	public static void main(String[] args) throws IOException {
		//System.out.println(args[0]);
		
		File f = new File(args[0]);
		
		if(f.exists()){
			System.out.println("Line;Variable;From;Scope;Type");
			Main runParser = new Main();
			runParser.parse(runParser.readFileToString(args[0]));	
		}else{
			System.out.println("Sorry. We did not find the file: "+args[0]);
		}
		
			
		//ParseFilesInDir();
	}
}
