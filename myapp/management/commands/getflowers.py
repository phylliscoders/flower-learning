from django.core.management import BaseCommand
from myapp.models import Flower

class Command(BaseCommand):
    help = 'get flowers from wikipedia'

    def handle(self, *args, **options):
        import requests
        from bs4 import BeautifulSoup

        def get_text(url):
            '''url을 인자로 받아 html text를 반환한다.
            Args:
                url: text를 가져올 url

            Returns: requests 가 반환하는 html text
            '''
            r = requests.get(url)
            return r.text

        def get_elements(html, selector):
            '''CSS Selector를 인자로 받아 인자에 맞는 elements를 반환한다.
            Args:
                html: html text
                selector: CSS Selector

            Returns: BeautifulSoup Element List
            '''
            soup = BeautifulSoup(html, "html.parser")
            elements = soup.select(selector)
            return elements

        print('--- 시작 ---')
        # 위키백과 원예 식물 분류 url
        url = "https://ko.wikipedia.org/wiki/%EB%B6%84%EB%A5%98:%EC%9B%90%EC%98%88_%EC%8B%9D%EB%AC%BC"
        # html text를 가져온다
        html = get_text(url)
        # BeautifulSoup Element List를 가져온다.
        elements = get_elements(html, ".mw-category-group > ul > li > a")
        add_flower_list = []

        # 이미 존재하는 꽃들을 제외시키기 위해 테이블의 내용을 가져온다.
        all_flower_list = Flower.objects.all()
        flower_list = []
        for flower_obj in all_flower_list:
            flower_list.append(flower_obj.name)

        for i, element in enumerate(elements):
            # 꽃 이름을 화면에 출력한다.
            flower_name = element.get_text()

            # 이미 등록된 꽃이면 continue
            if flower_name in flower_list:
                print(str(i) + ') ' + flower_name + ' is Already Exist')
                continue

            flower_obj = Flower(name=flower_name)
            add_flower_list.append(flower_obj)

            print(str(i) + ') ' + flower_name)

        res = Flower.objects.bulk_create(add_flower_list)
        print('--- 종료 ---')
