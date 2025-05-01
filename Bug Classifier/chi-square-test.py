import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

project = 'swt'
# Step 1: Read the data from CSV files
# Replace 'bug_report_file.csv' and 'accuracy_file.csv' with the actual file paths
bug_df = pd.read_csv(f'keywords/reproduction-keyword-{project}.csv')
accuracy_df = pd.read_csv(f'../Localized Bugs/genloc/localized_bugs_{project}.csv')

accuracy = 'Accuracy@10'
# Step 2: Determine if each bug_id from bug_df was localized at accuracy@1
# A bug is "localized" if its bug_id appears in the accuracy@1 column
bug_df['localized'] = bug_df['bug_id'].apply(lambda x: 'localized' if x in accuracy_df[accuracy].values else 'not-localized')

# Step 3: Create a contingency table
# We need counts for the combinations of 'decision' (found/not-found) and 'localized' (localized/not-localized)
contingency_table = pd.crosstab(bug_df['decision'], bug_df['localized'])

# Display the contingency table
print("Contingency Table:")
print(contingency_table)

# Step 4: Perform the chi-square test
chi2, p, dof, expected = chi2_contingency(contingency_table)

# Display the results
print("\nChi-Square Test Results:")
print(f"Chi-Square Statistic: {chi2:.4f}")
print(f"P-value: {p:.4f}")
print(f"Degrees of Freedom: {dof}")
print("\nExpected Frequencies:")
print(expected)

# Step 5: Interpret the results
alpha = 0.05  # Significance level
if p < alpha:
    print(f"\nSince the p-value ({p:.4f}) is less than {alpha}, we reject the null hypothesis.")
    print(f"There is a significant relationship between the presence of 'test' and 'build' keywords and bug localization {accuracy}")
else:
    print(f"\nSince the p-value ({p:.4f}) is greater than {alpha}, we fail to reject the null hypothesis.")
    print(f"There is no significant relationship between the presence of 'test' and 'build' keywords and bug localization {accuracy}")