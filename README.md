# Frequent-Change-Set
Finding set of files that change very often.

I. Use of Apriori Algorithm
Used apriori algorithm which is used to find frequent itemset, by passing through all the elements (here files) in a transaction 
(here commits). To prune the itemset I have provided support of 0.004 i.e. Singular items should appear in at least 0.4 % commits,
all other items will get pruned. For next pass it looks for two items appearing together in at least 0.4 % commits and all other items
will get pruned and so on. Only those items are considered which did not get pruned in the previous pass. 
This goes on until all change sets are found which appeared together in at least 0.4% commits.
