"""
Schemas Pydantic para validação de entrada e saída da API.
"""

from pydantic import BaseModel, Field
from typing import Optional


class DadosEstudante(BaseModel):
    """Schema de entrada: dados de um estudante para predição de risco."""

    fase: Optional[float] = Field(None, description="Fase atual no programa")
    ano_nascimento: Optional[float] = Field(
        None, description="Ano de nascimento")
    idade: Optional[float] = Field(
        None, ge=5, le=25, description="Idade do estudante")
    genero: Optional[str] = Field(None, description="Gênero do estudante")
    ano_ingresso: Optional[float] = Field(
        None, ge=2016, description="Ano de ingresso no programa")
    instituicao_de_ensino: Optional[str] = Field(
        None, description="Tipo de instituição de ensino")
    cg: Optional[float] = Field(
        None, ge=0, le=10, description="Conceito Global")
    cf: Optional[float] = Field(
        None, ge=0, le=10, description="Conceito de Frequência")
    ct: Optional[float] = Field(
        None, ge=0, le=10, description="Conceito Técnico")
    n_av: Optional[float] = Field(None, description="Número de avaliações")
    iaa: Optional[float] = Field(
        None, ge=0, le=10, description="Índice de Auto Avaliação")
    ieg: Optional[float] = Field(
        None, ge=0, le=10, description="Índice de Engajamento")
    ips: Optional[float] = Field(
        None, ge=0, le=10, description="Índice Psicossocial")
    ida: Optional[float] = Field(
        None, ge=0, le=10, description="Índice de Desenvolvimento Acadêmico")
    nota_matematica: Optional[float] = Field(
        None, ge=0, le=10, description="Nota de Matemática")
    nota_portugues: Optional[float] = Field(
        None, ge=0, le=10, description="Nota de Português")
    nota_ingles: Optional[float] = Field(
        None, ge=0, le=10, description="Nota de Inglês")
    ipp: Optional[float] = Field(
        None, ge=0, le=10, description="Índice Psicopedagógico")
    avaliador5: Optional[float] = Field(
        None, ge=0, le=10, description="Nota avaliador 5")
    avaliador6: Optional[float] = Field(
        None, ge=0, le=10, description="Nota avaliador 6")
    escola: Optional[str] = Field(None, description="Nome da escola")
    media_notas: Optional[float] = Field(
        None, ge=0, le=10, description="Média das notas")
    score_indices: Optional[float] = Field(
        None, ge=0, le=10, description="Score dos índices")
    anos_no_programa: Optional[float] = Field(
        None, description="Anos no programa")

    model_config = {
        "json_schema_extra": {
            "example": {
                "fase": 5.0,
                "ano_nascimento": 2005.0,
                "idade": 15.0,
                "genero": "F",
                "ano_ingresso": 2020.0,
                "instituicao_de_ensino": "EMEF",
                "cg": 6.0,
                "cf": 7.0,
                "ct": 6.5,
                "n_av": 2.0,
                "iaa": 7.0,
                "ieg": 6.5,
                "ips": 6.0,
                "ida": 7.0,
                "nota_matematica": 6.0,
                "nota_portugues": 5.5,
                "nota_ingles": 7.0,
                "ipp": 6.5,
                "avaliador5": 7.0,
                "avaliador6": 6.5,
                "escola": "EMEF Centro",
                "media_notas": 6.17,
                "score_indices": 6.6,
                "anos_no_programa": 4.0,
            }
        }
    }


class ResultadoPredicao(BaseModel):
    """Schema de saída: resultado da predição."""
    predicao: int = Field(...,
                          description="0 = sem risco, 1 = em risco de defasagem")
    probabilidade_risco: float = Field(...,
                                       description="Probabilidade de estar em risco (0-1)")
    classificacao: str = Field(...,
                               description="Descrição textual do resultado")


class RespostaPredicao(BaseModel):
    """Envelope padrão de resposta da API."""
    status: str = "sucesso"
    dados: ResultadoPredicao
    versao_modelo: str = "1.0.0"


class RespostaSaude(BaseModel):
    """Resposta do endpoint de health check."""
    status: str
    modelo_carregado: bool
    versao: str


class RespostaErro(BaseModel):
    """Schema de resposta em caso de erro."""
    status: str = "erro"
    mensagem: str
    detalhe: Optional[str] = None
