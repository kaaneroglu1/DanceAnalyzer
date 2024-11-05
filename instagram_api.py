import requests


def get_hashtag_id(access_token, user_id, hashtag_name):
    """
    Verilen bir hashtag adına göre Instagram hashtag ID'sini alır.

    Parameters:
    - access_token (str): Instagram API erişim token'ı.
    - user_id (str): Business veya Creator Instagram kullanıcı ID'si.
    - hashtag_name (str): Aranacak hashtag'in adı.

    Returns:
    - str: Hashtag'in ID'si.
    """
    try:
        url = f"https://graph.facebook.com/v14.0/ig_hashtag_search"
        params = {
            "user_id": user_id,
            "q": hashtag_name,  # Parametre adı 'q' olacak
            "access_token": access_token
        }
        response = requests.get(url, params=params)

        # Hata kontrolü: Yanıtı yazdırarak detayları kontrol et
        if response.status_code != 200:
            print(f"API Hatası: {response.status_code} - {response.text}")
            return None

        response.raise_for_status()
        hashtag_data = response.json()

        # Hashtag ID'sini al
        if 'data' in hashtag_data and len(hashtag_data['data']) > 0:
            hashtag_id = hashtag_data['data'][0]['id']
            return hashtag_id
        else:
            print("Hashtag verisi bulunamadı")
            return None

    except requests.exceptions.RequestException as e:
        print("Hashtag ID alma sırasında bir hata oluştu:", e)
        return None


def fetch_videos_by_hashtag_id(access_token, user_id, hashtag_id):
    """
    Verilen hashtag ID'sine göre, o hashtag altındaki videoları getirir.

    Parameters:
    - access_token (str): Instagram API erişim token'ı.
    - user_id (str): Business veya Creator Instagram kullanıcı ID'si.
    - hashtag_id (str): Hashtag ID'si.

    Returns:
    - list: Hashtag altındaki videoların URL'leri, başlıkları ve bağlantıları içeren bir liste.
    """
    try:
        url = f"https://graph.facebook.com/v14.0/{hashtag_id}/top_media"
        params = {
            "user_id": user_id,
            "fields": "id,caption,media_type,media_url,thumbnail_url,permalink",
            "access_token": access_token
        }
        response = requests.get(url, params=params)

        # Hata kontrolü: Yanıtı yazdırarak detayları kontrol et
        if response.status_code != 200:
            print(f"API Hatası: {response.status_code} - {response.text}")
            return []

        response.raise_for_status()
        media_data = response.json().get('data', [])

        # Sadece videoları filtreleme
        videos = [
            {
                "media_url": item['media_url'],
                "caption": item.get('caption', ''),
                "permalink": item['permalink']
            }
            for item in media_data if item['media_type'] == 'VIDEO'
        ]

        return videos  # Video bilgilerini içeren listeyi döndürür

    except requests.exceptions.RequestException as e:
        print("Videoları alma sırasında bir hata oluştu:", e)
        return []


# Kullanım Örneği
access_token = "EAANMW1ouMIsBO2TAskAKkZBZAKrp0ZBWRRDFIq9wdYXQtu1gKr2US0tflgVuizSmlIbEMifVHK5ODpLiqqcD9QQgdcXF8v1qUC6ZAMq2DJZBrqNC3f9hyx0zrW5en9qYXQyEthxJhd6PZB96kjqadoQGIQFALKoD2lLu2wYr4h7qN2sAJTgvgWzAvmzcdcDDbQhzhTA4wSD4IJBETdbqktFyCslrXi7Smd0Sq0Ee0HLafmwDacCJI55mZAC98Dq"
user_id = "122095717052614006"
hashtag_name = "DANCE"

# 1. Hashtag ID'sini alma
hashtag_id = get_hashtag_id(access_token, user_id, hashtag_name)
if hashtag_id:
    # 2. Hashtag'e ait videoları getirme
    videos = fetch_videos_by_hashtag_id(access_token, user_id, hashtag_id)
    for video in videos:
        print(f"Video URL: {video['media_url']}")
        print(f"Caption: {video['caption']}")
        print(f"Permalink: {video['permalink']}\n")
