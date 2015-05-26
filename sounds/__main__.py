
import os
if os.name == 'nt':
    import winsound


def male_report(words):
    if os.name == 'posix':
        os.system("say "+words)
    else:
        
