# 23-2-md-proj-sql-jessehomemrosa

## Projeto 1 - SQL

### Integrantes:

- Eric Possato
- Rodrigo Anciães Patelli

### Instruções para execução:

1. Instale o [Docker](https://docs.docker.com/get-docker/).
2. Clone o repositório.
3. Garanta que o Docker esteja rodando.
#### dentro da pasta postgres_app:
4. Execute o comando `docker-compose build` para construir a imagem.
5. Execute a primeira migração com o comando `docker-compose run web alembic revision --autogenerate -m "First migration"`. Isso irá criar o arquivo de migração.
6. Execute a migração com o comando `docker-compose run web alembic upgrade head`. Isso irá criar o banco de dados.
7. Execute o comando `docker-compose up` para iniciar o servidor, com o banco de dados e a aplicação.
8. Acesse o endereço `http://localhost:8000/docs` para acessar a documentação da API.
9. Para acessar o pgAdmin, acesse o endereço `http://localhost:5050/` e faça login com as credenciais `pgadmin4@pgadmin.org` e `admin`.
10. Para acessar o banco de dados, crie um novo servidor com as seguintes credenciais:
    - Host name/address: `db`
    - Port: `5432`
    - Maintenance database: `test_db`
    - Username: `postgres`
    - Password: `postgres`
11. !!!Atenção!!! Como medida de segurança, altere a senha do usuário do pgAdmin e do banco de dados, pela interface do pgAdmin.
12. Adicione o seu novo username e senha no arquivo `postgres_app/.env`, conforme o exemplo do arquivo `postgres_app/.env.example`, assim como o host e a porta do banco de dados.
13. Agora você pode acessar o banco de dados pelo pgAdmin e pela aplicação.


### Diagrama EER:

![Diagrama de relacionamentos](EER_model.png)


### Video explicativo:

https://youtu.be/bv8XUbQ5m70
