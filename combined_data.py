import csv, os




with open("data_whole.csv", "r") as f:

    data_whole = list(csv.reader(f))

with open("data_whole_3.csv", "r", encoding='utf-8') as f:

    data_old = list(csv.reader(f))

data_whole_dict = {item_id:value for item_id, value in data_whole}
data_old_dict = {each[0]:each for each in data_old[1:]}

final_data = []

for item_id, data in data_old_dict.items():

    if item_id in data_whole_dict:

        final_data.append(data + [data_whole_dict[item_id]])

    else:

        print(item_id)


    

with open("data_whole___3.csv", "w+", newline="", encoding='utf-8') as f:

    writer = csv.writer(f)

    writer.writerows(final_data)
