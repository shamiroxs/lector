import subprocess
import random

def get_active_wifi_name(interface="wlan0"):
    """
    Get the name of the WiFi network currently connected to the specified interface.
    """
    try:
        # Use nmcli to fetch details of the active connection
        result = subprocess.run(
            ["nmcli", "-t", "-f", "NAME,DEVICE", "connection", "show", "--active"],
            stdout=subprocess.PIPE,
            text=True,
            check=True
        )
        active_connections = result.stdout.strip().split("\n")
        for connection in active_connections:
            name, device = connection.split(":")
            if device == interface:
                return name
    except subprocess.CalledProcessError as e:
        print(f"Error getting active WiFi name: {e}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
    return None

def set_random_ip(connection_name, interface, gateway="192.168.43.1"):
    """
    Set a random IP address for the given WiFi connection.
    """
    random_ip = f"192.168.43.{random.randint(2, 254)}"
    command = [
        "nmcli", "connection", "modify",
        connection_name,
        "ipv4.addresses", f"{random_ip}/24",
        "ipv4.gateway", gateway,
        "ipv4.method", "manual"
    ]
    
    try:
        subprocess.run(command, check=True)
        print(f"Successfully set IP address to {random_ip} for connection '{connection_name}'.")
        subprocess.run(["nmcli", "connection", "down", connection_name], check=True)
        subprocess.run(["nmcli", "connection", "up", connection_name], check=True)
        print(f"Connection '{connection_name}' restarted successfully.")
        
        # After setting the random IP, run `sudo dhclient wlan0`
        subprocess.run(["sudo", "dhclient", interface], check=True)
        print(f"Executed 'sudo dhclient {interface}' to renew IP address.")
        
    except subprocess.CalledProcessError as e:
        print(f"Error executing nmcli or dhclient: {e}")
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")

if __name__ == "__main__":
    interface = "wlan0"
    
    connection_name = get_active_wifi_name(interface)
    if connection_name:
        print(f"Active WiFi connection: {connection_name}")
        
        subprocess.run(["sudo", "dhclient", "-r", interface], check=True)
        print("Released the current IP address.")
        
        set_random_ip(connection_name, interface)
    else:
        print("No active WiFi connection found on the specified interface.")

