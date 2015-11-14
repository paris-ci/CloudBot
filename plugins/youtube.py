import re
import time

import isodate
import requests

from cloudbot import hook
from cloudbot.util import timeformat
from cloudbot.util.formatting import pluralize
from cloudbot.util.colors import parse

youtube_re = re.compile(r'(?:youtube.*?(?:v=|/v/)|youtu\.be/|yooouuutuuube.*?id=)([-_a-zA-Z0-9]+)', re.I)

base_url = 'https://www.googleapis.com/youtube/v3/'
api_url = base_url + 'videos?part=contentDetails%2C+snippet%2C+statistics&id={}&key={}'
search_api_url = base_url + 'search?part=id&maxResults=1'
playlist_api_url = base_url + 'playlists?part=snippet%2CcontentDetails%2Cstatus'
video_url = "http://youtu.be/%s"
err_no_api = "The YouTube API is off in the Google Developers Console."

global time_last_request
time_last_request = time.time()

def get_video_description(video_id):
    global time_last_request
    time_elapsed = time.time() - time_last_request
    if time_elapsed > 10:

        time_last_request = time.time()
    else:
        #return "This looks like a YouTube video. However, the YT api have been called too much, I'm sorry I won't be able to fetch details for you."
        return None
    json = requests.get(api_url.format(video_id, dev_key)).json()

    if json.get('error'):
        if json['error']['code'] == 403:
            return err_no_api
        else:
            return

    data = json['items']
    snippet = data[0]['snippet']
    statistics = data[0]['statistics']
    content_details = data[0]['contentDetails']

    out = '\x02{}\x02'.format(snippet['title'])

    if not content_details.get('duration'):
        return out

    length = isodate.parse_duration(content_details['duration'])
    out += ' - length \x02{}\x02'.format(timeformat.format_time(int(length.total_seconds()), simple=True))
    total_votes = float(statistics['likeCount']) + float(statistics['dislikeCount'])

    if total_votes != 0:
        # format
        likes = pluralize(int(statistics['likeCount']), "like")
        dislikes = pluralize(int(statistics['dislikeCount']), "dislike")

        percent = 100 * float(statistics['likeCount']) / total_votes
        likes = parse("$(dark_green)" + likes + "$(clear)")
        dislikes = parse("$(dark_red)" + dislikes + "$(clear)")
        out += ' - {}, {} (\x02{:.1f}\x02%)'.format(likes,
                                                    dislikes, percent)

    if 'viewCount' in statistics:
        views = int(statistics['viewCount'])
        out += ' - \x02{:,}\x02 view{}'.format(views, "s"[views == 1:])

    uploader = snippet['channelTitle']

    upload_time = time.strptime(snippet['publishedAt'], "%Y-%m-%dT%H:%M:%S.000Z")
    out += ' - \x02{}\x02 on \x02{}\x02'.format(uploader,
                                                time.strftime("%Y.%m.%d", upload_time))

    if 'contentRating' in content_details:
        out += ' - \x034NSFW\x02'

    # return re.sub(
    #		r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',
    #		'[URL]', out)

    return out.replace("youtu", "you tu") #nup. No spam please


@hook.on_start()
def load_key(bot):
    global dev_key
    dev_key = bot.config.get("api_keys", {}).get("google_dev_key", None)


@hook.regex(youtube_re)
def youtube_url(match, event):
    if event.chan == "#harmonyhosting":  # if the channel is #harmonyhosting
        return None  # return None, canceling the action

    return get_video_description(match.group(1))


@hook.command("youtube", "you", "yt", "y")
def youtube(text):
    """youtube <query> -- Returns the first YouTube search result for <query>."""
    if not dev_key:
        return "This command requires a Google Developers Console API key."

    json = requests.get(search_api_url, params={"q": text, "key": dev_key, "type": "video"}).json()

    if json.get('error'):
        if json['error']['code'] == 403:
            return err_no_api
        else:
            return 'Error performing search.'

    if json['pageInfo']['totalResults'] == 0:
        return 'No results found.'

    video_id = json['items'][0]['id']['videoId']

    return get_video_description(video_id) + " - " + video_url % video_id


@hook.command("youtime", "ytime")
def youtime(text):
    """youtime <query> -- Gets the total run time of the first YouTube search result for <query>."""
    if not dev_key:
        return "This command requires a Google Developers Console API key."

    json = requests.get(search_api_url, params={"q": text, "key": dev_key, "type": "video"}).json()

    if json.get('error'):
        if json['error']['code'] == 403:
            return err_no_api
        else:
            return 'Error performing search.'

    if json['pageInfo']['totalResults'] == 0:
        return 'No results found.'

    video_id = json['items'][0]['id']['videoId']
    json = requests.get(api_url.format(video_id, dev_key)).json()

    if json.get('error'):
        return
    data = json['items']
    snippet = data[0]['snippet']
    content_details = data[0]['contentDetails']
    statistics = data[0]['statistics']

    if not content_details.get('duration'):
        return

    length = isodate.parse_duration(content_details['duration'])
    l_sec = int(length.total_seconds())
    views = int(statistics['viewCount'])
    total = int(l_sec * views)

    length_text = timeformat.format_time(l_sec, simple=True)
    total_text = timeformat.format_time(total, accuracy=8)

    return 'The video \x02{}\x02 has a length of {} and has been viewed {:,} times for ' \
           'a total run time of {}!'.format(snippet['title'], length_text, views,
                                            total_text)


ytpl_re = re.compile(r'(.*:)//(www.youtube.com/playlist|youtube.com/playlist)(:[0-9]+)?(.*)', re.I)


@hook.regex(ytpl_re)
def ytplaylist_url(match, event):
    global time_last_request
    time_elapsed = time.time() - time_last_request
    if time_elapsed > 10:
        time_last_request = time.time()
    else:
        #return "This looks like a YouTube Playlist. However, the YT api have been called too much, I'm sorry I won't be able to fetch details for you."
        return None
    if event.chan == "#harmonyhosting":  # if the channel is #harmonyhosting
        return None  # return None, canceling the action

    location = match.group(4).split("=")[-1]
    json = requests.get(playlist_api_url, params={"id": location, "key": dev_key}).json()

    if json.get('error'):
        if json['error']['code'] == 403:
            return err_no_api
        else:
            return 'Error looking up playlist.'

    data = json['items']
    snippet = data[0]['snippet']
    content_details = data[0]['contentDetails']

    title = snippet['title']
    author = snippet['channelTitle']
    num_videos = int(content_details['itemCount'])
    count_videos = ' - \x02{:,}\x02 video{}'.format(num_videos, "s"[num_videos == 1:])
    return "\x02{}\x02 {} - \x02{}\x02".format(title, count_videos, author)
