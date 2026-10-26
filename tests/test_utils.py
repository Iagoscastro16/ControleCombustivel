import pytest
from functions.utils import calcular_av,calcular_ah,normalizar_data

def test_calcular_av_com_sucesso():
    
    # Arrange (Preparar)
    total_veiculo = 20
    total_geral = 50
    

    # Act (Agir)

    total = calcular_av(total_veiculo,total_geral)

    # assert (verificar)
    assert total == 40

def test_calcular_av_total_geral_igual_zero():

    # Arrange (Preparar)

    total_veiculo = 40
    total_geral = 0

    # Act (Agir)
    total = calcular_av(total_veiculo,total_geral)

    # Assert (Verificar)
    assert total == 0

def test_calcular_ah_com_sucesso_com_acrescimo():

    # Arrange (Prepara)
    atual = 150
    anterior = 100

    # Act (Agir)

    total = calcular_ah(atual,anterior)

    # Assert (Verificar)
    assert total == 50

def test_calcular_ah_com_sucesso_com_decréscimo():
    
    # Arrange (Preparar)
    atual = 100
    anterior = 150

    # Act (Agir)

    total = calcular_ah(atual,anterior)

    # Assert (Verificar)
    
    assert total == pytest.approx(-33.33, abs=0.01)

def test_calcular_ah_anterior_mes_anterior_igual_zero():

    # Arrange (Preparar)

    atual = 50
    anterior = 0

    # Act (Agir)

    total = calcular_ah(atual,anterior)

    # assert (Verificar)

    assert total == 0

def test_normalizar_data_sem_barras_retorna_formato_iso():

    # Arrange (Preparar)

    entrada = "150325"

    # Act (Agir)

    data = normalizar_data(entrada)

    # Assert (Verificar)

    assert data == "2025-03-15"

def test_normalizar_data_com_barras_retorna_formato_iso():

    # Arrange (Preparar)

    entrada = "15/03/25"

    # Act (Agir)

    data = normalizar_data(entrada)

    # Assert (Verificar)

    assert data == "2025-03-15"

def test_normalizar_data_inexistente_retorna_none():

    # Arrange (Preparar)

    entrada = "319926"

    # Act (Agir)

    data = normalizar_data(entrada)

    # Assert (Verificar)

    assert data is None

def test_normalizar_data_tamanho_errado_retorna_none():

    # Arrange (Preparar)

    entrada = "1503"

    # Act (Agir)

    data = normalizar_data(entrada)

    # Assert (Verificar)

    assert data is None

def test_normalizar_data_com_letras_retorna_none():

    # Arrange (Preparar)

    entrada = "15032x"

    # Act (Agir)

    data = normalizar_data(entrada)

    # Assert (Verificar)

    assert data is None

def test_normalizar_data_com_digito_a_mais_retorna_none():

    # Arrange (Preparar)

    entrada = "1503261"

    # Act (Agir)

    data = normalizar_data(entrada)

    # Assert (Verificar)

    assert data is None