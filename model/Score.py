class Score:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.reset()
        return cls._instancia

    def reset(self):
        self.respostas = []

    def adicionarLinha(self, index, linha):
        if len(self.respostas) > index:
            self.respostas[index] = linha
        else:
            while len(self.respostas) < index:
                self.respostas.append(None)
            self.respostas.append(linha)

    def getRespostas(self):
        return self.respostas
    def getResposta(self, index):
        if index < len(self.respostas):
            return self.respostas[index]
        else:
            return None