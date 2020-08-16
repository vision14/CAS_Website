def my_predictions(my_url, s_date):

    data = requests.get(my_url).json()
    data = data["result"]["pageContext"]["countryGroup"]

    total_cases = []
    total_deaths = []
    new_cases = []
    new_deaths = []

    for i in data["data"]["rows"]:
        new_deaths.append(i[2])
        total_deaths.append(i[3])
        new_cases.append(i[7])
        total_cases.append(i[8])

    date_list = pd.date_range(start=s_date, end=datetime.today()).tolist()

    if len(date_list) > len(new_cases):
        date_list = date_list[:len(new_cases)]

    data_dict = {"Date": date_list,
                 "New Cases": new_cases,
                 "Total Cases": total_cases,
                 "New Deaths": new_deaths,
                 "Total Deaths": total_deaths}

    data_dict["Date"] = data_dict["Date"][:-30]
    data_dict["New Cases"] = data_dict["New Cases"][:-30]
    data_dict["Total Cases"] = data_dict["Total Cases"][:-30]
    data_dict["New Deaths"] = data_dict["New Deaths"][:-30]
    data_dict["Total Deaths"] = data_dict["Total Deaths"][:-30]

    df = pd.DataFrame.from_dict(data_dict)
    df = df.set_index("Date")
    df = df.asfreq(pd.infer_freq(df.index))
    df.columns = df.columns.str.replace(' ', '_')
    new_cases_df = df.iloc[:, 0]
    total_cases_df = df.iloc[:, 1]
    new_deaths_df = df.iloc[:, 2]
    total_deaths_df = df.iloc[:, 3]

    nc_preds = covid_prediction(new_cases_df)
    nd_preds = covid_prediction(new_deaths_df)

    for i in range(len(nc_preds)):
        if nc_preds[i] < 0:
            nc_preds[i] = 0
        if nd_preds[i] < 0:
            nd_preds[i] = 0

    tc_preds = [int(abs(nc_preds[0] + total_cases_df.iloc[-1]))]
    td_preds = [int(abs(nd_preds[0] + total_deaths_df.iloc[-1]))]
    for i in range(1, len(nc_preds)):
        tc_preds.append(int(abs(nc_preds[i] + tc_preds[i - 1])))
        td_preds.append(int(abs(nd_preds[i] + td_preds[i - 1])))

    start_date = data_dict["Date"][-1] + timedelta(days=1)
    end_date = start_date + timedelta(days=30)

    date_list = pd.date_range(start=start_date, end=end_date).tolist()
    if len(date_list) > len(nc_preds):
        date_list = date_list[:len(nc_preds)]

    predictions_dict = {"Date": date_list,
                        "New Cases": nc_preds,
                        "Total Cases": tc_preds,
                        "New Deaths": nd_preds,
                        "Total Deaths": td_preds}

    return [data_dict, predictions_dict]