class listParser:

    def __init__(self,ls):
        self.newl = []
        self.parserl=ls


    @property
    def Parser(self):
        for el in self.parserl:
            self.newl.append(el.text)
        return self.newl