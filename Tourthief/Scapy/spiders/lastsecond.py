#import Laibrary 
import scrapy
import random
import pandas as pd
#Start Spider 
class LastsecondSpider(scrapy.Spider):
    name = "lastsecond"
    start_urls=["https://lastsecond.ir/tours/%D8%AA%D9%88%D8%B1-%D8%AA%D8%B1%DA%A9%DB%8C%D9%87"]
# Insert List for Save Prices 
    prices = []

    def parse(self, response):
        for item in response.css("div.tour-list-item__upper"):

            price = item.css("span.price__item__value::text").getall()

            self.prices.extend(price)

        class Node:
            # برای ایجاد گره های درخت treap
            def __init__(self, key):
                self.key = key
                self.number = random.randint(1, 100)
                self.left = None
                self.right = None

        #برای پیاده سازی از مثال ها استفاده شده است
        #شروع ساختمان داده ی تریپ
        class Treap:
            def __init__(self):
                # در این بخش ریشه تعریف شده است.
                self.root = None

            #تابع گردش به راست
            def rotate_right(self, z):
                y = z.left
                T3 = y.right

                y.right = z
                z.left = T3

                return y

            #تابع گردش به چپ
            def rotate_left(self, z):
                y = z.right
                T2 = y.left

                y.left = z
                z.right = T2

                return y
            # درج داده ها در ساختمان داده ی  تریپ
            def insert_util(self, root, key):
                #ریشه چک میشود، اگر خالی باشد مقدار در آن قرار میگیرد.
                if not root:
                    return Node(key)
                #اگر مقدار از ریشه کوچکتر باشد در فرزند راست قرارمیگرد
                if key < root.key:
                    root.left = self.insert_util(root.left, key)
                    # اگر شماره گره فرزند چپ از روت بزرگ تر بود ریشه به سمت راست میچرخد
                    if root.left.number > root.number:
                        root = self.rotate_right(root)
                # درصورتی که شرط قراردهی در چپ برقرار نبود در فرزند راست قرار میگرد.
                else:
                    root.right = self.insert_util(root.right, key)
                    # اگر گره راست از چپ شماره ی گره ی بزرگتری داشت به سمت چپ گردش میکند.
                    if root.right.number > root.number:
                        root = self.rotate_left(root)
                # مقدار روت به تابع برگردانده میشود.
                return root
            #  به صورت بازگشتی : تابعی تعریف شده برای درج داده ها
            def insert(self, key):
                self.root = self.insert_util(self.root, key)
            # در این تابع ساختمان داده را خوانده و به صورت صعودی به result اضافه میکند تا بتوانیم در فایل اکسل قرار دهیم.
            def inorder_util(self, root, result):
                if root:
                    self.inorder_util(root.left, result)
                    result.append(root.key)
                    self.inorder_util(root.right, result)
            # در این تابع ریزالت معرفی شده و مثدار ها در آن قرار گرفته میشود
            def inorder(self):
                result = []
                self.inorder_util(self.root, result)
                return result
        # در این بخش کلس تریپ را به متغییر تریپ داده ایم تا بتوانیم هر زمان اجرا کنیم
        treap = Treap()
        # در این بخش لیست price را به ساختمان داده ی treap وارد میکنیم.
        for price in self.prices:
            treap.insert(price)
        inorder_result = treap.inorder()
        print(inorder_result)

        # در این بخش آن را وارد فایل اکسل میکنیم.
        inorder_result = treap.inorder()
        df = pd.DataFrame({'Prices': inorder_result})
        df.to_excel('Prices.xlsx', index=False)

        # برای رفتن به صفحات دیگر سایت
        next_page = response.css("a.page-link::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
