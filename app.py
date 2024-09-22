from flask import Flask, request, jsonify
from browserManagerOnServer import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/query', methods=['POST'])
def api_query():
    data = request.get_json()
    apikey = data.get('apikey')
    print(apikey)

    if not apikey:
        return jsonify({"error": "API Key is required"}), 400
    # 调用 get_token_info 函数
    token_info = get_token_info(driver,apikey)
    print("get token info " + str(token_info))
    
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
    
    
@app.route('/api/renew', methods=['POST'])
def api_renew():
    data = request.get_json()
    apikey = data.get('apikey')
    dollar = data.get('dollar')
    date = data.get('date')  # 假设日期格式为 2024年12月31日

    print("Received renew request with API Key:", apikey, "Dollar:", dollar, "Date:", date)

    # 检查必要的参数是否提供
    if not apikey:
        return jsonify({"error": "API Key is not valid", "status": 4}), 400
    if not dollar:
        return jsonify({"error": "Dollar is not valid", "status": 2}), 400
    if not date:
        return jsonify({"error": "Date is valid", "status": 3}), 400

    try:
        # 调用 change_token_dollar_and_life 函数
        result = change_token_dollar_and_life(driver, apikey, dollar, date)
        print("Change token result:", result)

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
        print("Error occurred:", str(e))
        return jsonify({"error": "An error occurred while processing the renew request."}), 500

    
    
if __name__ == '__main__':
    app.run(debug=True)
