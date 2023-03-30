

"""     Filter with a condition.

$eq -	It will match the values that are equal to a specified value.\
$gt -	It will match the values that are greater than a specified value.\
$gte -	It will match all the values that are greater than or equal to a specified value.\
$in -	It will match any of the values specified in an array.\
$lt -	It will match all the values that are less than a specified value.\
$lte -	It will match all the values that are less than or equal to a specified value.\
$ne -	It will match all the values that are not equal to a specified value.\
$nin -	It will match none of the values specified in an array.\
"""

collection.find({
    "center_id": {"$eq": 55},
    "homepage_featured": {"$ne": 0}
})

"""     Filter based on Logical Operator 

$and -	It will join query clauses with a logical AND and returns all documents \
    that match both the conditions.\
$not -	It will invert the effect of a query and returns documents that do not \
    match the query expression.\
$nor -	It will join the query clauses with a logical NOR and return all\
    documents that fail to match the clauses.\
$or -	It will join the query clauses with a logical OR and return all \
    documents that match the conditions of either clause.\
"""

result_5 = collection.find_one(\
&nbsp;&nbsp;&nbsp;&nbsp;{"$or": [\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{"$and": [{"author": {"$ne": "David"}},\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{"author": {"$ne": "Eliot"}},\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{"author": {"$ne": "Papi2"}}]},\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{"id": 100}\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;]\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}\
&nbsp;&nbsp;&nbsp;&nbsp;)\

