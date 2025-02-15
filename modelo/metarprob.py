import joblib
import os
import re
from datetime import datetime
import numpy as np


def acharprob(metar):
    # Ajuste para cobrir CLR e tornar a altitude opcional (\d{3})?
    regex_patterns = {
        "vento_direcao": r"(\b\d{3}|VRB)(?=\d{2}KT)",
        "vento_velocidade": r"(?<=\b\d{3}|VRB)(\d{2,3})(?=KT)",
        "visibilidade": r"(\b\d{4}\b)(?=\s)",
        "cobertura_nuvens": r"(FEW|SCT|BKN|OVC|CLR)(\d{3})?",
        "temperatura": r"(-?\d{2})/(-?\d{2})",
        "precipitacao": r"(\b(?:DZ|RA|SN|TS|SH|GR|SG|PL|UP|BR|FG|FU|VA|DU|SA|HZ|PO|SQ|FC|SS|DS)\b)",
        "qnh": r"Q(\d{4})",
        "horario": r"\b\d{2}(\d{4})Z\b",
    }
    airport = re.findall(r"\b[A-Z]{4}\b", metar)
    airport = airport[0]

    # Função para classificar precipitação
    def classify_precipitation(precipitation_list):
        if not precipitation_list:
            return "Nenhuma"
        if any(p in precipitation_list for p in ["TS", "SHRA", "TSRA", "GR"]):
            return "Forte"
        if any(p in precipitation_list for p in ["RA", "SN", "SH", "PL"]):
            return "Moderada"
        if any(p in precipitation_list for p in ["-RA", "-SN", "-SH", "-DZ"]):
            return "Leve"
        return "Nenhuma"

    # Função para "classificar" nuvens - retorna (sigla, altura)
    def classify_cloud_cover_with_altitude(cloud_list):
        if not cloud_list:
            # Se não houver informação de nuvem, definimos CLR por padrão
            return ("CLR", 0)
        # Ordenar por altura, considerando que CLR não tem número
        sorted_clouds = sorted(
            cloud_list, key=lambda x: int(x[1]) if x[1].isdigit() else 999
        )
        lowest_layer = sorted_clouds[0]

        coverage = lowest_layer[0]
        altitude_str = lowest_layer[1] if len(lowest_layer) > 1 else ""
        if altitude_str and altitude_str.isdigit():
            cloud_altitude = int(altitude_str) * 100
        else:
            cloud_altitude = 0

        return (coverage, cloud_altitude)

    # Extrair dados do METAR via regex
    extracted = {
        field: re.findall(pattern, metar) for field, pattern in regex_patterns.items()
    }
    date = datetime.now().date()
    # time = datetime.now().time()
    time = datetime.strptime(extracted["horario"][0], "%H%M").time()
    processed = {
        "vento_direcao": extracted["vento_direcao"][0]
        if extracted["vento_direcao"]
        else None,
        "vento_velocidade": extracted["vento_velocidade"][0]
        if extracted["vento_velocidade"]
        else None,
        "visibilidade": extracted["visibilidade"][0]
        if extracted["visibilidade"]
        else None,
        "cobertura_nuvens": classify_cloud_cover_with_altitude(
            extracted["cobertura_nuvens"]
        )[0],
        "altura_nuvens": classify_cloud_cover_with_altitude(
            extracted["cobertura_nuvens"]
        )[1],
        "temperatura": extracted["temperatura"][0][0]
        if extracted["temperatura"]
        else None,
        "precipitacao": classify_precipitation(
            [p[0] for p in extracted["precipitacao"]]
        ),
        "qnh": extracted["qnh"][0] if extracted["qnh"] else None,
    }

    # Carregar modelo e encoders
    model_dir = os.path.dirname(__file__)
    model_path = os.path.join(model_dir, "bird_model.pkl")
    model = joblib.load(model_path)

    le_cobertura = joblib.load(os.path.join(model_dir, "le_cobertura.pkl"))
    le_precip = joblib.load(os.path.join(model_dir, "le_precip.pkl"))
    le_localidade = joblib.load(os.path.join(model_dir, "le_localidade.pkl"))

    # Funções para tratar valores nulos / parsear floats
    def safe_str(x):
        return x if x is not None else ""

    def safe_float(x):
        try:
            return float(x)
        except (ValueError, TypeError):
            return 0.0

    # Ajuste de cobertura
    processed_cobertura = safe_str(processed["cobertura_nuvens"])
    if processed_cobertura not in le_cobertura.classes_:
        # Fallback caso não exista no LabelEncoder
        processed_cobertura = "CLR"
    cobertura_enc = le_cobertura.transform([processed_cobertura])[0]

    # Ajuste de precipitação
    processed_precipitacao = safe_str(processed["precipitacao"])
    if processed_precipitacao not in le_precip.classes_:
        processed_precipitacao = le_precip.classes_[0]
    precip_enc = le_precip.transform([processed_precipitacao])[0]

    # Ajuste de localidade
    if airport not in le_localidade.classes_:
        airport_enc = le_localidade.transform([le_localidade.classes_[0]])[0]
    else:
        airport_enc = le_localidade.transform([airport])[0]

    # Precisamos 13 colunas (conforme o treino)
    # 0: vento_direcao
    # 1: vento_velocidade
    # 2: visibilidade
    # 3: cobertura_nuvens
    # 4: altura_nuvens
    # 5: temperatura
    # 6: precipitacao
    # 7: qnh
    # 8: localidade
    # 9: day
    # 10: weekday
    # 11: hour
    # 12: minute
    day = date.day
    weekday = date.weekday()
    hour = time.hour
    minute = time.minute

    features = [
        safe_float(processed["vento_direcao"]),
        safe_float(processed["vento_velocidade"]),
        safe_float(processed["visibilidade"]),
        float(cobertura_enc),
        safe_float(processed["altura_nuvens"]),
        safe_float(processed["temperatura"]),
        float(precip_enc),
        safe_float(processed["qnh"]),
        float(airport_enc),
        float(day),
        float(weekday),
        float(hour),
        float(minute),
    ]

    final_features = np.array(features).reshape(1, -1)

    # Obter probabilidade da classe "1" (avistamento)
    probability = model.predict_proba(final_features)[0][1] * 100

    return round(probability, 2)
