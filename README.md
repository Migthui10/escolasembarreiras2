# Escola Sem Barreiras — protótipo sem API

Protótipo web em Streamlit para demonstrar o fluxo de inclusão e adaptação de materiais escolares, sem chave de API, sem conta paga e sem serviços externos de IA.

## O que funciona
- Interface em português, adaptável para celular e computador.
- Entrada de texto digitado/colado.
- Leitura de arquivos PDF, PPTX e TXT.
- Pré-visualização de imagens, áudio e vídeo.
- Adaptações demonstrativas locais: texto em linguagem simples, resumo, glossário, perguntas e apoio visual com emojis.
- Edição e marcação de revisão humana.
- Leitura em voz alta pelo recurso nativo do navegador.
- Download das adaptações em TXT e dos indicadores em CSV.

## Limitações importantes
Esta versão é um protótipo funcional, não uma plataforma de IA. As adaptações usam regras simples e não têm a qualidade de uma análise pedagógica ou de uma IA generativa. A imagem é exibida, mas sua descrição precisa ser escrita por uma pessoa. Áudio e vídeo podem ser reproduzidos, mas não são transcritos automaticamente. Não gera Libras nem Braille.

## Como executar no Windows
1. Instale Python 3.10 ou superior.
2. Extraia este ZIP.
3. Abra o Prompt de Comando na pasta do projeto.
4. Execute:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

O navegador abrirá o protótipo. Não há etapa de configuração de chave API.

## Como executar no macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Publicação
É possível publicar gratuitamente em uma plataforma compatível com Streamlit, observando os limites do plano gratuito. Como não há chave API, não é necessário configurar Secrets. Não coloque dados pessoais de estudantes em uma demonstração pública.
