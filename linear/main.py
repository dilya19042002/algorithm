import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# CORS 설정: 웹 브라우저 cross-origin 요청 허용
CORS(app)

def binary_search_trace(arr, target):
    """
    이진 검색 수행 과정을 단계별(Left, Right, Mid 지점 및 상태)로 추적하는 함수
    """
    left, right = 0, len(arr) - 1
    steps = []
    
    while left <= right:
        mid = (left + right) // 2
        
        # 현재 단계 정보 기록
        step_info = {
            "left": left,
            "right": right,
            "mid": mid,
            "mid_val": arr[mid],
            "status": "comparing"
        }
        
        if arr[mid] == target:
            step_info["status"] = "found"
            steps.append(step_info)
            return steps, mid
        elif arr[mid] < target:
            step_info["status"] = "go_right"
            steps.append(step_info)
            left = mid + 1
        else:
            step_info["status"] = "go_left"
            steps.append(step_info)
            right = mid - 1
            
    return steps, -1

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    
    if not data or 'array' not in data or 'target' not in data:
        return jsonify({"error": "'array'와 'target' 필드가 필요합니다."}), 400
        
    arr = data['array']
    target = data['target']
    
    if not isinstance(arr, list):
        return jsonify({"error": "'array'는 배열 형태여야 합니다."}), 400

    # 이진 검색을 위한 정렬
    arr_sorted = sorted(arr)
    
    # 단계별 추적 실행
    steps, found_index = binary_search_trace(arr_sorted, target)
    
    return jsonify({
        "original_array": arr,
        "sorted_array": arr_sorted,
        "target": target,
        "found": found_index != -1,
        "final_index": found_index,
        "total_steps": len(steps),
        "steps": steps,  # 시각화용 핵심 데이터
        "time_complexity": {
            "best": "O(1)",
            "average": "O(log N)",
            "worst": "O(log N)"
        },
        "space_complexity": "O(1)"
    }), 200

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
