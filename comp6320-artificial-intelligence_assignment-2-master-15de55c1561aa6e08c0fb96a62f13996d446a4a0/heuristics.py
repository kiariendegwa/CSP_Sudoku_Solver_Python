# COMP3620/6320 Artificial Intelligence
# The Australian National University - 2014

""" Student Details
    Student Name: Kiarie Ndegwa
    Student number: u4742829
    Date: start 6/4/2015
"""
from _dbus_bindings import String
from test.test_support import temp_cwd
from __builtin__ import min
from audioop import reverse
import csp

""" This is where you need to write your heuristics for variable selection and
    value ordering.
    
    Information about these heuristics can be found in the Constraint Satisfaction Problems
    chapter of the text book.
    
    You will need to implement: degree_heuristic, mrv_heuristic,
        degree_mrv_heuristic, mrv_degree_heuristic, and
        least_constrained_value_ordering
        
    To do this you will need to understand the structure of a CSP.
    Look in the file csp.py to understand this.
"""

#-------------------------------------------------------------------------------
# Variable Selection Heuristics
#-------------------------------------------------------------------------------

def next_variable_heuristic(assignment, csp):
    """ Select the next variable from the remaining variables.
        This heuristic just selects the next variable in the CSP's variable list.
        Return None if there are no remaining unassigned variables.
        
        We have implemented this one for you.
        
        ({str : str}, CSP) -> str
    """
    for var in csp.variables:
        if var not in assignment:
            return var
    return None
    

def degree_heuristic(assignment, csp):
    """ Constraining variables:
    
        Select the next variable from the CSP given the current assignment.
        Return None if there are no remaining unassigned variables.
        
        This heuristic implements the maximum degree heuristic.
        
        It returns the variable that is involved in the largest number of
        constraints on other unassigned variables. 
        
        That is, it returns the variable with the most unassigned neighbours.
        
        It can break ties between variables arbitrarily.
        
        ({str : str}, CSP) -> str
    """
    var_n ={} #detects number of unassigned neighbours in constraint graph given each node, eg var = 81:, 12 unassigned neigbours 
    var = csp.variables
    for i in var:
        if i not in assignment:
            temp = [j for j in csp.neighbours[i] if j not in assignment] 
            var_n[i] = len(temp)
    #mrv picks the least constrain-ed var: Therefore node with least edges
    ordered_var_n =sorted(var_n, key = var_n.get, reverse = True) #variables ordered in terms of edges they have, i.e. descending order
                                                                 #i.e. picks the least constrain-ed var/constrain-ing variable
    
    if len(ordered_var_n) !=1:
        return ordered_var_n[0]
    else: return None

def mrv_heuristic(assignment, csp):
    """ 
        Contrained variables:
        
        Select the next variable from the CSP given the current assignment.
        Return None if there are no remaining unassigned variables.
        
        This heuristic implements the minimum remaining values (MRV) heuristic.
        
        It can break ties between variables arbitrarily.
        
        ({str : str}, CSP) -> str
    """
    var_n ={} #detects number of unassigned neighbours in constraint graph given each node, eg var = 81:, 12 unassigned neigbours 
    var = csp.variables
    for i in var:
        if i not in assignment:
            temp = [j for j in csp.neighbours[i] if j not in assignment] 
            var_n[i] = len(temp)
    #mrv picks the least constrain-ed var: Therefore node with least edges
    ordered_var_n =sorted(var_n, key = var_n.get) #variables ordered in terms of edges they have, i.e. ascending order
                                                 #i.e. picks most constrain-ed var
    
    if len(ordered_var_n) !=1:
        return ordered_var_n[0]
    else: return None
    
def degree_mrv_heuristic(assignment, csp):
    """ Wild card: i.e. constrained and then constraining
        
        Select the next variable from the CSP given the current assignment.
        Return None if there are no remaining unassigned variables.
        
        This heuristic implements the maximum degree heuristic.
        It then uses the MRV heuristic for tie breaking.
        
        ({str : str}, CSP) -> str
    """
    
    var = degree_heuristic(assignment, csp)

    if var != None:
        assignment[var] = list(csp.current_domains[var])[0]
    
    var_m = mrv_heuristic(assignment, csp)
   
    return var_m

def mrv_degree_heuristic(assignment, csp):
    
    """ 
        This heuristic implements the MRV heuristic and then the maximum degree
        heuristic for tiebreaking.
        
        ({str : str}, CSP) -> str
    """
   
    var_m = mrv_heuristic(assignment, csp)
    if var_m != None:
        assignment[var_m] = list(csp.current_domains[var_m])[0]
    
    print 'assignment after', len(assignment)
    var = degree_heuristic(assignment, csp)
    return var

#-------------------------------------------------------------------------------
# Value Ordering Heuristics
#-------------------------------------------------------------------------------

def default_value_ordering(var, assignment, csp):
    """ Select an ordering of the values of the given variable given the current
        assignment and the CSP.
        
        This heuristic just returns the default ordering.
        
        We have implemented this heuristic for you.
        
        (str, {str : str}, CSP) -> [str]
    """
    return list(csp.current_domains[var])


def least_constrained_value_ordering(var, assignment, csp):
    """ Select an ordering of the values of the given variable given the current
        assignment and the CSP.
        
        This heuristic returns values in order of how constraining they are.
        It prefers the value that rules out the fewest choices for the
        neighbouring variables in the constraint graph.
        
        That is, it prefers values which remove the fewest elements from the current
        domains of their neighbouring variables.
        
        (str, {str : str}, CSP) -> [str]
    """
    current_var = var
    var_list = default_value_ordering(var, assignment, csp)
    
    temp_neigbour = list(csp.neighbours[current_var])
    domain_copy = {} #copy of all neighbouring vatiables domain lengths
    lcv_av = {} # contains k, v, pairs, of values and average length of their neighbourng domainss 
    lcv = {}
    
    for j in range(0, len(temp_neigbour)):
        domain_copy[temp_neigbour[j]] = map(int, list(csp.current_domains[temp_neigbour[j]]))
        
    for k, v in domain_copy.iteritems():
        for i in var_list:
            if i in v:
                v.remove(i) #each chosen variable taken out form neihbouring domains
                lcv_av[k] = [len(v), i]
   
    for i in var_list:
        temp =0
        for k in temp_neigbour:
            t = list(csp.current_domains[k])
            
            if i in t:
                t.remove(i)
            
            temp+=len(t)
            
        #average length of domains given a value assigned to a neighbouring
        #variable
        lcv[i] = float(temp)/len(temp_neigbour)
       
    return sorted(lcv, key = lcv.get, reverse=True)
        
#-------------------------------------------------------------------------------
# Functions used by the system to select from the above heuristics for the search
# You do not need to look any further.
#-------------------------------------------------------------------------------

def get_variable_selection_function(variable_heuristic):
    """ Return the appropriate variable selection function
    
        (str) -> ({str : str}, CSP) -> str
    """
    if variable_heuristic == "next":
        return next_variable_heuristic
    
    if variable_heuristic == "degree":
        return degree_heuristic
    
    if variable_heuristic == "mrv":
        return mrv_heuristic
    
    if variable_heuristic == "degree-mrv":
        return degree_mrv_heuristic
    
    if variable_heuristic == "mrv-degree":
        return mrv_degree_heuristic
    
    assert False, "Error: unknown variable selection heuristic: " +\
        str(variable_heuristic)
    
  
def get_value_ordering_function(value_heuristic):
    """ Return the appropriate value ordering function.
        (str) -> (str, {str : str}, CSP) -> [str]
    """
    if value_heuristic == "default":
        return default_value_ordering
    
    if value_heuristic == "lcv":
        return least_constrained_value_ordering
    
    assert False, "Error: unknown value ordering heuristic: " +\
        str(value_heuristic)
    

