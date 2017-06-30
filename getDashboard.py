import parse
import sys, getopt

def main(argv):
	BoolSet = True
	try:
		opts, args = getopt.getopt(argv, 'dhdq:',['help','dates', 'question='])
	except getopt.GetoptError:
		print 'main.py -h <help> -d <dates> -q <question> '
		sys.exit(2)
	for opt, arg in opts:
		if opt in ('-h', 'help'):
			print 'findOmissions.py -h <help> -i <input> -o <output> -q <question> \n' \
			+ 'input file provides path to .json file, output provides location to print, q provides question to find omissions for'
		if opt in ('-d','--dates'):
			BoolSet = False
		if opt in ('-q','--question'):
			questionToQuery = arg
	result = parse.Results(questionToQuery)
	result.output(values = BoolSet) # gives dates, defaults to true to give values

if __name__ == '__main__':
	main(sys.argv[1:])
