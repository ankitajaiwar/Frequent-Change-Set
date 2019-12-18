from __future__ import division
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 09:50:41 2018


@author: Ankita
"""


import pandas as pd
import datetime
from mlxtend.frequent_patterns import apriori
 

# $ git log --name-status --pretty=format:"**%h--%ad" --no-renames
#$ git log --pretty=format:"**%h--%an--%ad"

logauthors_one= "./commons-math/logauthors.log"
projectname_one ="commons-math"
logauthors_two= "./pdfbox/logauthors.log"
projectname_two="PDFBox"
gitlog_one = "./commons-math/git.log"
gitlog_two = "./pdfbox/git.log"

def functionone(pathfile, projectname):
    commits = pd.read_csv(pathfile, 
                      engine = 'python',
                      sep="\u00019", 
                      header=None, 
                      names = ['raw']
                      )

    #store line containing commits

    commit_line = commits[commits['raw'].str.startswith("**")]

    commit_line.drop_duplicates()
    
    #calculate total number of unique commits
    
    total_commits = commit_line['raw'].nunique(dropna=True)
    
    print("total number of commits in "+str(projectname)+" is....."+str(total_commits))
    print("-----------------------------------------------------------------------------")
    
    #seperate date from commits line

    commit_sep = commit_line['raw'].str.extract(r"^\*\*(?P<sha>.*?)--(?P<date>.*?)$",  expand=True) 
    

    commit_sep['date'] = pd.to_datetime(commit_sep['date'])

    file_line = commits[~commits.index.isin(commit_line.index)]
    

    file_stats = file_line['raw'].str.split("\t", expand=True)
    file_stats = file_stats.rename(columns={ 0: "type_of_operation", 1: "filename"})


    
    total_files = file_stats['filename'].nunique(dropna=True)

    commit_data = commit_sep.reindex( commits.index).fillna(method="ffill")
    commit_data = commit_data[~commit_data.index.isin(commit_line.index)]

    # merge file data and commit data into one dataframe
    commit_data = commit_data.join(file_stats)
    preprocessed_df = commit_data
    preprocessed_df = preprocessed_df.drop('type_of_operation', 1)
    # aggregating(count) according to files
    avgperfile = preprocessed_df.groupby(['filename']).agg([ 'count'])
    avgperfile.columns = ['shacount', 'datecount']
    avgperfile = avgperfile.reset_index()
    total_shacount = avgperfile['shacount'].sum()
    avgsha_files = total_shacount/total_files
    print(total_shacount)
    print("Average number of commits per file in "+projectname+" is "+str(avgsha_files)+" rounding off to"+str(round(avgsha_files))+" commits per contributor")
    print("------------------------------------------------------------------------------------------")
    m=0
    d=0
    a=0
    
    # calculating datetime(to find dates before 12 months from today)
    date_before = datetime.date.today() - datetime.timedelta(days = 12*365/12)
    commit_data_final = commit_data[commit_data['date'] > date_before]
    compute_mod = commit_data_final['type_of_operation'].tolist()
    for i in range(len(compute_mod)):
        if(compute_mod[i]=='M'):
            m=m+1
        elif(compute_mod[i]=='A'):
            a=a+1
        elif(compute_mod[i]=='D'):
            d=d+1
    print("Number of files added in "+projectname+"..."+str(a))
    print("Number of files deleted in "+projectname+"..."+str(d))
    print("Number of files modified in "+projectname+"..."+str(m))
    print("-----------------------------------------------------------------------------")
    return commit_data
        
#**********************************************************************************




def functiontwo(pathfile, projectname):
    #"C:/Users/ARUN/Documents/assgn 3 commons math/commons-math/logauthors.log"
    commitauth = pd.read_csv(pathfile, 
                      engine = 'python',
                      sep="\u00019", 
                      header=None, 
                      names = ['raw']
                      )
    # extract commit line
    commit_commitauth = commitauth[commitauth['raw'].str.startswith("**")]
    #seperate information like authors and date from the commit line
    commit_info = commit_commitauth['raw'].str.extract(r"^\*\*(?P<sha>.*?)--(?P<author>.*?)--(?P<date>.*?)$",  expand=True) 
    commit_info['date'] = pd.to_datetime(commit_info['date'])
    total_authors = commit_info['author'].nunique(dropna=True)
    print("Number of authors in project "+projectname+" is....."+str(total_authors))
    print("-----------------------------------------------------------------------------")
    avgperauthor = commit_info.groupby(['author']).agg([ 'count'])
    avgperauthor.columns = ['shacount', 'datecount']
    avgperauthor = avgperauthor.reset_index()
    total_shacount = avgperauthor['shacount'].sum()
    avgsha_author = total_shacount/total_authors
    print(total_shacount)
    print("Average number of commits per author in "+projectname+" is "+str(avgsha_author)+" rounding off to"+str(round(avgsha_author))+" commits per contributor")
    print("------------------------------------------------------------------------------------------")    
    date_before = datetime.date.today() - datetime.timedelta(days = 6*365/12)
    a = commit_info[commit_info['date'] > date_before]
    taut = commit_info['author']
    taut = taut.drop_duplicates()
    activeauth = a['author'] 
    activeauth = activeauth.drop_duplicates()
    activeauth = activeauth.tolist()
    taut = taut.tolist()
    inactiveauth = list(set(taut)-set(activeauth))
    print("Authors inacitve from past 6 or more months")
    print("-----------------------------------------------------------------------------") 
    for i in inactiveauth:
        print(i)
    c =[]
    complist = avgperauthor['shacount'].tolist()
    for i in range(len(complist)):
        val = (complist[i]/6345)*100
        c.append(val)
        datecount_list = avgperauthor['datecount'].tolist()
        shacount_list = avgperauthor['shacount'].tolist() 
        author_list = avgperauthor['author'].tolist()
        final_list = zip( author_list, shacount_list, datecount_list, c) 
        label = ['Authors', 'Shacount', 'Datecount', 'Percentage_contri']
    final_dframe = pd.DataFrame.from_records(final_list, columns = label)
    final_result = final_dframe[['Authors', 'Percentage_contri']]
    print("Percentage of changes done by each contributor in project..."+projectname)
    print(final_result)
    print("-----------------------------------------------------------------------------")
    return avgperauthor
    
def functionthree(dfdata):
    
    df = dfdata.drop(['date', 'type_of_operation'], axis =1)
    quantity =[]
    complist = dfdata['filename'].tolist()
    for i in range(len(complist)):
        quantity.append(1)
    
    sha_list = df['sha'].tolist() 
    file_list = df['filename'].tolist()
    final_list = zip( sha_list, file_list, quantity)
    label = [ 'sha', 'filename', 'Quantity']
    final_dframe = pd.DataFrame.from_records(final_list, columns = label)

    basket = (final_dframe
          .groupby(['sha', 'filename'])['Quantity']
          .sum().unstack().reset_index().fillna(0)
          .set_index('sha'))

    
    frequent_itemsets_df = apriori(basket, min_support=0.004, use_colnames=True)
    frequent_itemsets = frequent_itemsets_df['itemsets'].tolist()

    two_items = 0
    three_items=0
    four_items=0
    five_items=0


    print("Frequent itemsets, 4 set of two files, 3 set of 3 files, 2 set of 4 files and 1 set of 5 files that change together at least 3 times.")
    for i in frequent_itemsets:
        if ((len(i)==2)&(two_items<4)):
            two_items = two_items+1
            print i
            print("-------------------------------------------------------------------------------")
        
        elif((len(i)==3)&(three_items<3)):
            three_items = three_items+1
            print i
            print("--------------------------------------------------------------------------------")
        
        elif((len(i)==4)&(four_items<2)):
            four_items = four_items+1
            print i
            print("--------------------------------------------------------------------------------")
        elif((len(i)==5)&(five_items<1)):
            five_items = five_items+1
            print i 
            print("--------------------------------------------------------------------------------")
         

    

commitdata_one = functionone(pathfile = gitlog_one, projectname = projectname_one)
commitdata_two = functionone(pathfile = gitlog_two, projectname = projectname_two)
contributors_one=  functiontwo(pathfile = logauthors_one, projectname = projectname_one)
contributors_two = functiontwo(pathfile = logauthors_two, projectname = projectname_two)
functionthree(dfdata = commitdata_two)

commoncontributors = list(set(contributors_one.author) & set(contributors_two.author))

print("common contributors in both project...")
print(len(commoncontributors))
print("-----------------------------------------------------------------------------")


#****************************************************************************************************

