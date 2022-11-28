from easymlserve import EasyMLServer, EasyMLService


class BasicCSVService(EasyMLService):
    """Just a dummy service that only returns empty dict."""

    def process(self, df):
        return {}


service = BasicCSVService()
server = EasyMLServer(service)


if __name__ == '__main__':
    server.deploy()
