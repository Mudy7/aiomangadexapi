# Asynchronous MangaDex python API 
An unofficial asynchronous python [MangaDex](https://www.mangadex.org) API built with the JSON API and web scraping.

[![Version](https://img.shields.io/npm/v/mangadex-full-api.svg?style=flat)]()
[![License](https://img.shields.io/github/license/md-y/mangadex-full-api.svg?style=flat)](https://github.com/Mudy7/aiomangadexapi/blob/master/LICENCE.txt)

```pip install aiomangadex-api```

# key features
 - get data on any manga from mangadex
 - get updates from mangadex main page
 - mangadex list scanner with a rss link
 - get any chapter link from mangadex
 
[Documentation](#Documentation)

# Examples

```python
#couple examples

import aiomangadexapi
import asyncio

async def get_manga():
  session = await aiomangadexapi.login(username='username',password='password') # we login into mangadex
  manga = await aiomangadexapi.search(session,'solo leveling') #search for solo leveling (will return the first result of the search on mangadex)
  await session.close() #close the session 
  return manga
 
manga = asyncio.run(get_manga())

```



# Documentation
[setup](#setup) <br>
[search function](#Search function) <br>
[updates](#updates) <br>
[mangadex list scanner](#mangadex list scanner ) <br>
[get_chapter](#get_chapter) <br>

# setup
**you need to login to make any of the functions work**
### ```login(username,password)```

|Arguments|Type|Information|Optional
|-|-|-|-
|username|```String```| Login username | No
|password|```String```| Login password | No

Returns a session that is needed in other functions.

### login example 
```python
session = await aiomangadexapi.login(username='username',password='password') # we login into mangadex
```

# Search function
**searches a manga on mangadex, can take a name or a link and returns a dictionnary(read below for more details)**

### ```search(session,name,link)```
|Arguments|Type|Information|Optional|default value
|-|-|-|-|-
|session|```ClientSession()```| session that you get with the login function | No
|name|```String```| manga name/manga link | No
|link|```Boolean```| value is True if name is a link, false otherwise (Default: False)  | Yes

#### what does it return : 

**it returns a dictionnarry with all these keys.**

|Key|Value Information|
|-|-
|title|manga title|
|stars|manga rating|
|alternative|manga alternative titles|
|link|manga link|
|image|manga's image|
|genre|manga's genres|
|author|manga's author|
|views|manga's views|
|chapters|number of chapters|
|status|the status of the manga (1=onGoing,2=Completed)|
|latest|latest manga's chapter link|
|description|manga's description|

                                                                            
### Search Example
```python
async def get_manga():
    session = await aiomangadexapi.login(username='username',password='password') # we login into mangadex
    manga = await aiomangadexapi.search(session,'solo leveling') #search for solo leveling (will return the first result of the search on mangadex)
    await session.close() #close the session 
    return manga
```

# updates
** Sends **







