# file: app.py
import random 
from flask import Flask, render_template, request, make_response
from data import get_all_products, get_product
from recommender import SASRecRecommender
import json


app = Flask(__name__)

# Khởi tạo recommender
recommender = SASRecRecommender(
    model_path='model/best_model.pt',
    item_map_path='model/item_mapping.pkl',
    params_path='model/params.pkl'
)

@app.route('/')
def product_list():
    """Trang chủ hiển thị danh sách sản phẩm."""
    products = get_all_products()
    return render_template('index.html', products=products)

@app.route('/product/<product_id>')
def product_detail(product_id):
    """Trang chi tiết sản phẩm và gợi ý."""
    product = get_product(product_id)
    if not product:
        return "Product not found", 404
    
    # Lấy lịch sử xem hàng từ cookie
    view_history_str = request.cookies.get('view_history', '[]')
    try:
        view_history = json.loads(view_history_str)
    except json.JSONDecodeError:
        view_history = []
    
    # ================== DÒNG KIỂM TRA 1 ==================
    print(f"--- Bắt đầu request cho sản phẩm {product_id} ---")
    print(f"Lịch sử đọc từ cookie: {view_history}")
    # =======================================================
    # Lấy các gợi ý dựa trên lịch sử
    # Nếu không có lịch sử, có thể trả về danh sách trống hoặc sản phẩm phổ biến
    recommended_ids = []
    if view_history:
        recommended_ids = recommender.recommend(view_history, k=4)
        
     # ================== DÒNG KIỂM TRA 2 ==================
    print(f"ID gợi ý từ model: {recommended_ids}")
    # =======================================================

    recommended_products = [get_product(pid) for pid in recommended_ids if get_product(pid)]
    
    # ================== THÊM ĐOẠN CODE FALLBACK TẠI ĐÂY ==================
    # Nếu danh sách gợi ý bị rỗng (do sản phẩm chưa có trong data.py),
    # thì lấy tạm 4 sản phẩm ngẫu nhiên để demo không bị trống.
    if not recommended_products and len(get_all_products()) > 1:
        all_prods = get_all_products()
        # Lọc bỏ sản phẩm đang xem hiện tại
        other_prods = [p for p in all_prods if p.get('id') != product_id]
        # Lấy ngẫu nhiên, đảm bảo không lấy nhiều hơn số sản phẩm có
        num_to_sample = min(4, len(other_prods))
        if num_to_sample > 0:
            recommended_products = random.sample(other_prods, num_to_sample)
    # ======================================================================

    # Cập nhật lịch sử xem hàng (thêm sản phẩm hiện tại vào đầu)
    if product_id in view_history:
        view_history.remove(product_id)
    view_history.insert(0, product_id)
    view_history = view_history[:10] # Giới hạn lịch sử 10 sản phẩm

# ================== DÒNG KIỂM TRA 3 ==================
    print(f"Lịch sử mới sẽ lưu vào cookie: {view_history}")
    print("-" * 40) # In ra dòng ngăn cách để dễ đọc
    # =======================================================
        
    # Tạo response và gán cookie mới
    resp = make_response(render_template(
        'product_detail.html',
        product=product,
        recommended=recommended_products
    ))
    
    # Lưu lịch sử vào cookie (thời hạn 30 ngày)
    resp.set_cookie('view_history', json.dumps(view_history), max_age=30*24*60*60)
    
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)