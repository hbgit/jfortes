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
 * This code has a Resource Injection CWE-99 vulnerability. http://cwe.mitre.org
 * It creates a file with the data read without filtering, which would allow, for
 * instance "/etc/passwd"!
 */


import java.io.*;
import java.util.logging.Logger;


public class ResourceInjection_099
{
	public ResourceInjection_099()
	{
		byte inputBuffer[] = new byte[ 128 ];
		
		// Data to write
		byte data[] = { 1,0,1,1,1,1,1,1,0,0,0,0 };

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
			
			// Create a file from the inputBuffer, but
			// there is no filtering!
			// BUG
			FileOutputStream f = new FileOutputStream( s );

			try
			{
				// Try to write data in the file
				f.write( data );
			}
			catch( IOException e )
			{
				final Logger logger = Logger.getAnonymousLogger();
				String exception = "Exception " + e;
				logger.warning( exception );
			}

			f.close();
		}
		catch( IOException e )
		{
			final Logger logger = Logger.getAnonymousLogger();
			String exception = "Exception " + e;
			logger.warning( exception );
		}
	}

	public static void main( String[] argv )
	{
		new ResourceInjection_099();
	}
}

// end of ResourceInjection_099.java