import copy
from gettext import find
from venv import create
from os import walk
import os


def get_available_tables():
    tablespath = os.path.abspath(os.getcwd())
    filenames = next(walk(tablespath), (None, None, []))[2]  # [] if no file
    available_tables = []
    for file in filenames:
        if("Int2-1-table " in file and ".txt" in file):
            file = file.replace("Int2-1-table ",'')
            file = file.replace(".txt",'')
            if(file.isdecimal()):
                available_tables.append(int(file))
    available_tables.sort()
    return available_tables

# display all the available tables
def display_available_tables(tables):
    if(tables.count == 0):
        print("\nNo available table")
    else:
        print("\nAvailable tables :")
        for table in tables:
            print(table, end=' ')
        print("")

#fct to get a dictionnary storing the file values
def get_dico(file):
    Arr=[]
    while 1:
        # read by character
        char = file.read(1)
        Arr.append(char)
        #stops reading
        if not char:
            break
    file.close()

# This function reads the file and saves it in the memory.
def read_from_file(file):
    constraint_table = {}
    for line in file:

        # For each line, we need to: remove the space, remove the \n, turn the strings into ints, and put the whole thing in an array. The following line does it all:
        values = list(map(lambda x: int(x), line.rstrip().split(' ')))

        # Then, we save the values in our dictionnary following this pattern:
        # {Key: (value, [constraints])}
        constraint_table[values[0]] = (values[1], values[2:])
    return constraint_table


# This function adds an alpha to the table read from memory.
def add_alpha(constraint_table):

    # The duration of alpha is 0.
    constraint_table[0] = (0, [])
    for i in constraint_table:

        # If the constraint array of a key is empty (and if the key is not 0 => Not alpha): we add 0 in the table
        if len(constraint_table[i][1]) == 0 and i != 0:
            constraint_table[i][1].append(0)


# This function returns True if a given element 'x' appears in a given dico. It returns False otherwise.
def verify_existence_dico(x, dico):
    for i in dico:
        if x in dico[i][1]:
            return True
    return False


# This function adds an omega to the table read from memory.
def add_omega(constraint_table):
    omega = len(constraint_table)

    # The duration of omega is null.
    constraint_table[omega] = (None, [])

    # We go through the constraint table ...
    for i in constraint_table:

        # ... and we add in the constraints of omega the elements that do not exist as constraints for other nodes.
        if i != omega and not verify_existence_dico(i, constraint_table):
            constraint_table[omega][1].append(i)

# This function gets the full constraint table.
def get_constraint_table(file):

    # First we load the table from the memory ...
    constraint_table = read_from_file(file)

    # ... then we compute alpha and omega and we return the table.
    add_alpha(constraint_table)
    add_omega(constraint_table)
    return constraint_table

#to get all vertices in an array 
def get_vertices(dico):
    vertices=[]

    #we fill vertices array with the keys from the dico
    for i in dico:
        vertices.append(i)
    vertices.sort()    

    return vertices

#to get all edges in an array 
def get_edges(dico):

    edges=[]
    # we fill edges array with the lists from the dico
    for k, v in dico.items():
        for i in v[1]:
            edges.append(i)

    return edges        

#to get all second column values in the graph we dispay (successors not sorted)
def get_second_col(dico):
    scol = []
    # we fill edges array with the lists from the dico
    for k, v in dico.items():
        for i in v[1]:
            scol.append(k)
    return scol            

#to get all successors vertices in an array 
def get_successors(edges,scol,vertices):
    #create a zip for edges and scol, to link edges and scol position, and sort it in edge ascending order
    successors = [x for _, x in sorted(zip(edges, scol))]
    edges.sort()

    return successors

#get all distances from the graph display (third column)
def get_distances(dico):

    vertices=get_vertices(dico)    
    edges=get_edges(dico) 
    scol=get_second_col(dico)
    successors=get_successors(edges,scol,vertices)
    
    distances=[]

    for i in range(0, len(edges)):
        if edges[i]==0:
            distances.append(0)
        else:
            distances.append(dico[edges[i]][0])

    return distances          

#display scheduling graph from dico
def display_graph(dico):

    vertices=get_vertices(dico)    
    edges=get_edges(dico) 
    scol=get_second_col(dico)
    successors=get_successors(edges,scol,vertices)

    print(len(vertices), " vertices")
    print(len(edges), " edges")

    #then we display the table like its showed in the example
    for i in range(0, len(edges)):
        #to handle edges going from alpha vertix
        if edges[i]==0:
            print(edges[i], "->", successors[i], "=", 0)
        #to handle edges going to all other vertices
        else:
            print(edges[i],"->",successors[i],"=",dico[edges[i]][0])

    return 0

#display adjacency matrix from dico
def display_adjacency_matrix(dico):

    vertices=get_vertices(dico)    
    edges=get_edges(dico) 
    scol=get_second_col(dico)
    successors=get_successors(edges,scol,vertices)

    vertices.append(-1)
    vertices.sort()
    if vertices[0]==-1:
        vertices[0]=" "

    AM=[]
    #we have the first row
    AM.append(vertices)
    #now we fill all the other rows
    for i in range (1,len(vertices)):
        new_row=[]
        new_row.append(vertices[i])
        for j in range (1,len(vertices)):
            new_row.append("0")
        AM.append(new_row)

    # fill the adjacency matrix
    for i in range(0, len(edges)):
        for j in range(0, len(successors)):
            if i==j:
                AM[edges[i]+1][successors[j]+1]=1

    #display the adjacency matrix
    for i in range(0, len(vertices)):
        for j in range(0, len(vertices)):
            if i<=10 :
                if j!=0:
                    if j>10 and i==0:
                        print("",AM[i][j], " ", end="")
                    else:
                        print(" ",AM[i][j]," ", end="")
                else :
                    print(AM[i][j]," ", end="")
            else:
                if j<2 and j!=0:
                    print("",AM[i][j]," ", end="")
                elif j>1:
                    print(" ", AM[i][j], " ", end="")
                else :
                    print(AM[i][j]," ", end="")
        print(" ")

    return 0

#display value matrix from dico
def display_value_matrix(dico):

    vertices=get_vertices(dico)    
    edges=get_edges(dico) 
    scol=get_second_col(dico)
    successors=get_successors(edges,scol,vertices)
    distances=get_distances(dico)

    vertices.append(-1)
    vertices.sort()
    if vertices[0] == -1:
        vertices[0] = " "

    VM = []
    # we have the first row
    VM.append(vertices)
    # now we fill all the other rows
    for i in range(1, len(vertices)):
        new_row = []
        new_row.append(vertices[i])
        for j in range(1, len(vertices)):
            new_row.append('*')
        VM.append(new_row)

    
    # fill the value matrix
    for i in range(0, len(edges)):
        for j in range(0, len(successors)):
            if i == j:
                VM[edges[i] + 1][successors[j] + 1] = distances[i]
                

    # display the value matrix
    for i in range(0, len(vertices)):
        for j in range(0, len(vertices)):
            if VM[i][j]=="*" or VM[i][j]==" ":
                print(" ", VM[i][j], " ", end="")     
            elif int(VM[i][j])>9:  
                print("", VM[i][j], " ", end="")      
            else:  
                print(" ", VM[i][j], " ", end="")         
        print(" ")
    return 0

# This function returns the number of negative edges in a graph.
def negative_weight_cpt(dico):
    cpt_negative_weight=0
    for k, v in dico.items():  
        if v[0] and v[0]<0:
            cpt_negative_weight+=1
    return cpt_negative_weight

# This function returns all the elements that are in the first given list but not in the second one.
def list_differences(list_1, list_2):
    differences = []
    for i in list_1:
        if i not in list_2:
            differences.append(i)
    return differences


def get_entries(dico, deleted):
    entries = []
    for i in dico:
        # if len(set(dico([i][1])).symmetric_difference(set(deleted)) == []):
        if i not in deleted and (list_differences(dico[i][1], deleted)) == []:
            entries.append(i)
    return entries

#to check if our table represents a scheduling graph : return 1 if its the case, 0 otherwise 
def check_scheduling_graph(dico):

    ### 1st check : check cycles  
    print("* Detecting a cycle")
    print("* Method of eliminating entry points")

    # This function will only virtually delete the nodes that have been entries: we will let them in the table, but we will add them to a "deleted" list, that represents all the nodes that were removed.
    # If a node is in this list, all the nodes that have it for constraints will count it as inexistant ; and if a node has all his constraints in the 'deleted' list (or no constraints in the case of alpha),
    # it means it is an entry. It will be added to the entries list and then to the deleted one.
    deleted = []
    entries = get_entries(dico, deleted)
    while len(deleted) != len(dico):
 
        #display new entries
        print("\nEntry points: ", end = "")
        for i in range (0, len(entries)):
            print(entries[i], end = " ")  
        print("")

        # If the list of entries is empty, it means we can't add any entries anymore. 
        # Since we're still in the while loop, it means the graph wasn't totally deleted yet (not all the nodes were added to the 'deleted' list). Having no more entries possible before
        # finishing to delete the graph means that there is a cycle. We return 0, the scheduling algorithms won't happen on this graph.
        if len(entries) == 0:
            print("There are no more entry points while there are still vertices.\n-> There is a cycle")  
            return 0 

        print("Eliminating entry points")

        # We add to the deleted tables all the new entries.
        for i in entries:
            deleted.append(i)

        print("Remaining vertices: ", end = "")
        for i in dico:
            if i not in deleted:
                print(i, end = " ")
        print("")

        # We get our new entries.
        entries = get_entries(dico, deleted)
        
    print("There are no more entry points, because we deleted all the vertices.\n-> There is no cycle")

    ### 2nd CHECK : check there are no negative-weight edges  
    # We want the number of negative weight to be 0. Otherwise, we return 0, and the scheduling algorithms won't happen on this graph.
    if negative_weight_cpt(dico)==0:
        print("\nThere are no negative-weight edges") 
    else : 
        print("\nSome edges have negative-weight") 
        return 0

    return 1


def get_successors_st(x):
    successors = []

    # We loop through the table...
    for i in constraint_table:

        # ... everytime 'x' appears as a constraint of 'i'...
        if x in constraint_table[i][1]:

            # ... then 'i' is a successor of 'x' and is appended.
            successors.append(i)
    return successors


# This function gets the successor table from the constraint table. The successor table is used to computer the latest dates.
def get_successor_table(constraint_table):
    successor_table = {}
    for i in constraint_table:

        # For each key from the constraint table, we create a key in the new table. The value (duration) stays the same.
        # We use get_successors() to find the successors of the key.
        successor_table[i] = (constraint_table[i][0], get_successors_st(i))
    return successor_table


# This function gets the critical path.
def get_critical_path():

    # We start by omega (last node)
    Tmp = len(earliest_dates) - 1
    critical_path = [latest_dates[Tmp][1]]

    # While we didn't reach alpha...
    while Tmp != 0:

        # ... we add the longest date constraint (or the source of its earliest date) of the last added node to the critical path...
        critical_path.insert(0, earliest_dates[Tmp][1])

        # ... then this node (the source of the earliest date of the last added node) becomes the new current node (for the next node to add).
        Tmp = earliest_dates[Tmp][1]
    return critical_path


# This function returns True if a given element 'x' appears in a given nested list. It returns False otherwise.
def verify_existence(x, nested_list):
    for i in nested_list:
        if x in i:
            return True
    return False


# This function checks if all the predecessors of a given node 'x' are already in the given rank list.
def to_add(x, cur_ranks):

    # We loop through the predecessors of x ...
    for i in constraint_table[x][1]:

        # ... and we verify if they are already in the rank list or not.
        if not verify_existence(i, cur_ranks):
            return False

    # If and only if they all validate the condition, we return True.
    return True


# This functions gets the ranks of the graph. They are stored in a double list.
def get_ranks():
    ranks = []
    count = 0
    i = 0

    # We continue as long as the count (of the elements added in the ranks list) is smaller than the number of nodes.
    while len(constraint_table) > count:
        ranks.append([])

        # We need to create a deep copy of the rank list so that an element that is added to a rank
        # does not influe on the other elements that need to be in the same rank.        
        current_ranks = copy.deepcopy(ranks)

        # We loop through the constraint table ...
        for j in constraint_table:

            # ... And we verify each time if the element verifies 2 conditions:
            # 1) It is not already in the rank list (with verify_existence() )
            # 2) All its predecessors are already in the rank list (with to_add() )
            if ((not verify_existence(j, ranks)) and (to_add(j, current_ranks))):
                ranks[i].append(j)

                # After appending the element that verified the 2 conditions to the list, we update the counter.
                count += 1
        i += 1
    return ranks


# This function returns a list of the elements in the order of which they need to be computed by the early dates and late dates algorithms.
def get_order(ranks, index):
    nodes = []

    # We loop through the ranks nested list and add the elements in a new 1 dimensional list.
    for i in ranks:
        for j in i:

            # The index will be either 0 (we add the values at the beginning, creating the list in the reverse order),
            # or the max size of the list (we add the values at the end, creating the list in the right order).
            nodes.insert(index, j)
    return nodes


# This function returns the earliest date for a given node x, represented by its list of predecessors.
# It is used by get_earliest_dates().
def get_largest(x, earliest_dates):
    
    # We set up our tuple. It represents: (duration, source). We begin with an empty one: (duration: -1, source: None).
    largest = (-1, None)

    # If we have alpha (no predecessors), we return (0, 0) that represents (duration: 0, source: alpha).
    if len(x) == 0:
        return (0, 0)

    # We loop through the predecessors.
    for i in x:

        # Each time, we verify if the computed element (earliest_dates[i][0] + constraint_table[i][0]) is larger than the previously computed ones.
        # If it is the case, it means that this newly computed element is the early date that we need to use.
        # It is going to be returned once we are sure that no others predecessors produces a bigger early date.
        if largest[0] < 0 or earliest_dates[i][0] + constraint_table[i][0] > largest[0]:

            # earliest_dates[i][0] + constraint_table[i][0] corresponds to: value of the predecessor in the early date table + its duration.
            largest = (earliest_dates[i][0] + constraint_table[i][0], i)
    return largest


# This function returns a dico with the earliest dates for each key.
def get_earliest_dates(nodes):
    earliest_dates = {}

    # We loop through the node_list (that was computed using the get_order function).
    for i in nodes:
        # For every value, we compute its earliest dates using get_largest().
        earliest_dates[i] = get_largest(constraint_table[i][1], earliest_dates)
    return earliest_dates


# This function returns the latest date for a given node i.
# It is used by get_latest_dates().
def get_smallest(i, latest_dates):

    # x represents the list of successors of i.
    x = successor_table[i][1]
    smallest = (-1, None)

    # If we have omega (no successors), we return (duration: early date of omega, source: omega).
    if len(x) == 0:
        return (earliest_dates[i][0], i)

    # Same principle as for the early dates.
    for j in x:
        if smallest[0] < 0 or latest_dates[j][0] - successor_table[i][0] < smallest[0]:
            smallest = (latest_dates[j][0] - successor_table[i][0], j)
    return smallest


# This function returns a dico with the earliest dates for each key.
# It is similar to get_earliest_dates()
def get_latest_dates(nodes):
    latest_dates = {}
    for i in nodes:
        latest_dates[i] = get_smallest(i, latest_dates)
    return latest_dates


# This function returns a dico with the flaots for each key.
def get_floats(nodes, latest_dates, earliest_dates):
    floats = {}

    # We loop through the nodes and, for each value, substract the earliest dates to the latest dates.
    for i in nodes:
        floats[i] = latest_dates[i][0] - earliest_dates[i][0]
    return floats

# The following functions are only to display the scheduling graph. They won't be explained.
def find_rank(x, ranks):
    for i in range(0, len(ranks)):
        if x in ranks[i]:
            return i

def print_loop(x, size):
    for i in range(0, size):
        print(x, end = "")

def print_str(value, size):
    print(str(value), end = '')
    print_loop(" ", size-len(str(value)))

def new_line():
    print("")

def end_of_line(x, string = ""):
    new_line()
    print_lines(x, len(order_early), 14, 8)
    if x != 5:
        print_str("│"+string, 15)
        print_loop("│", 1)

def print_lines(x, nb_col, size_first_col, size_col):
    if x == 0:
        first, middle, last = "┌", "┬", "┐"
    elif x == 5:
        first, middle, last = "└", "┴", "┘"
    else:
        first, middle, last = "├", "┼", "┤"

    print_loop(first, 1)
    print_loop("─", size_first_col)
    for i in range (0, nb_col):
        print_loop(middle, 1)
        print_loop("─", size_col)
    print_loop(last, 1)
    new_line()

def compute_board_values(row, col = -1):
    if row == 0:
        if col == -1:
            return "Ranks"
        return find_rank(col, ranks)
    if row == 1:
        if col == -1:
            return "Tasks"
        return col
    if row == 2:
        if col == -1:
            return "Earliest dates"
        return earliest_dates[col]
    if row == 3:
        if col == -1:
            return "Latest dates"
        return latest_dates[col]
    if col == -1:
        return "Floats"
    return floats[col]

def display_scheduling():
    for i in range(0, 5):
        end_of_line(i, compute_board_values(i))
        for j in order_early:
            print_str(compute_board_values(i, j), 8)
            print_loop("│", 1)
    end_of_line(5)
    print("\nThe critical path is: ", critical_path)


keep = True #used to check if the user still wants to and can check tables
bool = True #used later to check if the user entered an integer

while keep:
    available_tables = get_available_tables()
    display_available_tables(available_tables)

    if(available_tables == []): #no available table
        keep = False
        print("No available table")
    else:
        global param # global variable because it is needed later to reopen file to write in it(we think that is is better than passing the argument through all the functions)
        param = input("which table do you want to try ?  (press 0 to exit)\n")

        #try and catch to make sure we have a integer given by the user
        try:
            val=int(param)
            bool=True
        except ValueError:
            bool = False
            try:
                val = float(param)
                print("No.. input is not an integer. It's a float")
                print("You must chose a table from the list")
            except ValueError:
                print("No.. input is not an integer. It's a string")
                print("You must chose a table from the list")

        #this part is displayed only if the user entered an integer
        if bool==True:
            if(int(param) not in available_tables) :
                if int(param) == 0:
                    print("See you !")
                    keep = False
                else :
                    print("You must chose a table from the list")
            else:
                path = "Int2-1-table "
                extension = ".txt"

                # open file with given number parameter
                file = open(path + param + extension, "r")

                #create dictionary and store file content (and display it)
                constraint_table = get_constraint_table(file)
                print("* Creating the  graph :")
                display_graph(constraint_table)
                print(" ")


                # create table matrices (adjacency and value matrices)
                print("Representation of the table in a matrix form :")
                print("Adjacency Matrix :")
                display_adjacency_matrix(constraint_table)
                print(" ")
                print("Value Matrix :")
                display_value_matrix(constraint_table)
                print(" ")

                # check scheduling graph
                SG = check_scheduling_graph(constraint_table)
                if SG==1:
                    print("-> This is a scheduling graph")

                    successor_table = get_successor_table(constraint_table)
                    ranks = get_ranks()
                    order_early = get_order(ranks, len(constraint_table) - 1)
                    order_late = get_order(ranks, 0)
                    earliest_dates = get_earliest_dates(order_early)
                    latest_dates = get_latest_dates(order_late)
                    floats = get_floats(order_early, latest_dates, earliest_dates)
                    critical_path = get_critical_path()
                    
                    display_scheduling()

                else :    
                    print("-> This is NOT a scheduling graph")