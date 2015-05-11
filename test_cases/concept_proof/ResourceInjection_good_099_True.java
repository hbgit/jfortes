// from samate-2014-04-29-17-02-55/testcases/000/002/114
//package good;
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
 * It creates a file with the data read after filtering, which would allow, for
 * instance "admin.dat"!
 */


import java.io.*;
import java.util.logging.Logger;

public class ResourceInjection_good_099_True
{
	// Table of allowed files to use
	final String allowed_tab[] = { "users_site.dat", "users_reg.dat", 
			"users_info.dat", "admin.dat", "services.dat.cxx"};
	 
	// Function to check if the current file takes part of the allowed ones
	public boolean allowed( String in )
	{
		boolean bool = false;
		
        for( int i = 0; i < 5; i++ )
        {
            if( in.equals( allowed_tab[i] ) )
            {
              	// the current file is allowed to use
                bool = true;
                break;
            }
        }
        return bool;
	}
	
	public ResourceInjection_good_099_True()
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

			if( allowed( s ) == true )
	        {
				// The current file is allowed to use so we can create 
				// a FileOutputStream from it
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
			else
				return;
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
		new ResourceInjection_good_099_True();
	} 
}

//end of ResourceInjection_good_099.java
