import api_requests as api
from flask import Flask, flash, redirect, render_template, request, session, json
from flask_session import Session

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method== "POST":

        name = request.form.get("name")

        if name:

            video, channels = api.search_youtube(name)
            videos_stats = api.video_statistics(video)
            channel = api.channel_statistics(channels[0]["channelId"])["items"][0]
            banner = channel["brandingSettings"]["image"]["bannerExternalUrl"]
            icon = channel["snippet"]["thumbnails"]["medium"]["url"]
            js_data = json.dumps(list(map(lambda x: int(x["stats"]["viewCount"]), videos_stats)))
            print(js_data)

            return render_template("index.html", channel_name= channels[0]["title"], stats= channel["statistics"], videos = videos_stats, banner=banner, icon=icon, js_data=js_data)
    return render_template("index.html")



app.run( debug="True")

"""video, channels = api.search_youtube("Enygma")
    
    statistics = api.channel_statistics(channels[0]["channelId"])["items"][0]
    return f'Canal {channels[0]["title"]}, views: {statistics["statistics"]["viewCount"]} """
