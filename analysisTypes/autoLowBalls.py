import statistics


def autoLowBalls(analysis, rsRobotMatches):
    # Initialize the rsCEA record set and define variables specific to this function which lie outside the for loop
    rsCEA = {}
    rsCEA['AnalysisTypeID'] = 12
    numberOfMatchesPlayed = 0
    totalLowBallsList = []
    totalBallsList = []

    for matchResults in rsRobotMatches:
        rsCEA['Team'] = matchResults[analysis.columns.index('Team')]
        rsCEA['EventID'] = matchResults[analysis.columns.index('EventID')]
        autoDidNotShow = matchResults[analysis.columns.index('AutoDidNotShow')]
        scoutingStatus = matchResults[analysis.columns.index('ScoutingStatus')]
        # Skip if DNS or UR
        if autoDidNotShow == 1:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = 'DNS'
        elif scoutingStatus == 2:
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = 'UR'
        else:
            autoMoveBonus = matchResults[analysis.columns.index('AutoMoveBonus')]
            # Retrieve values from the matchResults and set to appropriate variables
            autoBallLow = matchResults[analysis.columns.index('AutoBallLow')]
            if autoBallLow is None:
                autoBallLow = 0
            
            autoBallHigh = matchResults[analysis.columns.index('AutoBallHigh')]
            if autoBallHigh is None:
                autoBallHigh = 0
            
            autoBallMiss = matchResults[analysis.columns.index('AutoBallMiss')]
            if autoBallMiss is None:
                autoBallMiss = 0
            
            defPlayedAgainst = matchResults[analysis.columns.index('SummDefPlayedAgainst')]
            if defPlayedAgainst is None:
                defPlayedAgainst = 0

            # Perform some calculations
            numberOfMatchesPlayed += 1
            totalAutoBalls = autoBallLow + autoBallLow
            totalLowBallsList.append(autoBallLow)
            totalBallsList.append(totalAutoBalls)

            if defPlayedAgainst == 0:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = \
                    str(autoBallLow)
            else:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Display'] = \
                    str(autoBallLow) + "*"
            rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Value'] = autoBallLow
            if autoBallLow > 3:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 5
            elif autoBallLow == 3:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 4
            elif autoBallLow < 3:
                rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 3
            else:
                if autoMoveBonus == 1:
                    rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 2
                else:
                    rsCEA['Match' + str(matchResults[analysis.columns.index('TeamMatchNo')]) + 'Format'] = 1

    if numberOfMatchesPlayed > 0:
        rsCEA['Summary1Display'] = round(statistics.mean(totalLowBallsList), 1)
        rsCEA['Summary1Value'] = round(statistics.mean(totalLowBallsList), 1)
        rsCEA['Summary2Display'] = statistics.median(totalLowBallsList)
        rsCEA['Summary2Value'] = statistics.median(totalLowBallsList)
        # summary 3 will be used for rank
        rsCEA['Summary4Display'] = round(statistics.mean(totalBallsList), 1)
        rsCEA['Summary4Value'] = round(statistics.mean(totalBallsList), 1)

    return rsCEA
