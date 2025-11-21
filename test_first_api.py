import pytest
import requests

class TestFirstAPI:
    names = [                            # создаем переменную (внутри класса, но за пределами функций), которая будет хранить в себе список(лист). внутри списка у нас будет последовательность кортежей (tuples). те в свою очередь состоят из параметров для запусков нашего теста (в нашем случае это имена, с которыми мы будем этот тест запускать)
        ("Vitalii"),                     # сколько кортежей в списке, столько раз пайтест и запустит наш код каждый раз передавая очередное имя. те в нашем случае будет 3 запуска теста.
        ("Arseniy"),
        ("")
    ]

    @pytest.mark.parametrize("name", names)               # указываем имя переменной, в которую пайтест будет передавать данные. а далее, через запятую, переменную, в которой эти данные у нас хранятся. тк @ - это функция декаратор пайтест, не забываем добавить ее через импорт в самом начале скрипта
    def test_hello_call(self, name):                      # далее в названии теста после селф добавляем ту самую переменную, в которой и будут данные (в нашем случае это имя). тк имя у нас приходит извне, определение самого имени из теста мы убираем
        url = "https://playground.learnqa.ru/api/hello"
        data = {"name":name}

        response = requests.get(url, params=data)

        assert response.status_code == 200, "Wrong response code"

        response_dict = response.json()
        assert "answer" in response_dict, "There is no field 'answer' in the response"

        if len(name) == 0:
            expected_response_text = "Hello, someone"
        else:
            expected_response_text = f"Hello, {name}"
        actual_response_text = response_dict["answer"]
        assert actual_response_text == expected_response_text, "Actual text in the response is not correct"