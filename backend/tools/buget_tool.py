def budget_tool(budget_min: int, budget_max: int, segments: list):
    """Analyze and validate budget allocation"""
    
    # Calculate total
    total = sum(seg['estimatedCost'] for seg in segments)
    
    # Determine fit
    if total < budget_min:
        fit = 'under'
    elif total <= budget_max:
        fit = 'within'
    else:
        fit = 'over'
    
    # Generate suggestions
    suggestions = []
    
    if fit == 'under':
        remaining = budget_min - total
        suggestions.append(f"You have ₹{remaining} remaining. Consider upgrading the dining experience.")
        suggestions.append("You could add a dessert stop at a premium patisserie.")
    elif fit == 'over':
        excess = total - budget_max
        suggestions.append(f"Budget exceeded by ₹{excess}. Consider these adjustments:")
        
        sorted_segments = sorted(segments, key=lambda x: x['estimatedCost'], reverse=True)
        
        for seg in sorted_segments:
            seg_type = seg['type'].lower()
            if 'dining' in seg_type and seg['estimatedCost'] > budget_max * 0.5:
                suggestions.append("Choose a mid-range restaurant instead of fine dining.")
            if 'gift' in seg_type and seg['estimatedCost'] > budget_max * 0.3:
                suggestions.append("Consider a more modest gift.")
    else:
        suggestions.append("Budget allocation is well-balanced!")
    
    return {
        'total': total,
        'fit': fit,
        'suggestions': suggestions
    }