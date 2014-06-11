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
 * We would appreciate acknowledgement if the software is used.
 * The SAMATE project website is: http://samate.nist.gov
 */

/*
 * This code shows an exploit of an Unrestricted Lock on Critical Resource CWE-412
 * vulnerability. http://cwe.mitre.org
 * Suppose the file /tmp/resourceLock is used as a resource lock. This program grabs
 * the lock (if available), but doesn't release it. Other processes that use the lock
 * will be delayed or stopped, and there is nothing they can do about it.
 */


import java.io.*;
import java.util.logging.Logger;


public class UnrestrictedLockOnCriticalResource_412
{
	public UnrestrictedLockOnCriticalResource_412()
	{
		try
		{
			// Try to create a file, which is used as a resource lock.
			FileWriter fw = new FileWriter("/tmp/resourceLock");
			
			// BUG
			// fw is not released for unrestricted lock on critical resource
		}
		catch (IOException e)
		{
	    	final Logger logger = Logger.getAnonymousLogger();
			String exception = "Exception " + e;
			logger.warning( exception );
	    }
		
	}
	
	public static void main( String[] argv )
	{
		new UnrestrictedLockOnCriticalResource_412();
	}
}

//end of UnrestrictedLockOnCriticalResource_412.java