## Pathfinder: Exploring Path Diversity for Assessing Internet Censorship Inconsistency

The 41st Annual Computer Security Applications Conference (ACSAC), 2025.

### High-level Ideas

Censorship is usually mandated through nationwide policies, which results in censorship measurement studies often focusing on country-level characterization. However, it is difficult to control the routing of probing packets to trigger censorship across different networks within a country. In this study, we find that censorship mechanisms vary significantly at the ISP level and investigate Internet censorship by scrutinizing diverse censorship deployments in a country-state.

The project aims to design and implement a censorship measurement framework, `Pathfinder`, which utilizes multiple geo-distributed control servers to probe different network paths within a country. By generating traffic targeting the same domain but different control servers, we induce `path diversity` that exposes the traffic to distinct transit networks and different censorship devices, enabling a more granular analysis of censorship practices.

Our findings reveal that diverse censorship resulting from various routing paths within a country is widespread, implying (1) the implementations of centralized censorship are commonly incomplete or flawed, (2) decentralized censorship is also prevalent. Additionally, different hosting platforms contribute to inconsistent censorship behaviors due to varying peering relationships with ISPs within a country. In terms of experiments, two experiments have been launched to measure the impact of censorship inconsistency behaviors specifically on `IP Destinations` and `Hosting Platforms`. Finally, we conduct case studies via Application Traceroute to explore the configurations that lead to such inconsistencies.

### Notes for Data and Code

Relevant Dataset:
- Install Python v3.9 or newer, see <https://www.python.org/downloads/release/python-390/>
- Install required dependencies on top of each `Code` file, also fill proxy.json with required parameters. (See attached)

### Vantage Points
- SOCKS proxies: We use residential proxies to issue HTTP queries through the SOCKS proxies. In our study, we signed up for [ProxyRack](https://www.proxyrack.com/).
- VPN: We use VPN vantage points to conduct the application traceroute to investigate the deployment of censors. We signed up for [HideMyIP](https://www.hidemyip.com/).

### Control Server Configuration
The backend control servers can be any ordinary Web servers accepting HTTP requests. In our research, we set up multiple geo-distributed control servers across several cloud platforms. These servers are all configured with static payloads as ground truth that only state our experiment purpose and return all incoming requests. 

- First, we need to choose `EC2`, `VM`, or `Virtual Machine` in AWS, GCP, and Microsoft Azure cloud platforms. Then we will select Ubuntu operating system and install Apache web server with code ```sudo apt-get update``` ```sudo apt-get upgrade -y``` ```sudo apt-get install apache2```.
- Second, we need to locate the index.html file on Apache web servers and edit it with any self-defined HTML content. That is, the static payload(e.g., 'http\n') will be relayed back to the client side within HTTP responses. Don't forget to enable port 80 on control servers to receive all HTTP traffic from anywhere.

### Code Repository 
The code files given a description reflect the core functions to run the experiments(1, 2, case_studies)

- pinpoint_censor.py: Perform application traceroutes on HTTP protocol, which pinpoints the censor's location on a specific router. To prompt the code with an argument, ```sudo python3 pinpoint_censor.py http example.com serverIP >> output.json```. 
- proxyrack_request.py: Define rules/thresholds to obtain the maximum number of distinct vantage points from the proxy platform for experiment usage.
- proxyrack.py: Initial censorship measurements on HTTP protocol from residential proxies (Proxyrack) to our control servers, store proxy information and HTTP responses (e.g., static payloads from control servers or censorship).
  To prompt the code, use ```sudo python3 proxyrack.py output.json```.
- proxy.json: Store confidential information for connecting to the Proxyrack api.

### Analysis Code 
Analysis Code files aim to identify the inconsistency experienced by different paths toward different backend control servers from a vantage point.

- http_analysis.py: Analyze censorship inconsistency rate and categorize it by countries for experiment1.
- http_censorship.py: Analyze the total detected censorship and categorize it by countries for experiment1.
- http_server_censorship.py: Analyze the total detected censorship and categorize it by countries for experiment2. 
- http_suspicious_server.py: Analyze censorship inconsistency rate and categorize it by countries for experiment2. 
### Parameters
The following parameters are necessary for running the experiments:

|       Parameters        |                           Function                                     |                  Example                      |
| ----------------------- | ---------------------------------------------------------------------- | --------------------------------------------- |
| proxy_address           | connect to Proxyrack proxy api                                         |"megaproxy.rotating.proxyrack.net"             |
| proxy_port              | default port number for proxy api                                      | 22225                                         |
| username                | Proxyrack account credentials                                          |                                               |
| password                | Proxyrack account credentials                                          |                                               | 
