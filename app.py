from flask import Flask, request, jsonify
from browserManagerOnServer import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/query', methods=['POST'])
def api_query():
    new_print("api query")
    data = request.get_json()
    apikey = data.get('apikey')
    new_print(apikey)

    if not apikey:
        return jsonify({"error": "API Key is required"}), 400
    # 调用 get_token_info 函数
    token_info = get_token_info(driver,apikey)
    new_print("get token info " + str(token_info))
    
    # 确保 token_info 返回的长度为4
    if len(token_info) != 4:
        return jsonify({"error": "Invalid token info returned"}), 500

    used_count, remaining_count, creation_date, expiration_date = token_info

    # 返回信息给前端
    return jsonify({
        "used_count": used_count,
        "remaining_count": remaining_count,
        "creation_date": creation_date,
        "expiration_date": expiration_date
    })
    
    
    
def split_date(date_str):
    # 去除年、月、日并将其分割为列表
    date_str = date_str.replace('年', '-').replace('月', '-').replace('日', '')
    date_list = date_str.split('-')
    
    # 将分割后的结果转换为对应的年月日
    year = date_list[0]
    month = date_list[1]
    day = date_list[2]
    
    return [year, month, day]
@app.route('/api/renew', methods=['POST'])
def api_renew():
    new_print("api_renew")
    data = request.get_json()
    apikey = data.get('apikey')
    dollar = data.get('dollar')
    date = split_date(data.get('date'))  # 假设日期格式为 2024年12月31日
    date = date +["0","0"]
    month_map = {
    "1": "一月",
    "2": "二月",
    "3": "三月",
    "4": "四月",
    "5": "五月",
    "6": "六月",
    "7": "七月",
    "8": "八月",
    "9": "九月",
    "10": "十月",
    "11": "十一月",
    "12": "十二月"
    }
    try:
        date[1] = month_map[date[1]]
    except:
        pass
    new_print("Received renew request with API Key:" + apikey+ " Dollar:"+ str(dollar))
    new_print("date:"+data.get('date'))

    # 检查必要的参数是否提供
    if not apikey:
        return jsonify({"error": "API Key is not valid", "status": 4}), 400
    if not dollar:
        return jsonify({"error": "Dollar is not valid", "status": 2}), 400
    if not date:
        return jsonify({"error": "Date is valid", "status": 3}), 400

    try:
        # 调用 change_token_dollar_and_life 函数
        result = change_token_dollar_and_life(driver, key = apikey, dollor=dollar, life=date)
        new_print("Change token result:"+ str(result))

        # 根据函数返回的结果，返回相应的消息
        if result == 1:
            return jsonify({"message": "Success", "status": 1})
        elif result == 2:
            return jsonify({"error": "No dollar provided", "status": 2}), 400
        elif result == 3:
            return jsonify({"error": "No date provided", "status": 3}), 400
        elif result == 4:
            return jsonify({"error": "No API key provided", "status": 4}), 400
        else:
            return jsonify({"error": "Unknown error", "status": 500}), 500

    except Exception as e:
        new_print("Error occurred:"+ str(e))
        return jsonify({"error": "An error occurred while processing the renew request."}), 500

    
    
if __name__ == '__main__':
    app.run(debug=True)
