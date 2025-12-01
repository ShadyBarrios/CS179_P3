def criteria_b(port_side_weight, starboard_side_weight) -> float:
    side_diff = abs(port_side_weight - starboard_side_weight)
    total_weight = port_side_weight + starboard_side_weight
    return side_diff - (total_weight * 0.1)

# criteria b: |Ph - Sh| <= (Sum(Po, So) * 0.10) therefore |Ph - Sh| - (sum(Po, So) * 10) <= 0
def meets_criteria_b(port_side_weight, starboard_side_weight) -> bool:
    criteria_b_calc = criteria_b(port_side_weight, starboard_side_weight)
    return (criteria_b_calc <= 0)

port_side = [203, 101]
starboard_side = [200, 99]

## NOTE:
## heuristic can be manhattan distance from 
# crane to closest free position if next type is moveitem
# crane to closest moveable object then to closest free position if next type is toItem
# crane to park if next type is ToPark
