# BGP AS Check for Internet Traceroute

#### Description

This is a quick tool to identify BGP AS Number of a traceroute result gathering from Juniper or Cisco Network Devices.

This tools helps to identify if BGP routing path is correct for a given traffic path.

The traceroute result can be paste in a text file and the script can parse the hop ips in the traceroute and identify the BGP AS number and carrier info.

Private IPs and Unreachables will be checked and identified in the script.

#### Installation

1. Clone the Source Code

```
git clone https://github.com/sunbath/Internet_traceroute_bgp_as_check.git
```

Then you should see the cloned folder "Internet_Traceroute_Check_AS"

```
ls -al | grep "Internet_Traceroute_Check_AS"
```

2. Create a virtual environment in your local environment and activate the virtual environment

```
cd Internet_Traceroute_Check_AS
python3 -m venv venv
source Internet_Traceroute_Check_AS/bin/activate
```

3. Install the necessary packages

```
pip install -r requirements.txt
```

4. Paste your traceroute result to a text file and copy the filename for #5.

5. Run the code

```
python Internet_Traceroute_Check_AS.py --f <traceroute_filename>
```

Or if you don't 

#### Output 
```
+-----+----------------+-----------+---------------------------------------------------------+  
| Hop | IP Address     |  Country  | AS Number - Telco Info                                  |  
+-----+----------------+-----------+---------------------------------------------------------+  
|  1  | *              |    N/A    | N/A (Non-Public IP)                                     |  
|  2  | 121.244.40.162 |   India   | AS4755 TATA Communications formerly VSNL is Leading ISP |  
|  3  | 172.17.169.202 |    N/A    | N/A (Non-Public IP)                                     |  
|  4  | 180.87.36.9    |   India   | AS6453 TATA COMMUNICATIONS (AMERICA) INC                |  
|  5  | 180.87.36.83   |   India   | AS6453 TATA COMMUNICATIONS (AMERICA) INC                |  
|  6  | 180.87.12.2    | Singapore | AS6453 TATA COMMUNICATIONS (AMERICA) INC                |  
|  7  | 116.0.93.168   | Hong Kong | AS6453 TATA COMMUNICATIONS (AMERICA) INC                |  
|  8  | 116.0.93.145   | Hong Kong | AS6453 TATA COMMUNICATIONS (AMERICA) INC                |  
|  9  | 134.159.128.5  | Hong Kong | AS4637 Telstra Global                                   |  
|  10 | 134.159.145.61 | Hong Kong | AS4637 Telstra Global                                   |  
|  11 | 202.84.157.38  | Hong Kong | AS4637 Telstra Global                                   |  
|  12 | 202.84.249.14  | Hong Kong | AS4637 Telstra Global                                   |  
|  13 | 42.99.163.9    |   Japan   | AS4637 Telstra Global                                   |  
|  14 | 10.249.92.230  |    N/A    | N/A (Non-Public IP)                                     |  
+-----+----------------+-----------+---------------------------------------------------------+ 
```