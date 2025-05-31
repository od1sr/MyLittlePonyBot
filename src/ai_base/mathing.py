def harris_benedict_formula(weight, height, age, gender):
    """
    Calculates Basal Metabolic Rate (BMR) using Harris-Benedict formula
    
    Args:
        weight (float): Weight in kilograms
        height (float): Height in centimeters
        age (int): Age in years
        gender (str): 'M' for male or 'F' for female
        
    Returns:
        float: BMR in calories per day
    """
    if gender.upper() == 'M':
        bmr = 66.47 + (13.75 * weight) + (5.003 * height) - (6.755 * age)
    elif gender.upper() == 'F':
        bmr = 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age)
    else:
        raise ValueError("Gender must be 'M' for male or 'F' for female")
    
    return round(bmr, 2)

def calculate_total_calories(bmr, activity_level):
    """
    Calculates total daily calorie needs based on BMR and activity level
    
    Args:
        bmr (float): Basal Metabolic Rate
        activity_level (str): Activity level ('sedentary', 'light', 'moderate', 'active', 'very_active')
        
    Returns:
        float: Total daily calorie needs
    """
    activity_multipliers = {
        'sedentary': 1.2,      # Little or no exercise
        'light': 1.375,        # Light exercise 1-3 times/week
        'moderate': 1.55,      # Moderate exercise 3-5 times/week
        'active': 1.725,       # Heavy exercise 6-7 times/week
        'very_active': 1.9     # Very heavy exercise, physical job
    }
    
    if activity_level not in activity_multipliers:
        raise ValueError("Invalid activity level")
        
    total_calories = bmr * activity_multipliers[activity_level]
    return round(total_calories, 2)
