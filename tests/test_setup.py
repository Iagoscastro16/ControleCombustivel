from database.connection import get_connection
from database.setup import criar_tabelas, inicializar_db

def listar_tabelas():
    with get_connection() as conn:
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        return [linha["name"] for linha in cursor.fetchall()]

def test_criar_tabelas_com_sucesso_mesmo_rodando_duas_vezes(banco_vazio):

    # Arrange (Preparar)
    # Banco vazio, como na primeira vez que o app abre

    # Act (Agir)

    primeira = criar_tabelas()
    segunda = criar_tabelas()

    # Assert (Verificar)

    assert primeira["success"] is True
    assert segunda["success"] is True
    assert "veiculos" in listar_tabelas()
    assert "abastecimentos" in listar_tabelas()

def test_criar_tabelas_com_erro_desfaz_tudo(banco_vazio):

    # Arrange (Preparar)
    # Um índice chamado "abastecimentos" faz o CREATE dessa tabela falhar
    with get_connection() as conn:
        conn.execute("CREATE TABLE outra (x)")
        conn.execute("CREATE INDEX abastecimentos ON outra (x)")

    # Act (Agir)

    resultado = criar_tabelas()

    # Assert (Verificar)

    assert resultado["success"] is False
    assert "veiculos" not in listar_tabelas()

def test_inicializar_db_com_sucesso(banco_vazio):

    # Arrange (Preparar)
    # Banco vazio, como na primeira vez que o app abre

    # Act (Agir)

    resultado = inicializar_db()

    # Assert (Verificar)

    assert resultado["success"] is True

def test_inicializar_db_com_erro_repassa_a_falha(banco_vazio):

    # Arrange (Preparar)
    # Mesmo índice do teste anterior, pra forçar o erro no criar_tabelas
    with get_connection() as conn:
        conn.execute("CREATE TABLE outra (x)")
        conn.execute("CREATE INDEX abastecimentos ON outra (x)")

    # Act (Agir)

    resultado = inicializar_db()

    # Assert (Verificar)

    assert resultado["success"] is False
    assert "abastecimentos" in resultado["message"]
