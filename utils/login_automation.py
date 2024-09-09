from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pickle

def automate_login(email, password):
    driver_path = './chromedriver'  # Certifique-se de que o caminho está correto
    driver = webdriver.Chrome(driver_path)

    driver.get("https://accounts.google.com/signin/v2/identifier?service=youtube")

    # Encontra o campo de e-mail e envia o e-mail
    email_input = driver.find_element(By.ID, 'identifierId')  # Usando ID para o campo de e-mail
    email_input.send_keys(email)
    email_input.send_keys(Keys.RETURN)

    time.sleep(3)  # Aguarde o carregamento da próxima página

    # Encontra o campo de senha e envia a senha
    password_input = driver.find_element(By.NAME, 'password')  # Usando NAME para o campo de senha
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    time.sleep(5)  # Aguarde o login e redirecionamento

    # Salva os cookies para uso futuro
    with open('cookies.pkl', 'wb') as file:
        pickle.dump(driver.get_cookies(), file)

    driver.quit()
    print("Cookies salvos com sucesso!")

# Substitua os valores abaixo com suas credenciais reais
email = 'diogoworkss@gmail.com'
password = '@diogo12'

automate_login(email, password)
