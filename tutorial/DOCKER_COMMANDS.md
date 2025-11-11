# 🐳 Comandos Básicos do Docker

Este guia apresenta os comandos essenciais do Docker, organizados por categoria para facilitar a consulta e o aprendizado.

---

## 📦 Imagens

Comandos para gerenciar imagens Docker:

| Comando | Descrição |
|---------|-----------|
| `docker pull <nome-da-imagem>` | Baixa uma imagem do Docker Hub |
| `docker images` | Lista todas as imagens baixadas localmente |
| `docker rmi <nome-da-imagem>` | Remove uma imagem específica |
| `docker build -t <nome-da-imagem> .` | Constrói uma imagem a partir de um Dockerfile |
| `docker image prune` | Remove imagens não utilizadas |

**Exemplo:**
```bash
docker pull python:3.9
docker images
docker rmi python:3.9
```

---

## 🚀 Contêineres

Comandos para gerenciar contêineres Docker:

| Comando | Descrição |
|---------|-----------|
| `docker run <nome-da-imagem>` | Cria e executa um novo contêiner |
| `docker run -d <nome-da-imagem>` | Executa um contêiner em segundo plano (detached) |
| `docker run -p 8080:80 <nome-da-imagem>` | Executa e mapeia portas (host:contêiner) |
| `docker run --name <nome> <imagem>` | Cria um contêiner com nome personalizado |
| `docker ps` | Lista contêineres em execução |
| `docker ps -a` | Lista todos os contêineres (ativos e parados) |
| `docker start <id-ou-nome>` | Inicia um contêiner parado |
| `docker stop <id-ou-nome>` | Para um contêiner em execução |
| `docker restart <id-ou-nome>` | Reinicia um contêiner |
| `docker rm <id-ou-nome>` | Remove um contêiner parado |
| `docker rm -f <id-ou-nome>` | Remove um contêiner forçadamente (mesmo em execução) |

**Exemplo:**
```bash
docker run -d -p 8080:80 --name meu-app nginx
docker ps
docker stop meu-app
docker rm meu-app
```

---

## 🔧 Gerenciamento e Debugging

Comandos para monitorar e interagir com contêineres:

| Comando | Descrição |
|---------|-----------|
| `docker logs <id-ou-nome>` | Visualiza os logs de um contêiner |
| `docker logs -f <id-ou-nome>` | Acompanha os logs em tempo real |
| `docker exec -it <id-ou-nome> bash` | Acessa o terminal de um contêiner em execução |
| `docker exec -it <id-ou-nome> sh` | Acessa o shell (útil para imagens Alpine) |
| `docker inspect <id-ou-nome>` | Exibe informações detalhadas do contêiner |
| `docker stats` | Mostra estatísticas de uso de recursos |
| `docker top <id-ou-nome>` | Lista processos em execução no contêiner |

**Exemplo:**
```bash
docker logs -f meu-app
docker exec -it meu-app bash
```

---

## 📂 Transferência de Arquivos

Comandos para copiar arquivos entre host e contêiner:

| Comando | Descrição |
|---------|-----------|
| `docker cp <arquivo> <container>:/caminho/destino` | Copia arquivo do host para o contêiner |
| `docker cp <container>:/caminho/origem <destino>` | Copia arquivo do contêiner para o host |

**Exemplo:**
```bash
docker cp arquivo.txt meu-app:/app/
docker cp meu-app:/app/resultado.txt ./
```

---

## 🧹 Limpeza

Comandos para liberar espaço em disco:

| Comando | Descrição |
|---------|-----------|
| `docker container prune` | Remove todos os contêineres parados |
| `docker image prune` | Remove imagens não utilizadas |
| `docker volume prune` | Remove volumes não utilizados |
| `docker system prune` | Remove contêineres, redes e imagens não utilizados |
| `docker system prune -a` | Limpeza completa (incluindo imagens sem contêineres) |

---

## 💡 Dicas Úteis

- Use a **flag `-d`** para executar contêineres em segundo plano
- Use **`--rm`** no `docker run` para remover o contêiner automaticamente após a execução
- Use **`docker-compose`** para gerenciar aplicações multi-contêiner
- Use **`ctrl + p + q`** para sair de um contêiner interativo sem pará-lo
- Use **tags** específicas de versão ao invés de `latest` em produção

---

## 📚 Recursos Adicionais

- [Documentação oficial do Docker](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Boas práticas para Dockerfile](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)