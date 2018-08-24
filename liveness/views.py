import base64
import uuid

import requests
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View


class IndexView(View):
    '''
    页面定时检测人脸---（使用ajax请求后台），激活页面--拍照---同时读取身份证信息
    ---传到服务器进行比对----对结果进行处理

    用户打开客户（您）的某个网站，并开始使用某项功能，进行到需要人脸核身的步骤；
    客户（您）的服务器，根据目前客户的信息，向 FaceID 的 GetToken 服务发送请求，并记录 token；
    使用 token，将给用户展示的网页跳转到 DoLiveness 页面，进行活体；
    用户在 FaceID 页面进行活体检测，结束后 FaceID 通过后台给 Notify_url 发送结果信息，并将用户网页跳转回 Return_url 并回传数据；
    用户跳回 Return_url 页面后，继续进行相关业务操作；此步骤中为了防止黑客攻击，客户（您）可以通过 Notify_url 得到的信息，向GetResult接口反查活体和比对结果，确认信息的有效性。

    --集成api:https://api.megvii.com/faceid/v2/verify
    '''
    def get(self,req):
        return render(req,"index.html")
    def post(self,req):

        app_key = ""  # key
        app_secret = ""  # secret

        detect_url = "https://api-cn.faceplusplus.com/facepp/v3/detect"
        # 获得一个用于网页端活体检测的token（token唯一且只能使用一次）。接口同时还能帮助完成人脸比对，并在完成活体检测后自动将人脸比对结果返回
        token_url = "https://api.megvii.com/faceid/liveness/v2/get_token"
        liveness_url = ""

        verify_url = "https://api.megvii.com/faceid/v2/verify"

        compare_url = "https://api-cn.faceplusplus.com/facepp/v3/compare"

        if req.POST.get("type") == "detect":
            pass
        if req.POST.get("type") == "compare":
            img_a = req.POST.get("img_video")
            img_b = req.POST.get("data_sfz")
            if not img_b:
                img_b = img_a
            #canvas图片就是base64编码：格式   data:image/type;base64,base_encode_data_string

            data = {"api_key": app_key, "api_secret": app_secret,
                    "image_base64_1": img_a, "image_base64_2": img_b}

            res = {}
            result = requests.post(compare_url, data=data).json()
            if result.get("error_message"):
                res["code"] = 0
                res["message"] = result.get("error_message")
            else:
                res["thresholds"] = result.get("thresholds").get("1e-5") # 误识率为十万分之一的置信度阈值
                res["code"] = 1
                res["message"] = result.get("confidence")  # 置信度
                res["same"] = True if res["thresholds"] <= res["message"] else False

            return JsonResponse({"code":2})

