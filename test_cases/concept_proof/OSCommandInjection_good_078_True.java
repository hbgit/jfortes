// from samate-2014-04-29-17-02-55/testcases/000/002/110
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
 * This code implements an OS Command Injection CWE-78 vulnerability.
 * http://cwe.mitre.org
 * It tries to execute a system command which is read in the inputBuffer
 * and checked for a valid operating system command.
 */


import java.io.*;
import java.util.logging.Logger;

public class OSCommandInjection_good_078_True
{
	public OSCommandInjection_good_078_True()
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

			// Turn data into a String and build a process
			String command = new String( inputBuffer );
			command = command.substring( 0, byteCount-2 );
			ProcessBuilder p = new ProcessBuilder( command );
			
			// The function start checks that the command is
			// a valid operating system command
			p.start();
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
		new OSCommandInjection_good_078_True();
	}
}

// end of OSCommandInjection_good_078.java
