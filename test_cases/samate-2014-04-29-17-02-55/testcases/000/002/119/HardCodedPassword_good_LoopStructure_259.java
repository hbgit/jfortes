package goodCodeComplexity;
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
 * This code has a Hard-Coded Incoming Password CWE-259 vulnerability, and a
 * Loop Structure complexity. http://cwe.mitre.org
 * The password to know if the user is authorized to do high-level work 
 * is verified by checking the matching with the username.
 */


import java.io.IOException;
import java.util.logging.Logger;

public class HardCodedPassword_good_LoopStructure_259
{
	public HardCodedPassword_good_LoopStructure_259()
	{
		for ( int i = 0; i < 3; i++ )
		{
		
			byte inputBuffer[] = new byte[ 128 ];
			try
			{
				// Read data from the standard input of this form:
				// "username password" separate by a space
				int byteCount = System.in.read( inputBuffer );
	
				// Check whether data has been read or not
				if( byteCount <= 0 )
				{
					return;
				}
	
				// Turn data into a String
				String s = new String( inputBuffer );
				s = s.substring( 0, byteCount-2 );
				String[] tab = s.split(" ");
				
				if ( tab.length > 1 )
				{
					// Check if the username and userpass match to grant access
					if (user_ok(tab[0], tab[1]) == true )
					{
						highlevel_authorized( s );
						break;
					}
				}
			}
			catch ( IOException e )
			{
				final Logger logger = Logger.getAnonymousLogger();
				String exception = "Exception " + e;
				logger.warning( exception );
			}
		}
	}
	
	String getUserPassword( String username )
	{
        String pass = null;
        // get the system password or do a query etc.
        return pass;
	}
	 
	boolean user_ok( String username, String userpass )
	{
		// Check if username and userpass match together
	    if ( userpass.equals(getUserPassword(username)) )
	       	return true;
	    else
	       	return false;
	}
	
	static int highlevel_authorized( String parm )
	{
	    // This user is authorized to do high level work
	    return 1;
	}
	
	public static void main( String[] argv )
	{
		new HardCodedPassword_good_LoopStructure_259();
	}
}

//end of HardCodedPassword_good_LoopStructure_259.java