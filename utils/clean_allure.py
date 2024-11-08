import json
import os


def clean_allure_results(directory):
    # 遍历 allure-results 目录中的每个文件
    for filename in os.listdir(directory):
        # 确保只处理 .json 文件
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            # 打开并加载 JSON 数据
            with open(filepath, 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    continue  # 如果文件不是有效的 JSON，跳过处理

            # 清理请求参数：删除所有 `parameters` 字段
            if 'parameters' in data:
                data['parameters'] = []

            # 重新保存文件，覆盖原始内容
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)


directory = '/Users/Wework/AutoTestX/allure-results'
clean_allure_results(directory)