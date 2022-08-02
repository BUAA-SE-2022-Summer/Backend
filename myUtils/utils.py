import oss2
import configparser
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
cf = configparser.ConfigParser()
cf.read(os.path.join(BASE_DIR, 'Config/django.conf'))
auth = oss2.Auth(cf.get('data', 'USER'), cf.get('data', 'PWD'))
endpoint = 'http://oss-cn-hangzhou.aliyuncs.com'
bucket = oss2.Bucket(auth, endpoint, 'xuemolan')
base_image_url = 'https://xuemolan.oss-cn-hangzhou.aliyuncs.com/'


def update_img_file(image, name):
    base_img_name = str(name) + '.jpg'
    image_name = base_image_url + base_img_name
    res = bucket.put_object(base_img_name, image)
    if res.status == 200:
        return image_name
    else:
        return False


# 检查是否已登录
def login_check(request):
    return 'userID' in request.session
