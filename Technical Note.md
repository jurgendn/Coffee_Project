# Flask templates tutorial

## Cấu trúc thư mục

- Các templates được đặt sẵn trong thư mục `templates`.

- Các base template được sử dụng để xác định sẵn cấu trúc của một file, thể hiện qua các file `html`.

- Ví dụ, file `base.html` với cấu trúc như sau:

  ```html
  <!doctype html>
  <title>{% block title %}{% endblock %} - Flaskr</title>
  <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
  <nav>
    <h1>Flaskr</h1>
    <ul>
      {% if g.user %}
        <li><span>{{ g.user['username'] }}</span>
        <li><a href="{{ url_for('auth.logout') }}">Log Out</a>
      {% else %}
        <li><a href="{{ url_for('auth.register') }}">Register</a>
        <li><a href="{{ url_for('auth.login') }}">Log In</a>
      {% endif %}
    </ul>
  </nav>
  <section class="content">
    <header>
      {% block header %}{% endblock %}
    </header>
    {% for message in get_flashed_messages() %}
      <div class="flash">{{ message }}</div>
    {% endfor %}
    {% block content %}{% endblock %}
  </section>
  ```

  Trong đoạn code trên, chú ý vào cấu trúc của file, ta thấy:

  1. `<!doctype>`  là phần định cấu trúc của html, nói chung là file nào cũng phải có cái này

  2. `<title></title>`: Phần tiêu đề của trang web

  3. Phần nằm giữa `<nav></nav>` là phần navigation bar. Trong file trên, phần navigation bar gồm có các elements sau:

     - Log Out: Đăng xuất
     - Register: Đăng kí
     - Log In: Đăng nhập

     Nói chung là tùy vào điều kiện mà các elements trên navbar có thể khác nhau.

  4. Phần nằm giữa `<section></section>` là phần nội dung của trang. Trong phần này, có 2 phần lớn

     - `<header></header>` là phần header của page. Cụ thể hơn, `header` là gì thì nên search google, giải thích ở đây không hợp lí
     - Phần còn lại là phần nội dung.

  ## Các block

  ### Chức năng

  - Nhìn vào đoạn chương trình mẫu cho file `base.html`