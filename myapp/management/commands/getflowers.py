from django.core.management import BaseCommand

class Command(BaseCommand):
    help = 'get flowers from wiki'

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

        # 위키백과 원예 식물 분류 url
        url = "https://ko.wikipedia.org/wiki/%EB%B6%84%EB%A5%98:%EC%9B%90%EC%98%88_%EC%8B%9D%EB%AC%BC"
        # html text를 가져온다
        html = get_text(url)
        # BeautifulSoup Element List를 가져온다.
        elements = get_elements(html, ".mw-category-group > ul > li > a")

        for element in elements:
            # 꽃 이름을 화면에 출력한다.
            print(element.get_text())