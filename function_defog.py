import base64
import urllib
import requests


def pic_defog(image):
    url = "https://aip.baidubce.com/rest/2.0/image-process/v1/dehaze?access_token=" + get_access_token()

    payload = base64.b64encode(image).decode("utf-8")
    payload = "image=" + urllib.parse.quote_plus(payload)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload).json()
    return base64.b64decode(response['image'].encode("utf-8"))


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    API_KEY = "GayIcxYhx9m8GpAWOp8SA4Dj"
    SECRET_KEY = "Gqh7EFsHnGntI6VaitQwy99IN4UEN7iG"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))