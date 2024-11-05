## Тестирование интерфейса koshelek.ru

### Описание
Доступные тесты:

test_username_validate_click - тест заполнения имени пользователя с нажатием на кнопку "Далее"

test_username_validate_no_click - тест заполнения имени пользователя  после нажатий клавиш на клавиатуре

test_email_validate - тест заполнения почты

test_password_click_validate - тест заполнения пароля с нажатием кнопки "Далее"

test_password_keypress_validate - тест заполнения пароля после нажатия клавиш на клавиатуре

test_referral_code_validate - тест заполнения реферального окода

test_agreement_checkbox - тест чекбокса принятия пользовательского соглашения

## Требования:
Для работы теста требуется python 3.11

### Подготовка
Настроить файл `.env` для программы, пример создания лежит в `.env.example`

### Создаем виртуальное окружение
```bash
python -m venv venv
```

### Активируем виртуального окружение
для Windows:
```bash
venv\Scripts\activate.bat
```
для Linux и MacOS:
```bash
source venv/bin/activate
```
### Устанавливаем в виртуальное окружение все пакеты
```bash
pip install -r requirements.txt
```

## Запуск тестов
Для запуска всех тестов - используем команду:
```bash
pytest -v -l test_register_form.py 
```

### Дополнительные команды запуска отдельных тестов:
Запуск только одного теста:
```bash
pytest -v -l test_register_form.py::test_username_validate_click
```
