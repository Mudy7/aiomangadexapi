from aiohttp import ClientSession
import json
import lxml.html
from collections import OrderedDict
import feedparser


async def fetch( session, url):

    async with session.get(url) as response:
        status = response.status
        
        if status == 200:
            response = await response.text()
            return response
        else:
            raise STATUSERROR(f"Error {status}, please try again.")


def fetch_link(response):

    tree = lxml.html.fromstring(response)
    root = "https://mangadex.org/"
    try:
        link = root + "api/v2/manga/" + tree.xpath("""//*[@id="content"]/div[5]/div/@data-id""")[
            0] + "?include=chapters"
        print(link)
        return link
    except:
        raise NOTFOUND("manga not found")


async def login(username,password):
        session = ClientSession()
        link = 'https://mangadex.org/'
        data = {
            'login_username': username,
            'login_password': password,
            'remember_me': 1
        }
        headers = {
            'x-requested-with': "XMLHttpRequest",
            'user-agent': 'dedicatus545-discord'
        }
        path = 'ajax/actions.ajax.php?function=login'
        
        await session.post(link + path, headers=headers, data=data)
        return session


def parse(response):

    GENRES = {
        1: "4-Koma", 2: "Action", 3: "Adventure", 4: "Award Winning", 5: "Comedy", 6: "Cooking", 7: "Doujinshi",
        8: "Drama",
        9: "Ecchi", 10: "Fantasy", 11: "Gyaru", 12: "Harem", 13: "Historical", 14: "Horror", 16: "Martial Arts",
        17: "Mecha",
        18: "Medical", 19: "Music", 20: "Mystery", 21: "Oneshot", 22: "Psychological", 23: "Romance",
        24: "School Life",
        25: "Sci-Fi", 28: "Shoujo Ai", 30: "Shounen Ai", 31: "Slice of Life", 32: "Smut", 33: "Sports",
        34: "Supernatural",
        35: "Tragedy", 36: "Long Strip", 37: "Yaoi", 38: "Yuri", 40: "Video Games", 41: "Isekai", 42: "Adaptation",
        43: "Anthology", 44: "Web Comic", 45: "Full Color", 46: "User Created", 47: "Official Colored",
        48: "Fan Colored",
        49: "Gore", 50: "Sexual Violence", 51: "Crime", 52: "Magical Girls", 53: "Philosophical", 54: "Superhero",
        55: "Thriller", 56: "Wuxia", 57: "Aliens", 58: "Animals", 59: "Crossdressing", 60: "Demons",
        61: "Delinquents",
        62: "Genderswap", 63: "Ghosts", 64: "Monster Girls", 65: "Loli", 66: "Magic", 67: "Military",
        68: "Monsters",
        69: "Ninja", 70: "Office Workers", 71: "Police", 72: "Post-Apocalyptic", 73: "Reincarnation",
        74: "Reverse Harem",
        75: "Samurai", 76: "Shota", 77: "Survival", 78: "Time Travel", 79: "Vampires", 80: "Traditional Games",
        81: "Virtual Reality", 82: "Zombies", 83: "Incest", 84: "Mafia"
    }
    payload = json.loads(response)
    data, chapters = payload['data']['manga'], payload['data']['chapters']

    data = {
        'id': data['id'],
        'title': data['title'],
        'stars': data['rating']['mean'],
        'alternative': data['altTitles'],
        'link': 'https://mangadex.org/title/{}'.format(data['id']),
        'image': data['mainCover'].replace('.jpeg','.large.jpg'),
        'genre': ' '.join([GENRES[genre] for genre in data['tags']]),
        'author': data['author'][0],
        'views': data['views'],
        'chapters':'',
        'status': data['publication']['status'],
        'latest': '',
        'description':data['description'],
        'chapters_read': OrderedDict({chapter['chapter']: chapter['id']
                                      for chapter in chapters
                                      if chapter['language'] == 'gb'})
    }
    if data['chapters_read'] != {}:
        data['chapters'] = float(next(iter(data['chapters_read'])))
        data['latest'] = 'https://mangadex.org/chapter/' + str(next(iter(data['chapters_read'].values())))

    else:
        data['chapters'] = float(next(iter(OrderedDict({chapter['chapter']: chapter['id']
                                                        for chapter in chapters}))))
        data['latest'] = None


    return [data]

async def search(session,name,link=False):

    if not link:
        name = name.replace(" ", "%20")
        name = name.replace("[", "%5B")
        name = name.replace("[", "%5D")
        name = name.replace("?", "%3F")

        response = await fetch(session, 'https://mangadex.org/search?title={}'.format(name))
        link = fetch_link(response)
    else:
        link = 'https://mangadex.org/' + "api/v2/manga/" + name.split("title/")[1].split('/',1)[0] + "?include=chapters"

    response = await fetch(session, link)
    data = parse(response)

    return data

async def get_info3(response):

    tree = lxml.html.fromstring(response)
    updates = []

    for i in tree.xpath("""//div[@class='row m-0']/div"""):
        update = []
        if i.xpath(""".//div[@class='ml-1']/span/@title""")[0] == "English":
            update.append(i.xpath(
                """.//div[@class='pt-0 pb-1 mb-1 border-bottom d-flex align-items-center flex-nowrap']/a/text()""")[
                             0])
            update.append('https://mangadex.org' + i.xpath(
                """.//div[@class='py-0 mb-1 row no-gutters align-items-center flex-nowrap']/a/@href""")[0])
            chapter = \
                i.xpath(""".//div[@class='py-0 mb-1 row no-gutters align-items-center flex-nowrap']/a/text()""")[0]

            try:
                update.append(float(chapter.split("Chapter ", 1)[1]))

            except:
                try:
                    update.append(float(chapter.split("Ch. ", 1)[1].split(" ", 1)[0]))
                except:
                    update.append(None)
        updates.append(update)
    
    return updates

async def updates(session):

    response = await fetch(session,url='https://mangadex.org/')
    # parsing
    updates = await get_info3(response)
    return updates

async def get_chapter(session,name,chapter):

        data = await search(session,name)
        try:
            site = 'https://mangadex.org/chapter/'+ str(data[0]['chapters_read'][str(chapter)])
            return site
        except:
            raise NOTFOUND('no such chapters')

def parse_ids(response):

    rss = feedparser.parse(response).entries
    ids = set()
    for item in rss:
        ids.add(item['mangalink'])
    return ids

async def get_list(session,link):
    root = "https://mangadex.org/title/"
    response = await fetch(session,link)
    ids = parse_ids(response)
    return ids

class STATUSERROR(Exception):
    pass

class NOTFOUND(Exception):
    pass
