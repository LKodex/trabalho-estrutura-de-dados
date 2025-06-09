# Trabalho de Estrutura de Dados 2025/1 P04

**Aluno:** Lucas Gonçalves Cordeiro &lt;lucas.g.cordeiro@ufms.br&gt; (2021.1906.031-0)

É necessário Python versão &lt;=3.9 para executar o projeto.

## Mapeamento de Features/Requisitos Solicitados
Feature | Status
:------ | :----:
[KDTree] Suporta vetor de 128 floats (utilizado doubles) | ✅
[KDTree] Suporta string de 100 caracteres para o _face id_ | ✅
[KDTree] Utiliza heap para buscar os N vizinhos mais próximos | ❌
[API] Endpoint para construir a árvore | ✅
[API] Endpoint para inserir elementos na árvore | ✅
[API] Endpoint para buscar elementos na árvore | ✅

**Legenda:**
Ícone | Descrição
:---: | :--------
✅ | Concluído
❌ | Não desenvolvido
⚙️ | Em progresso

## Sobre o Projeto

Esse projeto faz parte de um trabalho da matéria de Estrutura de Dados ministrado pelo professor Edson Takashi Matsubara na Universidade Federal de Mato Grosso do Sul onde foi disponibilizado um [código base](https://github.com/edpfacom/libfacom2025/tree/main/api) em C e Python para ser modificado de acordo com os requisitos fornecidos que podem ser visualizados em [mapeamento de features](#mapeamento-de-features). A seguir segue um "diário" em ordem cronológica do que e como foi feito

### Diário Cronológico do Projeto

Iniciei copiando o código base disponibilizado e convertendo para padrões e estruturas de minha preferência como utilizar nomenclaturas em inglês para funções e variáveis, alterar nomes de `struct`s para possuírem o sufixo `_t`, entre outras.

Em seguida tratei da melhor forma a adequação da árvore KD em C para comportar 128 floats (o qual optei substituir por doubles) e uma string de 100 caracteres conforme os requisitos fornecidos.

Para uma melhor portabilidade entre plataformas Windows e Linux gerei um arquivo Makefile utilizando GenAI para compilar os códigos fonte em C para bibliotecas dinâmicas. Também adaptei os _wrappers_ em Python das respectivas bibliotecas para buscar a biblioteca dinâmica correta para a plataforma utilizada (Windows ou Linux).

Iniciei a implementação da API Web utilizando FastAPI, ao longo da implementação tive que fazer algumas pequenas correções para fazer o código funcionar corretamente e comunicar com a API das bibliotecas em C sem problemas.

Ao longo do desenvolvimento da API Web em FastAPI realizei testes utilizando Postman onde foi identificado diversos bugs que foram corrigidos, os que não foram corrigidos na hora tiveram uma _issue_ de bug aberta para eles como o [#1](https://github.com/LKodex/trabalho-estrutura-de-dados/issues/1)
