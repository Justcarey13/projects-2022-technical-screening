"""
Inside conditions.json, you will see a subset of UNSW courses mapped to their 
corresponding text conditions. We have slightly modified the text conditions
to make them simpler compared to their original versions.

Your task is to complete the is_unlocked function which helps students determine 
if their course can be taken or not. 

We will run our hidden tests on your submission and look at your success rate.
We will only test for courses inside conditions.json. We will also look over the 
code by eye.

NOTE: This challenge is EXTREMELY hard and we are not expecting anyone to pass all
our tests. In fact, we are not expecting many people to even attempt this.
For complete transparency, this is worth more than the easy challenge. 
A good solution is favourable but does not guarantee a spot in Projects because
we will also consider many other criteria.
"""
import json

# NOTE: DO NOT EDIT conditions.json
with open("./conditions.json") as f:
    CONDITIONS = json.load(f)
    f.close()

################################### Check & Execute Single Condition #############################
def isSingle(condition):
    if sum(c.isdigit() for c in condition) == 4:
        return True
    if sum(c.isdigit() for c in condition) == 8: 
        return True
    return False

def excSingle(condition, courses_list):
    if sum(c.isdigit() for c in condition) == 4:
        for i, c in enumerate(condition):
            if c.isdigit():             
                if i-4 >= 0:
                    singleCon = condition[i-4:i+4]
                else:
                    singleCon = condition[i:i+4]
                if singleCon in courses_list:
                    return True
                else:
                    return False
    if sum(c.isdigit() for c in condition) == 8: 
        if "or" in condition:
            cOrs = condition.split("or")
            for cor in cOrs:
                if "(" in cor:
                    cor = cor[1:9]
                if ")" in cor:
                    cor = cor[0:-2]
                if cor in courses_list:
                    return True
            return False     

################################### Check & Execute Simple UOC Condition #############################
def isCompletion(condition):
    if "completion" in condition: return True
    else: return False

def excCompletion(condition, courses_list):
    if "completion" in condition:
        cComs = condition.split("completion")
        comUoc = cComs[1][2:4]
        # Assume all courses in the list have 6 uoc
        if len(courses_list) * 6 < int(comUoc):
            return False
        return True

################################### Check & Execute Annoying UOC Condition #############################
def isIn(condition):
    if "in(" in condition: return True
    else: return False

def excIn(condition, courses_list):
    cIns = condition.split("in(")
    cIn = cIns[1][0:-1]
    cInUoc = cIns[0][0:2]
    haveDone = 0
    for c in cIn.split(","):
        if c in courses_list:
            haveDone += 1
    # Assume all courses in the list have 6 uoc
    if haveDone * 6 < int(cInUoc):
        return False
    return True

################################### Check & Execute Annoying Level UOC Condition #############################
def isInLevel(condition):
    if "inlevel" in condition: return True
    else: return False

def excInLevel(condition, courses_list):
    cIns = condition.split("inlevel")
    clevel = cIns[1][0:1]
    cInUoc = cIns[0][-15:-13]
    haveDone = 0
    for c in courses_list:
        if str(c[0:4]) == "comp" and int(c[4:5]) == int(clevel):
            haveDone += 1
    # Assume all courses in the list have 6 uoc
    if haveDone * 6 < int(cInUoc):
        return False
    return True

def is_unlocked(courses_list, target_course):
    """Given a list of course codes a student has taken, return true if the target_course 
    can be unlocked by them.
    
    You do not have to do any error checking on the inputs and can assume that
    the target_course always exists inside conditions.json

    You can assume all courses are worth 6 units of credit
    """
    # Find condition for target course
    condition = CONDITIONS[target_course]
    # Sepatate cases to make condition more understandable
    condition = "".join(condition.split())
    courses_list = [each_string.lower() for each_string in courses_list]
    condition = condition.lower()

    # Empty
    if condition == "":
        return True

    # Compound
    if "and" in condition:
        cAnds = condition.split("and")
        for cand in cAnds:
            if isSingle(cand):
                # print(cand, excSingle(cand, courses_list))
                if not excSingle(cand, courses_list): return False
            if isCompletion(cand):
                # print(cand, excCompletion(cand, courses_list))
                if not excCompletion(cand, courses_list): return False
            if isIn(cand):
                # print(cand, excIn(cand, courses_list))
                if not excIn(cand, courses_list): return False
            if isInLevel(cand):
                # print(cand, excIn(cand, courses_list))
                if not excInLevel(cand, courses_list): return False
        return True

    # Single
    if isSingle(condition):
        if excSingle(condition, courses_list): return True
        else: return False
    
    # Simple UOC
    if isCompletion(condition):
        if excCompletion(condition, courses_list): return True
        else: return False

    # Annoying UOC
    if isIn(condition):
        if excIn(condition, courses_list): return True
        else: return False
    if isInLevel(condition):
        if excInLevel(condition, courses_list): return True
        else: return False  

    # Cross Discipline

    return False


        




    