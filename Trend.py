import pandas as pd 
import matplotlib.pyplot as plt

# Load Excel file
file_path = r"C:\Users\talha.khan\Desktop\SDSU\Thesis\SwineBarn\Data after pigs\3rd Week\d-sesnor1.xlsx"  
df = pd.read_excel(file_path)

# Ensure the column names match exactly
date_col = "date"
time_col = "time"
value_col = "distance"

# Combine Date and Time columns into a single datetime column
df["Datetime"] = pd.to_datetime(df[date_col].astype(str) + " " + df[time_col].astype(str))

# Sort by datetime (if necessary)
df = df.sort_values("Datetime")

# Plot the data
plt.figure(figsize=(10, 5))
plt.plot(df["Datetime"], df[value_col], marker="o", linestyle="-", color="b", label="Value")

# Formatting the plot
plt.xlabel("Time")
plt.ylabel("Depth") 
plt.title("Time vs Value Plot")
plt.xticks(rotation=45)
plt.grid(True)
plt.legend()

# Show the plot
plt.show()