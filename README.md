## Como configurar

1. Clone o repositório
2. Crie um virtualenv com Python 3.5
3. Ative o virtualenv.
4. Instale as dependências.
5. Configure a instância com o .env
6. Execute os testes.

```console
git clone git@github.com:erikopa/employee_manager_app.git employee_manager_app
cd employee_manager_app
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp contrib/env-sample .env
python manage.py test
```

### Como rodar a aplicação
```console
python manage.py migrate
python manage.py runserver 8080
```