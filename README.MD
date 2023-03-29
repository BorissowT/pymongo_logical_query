import pprint

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client.test_database

collection = db.test_collection


"""     Getting a Single Document       """
collection.find_one({"author": "Eliot"})
collection.find_one({"_id": "sDSCxSS__wE"})

################################################################################
"""   Querying for More Than One Document     
To get more than a single document as the result of a query we use the find()
method. find() returns a Cursor instance
(NOTE tb: this is a pymongo object. Extension of
generator. We could implement a new one. This would take skip, limit, filter
and other parameters for multiple document queries).
, which allows us to iterate over all matching documents.

****

class pymongo.cursor.Cursor(collection, filter=None, projection=None, skip=0,
limit=0, no_cursor_timeout=False, cursor_type=CursorType.NON_TAILABLE,
ort=None, allow_partial_results=False, oplog_replay=False, batch_size=0,
collation=None, hint=None, max_scan=None, max_time_ms=None, max=None,
min=None, return_key=False, show_record_id=False, snapshot=False,
comment=None, session=None, allow_disk_use=None)
 
"""

"""cursor object is not a list. we iterate with next() method"""
for item in collection.find():
    pprint.pprint(item)

collection.find()[50] # cursor with one elem
collection.find()[20:25] # cursor with a slice


"""     Filter with a condition.

$eq -	It will match the values that are equal to a specified value.
$gt -	It will match the values that are greater than a specified value.
$gte -	It will match all the values that are greater than or equal to a specified value.
$in -	It will match any of the values specified in an array.
$lt -	It will match all the values that are less than a specified value.
$lte -	It will match all the values that are less than or equal to a specified value.
$ne -	It will match all the values that are not equal to a specified value.
$nin -	It will match none of the values specified in an array
"""

collection.find({
    "center_id": {"$eq": 55},
    "homepage_featured": {"$ne": 0}
})

"""     Filter based on Logical Operator 

$and -	It will join query clauses with a logical AND and returns all documents 
    that match both the conditions.
$not -	It will invert the effect of a query and returns documents that do not 
    match the query expression.
$nor -	It will join the query clauses with a logical NOR and return all
    documents that fail to match the clauses.
$or -	It will join the query clauses with a logical OR and return all 
    documents that match the conditions of either clause.
"""

result_5 = collection.find({
    "$and": [{
                 "center_id": {"$eq": 11}
              },
              {
                   "meal_id": {"$ne": 1778}
              }]
})

for i in result_5:
    print(i)


"""     Filter with Regular Expressions     """
result_7 = collection.find({
    "cuisine": {"$regex": "^C"}
})

for i in result_7:
    print(i)


"""     Counting       

If we just want to know how many documents match a query we can perform a 
count_documents() operation instead of a full query. We can get a count of all 
of the documents in a collection:"""

collection.count()
collection.countDocuments(<query>, <options>)
"""
options: 
    limit Optional. The maximum number of documents to count.
    skip Optional. The number of documents to skip before counting.
    hint Optional. An index name or the index specification to use for the query.
    maxTimeMS Optional. The maximum amount of time to allow the count to run.
"""
################################################################################
def func():
    ...