import random


def choose_picture():
    url = random.choice(["https://xuemolan.oss-cn-hangzhou.aliyuncs.com/1/WechatIMG1457.jpeg",
                         "https://xuemolan.oss-cn-hangzhou.aliyuncs.com/1/WechatIMG1458.jpeg",
                         "https://xuemolan.oss-cn-hangzhou.aliyuncs.com/1/WechatIMG1459.jpeg",
                         "https://xuemolan.oss-cn-hangzhou.aliyuncs.com/1/WechatIMG1460.jpeg",
                         "https://xuemolan.oss-cn-hangzhou.aliyuncs.com/1/WechatIMG1463.jpeg",
                         "https://xuemolan.oss-cn-hangzhou.aliyuncs.com/1/WechatIMG1464.jpeg"])
    return url
