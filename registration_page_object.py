from playwright.sync_api import Locator, Page, TimeoutError

import config

LOCATOR_WAIT_TIMEOUT = config.LOCATOR_TIMEOUT


def get_locator_by_text(locator: Locator, reference_text: str) -> bool:
    """
    Поиск элемента на странице с введенным текстом. Нужна для ожидания появления сообщений верификации после нажатия на кнпоку "Далее"
    :param locator: Локатор, в котором будет происходить поиск вложенного текста
    :param reference_text: Искомая строка для поиска
    :return: True - если найден на странице за время LOCATOR_WAIT_TIMEOUT, False - если не дождались по таймауту
    """
    try:  # конструкция для ожидания отображения элемента при подгрузке валидации после нажатия на кнопку "Далее". Нужна для проверки сущестования пользователя
        locator.get_by_text(reference_text, exact=True).wait_for(state="attached",
                                                                 timeout=LOCATOR_WAIT_TIMEOUT)
        return True
    except TimeoutError:
        return False


class RegistrationPageObject:
    """
    Класс страницы регистрации
    """
    class Locators:
        username_input = 'div[data-wi="user-name"] input[type="text"]'
        username_validate = 'div[data-wi="user-name"] div[data-wi="message"]>span'
        next_button = 'button[type="submit"]'

        email_input = 'div[data-wi="identificator"] input[type="email"]'
        email_validate = 'div[data-wi="identificator"] div[data-wi="message"]>span'

        pass_input = 'div[data-wi="password"] input'
        pass_click_validate = 'div[data-wi="password"] div[data-wi="error"]>.k-text'
        pass_keypress_validate = 'div[data-wi="password"] div[data-wi="message"]>.k-text'
        pass_visible_icon = 'div[data-wi="password"] div[data-wi="preview-button"] button'

        agreement_checkbox_locator = 'div[data-wi="user-agreement"] .v-input'

        referral_code_input = 'div[data-wi="referral"] input[type="text"]'
        referral_code_validate = 'div[data-wi="referral"] div[data-wi="message"]>span'

    def __init__(self, page: Page, domain_url: str):
        self.page = page  # объект страницы
        self.domain_url = domain_url  # адрес домена
        self.url = domain_url + "/authorization/signup"  # адрес страницы регистрации
        self.username = Field(page.locator(self.Locators.username_input), page.locator(self.Locators.username_validate))  # Имя пользователя
        self.email = Field(page.locator(self.Locators.email_input), page.locator(self.Locators.email_validate))  # Почта
        self.password = PasswordField(page.locator(self.Locators.pass_input),  # Пароль
                                      page.locator(self.Locators.pass_click_validate),
                                      page.locator(self.Locators.pass_keypress_validate),
                                      page.locator(self.Locators.pass_visible_icon))
        self.referral_code = Field(page.locator(self.Locators.referral_code_input), page.locator(self.Locators.referral_code_validate))  # Реферальный код
        if self.page.url != self.url:
            self.page.goto(self.url)

    def next_button_click(self) -> None:
        """
        Нажатие кнопки "Далее"
        :return: None
        """
        self.page.locator(self.Locators.next_button).click()

    def get_text_on_page(self, reference_text: str) -> bool:
        """
        Поиск элемента на странице с введенным текстом. Нужна для ожидания появления сообщений верификации после нажатия на кнпоку "Далее"
        :param reference_text: Искомая строка для поиска
        :return: True - если найден на странице за время LOCATOR_WAIT_TIMEOUT, False - если завершено по таймауту
        """
        try:  # конструкция для ожидания отображения элемента при подгрузке валидации после нажатия на кнопку "Далее". Нужна для проверки сущестования пользователя
            self.page.get_by_text(reference_text, exact=True).wait_for(state="attached",
                                                                       timeout=LOCATOR_WAIT_TIMEOUT)
            return True
        except TimeoutError:
            return False

    def get_agreement_checkbox_error_state(self) -> bool:
        """
        Получение состояния валидации чекбокса принятия пользовательского соглащения
        :return: True - если с ошибкой, False - если ошибки нет
        """
        classes = self.page.locator(self.Locators.agreement_checkbox_locator).get_attribute("class")
        return 'error--text' in classes


class Field:
    """
    Универсальный класс поля. Позволяет считать значение поля, заполнить, проверить текст валидации под ним
    """
    def __init__(self, input_locator: Locator, validate_locator: Locator):
        self.input_locator = input_locator  # локатор элемента input
        self.validate_locator = validate_locator  # локатор элемента input

    def get(self) -> str:
        """
        Получение значения поля
        :return: str - текстовое значение
        """
        return self.input_locator.text_content()

    def set(self, text) -> None:
        """
        Установить значение поля
        :param text: строка для заполнения
        :return: None
        """
        self.input_locator.fill(text)

    def click(self) -> None:
        """
        Нажатие на поле
        :return: None
        """
        self.input_locator.click()

    def validate_text(self) -> str:
        """
        Получение значения сообщения валидации под полем
        :return: str - строка значения
        """
        return self.validate_locator.text_content()

    def get_text_on_page(self, reference_text):  # поиск идет внутри локатора текста валидатора
        """
        Поиск текста внутри валидатора. Нужен для ожидания отображения текста при запросах к бэку - мягкое ожидание
        :param reference_text: str - строка для поиска
        :return: True - если найден на странице за время LOCATOR_WAIT_TIMEOUT, False - если завершено по таймауту
        """
        return get_locator_by_text(locator=self.validate_locator, reference_text=reference_text)


class PasswordField(Field):
    """
    Класс поля пароля. Расширен от класса Field для анализа дополнительной валидации
    """
    def __init__(self, input_locator: Locator, validate_click_locator: Locator, validate_keypress_locator: Locator, visible_symbols_check_locator: Locator):
        super().__init__(input_locator, validate_click_locator)
        self.validate_keypress_locator = validate_keypress_locator  # локатор поля валидации сложности пароля

    def get_text_on_page(self, reference_text) -> bool:  # главное отличие от оригинальной функции - поиск идет по всей странице
        """
        Поиск текста по всей странице. Нужен для ожидания отображения текста при запросах к бэку - мягкое ожидание
        :param reference_text: str - строка для поиска
        :return: True - если найден на странице за время LOCATOR_WAIT_TIMEOUT, False - если завершено по таймауту
        """
        return get_locator_by_text(locator=self.validate_locator.page, reference_text=reference_text)

    def get_validate_keypress_text(self) -> str:
        """
        Получение значения сообщения валидации сложности пароля под полем
        :return: str - строка значения
        """
        return self.validate_keypress_locator.text_content()
