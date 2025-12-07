import requests
import json

BASE_URL = "https://calculadora-fxpc.onrender.com"

def listar_operacoes():
    """Lista todas as operações disponíveis"""
    print("\n" + "="*60)
    print("LISTANDO OPERAÇÕES DISPONÍVEIS")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/operations")
    
    print(f"\n[REQUISIÇÃO]")
    print(f"Método: GET")
    print(f"URL: {BASE_URL}/operations")
    print(f"Headers enviados:")
    for key, value in response.request.headers.items():
        print(f"  {key}: {value}")
    
    print(f"\n[RESPOSTA]")
    print(f"Status Code: {response.status_code}")
    print(f"Headers recebidos:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
    
    print(f"\nPayload (corpo da resposta):")
    print(json.dumps(response.json(), indent=2))
    
    return response.json()

def executar_operacao(nome_op, path, num1, num2):
    """Executa uma operação matemática"""
    print("\n" + "="*60)
    print(f"EXECUTANDO OPERAÇÃO: {nome_op}")
    print("="*60)
    
    # Substituir param1 e param2 pelos valores reais
    url = f"{BASE_URL}{path}".replace("param1", str(num1)).replace("param2", str(num2))
    
    response = requests.post(url)
    
    print(f"\n[REQUISIÇÃO]")
    print(f"Método: POST")
    print(f"URL: {url}")
    print(f"Headers enviados:")
    for key, value in response.request.headers.items():
        print(f"  {key}: {value}")
    
    print(f"\n[RESPOSTA]")
    print(f"Status Code: {response.status_code}")
    print(f"Headers recebidos:")
    for key, value in response.headers.items():
        print(f"  {key}: {value}")
    
    print(f"\nPayload (corpo da resposta):")
    try:
        print(json.dumps(response.json(), indent=2))
        return response.json()
    except:
        print(response.text)
        return None

if __name__ == "__main__":
    print("="*60)
    print("CLIENTE REST - API CALCULADORA")
    print("="*60)
    
    # 1. Listar operações
    dados = listar_operacoes()
    operacoes = dados['operations']
    
    # 2. Executar as 4 operações
    for op in operacoes:
        executar_operacao(op['name'], op['path'], 10, 5)
    
    print("\n" + "="*60)
    print("ANÁLISE: POST vs Formulário HTML")
    print("="*60)
    print("""
SIMILARIDADES:
- Ambos usam método HTTP POST
- Podem usar Content-Type: application/x-www-form-urlencoded
- Enviam dados para o servidor

DIFERENÇAS:
┌─────────────────┬──────────────────────┬────────────────────┐
│ Aspecto         │ API REST             │ Formulário HTML    │
├─────────────────┼──────────────────────┼────────────────────┤
│ Accept Header   │ application/json     │ text/html          │
│ Resposta        │ JSON/XML             │ Página HTML        │
│ Redirecionamento│ Não redireciona      │ Geralmente sim     │
│ Cliente         │ Programático         │ Navegador humano   │
│ Uso             │ Sistema-a-sistema    │ Interação humana   │
└─────────────────┴──────────────────────┴────────────────────┘
    """)
    
    print("="*60)
    print("TESTES CONCLUÍDOS!")
    print("="*60)