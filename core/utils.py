def calculate_rounded_value(total, celling_start):
        last_digit = int(str(total)[-1])  # Get the last digit of the total
        result = 0
        
        print(last_digit)
        if total > celling_start and celling_start != 0:
            if last_digit == 3:
                result = round(total) + 7 - total
            elif last_digit == 4:
                result = round(total) + 6 - total
            elif last_digit == 5:
                result = round(total) + 5 - total
            elif last_digit == 6:
                result = round(total) + 4 - total
            elif last_digit == 7:
                result = round(total) + 3 - total
            elif last_digit == 8:
                result = round(total) + 2 - total
            elif last_digit == 9:
                result = round(total) + 1 - total

        return result