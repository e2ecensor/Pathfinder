This sample data represents one of the application traceroute datasets from our case studies. 
While we run our code, pinpoint_censor.py, we must ensure that the Hide-My-IP VPN is active and stable on a specific VPN node for the entire experiment.
Our case studies are designed to trace the exact paths taken by packets.
For each complete application traceroute, a total of 12 paths are recorded.
In this example, application traceroutes are performed from a VPN node in South Korea to our control servers.
If no censorship is present along the path, the control servers return our static payloads (e.g., "http/n"), 
which are typically reflected in the "text" field of the response at the last hop.

However, if censorship is applied by the South Korean government, the requests are rerouted to a censorship server at "http://warning.or.kr" with an HTTP status code 302.
This behavior can be verified by copying this url in the "location" field and pasting it into any web browser, which will display a block page.
To this end, this sample demonstrates censorship inconsistency, as some paths encounter censorship while others do not. 
 
