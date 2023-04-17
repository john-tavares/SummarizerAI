from bs4 import BeautifulSoup
from pytube import YouTube

VALID_LANGUAGES = ["pt", "a.pt", "en", "a.en"]
MAX_RETRIES = 10

def extract_video_info(youtube_url):
    data = {}
    video = YouTube(youtube_url)

    for language in VALID_LANGUAGES:
        try:
            caption = video.captions.get(language, None).xml_captions
            break
        except:
            print(f"{language} - caption unavaible")

    data['title'] = video.title
    data['channel'] = video.author
    data['captions'] = format_caption(caption)

    return data

def get_video_info(youtube_url):
    for i in range(MAX_RETRIES):
        try:
            data = extract_video_info(youtube_url)
            break
        except Exception as e:
            print(e)
            print(f"Erro do pytube! {i}")
    
    return data

def format_time(time_in_ms):
    time_in_s = int(time_in_ms) / 1000
    minutes, seconds = divmod(time_in_s, 60)
    return f"{minutes:.0f}:{seconds:.0f}"


def format_caption(caption):
    soup = BeautifulSoup(caption, 'xml')
    caption_list = soup.find_all('p')
    caption_text = ""
    for tag in caption_list:
        time_in_ms = tag['t']
        legenda = tag.get_text()
        tempo_legivel = format_time(time_in_ms)
        caption_text += f"{tempo_legivel} - {legenda},"
    return caption_text