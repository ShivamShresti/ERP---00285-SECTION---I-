import pandas as pd

# ---------- Step 1: Load the CSV and skip bad rows ----------
def load_data(filename):
    try:
        raw = pd.read_csv(filename, header=None,
                          names=["Name", "Marks", "Income", "Attendance"],
                          dtype=str)
    except FileNotFoundError:
        print("File not found:", filename)
        return pd.DataFrame()

    # If the file has a header row (Name,Marks,...), drop it
    if len(raw) > 0 and str(raw.iloc[0]["Name"]).strip().lower() == "name":
        raw = raw.iloc[1:]

    good_rows = []
    for _, row in raw.iterrows():
        name = str(row["Name"]).strip()
        valid = True
        values = {}
        for col in ["Marks", "Income", "Attendance"]:
            text = row[col]
            try:
                values[col] = float(text)
            except (ValueError, TypeError):
                print(f"Invalid {col.lower()} for {name}: '{text}'. Row skipped.")
                valid = False
                break
        if valid:
            good_rows.append({"Name": name, **values})

    return pd.DataFrame(good_rows, columns=["Name", "Marks", "Income", "Attendance"])


# ---------- Step 2: Eligibility and scholarship rules ----------
def get_result(row):
    eligible = (row["Attendance"] >= 75 and row["Marks"] >= 75
                and row["Income"] <= 500000)
    if not eligible:
        return "Not Eligible", 0
    if row["Marks"] >= 90 and row["Income"] <= 300000:
        return "Full", 50000
    return "Partial", 25000


def add_results(df):
    results = df.apply(get_result, axis=1)
    df["Result"] = [r[0] for r in results]
    df["Scholarship"] = [r[1] for r in results]
    return df


# ---------- Step 3: Menu options ----------
def show_eligibility(df):
    for _, row in df.iterrows():
        if row["Result"] == "Not Eligible":
            print(f"{row['Name']} | Not Eligible")
        else:
            print(f"{row['Name']} | {row['Result']} | Rs. {int(row['Scholarship'])}")


def show_summary(df):
    eligible = df[df["Result"] != "Not Eligible"]
    not_eligible = df[df["Result"] == "Not Eligible"]
    full = df[df["Result"] == "Full"]
    partial = df[df["Result"] == "Partial"]

    print(f"Eligible: {len(eligible)} | Not Eligible: {len(not_eligible)} "
          f"| Full: {len(full)} | Partial: {len(partial)}")

    total = int(df["Scholarship"].sum())
    avg = eligible["Marks"].mean() if len(eligible) > 0 else 0.0
    print(f"Total scholarship: Rs. {total} | Average marks (eligible): {avg:.2f}")


def filter_by_marks(df):
    try:
        min_marks = float(input("Enter minimum marks: "))
    except ValueError:
        print("Please enter a valid number.")
        return
    filtered = df[df["Marks"] >= min_marks]
    if filtered.empty:
        print("No students found.")
    for _, row in filtered.iterrows():
        print(f"{row['Name']} | {int(row['Marks'])}")


# ---------- Step 4: Main program ----------
def main():
    df = load_data("students.csv")
    if df.empty:
        print("No valid data to process.")
        return
    df = add_results(df)

    while True:
        print("\n--- Student Scholarship Eligibility Analyzer ---")
        print("1. Eligibility")
        print("2. Summary")
        print("3. Filter by minimum marks")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_eligibility(df)
        elif choice == "2":
            show_summary(df)
        elif choice == "3":
            filter_by_marks(df)
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-4.")


main()





















