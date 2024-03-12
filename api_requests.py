from googleapiclient.discovery import build

youtubeApiKey = 'some_key'
youtube = build("youtube", "v3", developerKey=youtubeApiKey)

def search_youtube(name):
    res = youtube.search().list(
        q= name,
        part= "id,snippet",
        maxResults= 10
    ).execute()

    videos = []
    videos_id = list()
    channels = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in res.get("items", []):
        '''if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                        search_result["id"]["videoId"]))
            print(search_result["snippet"].keys())
            videos_id.append(search_result["id"]["videoId"])'''
        
        if search_result["id"]["kind"] == "youtube#channel":
           channels.append({"title":  search_result["snippet"]["title"],
                            "channelId":search_result["id"]["channelId"]})
    
   
    res = youtube.search().list(
        channelId = channels[0]["channelId"],
        type="video",
        part= "id, snippet",
        order="date",
        maxResults=10
    ).execute()

    for data in res.get("items", []):
        videos.append(data["id"]["videoId"])

    
    return videos, channels


def channel_statistics(id):
    request = youtube.channels().list(
            part="id,statistics, brandingSettings, snippet",
            id=id
        ).execute()
    return request


def video_statistics(videos):
    data = list()
    for video in videos:
        res = youtube.videos().list(
            id = video,
            part="id, statistics, snippet"
        ).execute()
        data.append(res["items"][0])
    
    #with open("text.txt", "a") as texto:
    statistics = list()
    for d in data:                                
        statistics.append({"stats": d["statistics"], "title": d["snippet"]["title"], "thumb": d["snippet"]["thumbnails"]["medium"]["url"], "url":'https://www.youtube.com/watch?v='+d["id"]})
    return statistics


def main():
    videos, channels = search_youtube("enygma")
    #print("Videos:\n", "\n".join(videos), "\n")
    for channel in channels:
        statistics =  channel_statistics(channel["channelId"])["items"][0]
        #print(statistics)
        print(f'Channel: {channel["title"]}, \nViews:{statistics["statistics"]["viewCount"]}')

