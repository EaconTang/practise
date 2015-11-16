#coding=utf-8

def print_Highlighted_Red(str):
    print '\033[1;41m %s \033[1;m' %str
def print_Highlighted_Green(str):
    print '\033[1;42m %s \033[1;m' %str
def print_Highlighted_Brown(str):
    print '\033[1;43m %s \033[1;m' %str
def print_Highlighted_Blue(str):
    print '\033[1;44m %s \033[1;m' %str
def print_Highlighted_Magenta(str):
    print '\033[1;45m %s \033[1;m' %str
def print_Highlighted_Cyan(str):
    print '\033[1;46m %s \033[1;m' %str
def print_Highlighted_Gray(str):
    print '\033[1;47m %s \033[1;m' %str
def print_Highlighted_Crimson(str):
    print '\033[1;48m %s \033[1;m' %s

print_Highlighted_Blue('test')


#Set Color Class
class colors:
    BLACK         = '\033[0;30m'
    DARK_GRAY     = '\033[1;30m'
    LIGHT_GRAY    = '\033[0;37m'
    BLUE          = '\033[0;34m'
    LIGHT_BLUE    = '\033[1;34m'
    GREEN         = '\033[0;32m'
    LIGHT_GREEN   = '\033[1;32m'
    CYAN          = '\033[0;36m'
    LIGHT_CYAN    = '\033[1;36m'
    RED           = '\033[0;31m'
    LIGHT_RED     = '\033[1;31m'
    PURPLE        = '\033[0;35m'
    LIGHT_PURPLE  = '\033[1;35m'
    BROWN         = '\033[0;33m'
    YELLOW        = '\033[1;33m'
    WHITE         = '\033[1;37m'
    DEFAULT_COLOR = '\033[00m'
    RED_BOLD      = '\033[01;31m'
    ENDC          = '\033[0m'


print colors.BLUE   + "蓝色" + colors.ENDC
print colors.RED    + "红色" + colors.ENDC
print colors.YELLOW + "黄色" + colors.ENDC