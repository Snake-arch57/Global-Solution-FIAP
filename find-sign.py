import sys
from pathlib import Path
import base64

if len(sys.argv) < 2:
    print(" Uso: python script.py <caminho_da_pasta>")
    sys.exit(1)

caminho_raiz = Path(sys.argv[1])

if not caminho_raiz.exists() or not caminho_raiz.is_dir():
    print(f" Caminho inválido: {caminho_raiz}")
    sys.exit(1)

nivel_maximo = 3
TARGET_SIGNATURE = "@author: r1g312"

def encode_base64(text):
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')

def decode_base64(text):
    return base64.b64decode(text.encode('utf-8')).decode('utf-8')

assinatura_codificada = encode_base64(TARGET_SIGNATURE)

# Criar pasta textos_puros
pasta_puros = Path("textos_puros")
pasta_puros.mkdir(exist_ok=True)

# Abrir arquivo decodificado.txt dentro da pasta textos_puros
decodificado_path = pasta_puros / "decodificado.txt"
saida_decodificado = open(decodificado_path, "w", encoding="utf-8")

# Abrir arquivo author.txt fora da pasta, contendo a assinatura fixa
author_path = Path("author.txt")
author_log = open(author_path, "w", encoding="utf-8")

# Grava assinatura no author.txt no formato pedido
linha_codificada = f"Assinatura codificada: {assinatura_codificada}"
linha_decodificada = f"Assinatura decodificada: {TARGET_SIGNATURE}"
author_log.write(f"{linha_codificada}\n{linha_decodificada}\n")
author_log.close()

for item in caminho_raiz.rglob('*'):
    if item.is_file():
        nivel = len(item.relative_to(caminho_raiz).parts)
        if nivel <= nivel_maximo:
            try:
                f = open(item, "r", encoding="utf-8")
                conteudo = f.read()
                f.close()

                
                caminho_relativo = item.relative_to(caminho_raiz)
                destino_puro = pasta_puros / caminho_relativo
                destino_puro.parent.mkdir(parents=True, exist_ok=True)

                f_out = open(destino_puro.with_suffix(".txt"), "w", encoding="utf-8")
                f_out.write(conteudo)
                f_out.close()

                
                try:
                    decodificado = decode_base64(conteudo)
                except Exception as e:
                    decodificado = f"[Falha ao decodificar: {str(e)}]"

                
                saida_decodificado.write(f"Arquivo: {item}\n")
                saida_decodificado.write("Conteúdo codificado:\n")
                saida_decodificado.write(conteudo + "\n\n")
                saida_decodificado.write("Conteúdo decodificado:\n")
                saida_decodificado.write(decodificado + "\n")
                saida_decodificado.write("-" * 60 + "\n\n")

                print(f" Processado: {item}")

            except Exception as e:
                print(f" Erro ao processar {item}: {e}")

saida_decodificado.close()

print("\n Finalizado:")
print(f" - Decodificações salvas em: {decodificado_path}")
print(f" - Assinatura salva em: {author_path}")
print(" - Arquivos originais salvos na pasta: textos_puros/")
