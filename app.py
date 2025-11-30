import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="HR Analytics Dashboard", layout="wide")

#Load data
df = pd.read_csv('HR Employee Attrition.csv')


# SIDEBAR

st.sidebar.title("📘 Dataset Description")
st.sidebar.info("""
HR Employee Attrition Dataset:
                
This dataset includes employee information 
such as department, salary, experience level, 
and involvement in R&D. It can be used to explore 
workforce trends, compare departments, and generate
 insights.
""")

#FILTERS
st.sidebar.title("Filters")

# Department filter
selected_departments = st.sidebar.multiselect(
    "Select Department",
    df["Department"].unique(),
    default=df["Department"].unique()
)

# Job role filter
selected_roles = st.sidebar.multiselect(
    "Select Job Role",
    df["JobRole"].unique(),
    default=df["JobRole"].unique()
)

# Age slider
age_range = st.sidebar.slider(
    "Select Age Range",
    int(df["Age"].min()),
    int(df["Age"].max()),
    (int(df["Age"].min()), int(df["Age"].max()))
)

# Attrition dropdown
selected_attrition = st.sidebar.selectbox(
    "Select Attrition Status",
    ["All", "Yes", "No"]
)

#Filters
df_filtered = df[
    (df["Department"].isin(selected_departments)) &
    (df["JobRole"].isin(selected_roles)) &
    (df["Age"].between(age_range[0], age_range[1]))
]

if selected_attrition != "All":
    df_filtered = df_filtered[df_filtered["Attrition"] == selected_attrition]



# MAIN PAGE

st.title("HR Employee Attrition Dashboard")

# SECTION 1 — DATA PREVIEW
st.header("📌 Data Preview")
st.dataframe(df_filtered.head())

# SECTION 2 — SUMMARY STATISTICS
st.header("📌 Summary Statistics")
st.write(df_filtered.describe())

# DATA INFO
st.subheader("Dataset Information")
summary_df = pd.DataFrame({
    "Column": df.columns,
    "Data Type": df.dtypes.astype(str),
    "Missing Values": df.isnull().sum(),
    "Unique Values": df.nunique()
})

st.dataframe(summary_df)


# VISUALIZATIONS 

st.header("📊 Visualizations")

# 1) Employees per Department
st.subheader("Employees per Department")
plt.figure(figsize=(8,5))
sns.countplot(data=df_filtered, x='Department')
plt.xticks(rotation=20)
st.pyplot(plt.gcf())
plt.clf()

# 2) Attrition Pie Chart
st.subheader("Attrition Rate")
plt.figure(figsize=(6,6))
df_filtered['Attrition'].value_counts().plot.pie(autopct='%1.0f%%')
plt.ylabel('')
st.pyplot(plt.gcf())
plt.clf()

# 3) Population Pyramid
st.subheader("Attrition by Department (Population Pyramid)")
departments_unique = df_filtered['Department'].unique()
stayed = df_filtered[df_filtered['Attrition']=='No']['Department'].value_counts().reindex(departments_unique, fill_value=0)
left = df_filtered[df_filtered['Attrition']=='Yes']['Department'].value_counts().reindex(departments_unique, fill_value=0)

fig, ax = plt.subplots(figsize=(8,5))
ax.barh(departments_unique, stayed, label='Stayed')
ax.barh(departments_unique, -left, label='Left')
ax.legend()
st.pyplot(fig)
plt.clf()

# 4) Violin Plot
st.subheader("Income Distribution by Department")
plt.figure(figsize=(10,5))
sns.violinplot(data=df_filtered, x='Department', y='MonthlyIncome', inner='box')
plt.xticks(rotation=25)
st.pyplot(plt.gcf())
plt.clf()

# 5) Tenure (left)
st.subheader("Avg Tenure of Employees Who Left")
plt.figure(figsize=(8,5))
df_filtered[df_filtered['Attrition']=='Yes'].groupby('Department')['YearsAtCompany'].mean().plot(kind='bar')
plt.xticks(rotation=25)
st.pyplot(plt.gcf())
plt.clf()

# 6) Attrition by Income Range
st.subheader("Attrition by Income Range")
left_df = df_filtered[df_filtered["Attrition"] == "Yes"].copy()
bins = [0,3000,6000,9000,12000,15000,18000]
labels = ['0-3k','3-6k','6-9k','9-12k','12-15k','15-18k']
left_df['IncomeRange'] = pd.cut(left_df['MonthlyIncome'], bins=bins, labels=labels)
left_df['IncomeRange'].value_counts().sort_index().plot(kind='line', marker='o')
st.pyplot(plt.gcf())
plt.clf()

# 7) Histogram — Years at Company
st.subheader("Years at Company — Employees Who Left")
plt.figure(figsize=(8,5))
df_filtered[df_filtered['Attrition']=='Yes']['YearsAtCompany'].plot.hist(bins=15)
st.pyplot(plt.gcf())
plt.clf()

# 8) Job Role Attrition
st.subheader("Attrition by Job Role")
plt.figure(figsize=(10,5))
sns.countplot(data=df_filtered[df_filtered['Attrition']=='Yes'], x='JobRole')
plt.xticks(rotation=35)
st.pyplot(plt.gcf())
plt.clf()

# 9) Heatmap
st.subheader("Correlation Heatmap")
plt.figure(figsize=(8,5))
sns.heatmap(df_filtered[['Age','MonthlyIncome','YearsAtCompany']].corr(), annot=True)
st.pyplot(plt.gcf())
plt.clf()


# INSIGHT SECTION:

st.subheader("📌 Key Insights from the HR Attrition Dataset")

st.markdown("""
### 1. Departments with the highest attrition
- The HR and R&D departments show the highest attrition rates.
- This indicates potential internal issues such as workload, job satisfaction, or compensation gaps within these departments.

---

### 2. Low salary is a major driver of attrition
- Employees who left the company tend to have significantly lower monthly incomes.
- This pattern appears consistently across departments, making salary one of the strongest predictors of attrition.

---

### 3. Sales department characteristics
- The Sales department has a large employee count, similar to R&D.
- Employees in Sales who left the company often had longer years of experience.
- This suggests they may have received better job offers elsewhere due to their skill level and experience.

---

### 4. Job roles with the highest attrition
- The Laboratory Technician role shows one of the highest exit rates.
- This group also falls into the lower-income range, reinforcing the role of salary in attrition behavior.

---

### 5. Employees with fewer years at the company tend to leave more
- A significant number of employees who left had short tenure.
- This may indicate difficulty in early-stage engagement, onboarding quality, or lack of job fit, causing employees to leave before settling.

---

### 🔍 Overall Conclusion
- Low income is the strongest and most consistent factor related to employee attrition.
- Department culture, experience level, and early career engagement also play major roles.
- Improving compensation, onboarding, and (department-level conditions)—especially in HR and R&D—may help reduce turnover.

""")
