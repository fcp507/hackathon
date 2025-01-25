import statistics

def war_prediction(data):
    """
    This function takes a list of numerical data and returns the mode.
    If there are multiple modes, it returns a list of the modes.
    
    Parameters:
    data (list): A list of numerical data
    
    Returns:
    mode: The mode of the dataset or list of modes if multiple modes exist
    """
    try:
        mode_value = statistics.multimode(data)
        if len(mode_value) == 1:
            return mode_value[0]
        else:
            return mode_value
    except statistics.StatisticsError as e:
        return str(e)
# Example usage
mode_result = mode_prediction(data)
print(f"The mode(s) of the dataset is/are: {mode_result}")
