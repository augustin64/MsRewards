#  MsReward


A Microsoft reward automator, designed to work headless on a raspberry pi. Tested with a pi 3b+ and a pi 4 2Gb .  
Using a discord bot to log eveything.  
Using Selenium and geckodriver.  
you have to put your credentials in the same folder as the script, in a file named `login.csv`. You have to put info this way : `email,password`   
you have to put two discord webhook links, the first one for success and the second one for failure, separated with a coma, in the same folder as the script, in a file named `webhook.txt`   
you have to put a list with a dictionnary in the same folder as the script, in a file named  `liste.txt`  .It should have a lot of words, used to make random search on bing, as shown in the example file.  

Python 3.**10** is mandatory
