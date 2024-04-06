import paramiko

def isolate_host(hostname, port, username, password, infected_host_ip, firewall_config_path="/home/kali/IR/firewall_rules.txt"):
    """
    Isolates the infected host by updating the firewall rules via SSH.
    
    :param hostname: The hostname or IP address of the network device or server.
    :param port: The SSH port number.
    :param username: The SSH username.
    :param password: The SSH password.
    :param infected_host_ip: The IP address of the infected host to be isolated.
    :param firewall_config_path: Path to the firewall configuration file.
    """
    # SSH command to update the firewall rules to isolate the infected host
    isolation_rule = f"iptables -A INPUT -s {infected_host_ip} -j DROP && iptables -A OUTPUT -d {infected_host_ip} -j DROP"
    
    try:
        # Establishing an SSH session
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, port=port, username=username, password=password)
        
        # Updating the firewall rules
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(isolation_rule)
        print(f"Isolation rule applied for {infected_host_ip}. Output: {ssh_stdout.read().decode('utf-8')}")
        
        # Optionally, save or update a local firewall configuration file with the new rule
        with open(firewall_config_path, 'a') as file:
            file.write(f"{isolation_rule}\n")
        
        # Closing the SSH session
        ssh.close()
        
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    # Replace these variables with your actual network device or server details and the infected host IP
    hostname = '192.168.1.1'  # Network device or server IP
    port = 22  # SSH port
    username = 'admin'  # SSH username
    password = 'your_password'  # SSH password
    infected_host_ip = '192.168.1.100'  # Infected host IP
    
    # Call the function to isolate the infected host
    isolate_host(hostname, port, username, password, infected_host_ip)
