#!/usr/bin/env python3

import psycopg2
from datetime import datetime

db = psycopg2.connect("dbname=news")

c = db.cursor()

# Create Log Formatted View
createViewLogs = '''
create or replace view logsformatted as
    (select id,
            REPLACE(path,'/article/','') as slug,
            time
    from log
    where status='200 OK');'''
c.execute(createViewLogs)

# Create Articles Visits Number View
createViewArticlesVisit = '''
create or replace view articles_visits as
    (select articles.slug,
            articles.author,
            count(logsformatted.id) as visitsNumber
    from articles
    left join logsformatted
    on articles.slug=logsformatted.slug
    group by articles.id);'''
c.execute(createViewArticlesVisit)

# Create View to check request status by date
createViewRequestStatus = '''
create or replace view requests_status as
    (select count(id) as num,
    status,
    time::timestamp::date as date
    from log
    group by status, date
    order by date);
'''
c.execute(createViewRequestStatus)

# Create View to get error percentage by date
createViewErrorPercentage = '''
create or replace view error_percentage as
    (select A.date,
            100*B.num/sum(A.num) as error
            from requests_status A
            JOIN requests_status B
            on A.date=B.date
            where B.status != '200 OK'
            group by A.date, B.num
            order by error desc);
'''
c.execute(createViewErrorPercentage)

# 1. What are the most popular three articles of all time?
# Which articles have been accessed the most?
# Present information as sorted list with the most popular article at the top.

query1 = '''
    select articles.title,
           count(logsformatted.id) as visitsNumber
    from articles
    left join logsformatted
    on articles.slug=logsformatted.slug
    group by articles.id order by visitsNumber desc limit 3;'''
c.execute(query1)
rows = c.fetchall()

print "1. Three most popular articles of all time \n"
for row in rows:
    print " * \"{0}\" - {1} visits".format(row[0], row[1])

# 2. Who are the most popular article authors of all time?
# That is, when you sum up all of the articles each author has written,
# which authors get the most page views?
# Present this as a sorted list with the most popular author at the top.

query2 = '''
    select authors.name,
           sum(articles_visits.visitsnumber) as visits
    from authors
    join articles_visits
    on authors.id = articles_visits.author
    group by authors.name order by visits desc;'''
c.execute(query2)
rows = c.fetchall()

print "\n2. Most popular article authors of all time \n"
for row in rows:
    print " * \"{0}\" - {1} visits".format(row[0], row[1])


# 3. On which days did more than 1% of requests lead to errors?
# The log table includes a column status that indicates the HTTP
# status code that the news site sent to the user's browser.

query3 = "select date, error from error_percentage where error>1;"

c.execute(query3)
rows = c.fetchall()

print "\n3. Which days did more than 1% of requests lead to errors \n"
for row in rows:
    print " * {0} - {1}% errors".format(datetime.strftime(row[0],'%b %d, %Y'), round(row[1],2))


db.close()
