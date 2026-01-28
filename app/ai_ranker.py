def relevance_score(call, query_params: dict):
    score = 0.0

    q = (query_params.get("q") or "").lower()
    country = (query_params.get("host_country") or "").lower()
    degree = (query_params.get("degree_level") or "").lower()

    title = (call.title or "").lower()
    field = (call.field or "").lower()
    theme = (call.theme or "").lower()
    sdg = (call.sdg_tags or "").lower()

    # =========================
    # KEYWORD RELEVANCE
    # =========================
    if q:
        if q in title:
            score += 3.0
        if q in field:
            score += 2.0
        if q in theme:
            score += 1.5
        if q in sdg:
            score += 1.0

    # =========================
    # DEGREE MATCH
    # =========================
    if degree and degree in (call.degree_level or "").lower():
        score += 2.0

    # =========================
    # COUNTRY MATCH
    # =========================
    if country and country in (call.host_country or "").lower():
        score += 2.0

    # =========================
    # FIELD MATCH
    # =========================
    if q and q in field:
        score += 2.0

    # =========================
    # THEME MATCH
    # =========================
    if q and q in theme:
        score += 1.5

    # =========================
    # SDG MATCH
    # =========================
    if q and q in sdg:
        score += 1.0

    # =========================
    # CONFIDENCE BOOST
    # =========================
    if hasattr(call, "confidence_score") and call.confidence_score:
        score += float(call.confidence_score)

    return score
