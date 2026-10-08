import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# CORS 설정: 모든 도메인에서의 요청을 허용합니다.
# 특정 도메인만 허용하려면 CORS(app, resources={r"/*": {"origins": "https://yourdomain.com"}}) 형태로 수정하세요.
CORS(app)

def binary_search(arr, target):
    """정렬된 리스트(arr)에서 target의 인덱스를 반환하는 이진 검색 함수"""
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return -1

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    
    if not data or 'array' not in data or 'target' not in data:
        return jsonify({"error": "'array'와 'target' 필드가 필요합니다."}), 400
        
    arr = data['array']
    target = data['target']
    
    if not isinstance(arr, list):
        return jsonify({"error": "'array'는 배열 형태여야 합니다."}), 400

    # 이진 검색은 정렬된 배열을 전제로 합니다.
    # 배열이 정렬되어 있는지 확인하거나 미리 정렬합니다.
    arr_sorted = sorted(arr)
    
    result_index = binary_search(arr_sorted, target)
    
    return jsonify({
        "original_array": arr,
        "sorted_array": arr_sorted,
        "target": target,
        "found": result_index != -1,
        "index_in_sorted": result_index
    }), 200

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    # Cloud Run은 PORT 환경 변수를 주입합니다. (기본값: 8080)
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
