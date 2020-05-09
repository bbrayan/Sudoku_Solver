import copy
# ---------------------------------------------------------
#                           AC3
# ---------------------------------------------------------
def AC3(csp):
    queue = []
    #generate arcs, into queue
    for x in csp:
        for c in x[2]:
            queue.append([x[0],c])
    while queue:
        v = queue.pop(0)
        was_revised, csp = revise(csp, v[0], v[1])
        if was_revised:
            if (len(csp[v[0]][1]) == 0):
                return False, csp
            for x in csp[v[0]][2]:
                if x != csp[v[1]][0]:
                    queue.append([x,v[0]])
    return True, csp


def revise(csp,v1,v2):    
    revised = False
    if len(csp[v2][1]) == 1:
        value = csp[v2][1][0]
        if value in csp[v1][1]: 
            csp[v1][1].remove(value)
            revised = True       
    return revised, csp

# ------------------------------------------------------------------
#                            Backtracking 
# ------------------------------------------------------------------
def backtrack_dfs(vars_doms_consts):
    var = None
    for vari in vars_doms_consts:
        if len(vari[1]) != 1:
            var = vari
            break
    if var != None:
        # for value in domain
        for val in copy.deepcopy(var[1]):
            # create infered CSP
            infered = inference(vars_doms_consts, var[0], val)
            if infered != False:
                result = backtrack_dfs(infered)
                if result != False:
                    return result
            var[1].remove(val)
    else: 
        return vars_doms_consts
    return False

def inference(vars_doms_consts, var, val):
    copy1 = copy.deepcopy(vars_doms_consts)
    # do the assignment
    copy1[var][1] = [val]
    # remove values from the relevent (by constraints) domains
    for const in copy1[var][2]:
        const_dom = copy1[const][1]
        if val in const_dom:
            # if assignments conflict then failure
            if len(const_dom) == 1:
                return False
            elif len(const_dom) == 2:
                copy1 = inference(copy1, const, const_dom[1 - const_dom.index(val)])
                if copy1 == False:
                    return False
    return copy1
# ------------------------------------------------------------------
#                            Format Input 
# ------------------------------------------------------------------
# createConsts returns a 2d array that contains arrays that have 
# an index value, an array of possible numbers,
# and a constraint list with the index of other values
def createConsts(array):
    vars_doms_consts = []
    counter = 0
    for j in range(0, 9):
        for i in range(0, 9):
            if array[j][i] == 0:
                temp = [counter, createConnstrantList(i,j,array), createConected(i,j,array)]
                vars_doms_consts.append(temp)
            else:
                temp = [counter, [array[j][i]], createConected(i,j,array)]
                vars_doms_consts.append(temp)
            counter += 1
    return vars_doms_consts


#this function creates a list of constraints, the indexes of other values
def createConected(i,j,array):
    conected = []
    for y in range(0, 9):
        if array[y][i] == 0 and not(y == j):
            conected.append((i + 1) + (y * 9) - 1)
    for x in range(0, 9):
        if array[j][x] == 0 and not(x == i):
            conected.append((x + 1) + (j * 9) - 1)

    xMin, xMax, yMin, yMax = findSquareRange(i, j)

    for x in range (xMin, xMax + 1):
        for y in range (yMin, yMax + 1):
            temp = (x + 1) + (y * 9) - 1
            if (array[y][x] == 0) and (temp not in(conected)) and (not(x == i and y == j)):
                conected.append(temp)
    return conected


# returns a list of all possible values that could exist in this index
def createConnstrantList(i,j,array):
    consts=[1,2,3,4,5,6,7,8,9]
    for y in range(0, 9):
        if array[y][i] in(consts):
            consts.remove(array[y][i])
    for x in range(0, 9):
        if array[j][x] in(consts):
            consts.remove(array[j][x])

    xMin, xMax, yMin, yMax = findSquareRange(i,j)

    for x in range(xMin, xMax + 1):
        for y in range(yMin, yMax + 1):
            if array[y][x] in(consts):
                consts.remove(array[y][x])
    return consts


# helper function that returns the parameters of the 
# square of the index we are looking at
def findSquareRange(i, j):
    if (i < 3 and j < 3):
        return 0,2,0,2
    elif (i < 3 and 2 < j < 6):
        return 0,2,3,5
    elif (i < 3 and 5 < j < 9):
        return 0,2,6,8
    elif (2 < i < 6 and j < 3):
        return 3,5,0,2
    elif  (5 < i < 9 and j < 3):
        return 6,8,0,2
    elif (2 < i < 6 and 2 < j < 6):
        return 3,5,3,5
    elif (5 < i < 9 and 2 < j < 6):
        return 6,8,3,5
    elif (2 < i < 6 and 5 < j < 9):
        return 3,5,6,8
    elif (5 < i < 9 and 5 < j < 9):
        return 6,8,6,8
# ---------------------------------------------------------------
#                            Get Input 
# ---------------------------------------------------------------
def sudokuInput():
    sudoku = [[0 for x in range(9)] for y in range(9)]
    name = input("Filename: ")
    f = open(name, "r")
    data = f.read()
    f = open(name, "r")
    i = 0
    # Sudoku file has NO SPACES between numbers
    if not data[1].isspace():
        for x in f:
            for j in range(9):
                sudoku[i][j] = int(x[j])
            i += 1
    # Sudoku file HAS SPACES between numbers
    else:
        for x in f:
            k = 0
            for j in range(0, 18, 2):
                sudoku[i][k] = int(x[j])
                k += 1
            i += 1
    f.close()
    return sudoku


# ----------------------------------------------------------
#                            Main
# ----------------------------------------------------------
array = sudokuInput()
vars_doms_consts = createConsts(array)
#for var in vars_doms_consts:
    #print(var[0], var[1], var[2])
print("-----------------------------------------------------------")
v, csp = AC3(vars_doms_consts)
#for var in csp:
    #print(var[0], var[1], var[2])
print("-----------------------------------------------------------")
csp = backtrack_dfs(csp)

# print answer -------------------
horizontalCount = 0
verticalCount = 0
vert = 0
if csp != False:
    for var in csp:
            print(str(var[1]).strip("[]"), end=' ')
            horizontalCount += 1
            verticalCount += 1
            if verticalCount == 3 and vert < 2:
                print("|", end = ' ')
                verticalCount = 0
                vert += 1
            if horizontalCount % 27 == 0:
                if horizontalCount < 81:
                    print("\n" + "-" * 6 + "|"+ "-" * 7 + "|"+ "-" * 6, end = '')
            if horizontalCount % 9 == 0:
                print()
                vert = 0
                verticalCount = 0
else:
    print("Returned False")
