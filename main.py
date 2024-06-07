from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Инициализация драйвера для Firefox
driver = webdriver.Firefox()

# Открытие страницы
driver.get("http://over.org.tilda.ws/testuser")

# Функция для ожидания элемента
def await_element(driver, by, value, timeout=20):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

# Пример значений для заполнения полей
data = {
    'name': 'Иван Иванов',
    'email': 'ivan.ivanov@example.com',
    'phone': '123456789'  # без кода страны
}

try:
    # Ожидание и нахождение всех полей с классом 't-input-block'
    input_blocks = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 't-input-block'))
    )

    # Заполнение каждого поля значениями
    for index, input_block in enumerate(input_blocks):
        try:
            input_element = input_block.find_element(By.TAG_NAME, 'input')
            # Проверка, что поле не скрыто
            if input_element.get_attribute('type') != 'hidden':
                input_type = input_element.get_attribute('type')
                if input_type == 'text' and 'name' in input_element.get_attribute('name').lower():
                    input_element.clear()
                    input_element.send_keys(data['name'])
                    print(f"Заполнили поле имени значением '{data['name']}'")
                elif input_type == 'email':
                    input_element.clear()
                    input_element.send_keys(data['email'])
                    print(f"Заполнили поле email значением '{data['email']}'")
                else:
                    input_element.clear()
                    input_element.send_keys(f'Test Value {index + 1}')
                    print(f"Заполнили поле: {index + 1} значением 'Test Value {index + 1}'")
        except Exception as e:
            print(f"Не удалось заполнить поле {index + 1}: {e}")

    # Нахождение и заполнение поля для телефона по ID
    try:
        phone_input = await_element(driver, By.ID, 'input_1495040492013')
        phone_input.clear()
        phone_input.send_keys(data['phone'])
        print(f"Заполнили поле телефона значением '{data['phone']}'")
    except Exception as e:
        print(f"Не удалось найти или заполнить поле телефона: {e}")

    # Нахождение и нажатие кнопки отправки формы
    submit_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
    )
    submit_button.click()

    # Подтверждение действия (например, ожидание появления сообщения об успешной отправке)
    success_message = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.t-form-success'))
    )
    print("Форма успешно отправлена!")

except Exception as e:
    print(f"Ошибка при заполнении формы: {e}")

finally:
    # Закрытие браузера
    driver.quit()






