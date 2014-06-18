package good;
/* 
 * This software was developed at the National Institute of Standards and
 * Technology by employees of the Federal Government in the course of their
 * official duties. Pursuant to title 17 Section 105 of the United States
 * Code this software is not subject to copyright protection and is in the
 * public domain. NIST assumes no responsibility whatsoever for its use by
 * other parties, and makes no guarantees, expressed or implied, about its
 * quality, reliability, or any other characteristic.
 *
 * This reference program was developed in June 2009 as part of the Software
 * Assurance Metrics And Tool Evaluation (SAMATE) project.
 * We would appreciate acknowledgment if the software is used.
 * The SAMATE project website is: http://samate.nist.gov
 */

 /*
 * This code shows an exploit of an Unchecked Error Condition CWE-391 vulnerability.
 * http://cwe.mitre.org
 * A FileInputStream such as image data is tried to be created. Exceptions and
 * other error conditions are no more ignored.
 */
 
 
import java.io.*;
import java.util.logging.Logger;


public class UncheckedErrorCondition_good_391
{
	public static FileInputStream getInput( String fileName )
	{
		FileInputStream fis = null;
	
		// Try to create an FileInputStream
		try
		{
	        fis = new FileInputStream( fileName );
		}
		
		// The program checks error condition
		catch (FileNotFoundException e)
		{
			final Logger logger = Logger.getAnonymousLogger();
			String exception = "Exception " + e;
			logger.warning( exception );
		}
		
        return fis;
    }

    public static void main( String[] argv)
	{
    	String fileName = "foo.bar";
        getInput( fileName );
    }
}

// end of UncheckedException_good_391.java