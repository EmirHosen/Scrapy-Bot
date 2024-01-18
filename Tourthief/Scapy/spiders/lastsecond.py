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
            def __init__(self, key):
                self.key = key
                self.priority = random.randint(1, 100)
                self.left = None
                self.right = None

        class Treap:
            def __init__(self):
                self.root = None

            def rotate_right(self, z):
                y = z.left
                T3 = y.right

                y.right = z
                z.left = T3

                return y

            def rotate_left(self, z):
                y = z.right
                T2 = y.left

                y.left = z
                z.right = T2

                return y

            def insert_util(self, root, key):
                if not root:
                    return Node(key)

                if key < root.key:
                    root.left = self.insert_util(root.left, key)

                    if root.left.priority > root.priority:
                        root = self.rotate_right(root)
                else:
                    root.right = self.insert_util(root.right, key)

                    if root.right.priority > root.priority:
                        root = self.rotate_left(root)

                return root

            def insert(self, key):
                self.root = self.insert_util(self.root, key)

            def inorder_util(self, root, result):
                if root:
                    self.inorder_util(root.left, result)
                    result.append(root.key)
                    self.inorder_util(root.right, result)

            def inorder(self):
                result = []
                self.inorder_util(self.root, result)
                return result
        
        treap = Treap()
        for price in self.prices:
            treap.insert(price)
        inorder_result = treap.inorder()
        print(inorder_result)

        inorder_result = treap.inorder()
        df = pd.DataFrame({'Prices': inorder_result})
        df.to_excel('Prices.xlsx', index=False)


        next_page = response.css("a.page-link::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
