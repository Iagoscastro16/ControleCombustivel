from functions.utils import calcular_av

def test_calcular_av_com_sucesso():
    
    # arrange (Prepara)
    total_veiculo = 20
    total_geral = 50
    

    # Act (Agir)
    calcular_av(total_veiculo,total_geral)

    total = calcular_av(total_veiculo,total_geral)

    # assert (verificar)
    assert total == 40

    
