from optparse import OptionParser
import sys
import time

parser = OptionParser()
parser.add_option('-c','--config',dest='CONFIG_FILE',
                  help='specify a config file',
                  default='sanguo')
parser.add_option('-l','--log',dest='LOG_FILE',
                  help='specify a log file',
                  default='mails.test')
parser.add_option('-o','--output',dest='OUT_FILE',
                  help='specify the file to save the result',
                  default='result.%s'%str(time.time()))
parser.add_option('-n','--number',dest='NUMBER',
                  help='test int number',type='int',
                  default=10)

print parser.print_help()

print sys.argv
#args = ['-l','mails.test','-c','sanguo']
(options, args) = parser.parse_args()
#print options
print args
print options.CONFIG_FILE,type(options.CONFIG_FILE)
print options.LOG_FILE,type(options.LOG_FILE)
print options.OUT_FILE,type(options.OUT_FILE)
print options.NUMBER,type(options.NUMBER)
