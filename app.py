from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

# 유튜브 API 키 설정
API_KEY =('AIzaSyC5f7NF-wLRXKDve3-WrC8yix9zcWbHaRw')

# 조회할 유튜브 채널 ID 목록
CHANNEL_IDS = [
    'UCDN_4QfQtD1mEiTjpgf0AOw',  # 나라튜브
    # 나머지 채널 ID를 여기에 채워 넣으세요.
]

# 채널별 최신 영상 정보를 가져오는 함수
def get_latest_videos(channel_ids):
    videos = []

    for channel_id in channel_ids:
        # 채널의 업로드된 영상 검색
        search_url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel_id}&maxResults=1&order=date&type=video&key={API_KEY}'
        search_resp = requests.get(search_url)
        search_data = search_resp.json()
        
        if search_data['items']:
            # 최신 영상의 ID를 가져옴
            video_id = search_data['items'][0]['id']['videoId']
            
            # 영상의 상세 정보 가져오기
            video_details_url = f'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={video_id}&key={API_KEY}'
            video_details_resp = requests.get(video_details_url)
            video_data = video_details_resp.json()
            
            if video_data['items']:
                video_info = {
                    'channel': search_data['items'][0]['snippet']['channelTitle'],
                    'title': video_data['items'][0]['snippet']['title'],
                    'thumbnail': video_data['items'][0]['snippet']['thumbnails']['high']['url'],
                    'view_count': int(video_data['items'][0]['statistics']['viewCount']),
                    'like_count': int(video_data['items'][0]['statistics'].get('likeCount', 0)),
                    'comment_count': int(video_data['items'][0]['statistics'].get('commentCount', 0)),
                    'upload_time': video_data['items'][0]['snippet']['publishedAt'],
                    'video_link': f'https://www.youtube.com/watch?v={video_id}'
                }
                videos.append(video_info)
    
    return videos

def get_top_videos(videos, top=10):
    # 영상들을 조회수 기준으로 정렬하고 상위 10개를 추출
    return sorted(videos, key=lambda x: x['view_count'], reverse=True)[:top]

@app.route('/')
def youtube_traffic():
    # 최신 영상 목록 가져오기
    
    # TOP 10 영상 목록 가져오기
    
    return render_template('youtube_traffic.html', )

if __name__ == '__main__':
    app.run(debug=True)
