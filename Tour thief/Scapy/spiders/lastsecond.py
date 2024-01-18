#import Laibrary 
import scrapy
import random
#Start Spider 
class LastsecondSpider(scrapy.Spider):
    name = "lastsecond"
    start_urls=["https://lastsecond.ir/tours/%D8%AA%D9%88%D8%B1-%D8%AA%D8%B1%DA%A9%DB%8C%D9%87"]
    titles = []
    stays = []
    agencies = []
    starts = []
    ends = []
    prices = []

    def parse(self, response):
        for item in response.css("div.tour-list-item__upper"):
            title = item.css("h2.title::text").getall()
            stay = item.css("div.stay::text").getall()
            agency = item.css("div.agency::text").getall()
            start = item.css("span.airline__name::text").getall()
            end = item.css("span.airline__name::text").getall()
            price = item.css("span.price__item__value::text").getall()

            self.titles.extend(title)
            self.stays.extend(stay)
            self.agencies.extend(agency)
            self.starts.extend(start)
            self.ends.extend(end)
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
        for title in self.titles:
            treap.insert(title)
        inorder_result = treap.inorder()
        print(inorder_result)

        next_page = response.css("a.page-link::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
