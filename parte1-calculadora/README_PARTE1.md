# Parte 1 - Cliente REST Calculadora
## Descrição
Cliente Python que consome a API REST da Calculadora disponível em:
https://calculadora-fxpc.onrender.com

## Como Executar

1. Criar ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate
```

2. Instalar dependências:
```bash
pip install requests
```

3. Executar:
```bash
python calculadora_client.py
```

## Análise das Requisições e Respostas

### GET /operations

**Requisição:**
- Método: GET
- URL: https://calculadora-fxpc.onrender.com/operations
- Headers principais:
  - Accept: */*
  - User-Agent: python-requests/2.32.5

**Resposta:**
- Status: 200 OK
- Content-Type: application/json
- Payload: Lista de operações disponíveis

### POST /operation/{operacao}/{num1}/{num2}

**Requisição:**
- Método: POST
- URL dinâmica com parâmetros na rota
- Content-Length: 0 (sem body)

**Resposta:**
- Status: 200 OK
- Content-Type: application/json
- Payload: Resultado da operação

## Comparação: POST REST vs Formulário HTML

### Similaridades:
- Ambos usam método HTTP POST
- Podem usar Content-Type: application/x-www-form-urlencoded
- Enviam dados para o servidor

### Diferenças:

| Aspecto | API REST | Formulário HTML |
|---------|----------|-----------------|
| Accept Header | application/json | text/html |
| Resposta | JSON/XML estruturado | Página HTML completa |
| Redirecionamento | Não redireciona | Geralmente redireciona |
| Cliente | Código programático | Navegador (humano) |
| Uso | Integração sistema-a-sistema | Interação humana |

**Exemplo Formulário HTML:**
```html

  Calcular

```

O navegador enviaria e esperaria HTML de volta para renderizar uma nova página.
