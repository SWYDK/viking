import requests

API_KEY = '6ed8edbb18597fcb955280f28cf83ec4'
USER_TOKEN = '06b873005a509ae9df6818c801310a2d'
COMPANY_ID = '440555'
BASE_URL = 'https://api.yclients.com/api/v1'

def get_employees(api_key, user_token, company_id):
    url = f"https://api.yclients.com/api/v1/book_record/440555"
    headers = {
        'Authorization': 'Bearer 83uag8prg689533sw7cx',
        'Accept': 'application/vnd.yclients.v2+json',
        'Content-Type': 'application/json',
    }
    data = {
        "phone": "79000000000",
        "fullname": "ДИМА",
        "email": "d@yclients.com",
        "code": "38829",
        "comment": "тестовая запись!",
        "type": "mobile",
        "notify_by_sms": 6,
        "notify_by_email": 24,
        "api_id": "777",
       
        "appointments": [
            {
            "id": 1,
            "services": [
                1
            ],
            "staff_id": 1,
            "datetime": "2024-08-26T08:50:12+00:00",
            
            }
            
        ]
        }
    response = requests.post(url,  json=data, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    try:
        employees = get_employees(API_KEY, USER_TOKEN, COMPANY_ID)
        print("Список сотрудников:", employees)
    except Exception as e:
        print("Произошла ошибка:", e)
