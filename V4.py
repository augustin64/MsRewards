#!/usr/bin/python3
import os
from time import sleep
from random import uniform, choice, randint,shuffle
from re import search,findall
from os import path, sys, system
from requests import get
import discord
import asyncio
from sys import platform, exc_info
from socket import gethostbyname
from csv import reader

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions

main = True
Headless = True

IsLinux = platform == "linux"
print("Linux : "+ str(IsLinux))


def resource_path(relative_path): #permet de recuperer l'emplacement de chaque fichier, su linux et windows
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.dirname(__file__)
    return path.join(base_path, relative_path)


def FirefoxMobile(Headless = Headless):
    MOBILE_USER_AGENT = ('Mozilla/5.0 (iPhone; CPU iPhone OS 14_1_2 like Mac OS X)'
                    'AppleWebKit/603.1.30 (KHTML, like Gecko)'
                    'Version/14.1 Mobile/14E304 Safari/602.1')

    options = Options()
    options.set_preference("browser.link.open_newwindow", 3)
    if Headless :
        options.add_argument("-headless")
    
    MobileProfile = webdriver.FirefoxProfile() 
    MobileProfile.set_preference("general.useragent.override", MOBILE_USER_AGENT)
    

    return(webdriver.Firefox(options=options, firefox_profile=MobileProfile, service_log_path=os.devnull))


def FirefoxPC(Headless = Headless):
    PC_USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134')

    options = Options()
    options.set_preference("browser.link.open_newwindow", 3)
    
    if Headless :
        options.add_argument("-headless")

    PcProfile = webdriver.FirefoxProfile() 
    PcProfile.set_preference("general.useragent.override", PC_USER_AGENT)
    
    return(webdriver.Firefox(options=options, firefox_profile=PcProfile,service_log_path=os.devnull))


if IsLinux :
    MotPath = "/home/pi/MsReward/liste.txt"
    LogPath= "/home/pi/MsReward/login.csv"
    TokenPath = "/home/pi/MsReward/token.txt"
else :
    MotPath = resource_path('D:\Documents\Dev\MsReward\liste/liste.txt')
    LogPath = resource_path('D:\Documents\Dev\MsReward\login/login.csv')
    TokenPath = resource_path('D:\Documents\Dev\MsReward/token/token.txt')
    system("")



g =  open(MotPath, "r" , encoding="utf-8")
Liste_de_mot=(list(g.readline().split(',')))
g.close()
g = open(TokenPath,"r")
Token = g.readline()
g.close


def CustomSleep(temps):
    c = False
    points = [" .   ", "  .  ", "   . ", "    .", "    .", "   . ", "  .  "," .   "]
    for i in range (int(temps)):
        c = True
        for i in range (8):
            
            sleep(0.125)
            print(points[i], end='\r')

    if c:
        print('                ', end="\r")
    sleep(temps - int(temps))


def ListTabs():
    tabs = []
    for i in driver.window_handles :
        driver.switch_to.window(i)
        tabs.append(driver.current_url)
    return(tabs)


def LogError(message,log = False):
    if not IsLinux :
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        print(f'\033[93m Erreur : {str(message)}  \033[0m')
    else :

        with open('page.html', 'w') as f:
            f.write(driver.page_source)


        driver.save_screenshot("screenshot.png")
        asyncio.set_event_loop(asyncio.new_event_loop())

        client = discord.Client()
        @client.event
        async def on_ready():
            channel = client.get_channel(861181899987484692)
            if log :
                channel = client.get_channel(833275838837030912) #channel de log
            await channel.send(_mail)
            
            await channel.send(ListTabs())
            await channel.send(str(message))
            CustomSleep(1)
            await channel.send(file=discord.File('screenshot.png'))
            await channel.send(file=discord.File('page.html'))
            await client.close()


        client.run(Token)


def progressBar(current, total=30, barLength = 20, name ="Progress"):
    percent = float(current+1) * 100 / total
    arrow   = '-' * int(percent/100 * barLength - 1) + '>'
    spaces  = ' ' * (barLength - len(arrow))
    print(name + ': [%s%s] %d %%' % (arrow, spaces, percent), end='\r')


def Close(fenetre, SwitchTo = 0):
    driver.switch_to.window(fenetre)
    driver.close()
    driver.switch_to.window(driver.window_handles[SwitchTo])


def RGPD():
    driver.implicitly_wait(3)
    try :
        driver.find_element_by_id('bnp_btn_accept').click()
    except :
        pass
    
    try :
        driver.find_element_by_id('bnp_hfly_cta2').click()
    except :
        pass
    driver.implicitly_wait(5)


def PlayQuiz2():
    
    for j in range (10):
        try : 
            CustomSleep(uniform(3,5))
            
            txt = driver.page_source
            IG = search('IG:\"([^\"]+)\"', txt)[1] #variable dans la page, pour calculer le offset
            reponse1 = search("data-option=\"([^\"]+)\"", txt)[1]
            offset = int(IG[-2:],16) # la conversion ec decimal des deux dernier caracteres de IG
            reponse = search("correctAnswer\":\"([0-9]+)", txt)[1]

            somme = 0 

            for i in reponse1 :
                somme += ord(i)

            RGPD()
            if somme + offset == int(reponse) :
                elem = driver.find_element_by_id('rqAnswerOption0')
                elem.click()
                progressBar(j,10, name="quiz 2")
                
            else : 
                elem = driver.find_element_by_id('rqAnswerOption1')
                elem.click()
                progressBar(j,10, name="quiz 2")

        except exceptions.ElementNotInteractableException as e :
            driver.execute_script("arguments[0].click();", elem) 


        except Exception as e:
            LogError("PlayQuiz2" + str(e))
            break


def PlayQuiz8():

    try : 
        #RGPD()
        
        c = 0
        for i in range(3):
            sleep(uniform(3,5))
            ListeOfGood =[]
            for i in range(1,9):
                Card= driver.find_element_by_id(f'rqAnswerOption{i-1}')
                if 'iscorrectoption="True" 'in Card.get_attribute('outerHTML') :
                    ListeOfGood.append(f'rqAnswerOption{i-1}') #premier div = 3 ?
                
            shuffle(ListeOfGood)

            for i in ListeOfGood :
                sleep(uniform(3,5))
                c+=1
                progressBar(c,16, name="Quiz 8 ")
                try : 
                    elem = driver.find_element_by_id(i)
                    elem.click()
                except exceptions.ElementNotInteractableException as e:
                    driver.execute_script("arguments[0].click();", elem)   

          
    except Exception as e :
        LogError("PlayQuiz8" + str(e) + str(ListeOfGood))        
    

def PlayQuiz4():
    try : #permet de gerer les truc de fidélité
        max = int(findall("rqQuestionState([\d]{1,2})\"", driver.page_source)[-1])
    except :
        max = 3    
    try :
        
        
        for i in range(max):
            #RGPD()
            txt = driver.page_source
            
            reponse = search("correctAnswer\":\"([^\"]+)", txt)[1] #je suis pas sur qu'il y ait un espace
            reponse = reponse.replace('\\u0027',"'") #il faut cancel l'unicode avec un double \ (on replacer les caracteres en unicode en caracteres utf-8)
            
            
            print(f"validation de la reponse                                     " , end="\r")
            print(f"validation de la reponse {i+1}/{max} {reponse}" , end="\r")
            try : 
                elem = driver.find_element_by_css_selector(f'[data-option="{reponse}"]')
                elem.click()
            except exceptions.ElementNotInteractableException:
                driver.execute_script("arguments[0].click();", elem)

            CustomSleep(uniform(3,5))
    
    except Exception as e :
        LogError("PlayQuiz4" + str(e))
        raise ValueError(e)


def PlayPoll():
    try :
        try : 
            elem = driver.find_element_by_id(f'btoption{choice([0,1])}')
            elem.click()
        except exceptions.ElementNotInteractableException as e:
            driver.execute_script("arguments[0].click();", elem)
        CustomSleep(uniform(2,2.5))
    except Exception as e :
        LogError("PlayPoll" +  str(e))
        raise ValueError(e)


def AllCard(): #fonction qui repere le type de contenue et redireige sur la bonne fonction

    def reset(touch=False): #retourne sur la page de depart apres avoir finis
        if len(driver.window_handles) == 1 :
            driver.get('https://www.bing.com/rewardsapp/flyout')
            if touch :
                driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div[2]/div[2]/div[1]').click()
        else : 
            driver.switch_to.window(driver.window_handles[1])
            print(f"on ferme la fenetre {driver.current_url}")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])

    def dailyCards():
        try :
            for i in range(3):
                sleep(1)
                driver.find_element_by_xpath(f'/html/body/div/div/div[3]/div[2]/div[1]/div[2]/div/div[{i+1}]/a/div/div[2]').click()
                sleep(1)
                TryPlay()
                sleep(1)
                reset()
        except Exception as e :
            LogError(f'erreur dans la premiere partie de AllCard (les daily card). cela arrive si on relance le proramme uen deuxieme fois sur le meme compte \n {e}')

    dailyCards()

    try :    
        try : 
            driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div[2]/div[2]/div[1]').click() #declenche la premiere partie ?
        except :
            reset()
            try :
                driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div[2]/div[2]/div[1]').click()#declenche la deuxieme partie ?
            except :
                pass
        c = 0
        while True:
            driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div[2]/div[3]/div/div[1]/a/div/div[2]').click()
            
            driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])
            sleep(1)
            TryPlay()
            reset(True)
            sleep(1)
            c += 1
            if c ==20 :
                break
            try :
                link = findall('href="([^<]+)" title=""',driver.page_source)[3]
            except :
                break
    except Exception as e:
        LogError(f'2eme partie de AllCard (weekly card)\n {e}')


def send_keys_wait(element,keys):
    for i in keys :
        element.send_keys(i)
        CustomSleep(uniform(0, 0.5))


def login() :
    try :
        driver.get('https://www.bing.com/rewardsapp/flyout')

        try :

            driver.find_element_by_css_selector(f'[title="Rejoindre"]').click()

        except :

            driver.find_element_by_css_selector(f'[title="Join now"]').click()
        
        mail = driver.find_element_by_id('i0116')
        send_keys_wait(mail, _mail)
        mail.send_keys(Keys.ENTER)
        
        try :
            driver.find_element_by_id('idChkBx_PWD_KMSI0Pwd').click()
        except :
            try :
                driver.find_element_by_css_selector('''[data-bind="text: str['CT_PWD_STR_KeepMeSignedInCB_Text']"]''').click()
            except :
                pass
        CustomSleep(3)
        pwd = driver.find_element_by_id('i0118')
        send_keys_wait(pwd, _password)
        pwd.send_keys(Keys.ENTER)
        try :
            driver.find_element_by_id('iNext').click()

        except :
            assert('il y a eu une erreur dans le login, il faut regarder pourquoi')    #dans le cas ou ms change ses parametre de confidentialité
        CustomSleep(2)
        try : 
            driver.find_element_by_id('KmsiCheckboxField').click()
        except Exception as e  :
            pass
            print(f"erreur la {e}") 
        try : 
            driver.find_element_by_id('idSIButton9').click()
        except :
            pass
        
        RGPD()

        driver.get('https://www.bing.com/rewardsapp/flyout')
        
        MainWindows = driver.current_window_handle
        return(MainWindows)

    except Exception as e:
        LogError(e)
        

def BingPcSearch(override = randint(30,35)):
    driver.get(f'https://www.bing.com/search?q={choice([x for x in range (999999)])}&form=QBLH&sp=-1&pq=test&sc=8-4&qs=n&sk=&cvid=1DB80744B71E40B8896F5C1AD2DE95E9')
    CustomSleep(uniform(1,2))
    RGPD()
    CustomSleep(uniform(1,1.5))
    send_keys_wait( driver.find_element_by_id('sb_form_q'),Keys.BACKSPACE+Keys.BACKSPACE+Keys.BACKSPACE+Keys.BACKSPACE+Keys.BACKSPACE+Keys.BACKSPACE)
    
    
    for i in range(override):
        mot = str(Liste_de_mot[randint(0,9999)] )
        try :
            send_keys_wait( driver.find_element_by_id('sb_form_q'),mot)
            driver.find_element_by_id('sb_form_q').send_keys(Keys.ENTER)
        except :
            sleep(10)
            driver.refresh()
            sleep(10)
            send_keys_wait( driver.find_element_by_id('sb_form_q'),mot)
            driver.find_element_by_id('sb_form_q').send_keys(Keys.ENTER)

        progressBar(i,override, name="PC")
        sleep(uniform(5,20)) 

        try :
            #for i in range (len(mot)+1):
            #    send_keys_wait( driver.find_element_by_id('sb_form_q'),Keys.BACKSPACE)
            driver.find_element_by_id('sb_form_q').clear()
        except :
            driver.refresh()
            driver.find_element_by_id('sb_form_q').clear()
            #for i in range (len(mot)+1):
            #    send_keys_wait( driver.find_element_by_id('sb_form_q'),Keys.BACKSPACE)

    print('\n\n')


def BingMobileSearch(override = randint(20,25)):
    try :
        MobileDriver = FirefoxMobile()
        echec = 0
        def Mlogin(echec):
            
            try : 
                MobileDriver.get(f'https://www.bing.com/search?q={choice([x for x in range (999999)])}&form=QBLH&sp=-1&pq=test&sc=8-4&qs=n&sk=&cvid=1DB80744B71E40B8896F5C1AD2DE95E9')
                CustomSleep(uniform(3,5))

                MobileDriver.find_element_by_id('mHamburger').click()
                CustomSleep(uniform(1,2))
                MobileDriver.find_element_by_id('hb_s').click()
                CustomSleep(uniform(1,2))

                mail = MobileDriver.find_element_by_id('i0116')
                send_keys_wait(mail, _mail)
                mail.send_keys( Keys.ENTER)
                CustomSleep(uniform(1,2))
                #MobileDriver.find_element_by_id('idLbl_PWD_KMSI_Cb').click()
                pwd = MobileDriver.find_element_by_id('i0118')
                send_keys_wait(pwd, _password)
                pwd.send_keys( Keys.ENTER)
            except Exception as e :
                echec += 1
                if echec <= 3 :
                    print(f'echec du login sur la version mobile. on reesaye ({echec}/3), {e}')
                    CustomSleep(uniform(5,10))
                    Mlogin(echec)
                else :
                    LogError('recherche sur mobile impossible. On skip \n\n\n\n\n\n\n\n')
                    print(MobileDriver.page_source)
                    MobileDriver.quit()
                    return(True)
                    
        
        def MRGPD():
            try :
                MobileDriver.find_element_by_id('bnp_btn_accept').click()
            except :
                pass

            try :
                MobileDriver.find_element_by_id('bnp_hfly_cta2').click()
            except :
                pass        
        
        def Alerte():
            try:
                alert = MobileDriver.switch_to.alert
                alert.dismiss()
            except exceptions.NoAlertPresentException as e :
                pass

        if not Mlogin(echec) :        

            CustomSleep(uniform(1,2))
            MRGPD()
            CustomSleep(uniform(1,1.5))
            send_keys_wait( MobileDriver.find_element_by_id('sb_form_q'),Keys.BACKSPACE+Keys.BACKSPACE+Keys.BACKSPACE+Keys.BACKSPACE+Keys.BACKSPACE+Keys.BACKSPACE)
            
            for i in range(override): #20

                mot = str(Liste_de_mot[randint(0,9999)] )
                send_keys_wait( MobileDriver.find_element_by_id('sb_form_q'),mot)
                MobileDriver.find_element_by_id('sb_form_q').send_keys(Keys.ENTER)
                progressBar(i,override,name="Mobile")

                sleep(uniform(5,20)) 

                Alerte() #noralement le seul utile, a voir plus tard
                
                for i in range (len(mot)):
                    MobileDriver.find_element_by_id('sb_form_q').clear()
                    #send_keys_wait(MobileDriver.find_element_by_id('sb_form_q'),Keys.BACKSPACE)
                    #CustomSleep(uniform(0, 0.5))

            MobileDriver.quit()
            

    except Exception as e:
        LogError("BingMobileSearch" + str(e))
        try :
            MobileDriver.quit()
        except : 
            pass

def TryPlay(nom ="inconnu"):

    RGPD()
    
    try :
        driver.find_element_by_id('rqStartQuiz').click() #start the quiz

        number = driver.page_source.count('rqAnswerOption')

        if number == 9:
            try :
                print(f'Quiz 8 détécté sur la page {nom}')
                RGPD()
                PlayQuiz8()
            except :
                print('echec de PlayQuiz 8. Aborted ')

        elif number == 5 :
            try :
                print(f'Quiz 4 détécté sur la page {nom}')
                RGPD()
                PlayQuiz4()
                print('Quiz 4 reussit')
            except :
                print('echec de PlayQuiz 4. Aborted')

        elif number == 3 :
            try :
                RGPD()
                print(f'Quiz 2 détécté sur la page {nom}')
                PlayQuiz2()
            except :
                print('echec de PlayQuiz 2. Aborted ')

        else :
            LogError('probleme dans la carte : il y a un bouton play et une erreur')
    except :
        if "bt_PollRadio" in driver.page_source :
            try :
                print('Poll détected',  end ="\r")
                RGPD()
                PlayPoll()
                print('Poll reussit  ')
            except :
                print('poll Aborted  ')

        elif search("([0-9]) de ([0-9]) finalisée",driver.page_source) :
            print('fidélité')
            RGPD()
            Fidelité()
                
        else :
            print(f'rien a faire sur la page {nom}')
            RGPD()
            CustomSleep(uniform(3,5))


def LogPoint(account="unknown", log = False): #log des points sur discord
    if not IsLinux :
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    else :
        asyncio.set_event_loop(asyncio.new_event_loop())

    elem = driver.find_element_by_css_selector('[title="Microsoft Rewards"]')
    elem.click()
    driver.switch_to.window(driver.window_handles[1])
    CustomSleep(uniform(10,20))
    try :
        point = search("availablePoints\":([\d]+)",driver.page_source)[1]
    except :
        point = "erreur"

    CustomSleep(uniform(3,20))
    
    account = account.split('@')[0]
    client = discord.Client()
    @client.event
    async def on_ready():
        channel = client.get_channel(841338253625917450)

        await channel.send(f'{account} actuellement à {str(point)} points')
        CustomSleep(1)
        await client.close()


    client.run(Token)


def Fidelité():
    try :
       
        driver.switch_to.window(driver.window_handles[1])

        choix = driver.find_element_by_class_name('spacer-48-bottom')

        nb = search("([0-9]) de ([0-9]) finalisée",driver.page_source)
        

        for i in range(int(nb[2])-int(nb[1])):
            choix = driver.find_element_by_class_name('spacer-48-bottom')
            ButtonText = search('<span class=\"pull-left margin-right-15\">([^<^>]+)</span>',choix.get_attribute("innerHTML"))[1]
            bouton = driver.find_element_by_xpath(f'//span[text()="{ButtonText}"]')
            bouton.click()
            CustomSleep(uniform(3,5))
            driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])
            TryPlay()
            CustomSleep(uniform(3,5))
            Close(driver.window_handles[2],SwitchTo=1)
            driver.refresh()
            CustomSleep(uniform(3,5))

        Close(driver.window_handles[1])
        print('on a passer la partie fidélité')
    except Exception as e :
        LogError("Fidélité" + str(e))


def CheckPoint():# a fix, ne marche pas dans  80% des cas
    driver.get("https://rewards.microsoft.com/pointsbreakdown")
    txt = driver.page_source
    pc = search('([0-9][0-9]|[0-9])</b> / 90',txt)
    mobile = search('([0-9][0-9]|[0-9])</b> / 60',txt)
    if mobile :
        if mobile[1] != 60:
            BingMobileSearch(22-(int(mobile[1])/3))      
    if pc :
        if pc[1] != 90:
            BingPcSearch(32-(int(pc[1])/3))
             

def DailyRoutine():
    
    
    MainWindows = login()
    
    try :
        AllCard()
    except Exception as e :
        LogError(f'pas normal sauf si relancer a la main, juste pour les recherches bing (DalyRoutine -> AllCard) \n {e}')

    try : 
        BingPcSearch()
    except Exception as e :
        LogError(f"il y a eu une erreur dans BingPcSearch, {e}")
    CustomSleep(uniform(3,20)) 
    

    try : 
        BingMobileSearch()
    except Exception as e:
        LogError(f'BingMobileSearch - {e}')
    print('\n')
    CustomSleep(uniform(3,20))
    
    try :
        LogPoint(_mail)
    except :
        LogError('LogPoint')



with open(LogPath) as f:
    reader = reader(f)
    data = list(reader)

Credentials = data

CustomSleep(2)

shuffle(Credentials)

for i in Credentials :
    
    
    _mail =i[0]
    _password = i[1]

    print('\n\n')
    print(_mail)
    CustomSleep(1)
    if main: 
        driver = FirefoxPC()
        driver.implicitly_wait(5)

        try :
            DailyRoutine()
            driver.quit()
            print("finis")
            CustomSleep(uniform(120,360))
            
        except KeyboardInterrupt :
            print('canceled')
            driver.quit()
            quit()


#pyinstaller ./main.py --onefile --noconsole --add-binary "./driver/chromedriver.exe;./driver"
