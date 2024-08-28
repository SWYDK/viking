import requests

def send_sms_smsc(login, password, phones, message):
    url = "https://smsc.ru/sys/send.php"
    payload = {
        "login": login,
        "psw": password,
        "phones": phones,
        "mes": message
    }
    
    response = requests.get(url, params=payload)
    
    if response.status_code == 200:
        print("SMS sent successfully!")
        print("Response:", response.text)
    else:
        print(f"Failed to send SMS. Status code: {response.status_code}")
        print("Response:", response.text)

# Пример использования:
login = "your_login"
password = "your_password"
phones = "+77057746123"  # Номер телефона в формате 7XXXXXXXXXX
message = "Hello from Python!"

send_sms_smsc(login, password, phones, message)
