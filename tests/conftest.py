import pytest
from database import connection
from database.setup import criar_tabelas

@pytest.fixture
def banco_vazio(tmp_path, monkeypatch):

    # 1. Pasta vazia e nova pra cada teste: vem do tmp_path do pytest
    caminho_banco = tmp_path / "teste.db"

    # 2. Troca o DB_PATH que o get_connection lê, apontando pra essa pasta
    monkeypatch.setattr(connection, "DB_PATH", caminho_banco)

    return caminho_banco

@pytest.fixture
def banco_temporario(banco_vazio):

    # 3. Cria as tabelas no banco novo, parando aqui se falhar
    resultado = criar_tabelas()
    assert resultado["success"], resultado["message"]

    return banco_vazio
