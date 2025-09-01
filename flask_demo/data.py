# file: data.py

# Dữ liệu sản phẩm mẫu.
_products = {
    "285930": {
        "name": "Áo thun nam trắng",
        "price": 150000,
        "image": "ao_thun.jpg",
        "description": "Áo thun 100% cotton thoáng mát, thấm hút mồ hôi tốt, phù hợp cho mọi hoạt động hàng ngày."
    },
    "357564": {
        "name": "Quần jean nữ",
        "price": 350000,
        "image": "quan_jean.jpg",
        "description": "Quần jean nữ ống đứng, chất liệu co giãn tốt, tôn dáng và mang lại sự thoải mái khi vận động."
    },
    "67045": {
        "name": "Giày thể thao năng động",
        "price": 500000,
        "image": "giay_the_thao.jpg",
        "description": "Giày chạy bộ chuyên dụng với đế êm ái, trọng lượng nhẹ và thiết kế bền bỉ, bảo vệ đôi chân của bạn."
    },
    "248766": {
        "name": "Túi xách da thời trang",
        "price": 420000,
        "image": "tui_xach.jpg",
        "description": "Túi xách da PU cao cấp, thiết kế thanh lịch, không gian rộng rãi, phù hợp đi làm hoặc đi chơi."
    },
    "72028": {
        "name": "Đồng hồ nam lịch lãm",
        "price": 750000,
        "image": "dong_ho.jpg",
        "description": "Đồng hồ nam dây kim loại, mặt kính sapphire chống xước, thiết kế sang trọng và mạnh mẽ."
    },
    # ================= BỔ SUNG CÁC SẢN PHẨM MỚI TẠI ĐÂY =================
    "386857": {
        "name": "Áo Sơ Mi Lụa",
        "price": 280000,
        "image": "ao_so_mi1.jpg", # Tạm dùng ảnh cũ, bạn có thể thay
        "description": "Chất liệu lụa cao cấp, mềm mại và thoáng mát."
    },
    "440220": {
        "name": "Quần Kaki Nam",
        "price": 320000,
        "image": "quan_kaki_nam.jpg", # Tạm dùng ảnh cũ, bạn có thể thay
        "description": "Quần kaki form dáng hiện đại, dễ phối đồ."
    },
    "238902": {
        "name": "Giày Da Công Sở",
        "price": 650000,
        "image": "giay_da_cong_so.jpg", # Tạm dùng ảnh cũ, bạn có thể thay
        "description": "Giày da thật 100%, đế cao su chống trượt."
    },
    "324963": {
        "name": "Ví Cầm Tay Nữ",
        "price": 190000,
        "image": "vi_cam_tay_nu.jpg", # Tạm dùng ảnh cũ, bạn có thể thay
        "description": "Thiết kế nhỏ gọn, tiện lợi với nhiều ngăn chứa."
    },
    # ================= BỔ SUNG CÁC SẢN PHẨM MỚI TỪ GỢI Ý CỦA MODEL =================
    "417230": {
        "name": "Áo Sơ Mi Nam Tay Ngắn",
        "price": 250000,
        "image": "asm3.jpg",
        "description": "Kiểu sơ mi tay ngắn, cổ bâu thẳng nhọn, phom relaxed vừa vặn, phù hợp nhiều vóc dáng. Dễ phối cùng quần jean, short hoặc layer khoác ngoài tạo outfit casual street.."
    },
    "398036": {
        "name": "Áo Sơ Mi Nam Tay Dài Aether Fresh Press Form Slim",
        "price": 300000,
        "image": "asm41.jpg",
        "description": "Mô tả cho sản phẩm 398036."
    },
    "351445": {
        "name": "Áo Sơ Mi Nam Cotton Tay Dài Soft Touch Gingham Form Regular",
        "price": 450000,
        "image": "asm5.jpg",
        "description": "Mô tả cho sản phẩm 351445."
    },
    "433060": {
        "name": "Áo Thun Nam Cotton Tay Ngắn In Silence Form Regular",
        "price": 500000,
        "image": "atn1.jpg",
        "description": "Mô tả cho sản phẩm 433060."
    },
    "265462": {
        "name": "Áo Thun Nam Tay Ngắn Shoulder Line Form Slim",
        "price": 180000,
        "image": "atn21.jpg",
        "description": "Mô tả cho sản phẩm 265462."
    },
    "176256": {
        "name": "Áo Thun Nam Cotton Thêu Biểu Tượng Animals Form Regular",
        "price": 620000,
        "image": "atn31.jpg",
        "description": "Mô tả cho sản phẩm 176256."
    },
    "63072": {
        "name": "Áo Sơ Mi Nam Denim Cuban EST-19 Form Boxy",
        "price": 780000,
        "image": "asm6.jpg",
        "description": "Mô tả cho sản phẩm 63072."
    },
    "266085": {
        "name": "Áo Sơ Mi Cuban Vải Lưới Nam Họa Tiết Sọc Form Relaxed",
        "price": 290000,
        "image": "asm71.jpg",
        "description": "Mô tả cho sản phẩm 266085."
    },
    "358049": {
        "name": "Áo Khoác Kaki Nam Sage Moss Sundaze Rush Form Loose",
        "price": 330000,
        "image": "ak11.jpg",
        "description": "Mô tả cho sản phẩm 358049."
    }
    
    # ======================================================================

}

# Thêm trường 'id' vào mỗi sản phẩm để dễ dàng sử dụng trong template
for pid, product_data in _products.items():
    product_data['id'] = pid

def get_all_products():
    """Lấy danh sách tất cả sản phẩm."""
    return list(_products.values())

def get_product(product_id):
    """Lấy chi tiết một sản phẩm theo ID."""
    return _products.get(str(product_id))