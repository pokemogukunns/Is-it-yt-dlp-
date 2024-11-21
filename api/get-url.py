import yt_dlp
import json

def get_first_format_url(video_url):
    ydl_opts = {
        'quiet': True,
        'noplaylist': True,
        'extract_flat': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        if 'formats' in info and info['formats']:
            return info['formats'][0]['url']
        return None

def handler(request):
    try:
        # ユーザーが送信したリクエストからURLを取得
        body = json.loads(request.body)
        video_url = body.get("url")

        if not video_url:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "URLが指定されていません。"})
            }

        # フォーマットの最初のURLを取得
        format_url = get_first_format_url(video_url)

        if format_url:
            return {
                "statusCode": 200,
                "body": json.dumps({"url": format_url})
            }
        else:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "フォーマットが見つかりませんでした。"})
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
