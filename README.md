# Asynchronous MangaDex python API 
An unofficial asynchronous python [MangaDex](https://www.mangadex.org) API built with the JSON API and web scraping.

[![Version](https://warehouse-camo.ingress.cmh1.psfhosted.org/272daab11b917f0c559858562da44257e95d80e6/68747470733a2f2f696d672e736869656c64732e696f2f707970692f762f646a616e676f2e737667)](https://test.pypi.org/project/aiomangadexapi/)
[![License](https://img.shields.io/github/license/md-y/mangadex-full-api.svg?style=flat)](https://github.com/Mudy7/aiomangadexapi/blob/master/LICENCE.txt)

[<img src="https://reclaimthenet.org/wp-content/uploads/2020/01/mangadex-768x366.jpg">](https://reclaimthenet.org/wp-content/uploads/2020/01/mangadex-768x366.jpg)

# key features
 - get data on any manga from mangadex
 - get updates from mangadex main page
 - get the mangas from anyone's list with a rss link
 - get any chapter link from mangadex
 
# installation : 
## ```pip install -i https://test.pypi.org/simple/ aiomangadexapi==1.1.0```
## If you get errors install these first : 
 - ```pip install lxml```
 - ```pip install feedparser```
 - ```pip install aiohttp```
 
 
[Documentation](#Documentation)

# Examples

```python
#Getting a manga with a name.

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
[search](#Search) <br>
[updates](#updates) <br>
[mangadex_list](#mangadex_list) <br>
[get_chapter](#get_chapter) <br>

## setup
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

## Search
**searches a manga on mangadex, can take a name or a link and returns a dictionnary(read below for more details)**

### ```search(session,name,link)```
|Arguments|Type|Information|Optional
|-|-|-|-
|session|```ClientSession()```| session that you get with the login function | No
|name|```String```| manga name/manga link | No
|link|```Boolean```| value is True if name is a link, false otherwise (Default: False)  | Yes

### what does it return : 

it returns a dictionnarry with all these keys.

|Key|Value Information|
|-|-
|id| manga ID|
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
| chapter_read| all the chapters id and their number |

                                                                            
### Search Example
```python
async def get_manga():
    session = await aiomangadexapi.login(username='username',password='password') # we login into mangadex
    manga = await aiomangadexapi.search(session,'solo leveling') #search for solo leveling (will return the first result of the search on mangadex)
    await session.close() #close the session 
    return manga
```

## updates
**Get the updates from mangadex main page**

### ```updates(session)```
|Arguments|Type|Information|Optional
|-|-|-|-
|session|```ClientSession()```| session that you get with the login function | No

returns a list of all the mangas on the main page (manga name, latest chapter and its link (english only))

### Updates Example 
```python
async def updates():
 session = await aiomangadexapi.login(username='username',password='password') # we login into mangadex
 updates = await aiomangadexapi.updates(session) # get the updates
 return updates
```

## mangadex_list
**Get all the mangas of a user's mangadex list**

### ```get_list(session,link)```
|Arguments|Type|Information|Optional
|-|-|-|-
|session|```ClientSession()```| session that you get with the login function | No
|session|```String```| An RSS link that you find in  https://mangadex.org/follows by right clicking The RSS icon (located to the right and it looks like a sideways wifi icon). Here's an example: https://mangadex.org/rss/follows/TX7VKNS9hcudBenmUrFYM286ayGHvgfP?h=0 | No

returns a list of links of all the mangas in the user's mangadex list.

### mangadex_list Example 
```python
async def md_list():
 session = await aiomangadexapi.login(username='username',password='password') # we login into mangadex
 mangadex_list = await aiomangadexapi.get_list(session,'https://mangadex.org/rss/follows/TX7VKNS9hcudBenmUrFYM286ayGHvgfP?h=0') # get the user's mangadex list
 return mangadex_list
```
## get_chapter
**Get the specified chapter link of any manga**

### ```get_chapter(session,name,chapter)```
|Arguments|Type|Information|Optional
|-|-|-|-
|session|```ClientSession()```| session that you get with the login function | No
|name|```String```| manga name | No
|chapter|```Integer```| chapter number | No

returns the link of the specified chapter.

### get_chapter Example 
```python
async def chapter():
 session = await aiomangadexapi.login(username='username',password='password') # we login into mangadex
 chapter = await aiomangadexapi.get_chapter(session,'solo leveling',120) # get the chapter link
 return chapter
```







