from django.shortcuts import render
import pandas as pd
import matplotlib.pyplot as plt
from datetime import timedelta
import mpld3
from mpld3 import plugins
import numpy as np
from pymongo import MongoClient


# Create your views here.
def scatter(results, index, col_name, y_label, plot_title):
    df = pd.DataFrame.from_dict(results[0])
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df.columns = df.columns.str.replace(' ', '_')
    df = df.iloc[:, [0, index - 1, index]]

    df1 = pd.DataFrame.from_dict(results[1])
    df1['Date'] = pd.to_datetime(df1['Date']).dt.date
    df1.columns = df1.columns.str.replace(' ', '_')
    df1 = df1.iloc[:, [0, index - 1, index]]

    css = """

    table {
      font-family: 'Helvetica';
      margin: 1px auto;
      border: none;
      border-collapse: collapse;
      border-radius: 10px;
      background: #ffffff;
      box-shadow: 0px 0px 20px rgba(0,0,0,0.10),
         0px 10px 20px rgba(0,0,0,0.07),
         0px 20px 20px rgba(0,0,0,0.07),
         0px 30px 20px rgba(0,0,0,0.07);
      }
      th, td {
        color: #999;
        border: none;
        padding: 4px 12px;
        border-collapse: collapse;
      }
      th {
        background: #3c74cf;
        color: #fff;
        text-transform: uppercase;
        font-size: 12px;
        &.last {
          border-right: none;
        }
    """

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.grid(False)

    labels = []
    for i in range(len(df)):
        label = df.iloc[[i], :].T
        label.columns = ['Row {0}'.format(i)]
        # .to_html() is unicode; so make leading 'u' go away with str()
        labels.append(str(label.to_html()))

    labels_1 = []
    for i in range(len(df1)):
        label = df1.iloc[[i], :].T
        label.columns = ['Row {0}'.format(len(df) + i)]
        # .to_html() is unicode; so make leading 'u' go away with str()
        labels_1.append(str(label.to_html()))

    delta = timedelta(days=1)
    x = results[0]["Date"]
    y = np.array(df[col_name])
    x1 = results[1]["Date"]
    y1 = np.array(df1[col_name])

    points = ax.plot(x, y, 'o', color='b',
                     mec='k', ms=5, mew=0, alpha=.6, label='Existing')

    points_1 = ax.plot(x1, y1, 'o', color='r',
                       mec='k', ms=5, mew=0, alpha=.6, label='Predictions')

    yerr = np.linspace(0, 0.2, len(y1))
    yerr *= y1

    plt.fill_between(x1, y1 - yerr, y1 + yerr, facecolor='grey', alpha=0.5, label='Error Band')
    ax.set_xlabel('Date', fontsize=13)
    ax.set_ylabel(y_label, fontsize=13)
    ax.set_title(plot_title, size=20)
    ax.legend(loc="best")
    ax.tick_params(axis='y', which='major', pad=25)

    tooltip = plugins.PointHTMLTooltip(points[0], labels,
                                       voffset=10, hoffset=10, css=css)

    tooltip_1 = plugins.PointHTMLTooltip(points_1[0], labels_1,
                                         voffset=10, hoffset=10, css=css)

    plugins.connect(fig, tooltip)
    plugins.connect(fig, tooltip_1)

    g = mpld3.fig_to_html(fig)
    return g


def home(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.world
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)

    db_data = db.world_predictions
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)
    title_str = "Globally, as of " + str(results[0]["Date"][-1]) + ", there have been " + str(
        results[0]["Total Cases"][-1]) + \
                " confirmed cases of COVID-19, including " + str(results[0]["Total Deaths"][-1]) + \
                " deaths. These numbers are predicted to be " + str(results[1]["Total Cases"][-1]) + " cases and " + \
                str(results[1]["Total Deaths"][-1]) + " deaths by " + str(results[1]["Date"][-1]) + "."

    context = {
        'Title_String': title_str,
        'Total_Cases': scatter(results, 2, "Total_Cases", "Total Cases", "Total Cases in the World"),
        'Total_Deaths': scatter(results, 4, "Total_Deaths", "Total Deaths", "Total Deaths in the World")
    }

    return render(requests, 'home/welcome.html', context)


def argentina(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.argentina
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)

    db_data = db.argentina_predictions
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)
    title_str = "In Argentina, as of " + str(results[0]["Date"][-1]) + ", there have been " + str(
        results[0]["Total Cases"][-1]) + \
                " confirmed cases of COVID-19, including " + str(results[0]["Total Deaths"][-1]) + \
                " deaths. These numbers are predicted to be " + str(results[1]["Total Cases"][-1]) + " cases and " + \
                str(results[1]["Total Deaths"][-1]) + " deaths by " + str(results[1]["Date"][-1]) + "."

    context = {
        'Title_String': title_str,
        'Total_Cases': scatter(results, 2, "Total_Cases", "Total Cases", "Total Cases in Argentina"),
        'Total_Deaths': scatter(results, 4, "Total_Deaths", "Total Deaths", "Total Deaths in Argentina")
    }

    return render(requests, 'home/welcome.html', context)


def australia(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.australia
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)

    db_data = db.australia_predictions
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)
    title_str = "In Australia, as of " + str(results[0]["Date"][-1]) + ", there have been " + str(
        results[0]["Total Cases"][-1]) + \
                " confirmed cases of COVID-19, including " + str(results[0]["Total Deaths"][-1]) + \
                " deaths. These numbers are predicted to be " + str(results[1]["Total Cases"][-1]) + " cases and " + \
                str(results[1]["Total Deaths"][-1]) + " deaths by " + str(results[1]["Date"][-1]) + "."

    context = {
        'Title_String': title_str,
        'Total_Cases': scatter(results, 2, "Total_Cases", "Total Cases", "Total Cases in Australia"),
        'Total_Deaths': scatter(results, 4, "Total_Deaths", "Total Deaths", "Total Deaths in Australia")
    }

    return render(requests, 'home/welcome.html', context)


def brazil(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.brazil
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)

    db_data = db.brazil_predictions
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)
    title_str = "In Brazil, as of " + str(results[0]["Date"][-1]) + ", there have been " + str(
        results[0]["Total Cases"][-1]) + \
                " confirmed cases of COVID-19, including " + str(results[0]["Total Deaths"][-1]) + \
                " deaths. These numbers are predicted to be " + str(results[1]["Total Cases"][-1]) + " cases and " + \
                str(results[1]["Total Deaths"][-1]) + " deaths by " + str(results[1]["Date"][-1]) + "."

    context = {
        'Title_String': title_str,
        'Total_Cases': scatter(results, 2, "Total_Cases", "Total Cases", "Total Cases in Brazil"),
        'Total_Deaths': scatter(results, 4, "Total_Deaths", "Total Deaths", "Total Deaths in Brazil")
    }

    return render(requests, 'home/welcome.html', context)


def canada(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.canada
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)

    db_data = db.canada_predictions
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)
    title_str = "In Canada, as of " + str(results[0]["Date"][-1]) + ", there have been " + str(
        results[0]["Total Cases"][-1]) + \
                " confirmed cases of COVID-19, including " + str(results[0]["Total Deaths"][-1]) + \
                " deaths. These numbers are predicted to be " + str(results[1]["Total Cases"][-1]) + " cases and " + \
                str(results[1]["Total Deaths"][-1]) + " deaths by " + str(results[1]["Date"][-1]) + "."

    context = {
        'Title_String': title_str,
        'Total_Cases': scatter(results, 2, "Total_Cases", "Total Cases", "Total Cases in Canada"),
        'Total_Deaths': scatter(results, 4, "Total_Deaths", "Total Deaths", "Total Deaths in Canada")
    }

    return render(requests, 'home/welcome.html', context)


def china(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.china
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)

    db_data = db.china_predictions
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)
    title_str = "In China, as of " + str(results[0]["Date"][-1]) + ", there have been " + str(
        results[0]["Total Cases"][-1]) + \
                " confirmed cases of COVID-19, including " + str(results[0]["Total Deaths"][-1]) + \
                " deaths. These numbers are predicted to be " + str(results[1]["Total Cases"][-1]) + " cases and " + \
                str(results[1]["Total Deaths"][-1]) + " deaths by " + str(results[1]["Date"][-1]) + "."

    context = {
        'Title_String': title_str,
        'Total_Cases': scatter(results, 2, "Total_Cases", "Total Cases", "Total Cases in China"),
        'Total_Deaths': scatter(results, 4, "Total_Deaths", "Total Deaths", "Total Deaths in China")
    }

    return render(requests, 'home/welcome.html', context)


def germany(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.germany
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)

    db_data = db.germany_predictions
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)
    title_str = "In Germany, as of " + str(results[0]["Date"][-1]) + ", there have been " + str(
        results[0]["Total Cases"][-1]) + \
                " confirmed cases of COVID-19, including " + str(results[0]["Total Deaths"][-1]) + \
                " deaths. These numbers are predicted to be " + str(results[1]["Total Cases"][-1]) + " cases and " + \
                str(results[1]["Total Deaths"][-1]) + " deaths by " + str(results[1]["Date"][-1]) + "."

    context = {
        'Title_String': title_str,
        'Total_Cases': scatter(results, 2, "Total_Cases", "Total Cases", "Total Cases in Germany"),
        'Total_Deaths': scatter(results, 4, "Total_Deaths", "Total Deaths", "Total Deaths in Germany")
    }

    return render(requests, 'home/welcome.html', context)


def india(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.india
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)

    db_data = db.india_predictions
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)
    title_str = "In India, as of " + str(results[0]["Date"][-1]) + ", there have been " + str(
        results[0]["Total Cases"][-1]) + \
                " confirmed cases of COVID-19, including " + str(results[0]["Total Deaths"][-1]) + \
                " deaths. These numbers are predicted to be " + str(results[1]["Total Cases"][-1]) + " cases and " + \
                str(results[1]["Total Deaths"][-1]) + " deaths by " + str(results[1]["Date"][-1]) + "."

    context = {
        'Title_String': title_str,
        'Total_Cases': scatter(results, 2, "Total_Cases", "Total Cases", "Total Cases in India"),
        'Total_Deaths': scatter(results, 4, "Total_Deaths", "Total Deaths", "Total Deaths in India")
    }

    return render(requests, 'home/welcome.html', context)


def iran(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.iran
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)

    db_data = db.iran_predictions
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)
    title_str = "In Iran, as of " + str(results[0]["Date"][-1]) + ", there have been " + str(
        results[0]["Total Cases"][-1]) + \
                " confirmed cases of COVID-19, including " + str(results[0]["Total Deaths"][-1]) + \
                " deaths. These numbers are predicted to be " + str(results[1]["Total Cases"][-1]) + " cases and " + \
                str(results[1]["Total Deaths"][-1]) + " deaths by " + str(results[1]["Date"][-1]) + "."

    context = {
        'Title_String': title_str,
        'Total_Cases': scatter(results, 2, "Total_Cases", "Total Cases", "Total Cases in Iran"),
        'Total_Deaths': scatter(results, 4, "Total_Deaths", "Total Deaths", "Total Deaths in Iran")
    }

    return render(requests, 'home/welcome.html', context)


def italy(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.italy
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)

    db_data = db.italy_predictions
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)
    title_str = "In Italy, as of " + str(results[0]["Date"][-1]) + ", there have been " + str(
        results[0]["Total Cases"][-1]) + \
                " confirmed cases of COVID-19, including " + str(results[0]["Total Deaths"][-1]) + \
                " deaths. These numbers are predicted to be " + str(results[1]["Total Cases"][-1]) + " cases and " + \
                str(results[1]["Total Deaths"][-1]) + " deaths by " + str(results[1]["Date"][-1]) + "."

    context = {
        'Title_String': title_str,
        'Total_Cases': scatter(results, 2, "Total_Cases", "Total Cases", "Total Cases in Italy"),
        'Total_Deaths': scatter(results, 4, "Total_Deaths", "Total Deaths", "Total Deaths in Italy")
    }

    return render(requests, 'home/welcome.html', context)


def mexico(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.mexico
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)

    db_data = db.mexico_predictions
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)
    title_str = "In Mexico, as of " + str(results[0]["Date"][-1]) + ", there have been " + str(
        results[0]["Total Cases"][-1]) + \
                " confirmed cases of COVID-19, including " + str(results[0]["Total Deaths"][-1]) + \
                " deaths. These numbers are predicted to be " + str(results[1]["Total Cases"][-1]) + " cases and " + \
                str(results[1]["Total Deaths"][-1]) + " deaths by " + str(results[1]["Date"][-1]) + "."

    context = {
        'Title_String': title_str,
        'Total_Cases': scatter(results, 2, "Total_Cases", "Total Cases", "Total Cases in Mexico"),
        'Total_Deaths': scatter(results, 4, "Total_Deaths", "Total Deaths", "Total Deaths in Mexico")
    }

    return render(requests, 'home/welcome.html', context)


def philippines(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.philippines
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)

    db_data = db.philippines_predictions
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)
    title_str = "In Philippines, as of " + str(results[0]["Date"][-1]) + ", there have been " + str(
        results[0]["Total Cases"][-1]) + \
                " confirmed cases of COVID-19, including " + str(results[0]["Total Deaths"][-1]) + \
                " deaths. These numbers are predicted to be " + str(results[1]["Total Cases"][-1]) + " cases and " + \
                str(results[1]["Total Deaths"][-1]) + " deaths by " + str(results[1]["Date"][-1]) + "."

    context = {
        'Title_String': title_str,
        'Total_Cases': scatter(results, 2, "Total_Cases", "Total Cases", "Total Cases in Philippines"),
        'Total_Deaths': scatter(results, 4, "Total_Deaths", "Total Deaths", "Total Deaths in Philippines")
    }

    return render(requests, 'home/welcome.html', context)


def russia(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.russia
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)

    db_data = db.russia_predictions
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)
    title_str = "In Russia, as of " + str(results[0]["Date"][-1]) + ", there have been " + str(
        results[0]["Total Cases"][-1]) + \
                " confirmed cases of COVID-19, including " + str(results[0]["Total Deaths"][-1]) + \
                " deaths. These numbers are predicted to be " + str(results[1]["Total Cases"][-1]) + " cases and " + \
                str(results[1]["Total Deaths"][-1]) + " deaths by " + str(results[1]["Date"][-1]) + "."

    context = {
        'Title_String': title_str,
        'Total_Cases': scatter(results, 2, "Total_Cases", "Total Cases", "Total Cases in Russia"),
        'Total_Deaths': scatter(results, 4, "Total_Deaths", "Total Deaths", "Total Deaths in Russia")
    }

    return render(requests, 'home/welcome.html', context)


def south_africa(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.south_africa
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)

    db_data = db.south_africa_predictions
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)
    title_str = "In South Africa, as of " + str(results[0]["Date"][-1]) + ", there have been " + str(
        results[0]["Total Cases"][-1]) + \
                " confirmed cases of COVID-19, including " + str(results[0]["Total Deaths"][-1]) + \
                " deaths. These numbers are predicted to be " + str(results[1]["Total Cases"][-1]) + " cases and " + \
                str(results[1]["Total Deaths"][-1]) + " deaths by " + str(results[1]["Date"][-1]) + "."

    context = {
        'Title_String': title_str,
        'Total_Cases': scatter(results, 2, "Total_Cases", "Total Cases", "Total Cases in South Africa"),
        'Total_Deaths': scatter(results, 4, "Total_Deaths", "Total Deaths", "Total Deaths in South Africa")
    }

    return render(requests, 'home/welcome.html', context)


def spain(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.spain
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)

    db_data = db.spain_predictions
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)
    title_str = "In Spain, as of " + str(results[0]["Date"][-1]) + ", there have been " + str(
        results[0]["Total Cases"][-1]) + \
                " confirmed cases of COVID-19, including " + str(results[0]["Total Deaths"][-1]) + \
                " deaths. These numbers are predicted to be " + str(results[1]["Total Cases"][-1]) + " cases and " + \
                str(results[1]["Total Deaths"][-1]) + " deaths by " + str(results[1]["Date"][-1]) + "."

    context = {
        'Title_String': title_str,
        'Total_Cases': scatter(results, 2, "Total_Cases", "Total Cases", "Total Cases in Spain"),
        'Total_Deaths': scatter(results, 4, "Total_Deaths", "Total Deaths", "Total Deaths in Spain")
    }

    return render(requests, 'home/welcome.html', context)


def uk(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.uk
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)

    db_data = db.uk_predictions
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)
    title_str = "In UK, as of " + str(results[0]["Date"][-1]) + ", there have been " + str(
        results[0]["Total Cases"][-1]) + \
                " confirmed cases of COVID-19, including " + str(results[0]["Total Deaths"][-1]) + \
                " deaths. These numbers are predicted to be " + str(results[1]["Total Cases"][-1]) + " cases and " + \
                str(results[1]["Total Deaths"][-1]) + " deaths by " + str(results[1]["Date"][-1]) + "."

    context = {
        'Title_String': title_str,
        'Total_Cases': scatter(results, 2, "Total_Cases", "Total Cases", "Total Cases in United Kingdom"),
        'Total_Deaths': scatter(results, 4, "Total_Deaths", "Total Deaths", "Total Deaths in United Kingdom")
    }

    return render(requests, 'home/welcome.html', context)


def usa(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.usa
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)

    db_data = db.usa_predictions
    data_list = list(db_data.find())
    data_dict = {"Date": [],
                 "New Cases": [],
                 "Total Cases": [],
                 "New Deaths": [],
                 "Total Deaths": []}

    for i in data_list:
        data_dict["Date"].append(i["Date"])
        data_dict["New Cases"].append(i["New Cases"])
        data_dict["Total Cases"].append(i["Total Cases"])
        data_dict["New Deaths"].append(i["New Deaths"])
        data_dict["Total Deaths"].append(i["Total Deaths"])

    results.append(data_dict)
    title_str = "In USA, as of " + str(results[0]["Date"][-1]) + ", there have been " + str(
        results[0]["Total Cases"][-1]) + \
                " confirmed cases of COVID-19, including " + str(results[0]["Total Deaths"][-1]) + \
                " deaths. These numbers are predicted to be " + str(results[1]["Total Cases"][-1]) + " cases and " + \
                str(results[1]["Total Deaths"][-1]) + " deaths by " + str(results[1]["Date"][-1]) + "."

    context = {
        'Title_String': title_str,
        'Total_Cases': scatter(results, 2, "Total_Cases", "Total Cases", "Total Cases in the United States of America"),
        'Total_Deaths': scatter(results, 4, "Total_Deaths", "Total Deaths",
                                "Total Deaths in the United States of America")
    }

    return render(requests, 'home/welcome.html', context)


def world_table(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.world
    data_list = list(db_data.find())

    counter = 1
    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    db_data = db.world_predictions
    data_list = list(db_data.find())

    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    context = {
        'lines': results
    }

    return render(requests, 'home/data_tables.html', context)


def argentina_table(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.argentina
    data_list = list(db_data.find())

    counter = 1
    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    db_data = db.argentina_predictions
    data_list = list(db_data.find())

    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    context = {
        'lines': results
    }

    return render(requests, 'home/data_tables.html', context)


def australia_table(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.australia
    data_list = list(db_data.find())

    counter = 1
    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    db_data = db.australia_predictions
    data_list = list(db_data.find())

    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    context = {
        'lines': results
    }

    return render(requests, 'home/data_tables.html', context)


def brazil_table(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.brazil
    data_list = list(db_data.find())

    counter = 1
    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    db_data = db.argentina_predictions
    data_list = list(db_data.find())

    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    context = {
        'lines': results
    }

    return render(requests, 'home/data_tables.html', context)


def canada_table(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.canada
    data_list = list(db_data.find())

    counter = 1
    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    db_data = db.canada_predictions
    data_list = list(db_data.find())

    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    context = {
        'lines': results
    }

    return render(requests, 'home/data_tables.html', context)


def china_table(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.china
    data_list = list(db_data.find())

    counter = 1
    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    db_data = db.china_predictions
    data_list = list(db_data.find())

    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    context = {
        'lines': results
    }

    return render(requests, 'home/data_tables.html', context)


def germany_table(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.germany
    data_list = list(db_data.find())

    counter = 1
    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    db_data = db.germany_predictions
    data_list = list(db_data.find())

    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    context = {
        'lines': results
    }

    return render(requests, 'home/data_tables.html', context)


def india_table(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.india
    data_list = list(db_data.find())

    counter = 1
    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    db_data = db.india_predictions
    data_list = list(db_data.find())

    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    context = {
        'lines': results
    }

    return render(requests, 'home/data_tables.html', context)


def iran_table(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.iran
    data_list = list(db_data.find())

    counter = 1
    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    db_data = db.iran_predictions
    data_list = list(db_data.find())

    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    context = {
        'lines': results
    }

    return render(requests, 'home/data_tables.html', context)


def italy_table(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.italy
    data_list = list(db_data.find())

    counter = 1
    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    db_data = db.italy_predictions
    data_list = list(db_data.find())

    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    context = {
        'lines': results
    }

    return render(requests, 'home/data_tables.html', context)


def mexico_table(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.mexico
    data_list = list(db_data.find())

    counter = 1
    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    db_data = db.mexico_predictions
    data_list = list(db_data.find())

    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    context = {
        'lines': results
    }

    return render(requests, 'home/data_tables.html', context)


def philippines_table(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.philippines
    data_list = list(db_data.find())

    counter = 1
    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    db_data = db.philippines_predictions
    data_list = list(db_data.find())

    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    context = {
        'lines': results
    }

    return render(requests, 'home/data_tables.html', context)


def russia_table(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.russia
    data_list = list(db_data.find())

    counter = 1
    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    db_data = db.russia_predictions
    data_list = list(db_data.find())

    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    context = {
        'lines': results
    }

    return render(requests, 'home/data_tables.html', context)


def south_africa_table(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.south_africa
    data_list = list(db_data.find())

    counter = 1
    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    db_data = db.south_africa_predictions
    data_list = list(db_data.find())

    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    context = {
        'lines': results
    }

    return render(requests, 'home/data_tables.html', context)


def spain_table(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.spain
    data_list = list(db_data.find())

    counter = 1
    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    db_data = db.spian_predictions
    data_list = list(db_data.find())

    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    context = {
        'lines': results
    }

    return render(requests, 'home/data_tables.html', context)


def uk_table(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.uk
    data_list = list(db_data.find())

    counter = 1
    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    db_data = db.uk_predictions
    data_list = list(db_data.find())

    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    context = {
        'lines': results
    }

    return render(requests, 'home/data_tables.html', context)


def usa_table(requests):
    results = []
    client = MongoClient("mongodb+srv://user_1:USER_1@cluster0.0oqke.mongodb.net/<dbname>?retryWrites=true&w=majority")
    db = client.get_database('covid_db')
    db_data = db.usa
    data_list = list(db_data.find())

    counter = 1
    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    db_data = db.usa_predictions
    data_list = list(db_data.find())

    for i in data_list:
        temp = []
        temp.append(counter)
        temp.append(i["Date"])
        temp.append(i["New Cases"])
        temp.append(i["Total Cases"])
        temp.append(i["New Deaths"])
        temp.append(i["Total Deaths"])
        results.append(temp)
        counter += 1

    context = {
        'lines': results
    }

    return render(requests, 'home/data_tables.html', context)
