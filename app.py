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
    
if __name__ == '__main__':
    app.run(debug=True)
