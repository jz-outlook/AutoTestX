import requests


def get_access_token(app_key, app_secret):
    url = "https://oapi.dingtalk.com/gettoken"
    params = {"appkey": app_key, "appsecret": app_secret}
    response = requests.get(url, params=params)
    data = response.json()
    if data.get("errcode") == 0:
        return data.get("access_token")
    else:
        print("获取 Access Token 失败:", data)
        return None


def get_file_info(access_token, file_id):
    url = "https://oapi.dingtalk.com/v2.0/drive/file/get"
    headers = {"x-acs-dingtalk-access-token": access_token}
    payload = {"fileId": file_id}
    response = requests.post(url, headers=headers, json=payload)
    return response.json()


def download_file(access_token, file_id):
    url = "https://oapi.dingtalk.com/v2.0/drive/file/download"
    headers = {"x-acs-dingtalk-access-token": access_token}
    payload = {"fileId": file_id}
    response = requests.post(url, headers=headers, json=payload, stream=True)
    return response


# 主程序
app_key = "dingxb7tgd4fuqvanq0m"
app_secret = "eP90QWyHnBr2CkdtCLE0YDR61nDbrocKu0a6EgyDTAKbw55dDmz_92D_r7SrPeZb"
file_id = "MAeqxYNvxA9NO8j9"

access_token = get_access_token(app_key, app_secret)
if access_token:
    print("Access Token:", access_token)

    # 获取文件信息
    file_info = get_file_info(access_token, file_id)
    if file_info.get("errcode") == 0:
        print("文件信息:", file_info)

        # 下载文件
        response = download_file(access_token, file_id)
        if response.status_code == 200 and "application/octet-stream" in response.headers.get("Content-Type", ""):
            print("文件下载成功")
            with open("downloaded_file.xlsx", "wb") as f:
                f.write(response.content)
        else:
            print("文件下载失败:", response.json())
    else:
        print("获取文件信息失败:", file_info)
