
import os, random
if os.name == 'nt':
    import winsound

males = ['', ' -v Daniel', ' -v Bruce', ' -v Fred']

def male_report_clean(words):
    if os.name == 'posix':
        os.system("say "+words+'. -r 200')
        return words
        

def male_report(words):
    if os.name == 'posix':
        os.system("say "+words+'. -r 200'+random.choice(males))
        return words
        
