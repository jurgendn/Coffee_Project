# Flask - Note

## Templates

**Cấu trúc thư mục**

- Các templates được đặt sẵn trong thư mục `templates`.
- Các base template được sử dụng để xác định sẵn cấu trúc của một file, thể hiện qua các file `html`.

### Template file

Ví dụ, file `base.html` với cấu trúc như sau:

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

#### Các block

##### Chức năng

Nhìn vào đoạn chương trình mẫu cho file `base.html`, ta thấy có các đoạn `{% block title %} {% endblock %} ,{% block header %} {% content %} ,...` Nói chung đây là phần rất quan trọng. Nội dung của từng block sẽ được define trong các file template khác. 

Các page khi load sẽ được load theo thứ tự sau:

1. Chọn một template cơ bản, ví dụ như file `base.html` ở trên.
2. Từng phần một sẽ được load vào vị trí tương ứng, xác định bởi các đoạn `{% block %}{% endblock %}` ở trên.
3. Nội dung của từng block được xử lí bên ngoài.

Nói chung, ai đã từng tạo block với Jekyll thì sẽ thấy khá là quen thuộc, bởi cách thức tạo các template khá tương đồng, bên cạnh đó thì cú pháp của Jinja2 và Liquid cũng khá giống nhau.

Ví dụ, với file `base.html` đã viết ở trên, khi muốn load page `register.html`, ta làm như sau:

```html
{% extends 'base.html' %}

{% block header %}
  <h1>{% block title %}Register{% endblock %}</h1>
{% endblock %}

{% block content %}
  <form method="post">
    <label for="username">Username</label>
    <input name="username" id="username" required>
    <label for="password">Password</label>
    <input type="password" name="password" id="password" required>
    <input type="submit" value="Register">
  </form>
{% endblock %}
```



- Dòng đầu tiên `{% extend base.html %}` cho biết trang `register.html` sẽ sử dụng file cơ sở là `base.html`.

- ```html
  {% block header %}
    <h1>{% block title %}Register{% endblock %}</h1>
  {% endblock %}
  ```

  Đoạn code này xác định các thành phần `header` và `title`. Nội dung của phần này sẽ được chèn vào vị trí tương ứng trong file `base.html`.

- ```html
  {% block content %}
    <form method="post">
      <label for="username">Username</label>
      <input name="username" id="username" required>
      <label for="password">Password</label>
      <input type="password" name="password" id="password" required>
      <input type="submit" value="Register">
    </form>
  {% endblock %}
  ```

  Đoạn này là nội dung cho phần `content`, cách thức chèn tương tự như trên, tức là chèn vào vị trí `content` trong file `base.html`.

Đến cuối cùng, chương trình hoàn chỉnh cho page `register.html ` sẽ được render như sau:

```html
<!doctype html>
<title>Register - Flaskr</title>
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
    <h1>Register</h1>
  </header>
  {% for message in get_flashed_messages() %}
    <div class="flash">{{ message }}</div>
  {% endfor %}
  <form method="post">
    <label for="username">Username</label>
    <input name="username" id="username" required>
    <label for="password">Password</label>
    <input type="password" name="password" id="password" required>
    <input type="submit" value="Register">
  </form>
</section>
```



> Lưu ý là các hàm, các biến sử dụng ở trên được giả định là đã tồn tại trong chương trình.

> Nói chung là đến đây thì biết đến thế, chứ tiếp theo làm như nào với đống static file thì tôi cũng chưa rõ lmao

## Flask

### Cài đặt Flask

Vì đây là thư viện để viết cho web, không dùng rộng rãi trong các project sau này (có thể), do đó nên cài đặt Flask trên một virtual environment.

#### Virtual Environment

Giờ hầu hết đều sử dụng Python 3 (3.8.2) nên là ở đây chỉ hướng dẫn cài đặt `venv`. Các virtual env cho Python 2 vui lòng search google.

Các bước cài đặt ở đây viết cho Debian Linux, các phiên bản khác tương tự

Cài đặt `venv`:

```bash
pip3 install virtualenv
```

Sau khi đã cài xong `venv`, thực hiện cài đặt `venv`  lên một folder của project. Giả sử rằng tôi có một project đang đặt tại `home/project/`.

```bash
>> cd /home/project/
>> python -m venv env
```

Câu lệnh đầu để chuyển pwd vào folder của project, không có gì

Câu lệnh thứ 2, phân tích một chút

- `python`, dễ rồi, gọi ra python thôi

- `-m`: optional, sử dụng cho current user

- `venv`: gọi virtualenv vừa cài xong

- `env`: tên của venv đặt trong folder.
  Lưu ý với `env`: 

  - Không nên đặt các venv trùng tên nhau, tôi đã mất cả tháng với cái này

    Tất nhiên lúc đó tôi dùng jupyter notebook và cái venv nó còn liên quan đến ipykernel, còn lại thì tôi cũng không rõ trong trường hợp còn lại có ảnh hưởng gì không

Tất nhiên, sau khi tạo env, ta cần kích hoạt nó:

```bash
source /env/bin/activate
```

Khi đó terminal của các bạn sẽ như sau:

```bash
(env)/home/project/: 
```

Lúc đó là các bạn đã kích hoạt thành công venv. Sử dụng python như bình thường, các modules sẽ cần phải cài lại từ đầu.

#### Cài đặt Flask trên venv

Sau khi kích hoạt venv, thực hiện cài đặt Flask vào venv này như sau:

```bash
pip install flask
```

Done

### Chương trình cơ bản

Trước khi làm gì, cũng nên biết `Hello, World!` cái đã. Dưới đây