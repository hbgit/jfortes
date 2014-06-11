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
 * This code has a Hard-Coded Incoming Password CWE-259 vulnerability.
 * http://cwe.mitre.org
 * The password to know if the user is authorized to do high-level work 
 * ("admin"), is built into the code. 
 * The problems are that the password can be read from a copy of the
 * byte code, the password cannot be easily changed, and every copy
 * of the code uses the same password.
 */


import java.io.*;
import java.util.logging.Logger;


public class HardCodedPassword_259
{
	public  HardCodedPassword_259()
	{
		byte inputBuffer[] = new byte[ 128 ];
		try
		{
			// Read data from the standard input
			int byteCount = System.in.read( inputBuffer );
			
			// Check whether data has been read or not
			if( byteCount <= 0 )
			{
		      return;
		    }
			
			// Turn data into a String
		    String s = new String( inputBuffer );
		    s = s.substring( 0, byteCount-2 );		    
		    
			// BUG 
			// The password to grant access is here in the code: admin
		    if( ( s.equals( "admin" ) ) == true )
		    {
		    	highlevel_authorized( s );
		    }
		}
		catch ( IOException e )
		{
			final Logger logger = Logger.getAnonymousLogger();
        	String exception = "Exception " + e;
        	logger.warning( exception );
		}
	}
	   
	static    int  highlevel_authorized( String parm )
	{
	    // This user is authorized to do high level work
	    return 1;
	}
	
	public static void main( String[] argv )
	{
		new HardCodedPassword_259();
	}
}

// end of HardCodedPassword_259.java