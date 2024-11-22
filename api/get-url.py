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
            return cors_response(
                400,
                {"error": "URLが指定されていません。"}
            )

        # フォーマットの最初のURLを取得
        format_url = get_first_format_url(video_url)

        if format_url:
            return cors_response(
                200,
                {"url": format_url}
            )
        else:
            return cors_response(
                404,
                {"error": "フォーマットが見つかりませんでした。"}
            )

    except Exception as e:
        return cors_response(
            500,
            {"error": str(e)}
        )

def cors_response(status_code, body):
    """
    CORSヘッダーを追加したレスポンスを作成するヘルパー関数
    """
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",  # 全てのオリジンを許可
            "Access-Control-Allow-Methods": "POST, OPTIONS",  # 許可するHTTPメソッド
            "Access-Control-Allow-Headers": "Content-Type"  # 許可するヘッダー
        },
        "body": json.dumps(body)
    }
