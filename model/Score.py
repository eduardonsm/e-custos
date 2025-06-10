class Score:
    _instancia = None

    METODOS = {
        'RKW': {
            'alternativas': [96, 120, 148],
            'pontos_selecionada': 3,
            'penalidade_ignorada': -2
        },
        'ABC': {
            'alternativas': [13, 22, 85],
            'pontos_selecionada': 2,
            'penalidade_ignorada': -1
        },
        'TDABC': {
            'alternativas': [60, 85, 122],
            'pontos_selecionada': 2,
            'penalidade_ignorada': -2
        },
        'GECON': {
            'alternativas': [100, 110, 135],
            'pontos_selecionada': 3,
            'penalidade_ignorada': -1
        },
        'Rateio': {
            'alternativas': [5, 33, 100],
            'pontos_selecionada': 1,
            'penalidade_ignorada': 0
        },
        'UEP': {
            'alternativas': [22, 60, 135],
            'pontos_selecionada': 2,
            'penalidade_ignorada': -1
        }
    }
    
    PRINCIPIOS = {
        'RKW': 'Integral', 'ABC': 'Ideal', 'TDABC': 'Ideal',
        'GECON': 'Variável', 'Rateio': 'Integral', 'UEP': 'Integral'
    }

    PRIORIDADE_METODOS = ['ABC', 'TDABC', 'GECON', 'RKW', 'UEP', 'Rateio']

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
    def SelecionarMetodoPrincipio(self):
        pontuacao = {metodo: 0 for metodo in self.METODOS}

        # Itera sobre cada método para calcular sua pontuação
        for metodo, config in self.METODOS.items():
            for alternativa_chave in config['alternativas']:
                if alternativa_chave in self.respostas:
                    # Se foi selecionada, ganha pontos
                    pontuacao[metodo] += config['pontos_selecionada']
                else:
                    # Se foi ignorada, sofre penalidade
                    pontuacao[metodo] += config['penalidade_ignorada']
        
        # Lógica de desempate e seleção final (robusta)
        pontuacao_maxima = max(pontuacao.values())

        if pontuacao_maxima <= 0 and not all(p == 0 for p in pontuacao.values()):
             return "Dados insuficientes", "Indeterminado", pontuacao
        
        metodos_empatados = [m for m, p in pontuacao.items() if p == pontuacao_maxima]
        
        metodo_vencedor = None
        if len(metodos_empatados) > 1:
            for metodo_prioritario in self.PRIORIDADE_METODOS:
                if metodo_prioritario in metodos_empatados:
                    metodo_vencedor = metodo_prioritario
                    break
        else:
            metodo_vencedor = metodos_empatados[0]

        principio_selecionado = self.PRINCIPIOS.get(metodo_vencedor)
        
        return metodo_vencedor, principio_selecionado
