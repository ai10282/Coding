import pandas as pd


def count_bigger_5(dataseries):
    return sum(dataseries > 5)


office_a = pd.read_xml("../Data/A_office_data.xml")
index_a = ['A' + str(i) for i in office_a.employee_office_id]
office_a.index = index_a

office_b = pd.read_xml("../Data/B_office_data.xml")
index_b = ['B' + str(i) for i in office_b.employee_office_id]
office_b.index = index_b

office_hr = pd.read_xml("../Data/hr_data.xml")
office_hr.set_index('employee_id', drop=False, inplace=True)

# print(office_a.index.tolist())
# print(office_b.index.tolist())
# print(office_hr.index.tolist())

office_ab = pd.concat([office_a, office_b])
office_abhr = office_ab.merge(office_hr, right_index=True, left_index=True, indicator=True)
office_abhr.drop(columns=['employee_office_id', 'employee_id', '_merge'], inplace=True)
office_abhr.sort_index(inplace=True)

# print(office_abhr.index.tolist())
# print(office_abhr.columns.tolist())

first_line = office_abhr.sort_values('average_monthly_hours', ascending=False)
second_line = office_abhr.query("Department == 'IT' & salary == 'low'")
third_line = office_abhr.loc[['A4', 'B7064', 'A3033'], ['last_evaluation', 'satisfaction_level']]

# print(first_line.Department.head(10).tolist())
# print(second_line.number_project.sum())
# print(third_line.values.tolist())
# print(office_abhr.loc[office_abhr.number_project > 3])

# print(office_abhr.groupby(['left']).agg({'number_project': ['median', count_bigger_5],
#                                         'time_spend_company': ['mean', 'median'],
#                                         'Work_accident': ['mean'],
#                                         'last_evaluation': ['mean', 'std']}).round(2).to_dict())

pivot1 = office_abhr.pivot_table(index='Department', columns=['left', 'salary'],
                                 values='average_monthly_hours', aggfunc='median')
pivot1 = pivot1.loc[(pivot1[(0.0, 'medium')] > pivot1[(0.0, 'high')])
                    | (pivot1[(1.0, 'high')] > pivot1[(1.0, 'low')])].round(2)

pivot2 = office_abhr.pivot_table(index='time_spend_company', columns='promotion_last_5years',
                                 values=['last_evaluation', 'satisfaction_level'],
                                 aggfunc=['max', 'mean', 'min'])
pivot2 = pivot2.loc[pivot2[('mean', 'last_evaluation', 0)] >
                    pivot2[('mean', 'last_evaluation', 1)]].round(2)
print(pivot1.to_dict())
print(pivot2.to_dict())
