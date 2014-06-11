package bad;
/* This software was developed at the National Institute of Standards and
 * Technology by employees of the Federal Government in the course of their
 * official duties. Pursuant to title 17 Section 105 of the United States
 * Code this software is not subject to copyright protection and is in the
 * public domain. NIST assumes no responsibility whatsoever for its use by
 * other parties, and makes no guarantees, expressed or implied, about its
 * quality, reliability, or any other characteristic.
 * We would appreciate acknowledgement if the software is used.
 * The SAMATE project website is: http://samate.nist.gov
 */

/*
 * This servlet implements a Cross-Site Scripting vulnerability (XSS)
 * Parameters:
 *   - data: source of the vulnerability
 * Example:
 *   - url: http://server_address/path_to_servlet/CrossSiteScripting_080?data=<script>alert('XSS');</script>
 */

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.ServletOutputStream;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class CrossSiteScripting_080 extends HttpServlet
{
	private static final long serialVersionUID = 1L;
       
    public CrossSiteScripting_080()
    {
        super();
    }

    // Method which will be called to handle HTTP GET requests
	protected void doGet( HttpServletRequest req, HttpServletResponse resp )
		throws ServletException, IOException
	{
		// Prepare the output data that will be sent back to the client
		resp.setContentType( "text/html" );
		ServletOutputStream out = resp.getOutputStream();
		
		// Write the HTML document to the output stream.
		// Note that the data provided by the client in the field "data"
		// is written as is, without any filtering, to the output document.
		// Hence the vulnerability.
		out.println( "<html><body><blockquote><pre>" );
		
		// BUG
		// Cross Site Scripting
		out.println( req.getParameter( "data" ) );
		out.println( "</pre></blockquote></body></html>" );
	}

	protected void doPost(HttpServletRequest request, HttpServletResponse response)
		throws ServletException, IOException
	{
	}
}
