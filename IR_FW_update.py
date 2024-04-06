import subprocess
import paramiko
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient
from datetime import timedelta

def get_infected_ips_from_azure_sentinel(workspace_id, kql_query):
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    response = client.query_workspace(workspace_id, kql_query, timespan=timedelta(days=1))
    
    infected_ips = []
    for table in response.tables:
        for row in table.rows:
            infected_ips.append(row[0])  # Assuming the first column contains the IP addresses
    
    return infected_ips

def isolate_host(hostname, port, username, password, infected_host_ip):
    isolation_rule = f"iptables -A INPUT -s {infected_host_ip} -j DROP"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, port=port, username=username, password=password)
    ssh.exec_command(isolation_rule)
    ssh.close()
    print(f"Isolation rule applied for {infected_host_ip}.")

if __name__ == "__main__":
    # Azure Sentinel Workspace Configuration
    workspace_id = '<Your-Workspace-ID>'
    # Sample KQL query. Customize it to your needs to find alerts with IPs
    kql_query = """
    SecurityAlert
    | where TimeGenerated > ago(1d)
    | extend HostIP = parse_json(Entities).Address
    | where HostIP != ""
    | take 1
    """
    
    # Network device or server for SSH connection to update firewall rules
    hostname = '192.168.1.1'  # Example IP
    port = 22
    username = 'admin'
    password = 'your_password'

    # Retrieve infected IPs from Azure Sentinel
    infected_ips = get_infected_ips_from_azure_sentinel(workspace_id, kql_query)

    # Isolate each infected host
    for ip in infected_ips:
        isolate_host(hostname, port, username, password, ip)
