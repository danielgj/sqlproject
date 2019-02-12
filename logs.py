#!/usr/bin/env python3

# 1. What are the most popular three articles of all time? 
# Which articles have been accessed the most? 
# Present this information as a sorted list with the most popular article at the top.

# 2. Who are the most popular article authors of all time? 
# That is, when you sum up all of the articles each author has written, which authors get the most page views? 
# Present this as a sorted list with the most popular author at the top.

# 3. On which days did more than 1% of requests lead to errors? 
# The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser. 
# (Refer to this lesson for more information about the idea of HTTP status codes.)

import psycopg2

db = psycopg2.connect("dbname=news")

c = db.cursor()
query = "select * from articles;"
c.execute(query)
rows = c.fetchall()

# First, what data structure did we get?
print "Row data:"
print rows


