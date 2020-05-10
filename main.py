from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime
 

#dados
login="----"
senha="----"

#metodos
def doLogin(login,senha):
    print("----fazendo login----")
    global driver    
    driver.get("https://twitter.com/login")
    time.sleep(3)
    try:
        loginInput=driver.find_element_by_xpath("/html/body/div/div/div/div[2]/main/div/div/form/div/div[1]/label/div/div[2]/div/input")
        loginInput.send_keys(login)
        time.sleep(1)
        passInput=driver.find_element_by_xpath("/html/body/div/div/div/div[2]/main/div/div/form/div/div[2]/label/div/div[2]/div/input")
        passInput.send_keys(senha)
        time.sleep(1) 
        #entrar
        driver.find_element_by_xpath("/html/body/div/div/div/div[2]/main/div/div/form/div/div[3]/div/div").click()
        print("----Login feito----")
    except:
        print("----Insira credenciais de login válidas")

def getTrends():
    global driver
    driver.get("https://twitter.com/explore")
    time.sleep(2)

    #vai para trends do brasil
    ac = ActionChains(driver)
    ac.move_to_element(driver.find_element_by_xpath("/html/body/div/div/div/div[2]/main/div/div/div/div/div/div[1]/div[2]/nav/div/div[2]/div/div[2]")).move_by_offset(0, 0).click().perform()
    time.sleep(2)

    #pega a trend
    allTrends="/html/body/div/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/section/div/div/div"
    trendList=[]
    for posicao in range(0,10):
        print(f"----topico{posicao}")
        trendPath=f"{allTrends}[{posicao+3}]"
        try:        
            trend = {
                "titulo":driver.find_element_by_xpath(f"{trendPath}/div/div/div/div[2]/span/span").text,
                "categoria":driver.find_element_by_xpath(f"{trendPath}/div/div/div/div[1]/div[3]/span").text,
                "numero":driver.find_element_by_xpath(f"{trendPath}/div/div/div/div[3]/span").text    
            }
        except:
            trend = {
                "titulo":driver.find_element_by_xpath(f"{trendPath}/div/div/div/div[2]/span").text,
                "categoria":driver.find_element_by_xpath(f"{trendPath}/div/div/div/div[1]/div[3]/span").text,
                "numero":driver.find_element_by_xpath(f"{trendPath}/div/div/div/div[3]/span").text    
            }
        print(trend)
        trendList.append(trend)
    print("----lista de trends completa")
    return trendList

def doTweet(text):
    print("----Escrevendo")
    global driver
    driver.get("https://twitter.com/compose/tweet")
    time.sleep(2)
    textBox=driver.find_element_by_xpath("/html/body/div/div/div/div[1]/div[2]/div/div/div/div[2]/div[2]/div/div[3]/div/div/div/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div")
    textBox.send_keys(text)
    for i in range(0,3):
        print(f"----Tweetando em {i}...")
        time.sleep(1)
    try:
        driver.find_element_by_xpath("/html/body/div/div/div/div[1]/div[2]/div/div/div/div[2]/div[2]/div/div[3]/div/div/div/div[1]/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[4]/div").click()
        print("----tweetado com sucesso")
    except:
        print("----ocorreu um erro")

def createMessage(trendList):
    print("----Criando mensagem")
    momento = str(datetime.datetime.now()).split(" ")
    hora=momento[1][0:5]
    data=momento[0].split("-")
    data=f"{data[2]}/{data[1]}/{data[0]}"
    
    mensagem=f"Trending topics do Brasil às {hora} horas do dia {data}:\n"

    for i in range(10):
        trend=trendList[0][i]
        print(trend)
        mensagem+=f"#{i+1} {trend['titulo']}\n"
        #mensagem+=f"#{i+1} {trend['titulo']} com {trend['numero']}\n"
    return mensagem

def tweetTrends():
    time.sleep(3)
    input("----Aperte enter para começar")
    global driver
    doLogin(login,senha)
    trendList=getTrends()
    mensagem=createMessage([trendList])
    doTweet(mensagem)

#----------------
driver = webdriver.Chrome()
tweetTrends()
time.sleep(3)

input("----Aperte enter para fechar o navegador automatizado")
driver.quit()