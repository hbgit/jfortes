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
 * This code has a Time-of-Check Time-of-Use (TOCTOU) CWE-367 vulnerability.
 * http://cwe.mitre.org
 * It checks the state of the file myfile.txt, but its state can change
 * with the function sleep, but is verified before using it.
 */


import java.io.*;
import java.util.logging.Logger;


public class TimeOfCheckTimeOfUse_good_367
{
	public TimeOfCheckTimeOfUse_good_367()
	{
		try
		{
			// Try to open the given file
			File f = new File( "Z:/TCG_Java_Test_Cases/367_TOCTOU_java/myfile.txt" );
			
		    if( f.canWrite() == false )
		    {
		    	// Try to cause the currently executing thread to sleep
		    	try
		    	{
					// The state of the file may change in the meantime
		    		Thread.sleep( 1000 );
		    	}
			    catch (InterruptedException e)
			    {
			    	final Logger logger = Logger.getAnonymousLogger();
					String exception = "Exception " + e;
					logger.warning( exception );
			    }
			    
			    // Verify the state hasn't changed
			    if( f.canWrite() == false )
			    {
					// Create the file if it didn't exist before the sleep function
			    	FileWriter fw = new FileWriter( f );
			    	fw.close();
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
	
	public static void main( String argv[] )
	{
	    new TimeOfCheckTimeOfUse_good_367();
	}
}

//end of TimeOfCheckTimeOfUse_good_367.java