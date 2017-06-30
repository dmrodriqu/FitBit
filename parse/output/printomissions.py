from findOmissions import MainData
import sys, getopt


def main(argv):
	jsonInputFile = ''
	outputFile = ''
	questionToQuery = ''


	try:
		opts, args = getopt.getopt(argv, 'dhioq:',['help', 'input', 'output', 'question='])
	except getopt.GetoptError:
		print 'findOmissions.py -h <help> -i <input> -o <output> -q <question>'
		sys.exit(2)
	for opt, arg in opts:
		if opt in ('-h', 'help'):
			print 'findOmissions.py -h <help> -i <input> -o <output> -q <question> \n' \
			+ 'input file provides path to .json file, output provides location to print, q provides question to find omissions for'
		elif opt in ('-i', '--input'):
			jsonInputFile = arg
		elif opt in ('-o' '--output'):
			outputFile = arg
		elif opt in ('-q','--question'):
			if 'psqi' in  str.lower(arg):
				questionToQuery = 'PSQI/Q10'
			elif 'sibdq' in str.lower(arg):
				questionToQuery = 'SIBDQ/Q10'
			if 'sleep' in  str.lower(arg):
				questionToQuery = 'SleepQualityVAS'
			elif 'vas' in str.lower(arg):
				questionToQuery = 'SubjectGlobalAssessmentVAS'
	data =  MainData()
	data.createTraversal()
	contactList = []
	for df in data.getSubsetData():
		df._setEnrollmentDate(df.getQuestionDate('Demo'))
		df.calculateCompletionDates()
		if questionToQuery == 'SubjectGlobalAssessmentVAS':
			df.findLastVAS(questionToQuery, 2)
			contactList.append(df.patientsToContact)
		else:
			print df.findOmissions(questionToQuery)
			if df.contactPatient:
				print "CONTACT PATIENT"
	print"Patients to Contact: \n" 
	print set([item for sublist in contactList for item in sublist])
		

if __name__ == "__main__":
	main(sys.argv[1:])