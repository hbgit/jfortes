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
 * This code has a Leftover Debug Code CWE-489 vulnerability.
 * http://cwe.mitre.org
 * Basically developer can debug his code by typing "-debug"
 * but here debugging code is removed.
 */


import java.io.IOException;
import java.util.logging.Logger;


public class LeftOverDebugCode_good_489
{
	public LeftOverDebugCode_good_489()
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
			
			int nbArg = byteCount - 2;
			if ( nbArg > 1 )
			{
                if ( s.contains( "-debug" ) == true )
                {
                	final Logger user = Logger.getAnonymousLogger();
        			user.warning( "Debugging code is removed here" );
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

	
	public static void main( String[] argv )
	{
		new LeftOverDebugCode_good_489();
	}
}

//end of LeftOverDebugCode_good_489.java