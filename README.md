# Api Rest para gerenciamento de usuários/ Rest API for user management


## Propósito
Este repositório tem como objetivo organizar arquivos de um projeto de API Flask, para possibilitar o gerenciamento de usuários do sistema Management School System da YggBrasil Software.

A primeira funcionalidade é o registro de um novo usuário.

---
## 🛢️ Stack
- Python / Flask


---
## Requisitos de desenvolvimento e DEBUG

- VsCode
    - Configuração do arquivo launch.json para debug com VSCode.
- Renomear arquivo .env.hmlEXAMPLE na raiz do projeto para .env.hml e preencher com variáveis de ambiente
- Postman


---
## 🐑 Clonando o repositório

``` bash
#ssh
git clone git@github.com:GusTeixeira/mss-api-user-management.git
```
---
## Executando e debugando o Container Docker Localmente

```
docker-compose -f docker-compose-dev.yml up -d --build
```
Esse build cria uma imagem Docker, e um container.



---
## Debug com o VsCode
Para debug com o VsCode é necessário:
- O arquivo .env.hml deve ser criado e preenchiodo  na raiz do projeto

Para acesso ao BD RDS Aws é necessário estar conectado na VPN com o client PritUnl

Com o VsCode é possível Debugar utilizando a extensão Docker.

Após o build e o container em execução. 

Clicar com o botão direito em Attach Visual Studio Code no container em execução.

DebugExtensaoVsCode.gif
!Debug Extension for VS Code

![](assets/DebugExtensaoVsCode.gif)


```
localhost:8000
```

---
## 🏭 Debug e deploy

O deploy ocorre ao se  alterações das branchs develop e main, em staging e prod respectivamente. 


Url da API em homologação

```
**em produção**
```

Url da API em produção

```
**em produção**
```

Arrumar depois
