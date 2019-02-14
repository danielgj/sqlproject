# Full Stack Development Nanodegree - Project Logs Analysis Documentation

Logs analysis project main goal is to demonstrate the knowledge acquired on SQL and Python DB API. To achieve that, we need to extract several logs from an existing database.

This document describes the design and considerations in order to fulfill the project specification.


## Requirements

Project task is to create a reporting tool that prints out reports (in plain text) based on the data in the database. This reporting tool is a Python program using the psycopg2 module to connect to the database.

Here are the questions the reporting tool should answer.

1. What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.

2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.

3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser. (Refer to this lesson for more information about the idea of HTTP status codes.)

## Implementation

One single python script has been developed. This script makes use of two different imported libraries:

* *psycopg2* to connect to the PSQL database
* *datetime* to format the dates in the output

To fullfil the requirements, several views are created in the DB (as described later). The code itself ensures that if the views already exist in the database they are dropped before beeing recreated.

By using these views, each of the logs are queried from the DB in one single query.

Python processing of data only formats the output displayed in the console.

## Views

I've created four different views:

* *logsformatted*
* *articles_visits*
* *requests_status*
* *error_percentage*

### logsformatted view

Selects relevant information for the first query () from the logs table and adapts the *path* to the *slug* format in articles table.

```sql
create or replace view logsformatted as
    (select id,
            REPLACE(path,'/article/','') as slug,
            time
    from log
    where status='200 OK');
```

### articles_visits

Creates a view with the number of vists each article has.

```sql
create or replace view articles_visits as
    (select articles.slug,
            articles.author,
            count(logsformatted.id) as visitsNumber
    from articles
    left join logsformatted
    on articles.slug=logsformatted.slug
    group by articles.id);
```

### requests_status view

Query the number of request on each status by date (removing the time of day they were created)

```sql
create or replace view requests_status as
    (select count(id) as num,
    status,
    time::timestamp::date as date
    from log
    group by status, date
    order by date);
```

### error_percentage view

Displays for each day the total amount of requests and the number of errors.

```sql
create or replace view error_percentage as
    (select A.date,
            100*B.num/sum(A.num) as error
            from requests_status A
            JOIN requests_status B
            on A.date=B.date
            where B.status != '200 OK'
            group by A.date, B.num
            order by error desc);
```

## Log queries

### Most popular three articles

```sql
select articles.title,
           count(logsformatted.id) as visitsNumber
    from articles
    left join logsformatted
    on articles.slug=logsformatted.slug
    group by articles.id order by visitsNumber desc limit 3;
```

### Most popular article authors of all time

```sql
select authors.name,
           sum(articles_visits.visitsnumber) as visits
    from authors
    join articles_visits
    on authors.id = articles_visits.author
    group by authors.name order by visits desc;
```


### Which days did more than 1% of requests lead to errors

```sql
select date, error from error_percentage where error>1;
```



## Example Output

```
1. Three most popular articles of all time 

 * "Candidate is jerk, alleges rival" - 338647 visits
 * "Bears love berries, alleges bear" - 253801 visits
 * "Bad things gone, say good people" - 170098 visits

2. Most popular article authors of all time 

 * "Ursula La Multa" - 507594 visits
 * "Rudolf von Treppenwitz" - 423457 visits
 * "Anonymous Contributor" - 170098 visits
 * "Markoff Chaney" - 84557 visits

3. Which days did more than 1% of requests lead to errors 

 * Jul 17, 2016 - 2.26% errors
```


## How to Run the project

To run the project, on the VM symply run `python logs.py`.

The results will be displayed on screen.

## Additional comments

To ensure that python good coding practices has been achieved, [PEP8 style guide](https://www.python.org/dev/peps/pep-0008/) has been reviewed and `pep8` tool has been used until no errors were shown.