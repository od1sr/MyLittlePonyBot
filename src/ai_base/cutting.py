def parse_weekly_menu(text: str) -> dict:
    """
    Парсит текст с недельным меню и возвращает структурированные данные.
    Возвращает словарь с днями недели и рекомендациями.
    """
    result = {
        "days": {},
        "recommendations": ""
    }

    # Разделяем меню и рекомендации
    parts = text.split("===")
    menu_text = parts[0].strip()
    
    if len(parts) > 1:
        result["recommendations"] = parts[1].strip()

    # Разбиваем по дням недели
    day_blocks = [block.strip() for block in menu_text.split("-") if block.strip()]
    
    for block in day_blocks:
        # Извлекаем название дня (первая строка до двоеточия)
        day_lines = block.split('\n')
        day_name = day_lines[0].replace(':', '').strip()
        
        # Обрабатываем приемы пищи
        meals = {}
        current_meal = None
        
        for line in day_lines[1:]:
            line = line.strip()
            if not line:
                continue
                
            # Если строка начинается с приема пищи (содержит двоеточие)
            if ':' in line:
                meal_parts = line.split(':', 1)
                current_meal = meal_parts[0].strip()
                meals[current_meal] = meal_parts[1].strip()
            elif current_meal:
                # Продолжение описания предыдущего приема пищи
                meals[current_meal] += '\n' + line
        
        result["days"][day_name] = meals

    return result