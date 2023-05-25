import random
import numpy as np

def VerifyBurstStatus(Horse):
    
    if Horses[Horse]["RacePlaceHolders"]["BurstActive"] == True:
        
        if Horses[Horse]["RacePlaceHolders"]["BurstActiveCount"] < Horses[Horse]["RacePlaceHolders"]["BurstActiveSpread"]:
            Horses[Horse]["RacePlaceHolders"]["BurstActiveCount"] = Horses[Horse]["RacePlaceHolders"]["BurstActiveCount"] + 1
            print("Burst is active:", Horses[Horse]["RacePlaceHolders"]["BurstActiveCount"], "out of ", Horses[Horse]["RacePlaceHolders"]["BurstActiveSpread"])
            return True
        else:
            return False
    else:
        return False

def VerifyBurst(Horse, Distance):
    
    BurstPointOne = TrackDistance * .25
    BurstPointTwo = TrackDistance * .50
    BurstPointThree = TrackDistance * .75
    
    if Horses[Horse]["RacePlaceHolders"]["25th"] == False:
        if Distance >= BurstPointOne:
            Horses[Horse]["RacePlaceHolders"]["25th"] = True
            Horses[Horse]["RacePlaceHolders"]["BurstActivePoint"] = "1"
            return True
            
    else:
        if Horses[Horse]["RacePlaceHolders"]["Median"] == False:
            print("Haven't reached Median")
            if Distance >= BurstPointTwo:
                Horses[Horse]["RacePlaceHolders"]["Median"] = True
                Horses[Horse]["RacePlaceHolders"]["BurstActivePoint"] = "2"
                return True
        else:     
            if Horses[Horse]["RacePlaceHolders"]["75th"] == False:
                print("Haven't reached 75th")
                if Distance >= BurstPointThree:
                    Horses[Horse]["RacePlaceHolders"]["75th"] = True
                    Horses[Horse]["RacePlaceHolders"]["BurstActivePoint"] = "3"
                    return True
            
    return False

def ApplyConfidence( Horse, FavoredWeight):
    NormalWeight = ( 1 - FavoredWeight ) - ( Horses[Horse]["Traits"]["Confidence"] * 0.01 )
    FavoredWeight = FavoredWeight + ( Horses[Horse]["Traits"]["Confidence"] * 0.01 )
    try:
        return np.random.choice([ True, False ], p=[ FavoredWeight, NormalWeight ] )
    except:
        return True
 
#Obtain amount of Strides Burst will be Active for
def BurstLength(Horse):
    
    FavoredSpread = Horses[Horse]["Traits"]["BurstSpread"]
    BurstSpreadSelections = [2, 3, 4, 5]
    BurstSpreadSelections.remove(FavoredSpread)
    InFavor = ApplyConfidence( Horse, 0.25 )
    DesignatedLength = False
    if InFavor == True:
        Horses[Horse]["RacePlaceHolders"]["BurstActiveSpread"] = FavoredSpread
    else:
        Horses[Horse]["RacePlaceHolders"]["BurstActiveSpread"] = np.random.choice(BurstSpreadSelections)

def activeRoll(Horse, CurrentStride):
    BurstPoint = Horses[Horse]["RacePlaceHolders"]["BurstActivePoint"]
    StrideVar = CurrentStride + ( CurrentStride * Horses[Horse]["Traits"]["Burst"][BurstPoint]) 
    FavoredList = list(range(int(CurrentStride), int(StrideVar),1) )
    return np.random.choice(FavoredList)
    
    
def burstRoll(Horse, CurrentStride, MaxRange, MinRange ):
    CurrentRoll = False
    BurstPoint = Horses[Horse]["RacePlaceHolders"]["BurstActivePoint"]
    StrideVar = CurrentStride + round( CurrentStride * Horses[Horse]["Traits"]["Burst"][BurstPoint])
    
    if StrideVar > MaxStride:
        StrideVar = MaxStride
        
    FavoredList = list(range(int(CurrentStride + 1), int(StrideVar + 1),1) )
    NormalList = list(range(int(MinRange), int(MaxRange + 1),1) )
    # Calculate the weight FavoredList held overall percentage wise to add a 6% favor to it, could Bloodline affect this?
    FavoredWeight = len(FavoredList) / len(NormalList)
    FavoredSet = set(FavoredList)
    NormalSet = set(NormalList)
    NormalList = list( NormalSet - FavoredSet )
    print( CurrentStride, StrideVar, FavoredList, NormalList )
    #Stage 1 is 6% Var, all numbers within the 6% Var will be in favor when rolling
    InFavor =  ApplyConfidence(Horse, FavoredWeight)
    if InFavor == True:
        CurrentRoll = np.random.choice(FavoredList)
        if Horses[Horse]["RacePlaceHolders"]["BurstActive"] == False:
            Horses[Horse]["RacePlaceHolders"]["BurstActive"] = True
            BurstLength(Horse)
            Horses[Horse]["RacePlaceHolders"]["BurstActivePoint"] = BurstPoint
            
    if InFavor == False:
        CurrentRoll = np.random.choice(NormalList)
    print("Burst Available for:", Horse, "Roll", CurrentRoll, "PriorRoll", CurrentStride, "Favored", InFavor)
    return CurrentRoll
    
def normalRoll(CurrentStride, RollrangeMax, RollRangeMin):
        
    CurrentRoll = random.randint(int(RollRangeMin), int(RollRangeMax))
    
    print("Roll:", CurrentRoll) 
    return CurrentRoll

def verifyMomentum(Horse):
    
    priorRoll = Horses[Horse]["RacePlaceHolders"]["PriorRoll"]
    
    if priorRoll != False:
        if priorRoll < Horses[Horse]["Traits"]["Stride"]:
            #Momentum is active
            Horses[Horse]["RacePlaceHolders"]["MomentumStatus"] = True
            return True
        else:
            return False
    else:
        return False
    
def momentumRoll(Horse, CurrentStride, MaxRange, MinRange):
    CurrentRoll = False
    momentumStreak = Horses[Horse]["RacePlaceHolders"]["MomentumStreak"]
    
    if momentumStreak > 3:
        momentumStreak = 3
        
    StrideVar = ( CurrentStride + 1 ) + round( CurrentStride * Horses[Horse]["Traits"]["Momentum"][momentumStreak] )
    
    if StrideVar > MaxStride:
        StrideVar = MaxStride
        
    FavoredList = list(range(int(CurrentStride + 1), int(StrideVar + 1),1) )
    NormalList = list(range(int(MinRange), int(MaxRange + 1),1) )
    # Calculate the weight FavoredList held overall percentage wise to add a 6% favor to it, could Bloodline affect this?
    FavoredWeight = len(FavoredList) / len(NormalList)
    FavoredSet = set(FavoredList)
    NormalSet = set(NormalList)
    NormalList = list( NormalSet - FavoredSet )
    print( CurrentStride, StrideVar, FavoredWeight, FavoredList, NormalList )
    #Stage 1 is 6% Var, all numbers within the 6% Var will be in favor when rolling
    InFavor =  ApplyConfidence(Horse, FavoredWeight)
    if InFavor == True:
        CurrentRoll = np.random.choice(FavoredList)            
    if InFavor == False:
        CurrentRoll = np.random.choice(NormalList)
    print("Momentum Applied for:", Horse, "Roll", CurrentRoll, "PriorRoll", CurrentStride, "Favored", InFavor)
    return CurrentRoll

def verifyExhaustion(Horse):
    
    priorRoll = Horses[Horse]["RacePlaceHolders"]["PriorRoll"]
    
    if priorRoll != False:
        if priorRoll > Horses[Horse]["Traits"]["Stride"]:
            #Exhaustion is active
            Horses[Horse]["RacePlaceHolders"]["ExhaustionStatus"] = True
            return True
        else:
            return False
    else:
        return False
    
def exhaustionRoll(Horse, CurrentStride, MaxRange, MinRange):
    CurrentRoll = False
    exhaustionStreak = Horses[Horse]["RacePlaceHolders"]["ExhaustionStreak"]
    
    if exhaustionStreak > 3:
        exhaustionStreak = 3
        
    StrideVar = ( CurrentStride + 1 ) - round( CurrentStride * Horses[Horse]["Traits"]["Exhaustion"][exhaustionStreak] )
    
    if StrideVar < MinStride:
        StrideVar = MinStride + 1
        
    if StrideVar != MinStride:
        StrideVar = StrideVar - 1
        
    FavoredList = list(range(int(StrideVar), int(CurrentStride ), 1) )
    NormalList = list(range(int(MinRange), int(MaxRange + 1),1) )
    # Calculate the weight FavoredList held overall percentage wise to add a 6% favor to it, could Bloodline affect this?
    FavoredWeight = len(FavoredList) / len(NormalList)
    FavoredSet = set(FavoredList)
    NormalSet = set(NormalList)
    NormalList = list( NormalSet - FavoredSet )
    print( CurrentStride, StrideVar, FavoredWeight, FavoredList, NormalList )
    #Stage 1 is 6% Var, all numbers within the 6% Var will be in favor when rolling
    InFavor =  ApplyConfidence(Horse, FavoredWeight)
    if InFavor == True:
        CurrentRoll = np.random.choice(FavoredList)            
    if InFavor == False:
        CurrentRoll = np.random.choice(NormalList)
    print("Exhaustion Applied for:", Horse, "Roll", CurrentRoll, "PriorRoll", CurrentStride, "Favored", InFavor)
    return CurrentRoll

def defineWinnerandPlacement(Horses, TrackDistance, StartingDistance, positioningDict):
    # if possible winners are the same distance away from finish line the one with the highest stride wins, else if multiple winners determine the correct winner and determine correct placement for each horse.
    tempPositioningPlaceholder = {}
    placingHorses = []
    print("PositionDict in Placement Function", positioningDict)
    
    def inputPosition(H):
        if len(positioningDict) == 0:
            positioningDict[1] = H
        else:
            positioningDict[len(positioningDict) + 1] = H 
            
        
    for Horse in Horses:
    
        if len(positioningDict) == 0:
            if Horses[Horse]["RacePlaceHolders"]["CurrentDistance"] >= TrackDistance:
                placingHorses.append(Horse)
                    
        else:
            if Horse not in list(positioningDict.values()):
                if Horses[Horse]["RacePlaceHolders"]["CurrentDistance"] >= TrackDistance:
                    placingHorses.append(Horse)
                
    if len(placingHorses) == 0:
        return positioningDict
    
    if len(placingHorses) == 1:
        #Add horse to positioning Dict and return, if len of dict is 0 add horse to first placement else if greater then 0 obtain the highest ranking key and add the horse ex { 1: "ZedA", 2: "ZedB" }
        inputPosition(placingHorses[0])
    
    if len(placingHorses) > 1:
        # If multiple horses reach the finish line during the same stride then to determine the order of placement from such horses       
        tempRankingList = []
        
        for Horse in placingHorses:            
            distanceFromFinish = TrackDistance - StartingDistance 
            Ranking = ( ( Horses[Horse]["Traits"]["Stride"] - distanceFromFinish ) + Horses[Horse]["Traits"]["Stride"] ) / 2
            tempPositioningPlaceholder[Ranking] = Horse
            tempRankingList.append(Ranking)
            print(Horse, Ranking)
            
        while len(tempRankingList) > 0:
            maxRanking = max(tempRankingList)
            inputPosition(tempPositioningPlaceholder[maxRanking])
            tempRankingList.remove(maxRanking)
            
    return positioningDict
            
            
                

racesRaced = 0
racingStatistics = {}

#Get statistics, save to excel or file to reload, data; how many times did a horse burst per race, how many horses bursted at the same time per burst point, how many times did a horse gain momentum per race, streak per momentum, how many times did a horse gain exhaustion per race, streak per exhaustion, overall win rate per horse, overall win rate per bloodline, overall burst rate per bloodline, overall momentumrate for all bloodlines, overall exhaustion rate per all bloodlines, avg stride per bloodline in race, max stride per bloodline in race, min stride per bloodline in race. the difference of the spread for each horse per Burst Point, 


while racesRaced < 1:
    Horses = { "ZedA": { "Traits": { "Stride": 12, "Confidence": 8, "Burst": { "1": .16, "2": .12, "3": .24 }, "BurstSpread": 4, "Momentum": { 1: .16, 2: .13, 3: .9 }, "Exhaustion": { 1: .12, 2: .8, 3: .16 } }, "RacePlaceHolders": { "PriorRoll": False, "MomentumStatus": False, "MomentumStreak": 1, "TotalMomentumCount": 0, "ExhaustionStatus": False, "ExhaustionStreak": 1, "TotalExhaustionCount": 0, "BurstActive": False, "BurstActivePoint": False, "BurstActiveSpread": False, "BurstActiveCount": 1, "CurrentDistance": 0, "25th": False, "Median": False, "75th": False} }, "ZedE": { "Traits": { "Stride": 12, "Confidence": 8, "Burst": { "1": .16, "2": .12, "3": .24 }, "BurstSpread": 4, "Momentum": { 1: .16, 2: .13, 3: .9 }, "Exhaustion": { 1: .12, 2: .8, 3: .16 } }, "RacePlaceHolders": { "PriorRoll": False, "MomentumStatus": False, "MomentumStreak": 1, "ExhaustionStatus": False, "ExhaustionStreak": 1, "BurstActive": False, "BurstActivePoint": False, "BurstActiveSpread": False, "BurstActiveCount": 1, "CurrentDistance": 0, "25th": False, "Median": False, "75th": False} } }
    
    positioningDict = {}
    CurrentDistance = 0
    LastPlacingDistance = 0
    TrackDistance = 1000
    MinStride = 10
    MaxStride = 60
    leadingHorse = False
    losingHorse = False
    raceCompleted = False
    
    while raceCompleted == False:
        # For Horses get horse currentspeed and apply roll at each iteration
        # Horse can't gain momentum while a horse is in exhaustion but can gain boost and cancel exhaustion, Horse can't gain exhaustion while boost is active, horse can gain exhaustion while momentum is active, you can't gain momentum while boost is active, you can gain boost while momentum is active   
        for Horse in Horses:
            #print(Horse)
            CurrentStride = Horses[Horse]["Traits"]["Stride"]
            CurrentRoll = False
            startingDistance = Horses[Horse]["RacePlaceHolders"]["CurrentDistance"] 
            
            #Variance in which a horse can different speed per iteration
            RollVar = CurrentStride * .6
            RollRangeMin = CurrentStride - RollVar
            RollRangeMax = CurrentStride + RollVar
            
            if RollRangeMax > MaxStride:
                RollRangeMax = MaxStride
            if RollRangeMin < MinStride:
                RollRangeMin = MinStride
                
            isNormal = True
            isMomentum = Horses[Horse]["RacePlaceHolders"]["MomentumStatus"]
            isExhaustion = Horses[Horse]["RacePlaceHolders"]["ExhaustionStatus"]
            isBurst = False
            #Verify if Burst is active for current iteration
            isActive = VerifyBurstStatus(Horse)
                       
            # If Burst is not active verify if horse has reached burst point 
            if isActive == False:
                isBurst = VerifyBurst(Horse, Horses[Horse]["RacePlaceHolders"]["CurrentDistance"])
                
            # If Horse has reached Burst Point start Burst Roll if not do Momentum or Exhaustion roll
            if isBurst != False:
                isNormal = False
                CurrentRoll = burstRoll( Horse, CurrentStride, RollRangeMax, RollRangeMin )
                print("Burst!", "Roll:", isBurst)
            else:
                if isMomentum != False:
                    isNormal = False
                    if isActive == False:
                        if isBurst == False:
                            CurrentRoll = momentumRoll(Horse, CurrentStride, RollRangeMax, RollRangeMin )
                            Horses[Horse]["RacePlaceHolders"]["MomentumStreak"] = Horses[Horse]["RacePlaceHolders"]["MomentumStreak"] + 1
                            
                if isExhaustion != False:
                    isNormal = False
                    if isActive == False:
                        if isBurst == False:
                            CurrentRoll = exhaustionRoll(Horse, CurrentStride, RollRangeMax, RollRangeMin )
                            Horses[Horse]["RacePlaceHolders"]["MomentumStreak"] = Horses[Horse]["RacePlaceHolders"]["MomentumStreak"] + 1
                
            if isActive != False:
                isNormal = False
                CurrentRoll = activeRoll( Horse, CurrentStride )
            
            if isNormal == True:
                CurrentRoll = normalRoll(CurrentStride, RollRangeMax, RollRangeMin)
            
            #Update Horses Info end of Roll
            Horses[Horse]["RacePlaceHolders"]["PriorRoll"] = Horses[Horse]["Traits"]["Stride"]
            Horses[Horse]["Traits"]["Stride"] = CurrentRoll
            Horses[Horse]["RacePlaceHolders"]["CurrentDistance"] = Horses[Horse]["RacePlaceHolders"]["CurrentDistance"] + CurrentRoll
             
            # Verify if Horse has gained Momentum during this iteration or Exhaustion
            isMomentum = verifyMomentum(Horse)
            isExhaustion = verifyExhaustion(Horse)
                
            if isMomentum == True:
                Horses[Horse]["RacePlaceHolders"]["MomentumStatus"] = True
                print(Horse, "has gained Momentum")
            else:
                Horses[Horse]["RacePlaceHolders"]["MomentumStatus"] = False

                
            if isExhaustion == True:
                Horses[Horse]["RacePlaceHolders"]["ExhaustionStatus"] = True
                print(Horse, " has become Exhausted")
            else:
                Horses[Horse]["RacePlaceHolders"]["ExhaustionStatus"] = False
                
                
            if leadingHorse != False:
                if Horse != leadingHorse:
                    if Horses[Horse]["RacePlaceHolders"]["CurrentDistance"] > Horses[leadingHorse]["RacePlaceHolders"]["CurrentDistance"]:
                        leadingHorse = Horse
            else:
                leadingHorse = Horse
                
            if losingHorse != False:
                if Horse != losingHorse:
                    if Horses[Horse]["RacePlaceHolders"]["CurrentDistance"] < Horses[losingHorse]["RacePlaceHolders"]["CurrentDistance"]:
                        losingHorse = Horse
            else:
                losingHorse = Horse
                
            CurrentDistance = Horses[leadingHorse]["RacePlaceHolders"]["CurrentDistance"]
            
            # Once a horse has passed the finish line start to obtain and define a horses placement 
            if CurrentDistance >= TrackDistance:
                positioningDict = defineWinnerandPlacement(Horses, TrackDistance, startingDistance, positioningDict)
                
            #print("Horse:", Horse, "Distance", Horses[Horse]["RacePlaceHolders"]["CurrentDistance"])
                
        LastPlacingDistance = Horses[losingHorse]["RacePlaceHolders"]["CurrentDistance"]
        #print(leadingHorse, "is leading with a map placement of", CurrentDistance)
        #print(losingHorse, "is losing with a map placement of", LastPlacingDistance)
        #print(positioningDict)
        if LastPlacingDistance >= TrackDistance:
            raceCompleted = True
            racesRaced = racesRaced + 1
        
