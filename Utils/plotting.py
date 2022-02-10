import matplotlib.pyplot as plt
import re


def plot_table_result(schedule_group_stud: dict, schedule_group_pans: dict, score: int) -> None:
    """
    Table of the best group created
    """
    
    class_map = {
        'D1 S1': 0, 'D1 S2': 1, 'D1 S3': 2,
        'D2 S1': 3, 'D2 S2': 4, 'D2 S3': 5,
        'D3 S1': 6, 'D3 S2': 7, 'D3 S3': 8,
    }

    cell_colour_stud = []
    clean_schedule_stud = [[int(re.search(r'\d+', stu).group()), cls] for stu, cls in schedule_group_stud.items()]
    clean_schedule_stud.sort(key=lambda x: x[0])
    for infos in clean_schedule_stud:
        default_col = ['white' for _ in range(9)]
        position = class_map[infos[1]]
        default_col[position] = 'lightsteelblue'
        cell_colour_stud.append(default_col)

    cell_colour_pans = []
    clean_schedule_pans = [[int(re.search(r'\d+', stu).group()), cls] for stu, cls in schedule_group_pans.items()]
    clean_schedule_pans.sort(key=lambda x: x[0])
    print(clean_schedule_pans)
    for infos in clean_schedule_pans:
        default_col = ['white' for _ in range(9)]
        for info in infos[1]:
            position = class_map[info]
            default_col[position] = 'lightsteelblue'
        cell_colour_pans.append(default_col)

    fig, axes = plt.subplots(figsize=(15, 7), nrows=2, ncols=1)

    axes[0].xaxis.set_visible(False) 
    axes[0].yaxis.set_visible(False)
    table1 = axes[0].table(
        cellColours=cell_colour_stud, 
        rowLabels=['Student 1', 'Student 2', 'Student 3', 'Student 4', 'Student 5', 'Student 6', 'Student 7', 'Student 8', 'Student 9', 'Student 10'], 
        rowColours=['aquamarine' for _ in range(10)], 
        colLabels=['Day 1 Slot 1', 'Day 1 Slot 2', 'Day 1 Slot 3', 'Day 2 Slot 1', 'Day 2 Slot 2', 'Day 2 Slot 3', 'Day 3 Slot 1', 'Day 3 Slot 2', 'Day 3 Slot 3'], 
        colColours=['aquamarine' for _ in range(9)],
        loc='center')
    table1.auto_set_font_size(False)
    table1.set_fontsize(17)
    axes[0].axis("off")
    axes[0].set_title('Best Group Created for Students with quality score of {}'.format(score))

    axes[1].xaxis.set_visible(False) 
    axes[1].yaxis.set_visible(False)
    table2 = axes[1].table(
        cellColours=cell_colour_pans, 
        rowLabels=['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10'], 
        rowColours=['aquamarine' for _ in range(10)], 
        colLabels=['Day 1 Slot 1', 'Day 1 Slot 2', 'Day 1 Slot 3', 'Day 2 Slot 1', 'Day 2 Slot 2', 'Day 2 Slot 3', 'Day 3 Slot 1', 'Day 3 Slot 2', 'Day 3 Slot 3'], 
        colColours=['aquamarine' for _ in range(9)],
        loc='center')
    table2.auto_set_font_size(False)
    table2.set_fontsize(17)
    axes[1].axis("off")
    axes[1].set_title('Best Group Created for Panels with quality score of {}'.format(score))

    plt.show();

def plot_comparison_result(list1: list, label1: str, best1, avg1, worst1, 
                           list2: list, label2: str, best2, avg2, worst2) -> None:
    """
    Box plot result of result 1 and 2
    """

    fig, axes = plt.subplots(figsize=(15, 7), nrows=1, ncols=2)

    axes[0].boxplot(list1, showmeans=True, meanline=True, notch=True)
    axes[0].set_title("Boxplot result for {}".format(label1))
    axes[0].text(1 + 0.125, best1 - 0.75, "best-result: {}".format(best1))
    axes[0].text(1 + 0.125, avg1 - 0.75, "avg-result: {}".format(avg1))
    axes[0].text(1 + 0.125, worst1 - 0.75, "worst-result: {}".format(worst1))

    axes[1].boxplot(list2, showmeans=True, meanline=True, notch=True)
    axes[1].set_title("Boxplot result for {}".format(label2))
    axes[1].text(1 + 0.125, best2 - 0.75, "best-result: {}".format(best2))
    axes[1].text(1 + 0.125, avg2 - 0.75, "avg-result: {}".format(avg2))
    axes[1].text(1 + 0.125, worst2 - 0.75, "worst-result: {}".format(worst2))

    plt.show()