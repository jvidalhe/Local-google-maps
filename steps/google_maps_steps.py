from behave import given, when, then
from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Inicializar el driver en una variable global
driver = None


@given('the Google Maps app is launched on the device')
def step_launch_google_maps(context):
    global driver
    # Crear una instancia de AppiumOptions
    options = AppiumOptions()

    # Configurar las capacidades para Android
    options.set_capability('platformName', 'Android')
    options.set_capability('platformVersion', '15')  # La versión del emulador
    options.set_capability('deviceName', 'emulator-5554')
    options.set_capability('automationName', 'UiAutomator2')
    options.set_capability('appPackage', 'com.google.android.apps.maps')
    options.set_capability('appActivity', 'com.google.android.maps.MapsActivity')

    # Inicializar el WebDriver con las opciones configuradas
    driver = webdriver.Remote(
        command_executor='http://127.0.0.1:4723',
        options=options
    )

    print("Google Maps se abre en el dispositivo.")


@when('I skip the initial screen')
def step_skip_initial_screen(context):
    global driver
    # Define un tiempo de espera máximo
    wait = WebDriverWait(driver, 10)  # 10 segundos de espera máxima

    # Esperar a que el botón "SKIP" esté visible y pulsarlo
    skip_button = wait.until(
        EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.Button[@text="SKIP"]'))
    )
    skip_button.click()
    print("Botón 'SKIP' pulsado.")


@then('the search bar should be visible')
def step_verify_search_bar(context):
    global driver
    # Define un tiempo de espera máximo
    wait = WebDriverWait(driver, 10)  # 10 segundos de espera máxima

    # Esperar a que la barra de búsqueda esté visible
    search_box = wait.until(
        EC.presence_of_element_located((AppiumBy.ID, "com.google.android.apps.maps:id/search_omnibox_text_box"))
    )

    # Verificar que la barra de búsqueda está visible
    assert search_box.is_displayed(), "La barra de búsqueda no está visible"
    print("La aplicación Google Maps se lanzó correctamente y la barra de búsqueda está visible.")


@when('I navigate through the menu items')
def step_navigate_menu_items(context):
    global driver
    # Define un tiempo de espera máximo
    wait = WebDriverWait(driver, 10)  # 10 segundos de espera máxima

    # Lista de XPath de los elementos para navegar
    navigation_items = [
        '(//android.widget.ImageView[@resource-id="com.google.android.apps.maps:id/navigation_bar_item_icon_view"])[1]',
        '(//android.widget.ImageView[@resource-id="com.google.android.apps.maps:id/navigation_bar_item_icon_view"])[2]',
        '(//android.widget.ImageView[@resource-id="com.google.android.apps.maps:id/navigation_bar_item_icon_view"])[3]',
        '(//android.widget.ImageView[@resource-id="com.google.android.apps.maps:id/navigation_bar_item_icon_view"])[4]',
        '(//android.widget.ImageView[@resource-id="com.google.android.apps.maps:id/navigation_bar_item_icon_view"])[5]'
    ]

    # Navegar entre los elementos
    for index, xpath in enumerate(navigation_items):
        element = wait.until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath))
        )
        element.click()
        print(f"Elemento {index + 1} clicado.")


@then('I close the Google Maps app')
def step_close_google_maps(context):
    global driver
    # Cerrar la aplicación de manera explícita
    driver.terminate_app('com.google.android.apps.maps')
    print("Aplicación Google Maps cerrada explícitamente.")

    # Finalizar la sesión de Appium
    driver.quit()
    print("Sesión de Appium finalizada.")
