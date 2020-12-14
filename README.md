Project - parsing avito
=======================


## The following commands you can do with project

```
 cd avito/

 docker-compose up --build                  - to build and run server
 docker-compose up -d --build               - to build and run server background

 docker exec -it avito_server_1 /bin/bash
 python app/api/test_parser.py              - run tests
 ./pep_test.sh                              - check all .py-files onpycode stile
```

## Description

get / - root \n
get /add/ see all entries \n
get /add/{item_id} - see certain entry \n
post /add/- add new id by region and request and return id \n
post /stat/ - to see history of item with id between time1 and time2 \n
get /top5/{item_id} - to see last top5 links for item_id \n

Survey frequency = 1 time per hour(at 1 * * * *) for each id \n
The service processes requests asynchronously \n
As a region you need to submit the exact name of the region used in the search on avito \n
