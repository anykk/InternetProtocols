import pickle


class Cache:
    content = None

    def __init__(self, filename):
        self._filename = filename
        open(self._filename, 'a').close()

    def read(self):
        try:
            with open(self._filename, 'rb') as fd:
                self.content = pickle.load(fd)
        except EOFError as e:
            print("Cache file was corrupt:", e)
            print("Assuming cache is empty\n")

    def write(self):
        with open(self._filename, 'wb') as fd:
            pickle.dump(self.content, fd)

    def update(self):
        pass

    def add_entry(self, packet):
        self.content[packet.Question.QNAME] = packet

    def get_entry(self, name):
        self.content.get(name, None)
