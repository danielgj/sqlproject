#!/usr/bin/env python3

# 2. Who are the most popular article authors of all time? 
# That is, when you sum up all of the articles each author has written, which authors get the most page views? 
# Present this as a sorted list with the most popular author at the top.

# 3. On which days did more than 1% of requests lead to errors? 
# The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser. 
# (Refer to this lesson for more information about the idea of HTTP status codes.)

import psycopg2

db = psycopg2.connect("dbname=news")

c = db.cursor()

# Create Log Formatted View
createViewLogs = "create or replace view logsformatted as (select id, REPLACE(path,'/article/','') as slug, time from log where status='200 OK');"
c.execute(createViewLogs)

# 1. What are the most popular three articles of all time? 
# Which articles have been accessed the most? 
# Present this information as a sorted list with the most popular article at the top.

#query = "select articles.id as articleId, articles.slug, articles.title, articles.author, count(logsformatted.id) as visitsNumber from articles left join logsformatted on articles.slug=logsformatted.slug group by articles.id;"
query1 = "select articles.title, count(logsformatted.id) as visitsNumber from articles left join logsformatted on articles.slug=logsformatted.slug group by articles.id order by visitsNumber desc limit 3;"
c.execute(query1)
rows = c.fetchall()

print "1. Three most popular articles of all time \n"
for row in rows:
  print " * \"{0}\" - {1} visits".format(row[0], row[1])

db.close()


