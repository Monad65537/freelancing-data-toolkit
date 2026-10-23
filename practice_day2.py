import pandas as pd

data = {
    "Name": [" Anna ", "BOB", "Alice", "Bob"],
    "Amount": [100, 200, None, 200],
    "City": ["Warsaw", "Krakow", "Warsaw", "Krakow"],
}

df = pd.DataFrame(data)

df["Name"] = df["Name"].str.strip().str.title()
df["City"] = df["City"].str.upper()
df["Amount_Doubled"] = df["Amount"] * 2

df.to_csv("practice_output.csv", index=False)