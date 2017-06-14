# Finds and prints omissions of data to command line.

Command line usage:
$ python findomissions.py -h <help> -q <question> 

# Executable usage:

‘*’.command executables:

command executes findomissions.py as the following:
	
	python findomissions.py -q ‘*’

where asterisk denotes question to be queried

# Setup

1. Download .json file from the study-hub
2. Place .json file into this directory.
3. Run either the executable, or run the python file from the command line.

# Options

If using the command line stings for the -q option may be case insensitive variations of:
* sibdq
* psqi
* vas (pertains to global vas)
* sleep

* later additions wong baker

# Output:

For each ID, there will be 2, 4, or 5 lines of output possible:

If the patient completed dummy tasks during enrollment 
(which gives us a reference date for each patient)
we are able to calculate the following:

* anticipated survey delivery dates
* anticipated survey windows

With this information we can derive the following:

* ID
* Question completion dates within predicted window
* Question completion dates outside predicted window
* Surveys not completed with last date of possible completion

Please note, if a survey has not appeared, it has not yet been requested 
(and thus presented to the participant). 
I have compared the survey request times with the survey completion times
with respect to anticipated survey windows.

# Interpretation of Output:

The most common printout will be in the following form:

```
LJWQle 
 completed on following dates: [[datetime.datetime(2017, 6, 1, 0, 0)]] 
 completed after window on following dates (bug): [] 
 and did not complete by [] 
```

The first line represents the participant ID
The second line represents the dates of which 
the patient completed the survey in ISO notation (YYYY, MM, DD, HH, MM).
Hours and minutes are not calculated.
The above date can be read as 2017 June 1

The second line is included for any time that any individual is able to
complete or submit a survey outside of their given window.

Surveys not completed have the last day of completion noted in the last
line

If any surveys appear in the last line as in the below output:

```
joMLAD 
 completed on following dates: [] 
 completed after window on following dates (bug): [] 
 and did not complete by [datetime.datetime(2017, 6, 1, 0, 0)] 
CONTACT PATIENT
```

“CONTACT PATIENT” will appear. 

If the patient did not complete any of the dummy tasks, two lines will appear
denoting that the dates must be calculated.


