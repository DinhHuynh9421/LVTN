# Hệ thống Gợi ý Sản phẩm theo Phiên sử dụng mô hình SASRec

Đây là dự án Luận văn Tốt nghiệp, xây dựng một ứng dụng web demo hoàn chỉnh để minh họa khả năng của hệ thống gợi ý sản phẩm dựa trên hành vi người dùng trong một phiên làm việc (session-based).

Mô hình cốt lõi được sử dụng là **SASRec (Self-Attentive Sequential Recommendation)**, một kiến trúc hiện đại dựa trên cơ chế tự chú ý của Transformer.


---
## Mục lục
- [Tổng quan](#tổng-quan)
- [Công nghệ sử dụng](#công-nghệ-sử-dụng)
- [Tính năng chính](#tính-năng-chính)
- [Cài đặt và Chạy thử](#cài-đặt-và-chạy-thử)
- [Cấu trúc thư mục](#cấu-trúc-thư-mục)

---
## Tổng quan
Ứng dụng web này cho phép người dùng xem danh sách sản phẩm và khi click vào một sản phẩm, hệ thống sẽ tự động gợi ý các sản phẩm liên quan dựa trên lịch sử duyệt web ngay trong phiên đó. Mục tiêu là mô phỏng một tính năng "Có thể bạn thích" (You might also like) thông minh và được cá nhân hóa theo thời gian thực.

Mô hình SASRec đã được huấn luyện trước trên một bộ dữ liệu thương mại điện tử từ Kaggle.

---
## Công nghệ sử dụng
* **Backend:** Flask (Python)
* **Machine Learning:** PyTorch, Pandas, NumPy
* **Frontend:** HTML, CSS, Jinja2
* **Mô hình:** SASRec (Self-Attentive Sequential Recommendation)

---
## Tính năng chính
-   **Gợi ý theo thời gian thực:** Hệ thống sử dụng cookie để theo dõi hành vi của người dùng và cập nhật gợi ý ngay lập tức.
-   **Mô hình hóa logic:** Tách biệt rõ ràng giữa logic xử lý web (`app.py`) và logic của mô hình AI (`recommender.py`).
-   **Giao diện trực quan:** Một web demo đơn giản gồm trang danh sách sản phẩm và trang chi tiết sản phẩm để minh họa kết quả.

---
## Cài đặt và Chạy thử
Để chạy dự án này trên máy của bạn, hãy làm theo các bước sau:

1.  **Clone a repository:**
    ```bash
    git clone [https://github.com/DinhHuynh9421/LVTN.git](https://github.com/DinhHuynh9421/LVTN.git)
    cd LVTN/flask_demo
    ```

2.  **Tạo môi trường ảo (khuyên dùng):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Trên Windows: venv\Scripts\activate
    ```

3.  **Cài đặt các thư viện cần thiết:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Lưu ý: Bạn cần tạo file `requirements.txt` bằng cách chạy `pip freeze > requirements.txt` trong terminal của bạn)*

4.  **Chạy ứng dụng:**
    ```bash
    flask run
    ```
    Mở trình duyệt và truy cập `http://127.0.0.1:5003`.

---
## Cấu trúc thư mục
    .
    ├── model/                # Chứa các file model đã huấn luyện (.pt, .pkl)
    ├── static/               # Chứa các file tĩnh (CSS, images)
    ├── templates/            # Chứa các file HTML (Jinja2)
    ├── app.py                # File Flask chính, xử lý route và logic web
    ├── data.py               # "Kho" sản phẩm mini cho web demo
    └── recommender.py        # Module xử lý logic của mô hình AI
