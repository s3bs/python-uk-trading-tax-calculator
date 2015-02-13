"""
Useful utilities
"""


import pandas as pd
import numpy as np
import datetime

def star_line(line_length=110):
    return "".join(["*"]*line_length)+"\n"

def type_and_sense_check_arguments(classobject, kwargs, checkrequired=True):
    """
    Check that we have the right arguments being passed, of the right type
    
    If checkrequired is True then we make sure we have compulsory arguemnts
    """
    
    type_check_dict=classobject._type_check()
    possible_args_list=classobject._possible_args()

    for argname in kwargs:
        if argname not in possible_args_list:
            raise Exception("Cant construct or modify objectclass object with a %s" % argname)

        if not type(kwargs[argname]) is type_check_dict[argname]:
            raise Exception("Bad type for %s" % argname)

    if checkrequired:
        required_missing=[argname not in kwargs for argname in classobject._required_columns()]

        if any(required_missing):
            raise Exception("Compulsory argument missing")

    return kwargs

def list_of_dict_class_to_pandas_df(classobject, indexname=None):
    """
    Takes any classobject which is a list containing objects with some attributes; turns into pd dataframe
    
    Optional indexname
    """
    
    all_keys=[x._possible_args() for x in classobject]
    all_keys=list(set([j for i in all_keys for j in i]))
    
    ans={}
    for key in all_keys:
        ans[key]=[]
        for x in classobject:
            if key in dir(x):
                ans[key].append(getattr(x, key))
            else:
                ans[key].append(None)
    
    if indexname is None:
        ans=pd.DataFrame(ans)

    else:
        ans=pd.DataFrame(ans, index=ans[indexname])

    return ans
                 
def uniquets(df3):
    """
    Makes x unique
    """
    df3=df3.groupby(level=0).first()
    return df3

def repr_class(x):
    ans=", ".join(["%s:%s" % (name, str(getattr(x, name))) for name in x.argsused])
    
    return ans

def check_equal(lst):
    ## Are all elements in a list equal
    return lst[1:] == lst[:-1]

def check_identical_attribute(lst, element_name):
    ## Are all the elements in a list of objects with element_name equal
    listofelements=[getattr(x, element_name) for x in lst]
    return check_equal(listofelements)

def signs_match(x,y):
    ## Are the signs of x and y identical?
    newsign=np.sign(x)        
    oldsign=np.sign(y)
    
    return newsign==oldsign

def signs_match_list(xlist):
    if len(xlist)<2:
        return True
    
    return all(signs_match(xlist[idx], xlist[idx-1]) for idx in range(len(xlist))[1:]) 
    

def any_duplicates(xlist):
    if len(xlist)<2:
        return False

    xnewlist=sorted(xlist)
    
    return any(xnewlist[idx]== xnewlist[idx-1] for idx in range(len(xnewlist))[1:])

def tax_year(year=None):
    """
    Returns a tuple of datetime objects defining the start and end of a tax year (6 April to 5 April)
    
    (optional) year int is the calendar year when the year ended  
    """
    if year is None:
        ## use current year
        year=which_tax_year(datetime.datetime.now())
            
    next_tax_year_starts=datetime.datetime(year=year-1, month=4, day=6)
    next_tax_year_ends=datetime.datetime(year=year, month=4, day=5)
    
    return (next_tax_year_starts, next_tax_year_ends)

def which_tax_year(date_time):
    """
    Returns the tax year a date is in
    """
    
    thisapril6=datetime.datetime(year=date_time.year, month=4, day=6)
    if date_time>=thisapril6:
        year=date_time.year+1
    else:
        year=date_time.year

    return year

