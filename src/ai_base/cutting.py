def cut_text_with_week(text: str) -> dict:
    """Разбивает текст на недели"""
    data = {
        "recomendations": "",
        "days": {}
    }
    
    # Разделяем основную часть и рекомендации
    parts = text.split("===", maxsplit=1)
    days_text = parts[0].strip()
    
    if len(parts) > 1:
        data["recomendations"] = parts[1].strip()
    
    # Обрабатываем дни
    for day_block in days_text.split("-"):
        if not day_block.strip():
            continue
            
        # Разделяем название дня и содержание
        day_parts = day_block.split(":", maxsplit=1)
        if len(day_parts) < 2:
            continue
            
        day_name = day_parts[0].strip()
        day_content = day_parts[1].strip()
        
        data["days"][day_name] = {}
        
        # Обрабатываем приёмы пищи
        for eat_line in day_content.split("\n"):
            if not eat_line.strip():
                continue
                
            # Разделяем название приёма пищи и описание
            eat_parts = eat_line.split(":", maxsplit=1)
            if len(eat_parts) < 2:
                continue
                
            eat_name = eat_parts[0].strip()
            eat_description = eat_parts[1].strip()
            
            data["days"][day_name][eat_name] = eat_description
    
    return data