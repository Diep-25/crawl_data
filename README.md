# crawl_data


## B1. Clone source
```
git clone https://github.com/Diep-25/crawl_data.git

```
## B2. Setup môi trường
```
1. Cài đặt python

2. Cài thư viện requests và unidecode
pip install scrapy requests translate unidecode flask

```

## B3. Chạy chương trình
```
scrapy crawl data_spider -a url=https://tuoitre.vn/ -a keyword=chien -a limit=2 
-a  tag_card=div.box-category-item

```

## Giải thích câu lệnh chạy
### url
Là url mà trang website muốn cào

### keyword
Là tìm bài viết theo keyword nào ( có thể không cần keyword thì xóa khỏi câu lệnh )

### limit
Là giới hạn bài viết cào về

### tag_card
Là thẻ class bao ngoài mỗi bài viết