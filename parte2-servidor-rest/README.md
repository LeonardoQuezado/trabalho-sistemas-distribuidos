# Parte 2 - Servidor REST e Sistema de Favoritos

## Descrição
API REST que consome a API do Studio Ghibli e implementa sistema de favoritos de personagens.

## Tecnologias
- Python 3.12
- Flask
- Protocol Buffer
- Requests
- DictToXML

## Funcionalidades
1. **CRUD de Personagens**: Consulta personagens da API Ghibli
2. **Sistema de Favoritos**: Adicionar/remover/listar favoritos

## Formatos Suportados
- JSON (padrão)
- XML (parâmetro ?format=xml)
- Protocol Buffer (parâmetro ?format=protobuf)

## Como Executar

### Servidor REST:
```bash
cd parte2-servidor-rest
source venv/bin/activate
python server.py
```
Servidor rodando em: http://localhost:5000

### Cliente Web:
```bash
cd client-web
python app.py
```
Acesse: http://localhost:3000

### Cliente Desktop:
```bash
cd client-desktop
python3 desktop_app.py
```

## Rotas da API

- `GET /people` - Lista personagens
- `GET /people/<id>` - Busca personagem
- `GET /favorites` - Lista favoritos
- `POST /favorites` - Adiciona favorito
- `DELETE /favorites/<id>` - Remove favorito

## Documentação OpenAPI
Ver arquivo: `openapi.yaml`
Ou http://localhost:5000/docs utilizando swagger
