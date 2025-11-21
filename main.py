import requests

payload = {"login":"secret_login", "password":"secret_pass"}                                      # готовим данные
response1 = requests.post("https://playground.learnqa.ru/api/get_auth_cookie", data=payload)   # передаем их в дейта

cookies_value = response1.cookies.get('auth_cookie')   # получаем куки с названием auth_cookie

cookies = {}                                             # создали пустой массив кукиз
if cookies_value is not None:                            #  и с помощью if убедились, что куки_вэлью не является Нан, т.е только в этом случае мы добавляем ее значение в переменную кукиз с помощью фуекции апдейт
    cookies.update({'auth_cookie': cookies_value})               # значение auth_cookie из предыдущей переменной кладем в cookies_value

response2 = requests.post("https://playground.learnqa.ru/api/check_auth_cookie", cookies = cookies)

print(response2.text)

# в результате наш код готов работать с обеими парами логин-пароль - с правильной и неправильной