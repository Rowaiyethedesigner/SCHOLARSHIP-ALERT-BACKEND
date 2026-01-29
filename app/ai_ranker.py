def relevance_score(call, query_params: dict):
    try:
        score = 0.0

        q = (query_params.get("q") or "").lower()
        country = (query_params.get("host_country") or "").lower()
        degree = (query_params.get("degree_level") or "").lower()

        title = (getattr(call, "title", "") or "").lower()
        field = (getattr(call, "field", "") or "").lower()
        theme = (getattr(call, "theme", "") or "").lower()
        sdg = (getattr(call, "sdg_tags", "") or "").lower()
        host = (getattr(call, "host_country", "") or "").lower()
        deg = (getattr(call, "degree_level", "") or "").lower()

        # KEYWORD RELEVANCE
        if q:
            if q in title:
                score += 3.0
            if q in field:
                score += 2.0
            if q in theme:
                score += 1.5
            if q in sdg:
                score += 1.0

        # DEGREE MATCH
        if degree and degree in deg:
            score += 2.0

        # COUNTRY MATCH
        if country and country in host:
            score += 2.0

        return score

    except Exception:
        # Absolute safety: ranking can never crash API
        return 0.0
