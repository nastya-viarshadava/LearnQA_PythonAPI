import requests
import pytest

class TestUserAuth:                               # таким образом мы создали класс и нашу функцию тест
    def test_auth_user(self):
        data = {                                  # в переменную дата мы положили авторизационные данные
            "email":"vinkotov@example.com",
            "password":"1234"
        }

        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)    # делаем первый запрос на авторизацию

        assert "auth_sid" in response1.cookies, "There is no auth cookies in the response"         # проверка, что в ответе пришли нужные куки
        assert "x-csrf-token" in response1.headers, "There is no CSRF token header in the response"   # нужный хэдер
        assert "user_id" in response1.json(), "There is no user id in the response"    # нужный айди пользователя

        auth_sid = response1.cookies.get("auth_sid")          # переложим эти параметры в отдельные переменные, чтобы потом с ними работать
        token = response1.headers.get("x-csrf-token")
        user_id_from_auth_method = response1.json()["user_id"]

        response2 = requests.get(                             # создаем переменную, в которую запишем результат второго запроса
            "https://playground.learnqa.ru/api/user/auth",
            headers={"x-csrf-token":token},
            cookies={"auth_sid":auth_sid}
        )

        assert "user_id" in response1.json(), "There is no user id in the second response" # таким образом мы убедились, что в ответа второго респонса тоже присутсвуеи user_id
        user_id_from_check_method = response2.json()["user_id"]  # ... после этого занесли его в отдельную переменную

        assert user_id_from_auth_method == user_id_from_check_method, "User id from auth method is not equal too user id from check method"      # сравним две получившиеся у нас переменные

#NEGATIVE TEST
# в этой функции мы делаем практически то же самое, что и в позитивном тесте, только в конце во вторйо запрос мы будем передавать что-то одно
# чтобы не писать два одинаковых теста, в кот отличается только одна строка (передаем во торой запрос либо токен, либо куки), давайте сделаем этот тест параметризованным>
# для этого создадим переменную эксклюд парамс
# важно: мы создаем эту переменную не в какой-то их функций, а отдельно
    exclude_params = [
        ("no_cookie"),
        ("no_token")
    ]
# давайте эту переменную подклюим к созданной функции тест
    @pytest.mark.parametrize("condition", exclude_params) # внутри теста у нас будет переменная кондишн, кот будет либо равняться значению no_cookies либо no_token в зависимости от этого мы не будем передовать во втором запросе либо куки, либо токен и убеждаьбся, что в ответе нам приходит юзер айди = 0, т.е сервер не считает этот запрос авторизованным
    def test_negative_auth_check(self, condition):
# первая половина теста (до момента второго запроса) будет аналогична предыдущему
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        response1 = requests.post("https://playground.learnqa.ru/api/user/login",
                                  data=data)

        assert "auth_sid" in response1.cookies, "There is no auth cookies in the response"
        assert "x-csrf-token" in response1.headers, "There is no CSRF token header in the response"
        assert "user_id" in response1.json(), "There is no user id in the response"

        auth_sid = response1.cookies.get(
            "auth_sid")
        token = response1.headers.get("x-csrf-token")
        # user_id_from_auth_method = response1.json()["user_id"] - убираем эту строку тк эта переменная нам не понадобится, тк ответ второго запроса мы будем стравнивать теперь с нулем
#добавим условие: если переменная кондишн = no_cookie, мы сдеалем запрос без куки, иначе: мы сделаем запрос без токена

        if condition == "no_cookie":
            response2 = requests.get(
                "https://playground.learnqa.ru/api/user/auth",
                headers={"x-csrf-token": token}
            )
        else:
            response2 = requests.get(
                "https://playground.learnqa.ru/api/user/auth",
                cookies={"auth_sid": auth_sid}
            )

        assert "user_id" in response1.json(), "There is no user id in the response" #сделаем проверки, что юзер айди в ответе есть и он равен 0

        user_id_from_check_method = response2.json()["user_id"] #мы генерируем юзерайди и передаем в него результаты запроса на юзер айди
        assert user_id_from_check_method == 0, f"User is authorozed with condition {condition}"

