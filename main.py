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

def get_country(ip):
    try:
        response = requests.get(f"http://ipinfo.io/{ip}/country")
        country = response.text.strip()
        return country
    except Exception as e:
        print("Exception occurred (COUNTRY NAME):", e)
        return None

def save_to_file(content):
    try:
        with open("skrypt_log.txt", "a") as file:
            file.write(content + "\n")
        print("Saved to file.")
    except Exception as e:
        print("Error in saving to file: ", e)

if __name__ == "__main__":
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%d-%m-%Y | %H:%M")

    ip = get_ip_address()
    hostname = get_hostname()
    os_name, os_version = get_os_info()
    country = get_country(ip)

    log_content = "Date: " + formatted_time + "\n"

    if ip:
        log_content += "IP Address: " + ip + "\n"
    else:
        log_content += "IP Address: NONE\n"

    if hostname:
        log_content += "PC Hostname: " + hostname + "\n"
    else:
        log_content += "PC Hostname: NONE\n"

    if os_name:
        log_content += "OS: " + os_name + " " + os_version +"\n"
    else:
        log_content += "OS: NONE\n"

    if country:
        log_content += "Country: NONE\n"
        # log_content += "Country: " + country + "\n"
    else:
        log_content += "Country: NONE\n"

    print(log_content)
    save_to_file(log_content)