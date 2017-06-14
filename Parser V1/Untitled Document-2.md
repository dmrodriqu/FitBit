# Parser V1 

This folder contains multiple programs designed to parse, export, analyze, and plot data from the first iteration of the Fitbit study. While the format of the data has since changed, the main principles of these programs remain consistent across study amendments. Thus, it is still important to include these files.

The below are the most relevant for future documentation.

## Parser
Parser is the main program responsible for parsing the first version of JSON files provided with this study. It is important to note that the format of the key value pairs has since changed and thus this program is now deprecated. 

The usage of the main class, Table, is contingent on whether the question to be parsed is a survey, biometric data, or discrete question data.

### Examples:

```python
psqiTable = Table()
psqiTable = createSurveyTable(fullDataFrame, 'PSQI')
sibdqTable = createSurveyTable(fullDataFrame, 'SIBDQ')

heart = Table()
heartSeries = heart.recursiveRows(fullDataFrame, 'Fitbit', 'Heart')
heartFrame = heart.createStepOrHeartColumns(fullDataFrame, heartSeries)
```

## csvparser

While originally parsed to CSV files, later parsed to ID indexed HD5, csvparser takes the above commands and converts parsed JSON files to HD5 files.

## surveyScoringTree

surveyScoringTree contains a class based on a tree that organizes in a heirarchical manner first by ID; then survey instance by date; then, if necessary, by question instance.

The main class, ScoringTree, holds all Participant instances. Participant instances, in turn, hold all ParticipantSurvey instances.

The ParticipantSurvey encapsulates methods that allow for the scoring of the PSQI and SIBDQ, while the Participant class encapsulates methods allowing for the aquisition of times completed.

