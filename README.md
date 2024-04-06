**Automating Incident Response with Python and Azure Sentinel**

**Overview**
This Python script automates the Incident Response process by identifying infected hosts using IP addresses obtained from Azure Sentinel and then isolating these hosts by updating firewall rules.

**Prerequisites:**
Azure Setup: Ensure you have access to an Azure account with Azure Sentinel set up.
Permissions: Verify you have the necessary permissions to query Azure Sentinel and to execute commands on the network device or server.
Python Environment: Python 3.x should be installed, along with azure-identity, azure-monitor-query, and paramiko libraries.
Paramiko for SSH: Used to automate firewall rule updates on the network device or server.
Azure CLI: Recommended for local development and testing for authentication purposes.

**Installation:**

#pip install azure-identity azure-monitor-query paramiko

**Configuration:**
Azure Sentinel Workspace ID: Replace <Your-Workspace-ID> with your actual Log Analytics workspace ID associated with Azure Sentinel.
KQL Query: Customize the kql_query variable to accurately extract the infected host IPs based on your Sentinel alert schema.
SSH Connection Details: Set hostname, port, username, and password with the credentials of the network device or server where firewall rules will be updated.

**Execution:**
Run the script from your terminal:

#python3 IR_FW_Sentinel.py
