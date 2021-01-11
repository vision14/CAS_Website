# CAS_Website

**1. INTRODUCTION**

In the latter end of the year 2019, China discovered a disease rapidly spreading through one of its cities. However, within the span of two to three months, this disease took the whole world on its knees by infecting most of the major countries. Consequently, this forced the World Health Organization (WHO) to declare it as a pandemic. This disease is known as COVID-19 or coronavirus disease 19 which is a respiratory disease spread by &quot;Severe Acute Respiratory Syndrome Coronavirus 2&quot; or &quot;SARS-CoV-2&quot; [1]. Therefore, a lot of countries have suffered numerous casualties in the form of human resources as well as financially due to the direct impact of this virus. Due to these losses, various health experts are constantly working towards developing an effective vaccine to counter against this pandemic.

**2. PROBLEM STATEMENT**

Nowadays, many countries are struggling to fight against this virus due to the lack of guidelines and future outcomes of their measures. The reason behind this set back is that we lack the knowledge about this virus as nobody could have predicted its global impact. Hence, if we simply had some guidelines or a fortune teller to guide us what is going to happen next, we would have prepared more precisely than before. This simple future prediction might have saved thousands of lives lost during this battle. Thus, this report will talk about how we can use different techniques and tools of data science to create such an analytical system to predict how the measures taken today may impact the country in upcoming times.

**Category of the Problem:**

- University and research problem

**3. SOLUTION OVERVIEW**

Data Science and Machine Learning have performed eloquently in the field of finance and business to predict the future state of the company. Hence, we can use the same techniques to predict the future state of the country based on how that country has spared against the virus until now. The first step of solving this problem is to get data regarding case growth, death growth of different countries and store in a suitable format, so that, we can easily train a machine learning model using that data. Thus, this step can be achieved by web-scraping any website having a pool of COVID-19 cases from the start until now. One unique feature of this application is that it will web-scrape the necessary data each time a user visits the web application. This feature will allow the web application to update its database on a daily bases and hence we will always have an updated database. We will discuss the data extraction and storage portion of the project in an elaborated manner in the &quot;Data&quot; section as well as the &quot;Documentation&quot; section of this report.

After we have collected and stored the data, it is time to train a machine learning model. However, choosing a precise machine learning model to be trained on, is a very crucial step. Hence, after a thorough investigation of different machine learning models like ARMA model, ARIMA model and FbProphet model, I have concluded that, even though the data might look like continuous, we cannot use any regression model to predict the future outcome, as one of the crucial parameters in the data is &quot;time&quot;. Due to this factor, it is better to use a time series analysis algorithm, as these algorithms are known for their accuracy in predicting the outcomes when time is also involved in the data. Recently, ARIMA, also known as Auto-Regressive Integrated Moving Average has performed remarkably in predicting stock market prices and it performed remarkably in the tests as well. Therefore, this algorithm seemed like a suitable candidate for being trained on the COVID-19 dataset. The last step is to deploy this trained model onto a suitable platform. Moreover, as the whole project was developed using Python programming language, I decided that it will be better to deploy the final product on &quot;PythonAnywhere&quot; by developing a web application using the Django web framework.

**Components of the Project:**

- Web-scrapping real-time data from a website and storing it in a cloud-based database
- Training the ARIMA model on stored data and predicting the future outcomes
- Deploying the final results of the model on a Django based web application

**4. DATA**

The most important phase of any data science project is to define the right source of data, the technique to extract that data, and the way to store that data. In this project, I have collected my data from the World Health Organization&#39;s official website containing all the COVID-19 records until now [2]. They have systematically stored their data into a JSON file and then that data is being reflected on the COVID-19 section of their website. Hence, I decided to web-scrape that data using Python&#39;s &quot;requests&quot; and &quot;json&quot; packages. The JSON file contains an enormous amount of information in it. Furthermore, the script for retrieving the data runs every time a user will access the website, this will allow us to get the most updated data. Hence, the model is not static but rather a dynamic model, whose analysis gets updated every day. However, only the records of COVID-19 cases and deaths are needed for creating our analytical system. Thus, after web-scraping the JSON file, I have extracted all the necessary data to create the model and stored it into a JSON file as well as a CSV file on my local computer. Having said that, storing your data onto a local machine to create a data science application is not the ideal way to of executing the process.

Hence, the sole purpose of storing the data on a local machine is just for backup purposes. The actual data storage platform for our system is &quot;MongoDB Atlas&quot;. MongoDB Atlas is an open-source platform that allows you to create clusters on different cloud storage systems like AWS, Azure, and Google Cloud. The reason behind making MongoDB Atlas an intermediate agent between the cloud and my application is that, as my application is being developed in python. Consequently, it becomes a lengthy process to connect my python application with either AWS, Azure, or Google Cloud. Whereas, there is a package called &quot;pymongo&quot; which allows you to connect your Python application with your MongoDB Atlas cluster using two lines of code. For this project, I have created a cluster on MongoDB Atlas which stores all my data onto the AWS cloud [3]. Another reason behind choosing this platform is that, as the data provided by WHO&#39;s website is in JSON form, I cannot use a structured database system to store my data. Hence, I needed a cloud system that can easily store unstructured or NoSQL data. Additionally, it would be ideal to create different clusters for COVID-19 cases of different countries, so that, their data can be stored separately and hence can be accessed very easily. MongoDB gives me all the functionality I need for this project, that too in free of cost as well as with a lot of package support with python as well. Therefore, MongoDB Atlas has become the primary platform to store the data for this project. To summarize both of the above paragraphs:

- **Data Source:** WHO&#39;s COVID-19 website [2].
- **Accessing the data:** Web-scraping the data from the website using &quot;requests&quot; and &quot;json&quot; packages of python programming language.
- **Storage Platform:** MongoDB Atlas and Amazon Web Services (AWS).
- **Backup Data:** Local Machine; in the form of JSON file and CSV file.

**5. TOOLS**

The whole project is built using the Python programming language. Where the back-end is be performed using Spyder IDE and Jupyter notebook as they allow you to see the values of different variables at any point in development. Meanwhile, the Django application is built using PyCharm IDE as this platform allows you to easily create a server and debug the code. Additionally, there is an additional Jupyter notebook which contains literate programming of this project [3]. In other words, if someone wants to develop this project from scratch, then all the necessary steps, as well as the description of the code will be provided into the &quot;Documentation&quot; section.

The web-scraping is achieved by using &quot;requests&quot; as well as &quot;json&quot; packages of Python language. Whereas, the storage portion is handled by MongoDB Atlas and Amazon Web Services. Furthermore, for creating the model and training the model, I have used numpy, pandas, matplotlib, and statsmodels packages of Python language. At last, for building the web application, I used the Django web framework, HTML, CSS, BootStrap, and JavaScript as well. The deployment of the web application is done using a PythonAnywhere platform. To conclude:

- **Languages:** Python, HTML, CSS, JavaScript
- **IDE:** Spyder, PyCharm, Jupyter Notebook
- **Packages:** requests, json, datetime, pymongo, numpy, pandas, matplotlib, statsmodels
- **Web Framework:** Django
- **Database:** MongoDB Atlas
- **Cloud:** Amazon Web Services
- **Deployment:** PythonAnywhere

**6. DATA ANALYTICS LIFE CYCLE AND USER GUIDE FOR DATA ANALYSTS**

This project follows the guidelines of the Data Analytics Life Cycle. However, rather than being in a circular motion or a waterfall model motion, this project&#39;s life cycle will follow an &quot;Iterative model structure&quot; from software development models. The reason behind choosing an iterative model is that, in an iterative model, we first create a small prototype of our application and as we get more and more ideas about further implementation of the project, we can progressively add new features to our application. Hence, once it looks like the model and web application is ready, we can easily deploy it on the internet. The following two figures describe the Data Analytics Life Cycle as well as the Iterative Model.

**6.1 Discovery:**

As described in the &quot;Introduction&quot; section, the COVID-19 disease has spread its fear all around the world. Hence, all the countries had to face many adverse effects due to the virus. Consequently, it becomes necessary to develop different strategies to fight against it and eliminate it as soon as possible. This motivation led me to develop such a system that can predict the future outcome different countries, so that, different data analytics and medical experts can use those observations to use in the battle.

**6.2 Data Preparation:**

The data used in this project is extracted from the World Health Organization&#39;s website [2]. The reason behind selecting WHO&#39;s website is that, it is reliable and it gets updated every day. Additionally, web-scraping had been performed to retrieve the JSON data from the website and store it onto different tables of MongoDB Atlas collections. For that, I have created several tables for specific countries and dumped their data into the tables. After retrieving the data, it becomes necessary to pre-process it as well. As I have used time series analysis algorithm to train my model, it becomes necessary to have a data that has constant mean and constant standard deviation.

From the diagram, it can be inferred that, the data is increasing over time exponentially, where the range is between 0 to 120,000. Hence, the first step in the data-preprocessing becomes to normalize the data and keep it under a smaller range. This allows faster training and calculation of the model.

Now the data is centered around zero and the data is in a smaller rage from -1 to 1.5. However, when the data is analyzed closely, it can be seen that the local standard deviation of the data is not constant. This might result in a poorly trained time series model. Hence, the next step in data-preprocessing becomes, making the standard deviation constant. For that, we can calculate local mean of different blocks of data and divide the data with their corresponding mean.

The diagram states that, the standard deviation has become somewhat constant and mean has also become constant. However, the mean has shifted to 1 instead of 0. Having said that, the goal is to make the mean constant and centered around zero. Hence, we have achieved our final data pre-processing step. The code for applying data pre-processing and generating such graphs can be found on my GitHub repository [3].

**6.3 Model Planning**

The first step in the model planning is to identify different models and defining their parameters to train the data. For parameter tuning, I have performed three tests: Correlation test, ACF test and PACF test, on my data which can tune the parameter values needed for model training.

From all the tests, it can be concluded that, the given data does not concern a Moving Average model as the ACF graph is decreasing gradually over time. However, the PACF graph states that the data requires an Auto-Regression model with a lag between 5 to 7. Hence, the parameter for MA becomes zero and the parameter for AR become 1.

For creating a time series model, it is necessary to test the results on different models. For that, I had tested the processed data and calculated parameters onto three different time series algorithms which are: ARMA model, ARIMA model and FbProphet model. Additionally, for model evaluation, I have used the mean square error of the predicted data to calculate how much deviation each model has and then evaluate which model is best suited for my data.

From the observation, it can be stated that the FbProphet model has performed less accurately than the other two models, as the model takes the general pattern of the rise and plots a curve according to that. This phenomenon doesn&#39;t allow this model to capture smaller ups and downs in the data. Whereas, the ARMA and ARIMA model has performed remarkably well on the data set. However, ARIMA model over throws ARMA model to become the most accurate model out of all the three models. The reason behind this selection is that, the mean square error for ARIMA model is around 19576, whereas, the mean square error for ARMA model is around 32731. Hence, it can be concluded that, the ARIMA model is best suited for COVID-19 predictions.

**6.4 Model building:**

Now that the final model is described, it is time to train the model on different countries. For that, I have used ARIMA class from python&#39;s statsmodels package to create a model and train the model on different datasets. At first, the process retrieves the dataset for different countries from MongoDB Atlas and trains the model. After that, it predicts the total number of cases, new cases, total deaths and new deaths in all the countries and dumps the predicted data back onto the database.

**6.5 Communicate the Results:**

Now that the model is ready, it is time to integrate the model with the we application. I have developed the web application using Python&#39;s Django framework which uses python as its back-end and Html-CSS-JavaScript for the front-end. For developing the front-end of the web-application, I have used Start Bootstrap&#39;s admin template which allows you to design your web-app in a fancy way [5]. The last step of integration is to put the model prediction module into Django&#39;s views module, so that, each time a user visits the website, the model can retrieve the predictions and display updated values.

**6.6 Operationalize:**

The last step of the data analytics life cycle of this project is to deploy the website on the internet. For that I have used &quot;PythonAnywhere&quot; server and domain to deploy my website. The website can be visited by typing the following URL in a browser:

[http://cas19.pythonanywhere.com/](http://cas19.pythonanywhere.com/)

One thing to note here is that, the website is specifically designed for desktop use only. Hence, if the website is opened on a tablet or a cell-phone, it might not show the desired style and layouts on those devices.

**7. DOCUMENTATION AND SETUP**

**7.1 User Guide:**

Following are the steps for users to access my website and browse through different modules of it:

- Write down the following website on a desktop browser:

[http://cas19.pythonanywhere.com/](http://cas19.pythonanywhere.com/)

- The home page has two graphs for total number of cases and total number of deaths in the globe.
- The blue dots state the confirmed COVID-19 cases and deaths for a particular country, whereas, the red dots define the predictions made by the ARIMA model for one month in the future. Additionally, the gray colored cone shape defines the error-band the model. Meaning that the curve might go that much up or down.
- Hover the mouse cursor over the datapoints depicted in the charts for displaying more details about a particular day. That includes, total number of cases, new case, total number of deaths and new deaths for that particular day.
- Use the magnifying glass tool at the left corner of the graph to zoom into the graphs to get the details of a particular week or a month.
- To check the prediction about other countries, select the &quot;Countries&quot; option from the sidebar which is located at the left side of the screen. Click on the desired country and the website will take you to a page containing the data of that particular country.
- If you wish to see the tabular data of different countries rather than a graph, click on the &quot;Tables&quot; option from the sidebar and select your desired country to navigate to its tabular data page.

**7.2 Development and Setup:**

For developers and data scientists, here I am defining the steps needed to develop such a system from scratch:

- Install Python programming language IDE with any version after 3.5 from its official website.
- After installing the python language, install the following dependencies from the terminal by writing the script:
  - pip install requests
  - pip install django
  - pip install dnspython
  - pip install pymongo
  - pip install numpy
  - pip install pandas
  - pip install matplotlib
  - pip install mpld3
  - pip install statsmodels
  - pip install jupyter
- After installing all the dependencies, retrieve the required data from World Health Organization&#39;s website using requests package and store the retrieved data onto MongoDB Atlas using pymongo package as defined in the notebook [3].
- Perform data pre-processing methods like normalization, differentials and division by local mean to make the data more precise for model training using pandas and numpy packages as described in the notebook [3].
- Calculate the parameters needed to train the model by performing correlation test, ACF test and PACF test using statsmodels package [3].
- Train the ARIMA model from statsmodels package using the processed data and derived parameters. The default parameters for the model should be AR=5, D=1 and MA=0.
- Test the model by applying mean squared error on the test results to evaluate the accuracy of the model. If the results are not as expected, change the model parameters one by one to fine tune the model until the desired output is generated.
- After the model is ready, plot the predicted results using matplotlib and mpld3 packages to generate more interactive graphs.
- Integrate the graphs and model to a Django based web application to get updated data each time a user visits the web application [6].
- Finally, deploy the developed web application using &quot;PythonAnywhere&quot; hosting to make the website online.

**REFERENCES**

[1] Coronavirus disease 2019 (COVID-19) - Symptoms and causes. (2020). Retrieved 19 August 2020, from [https://www.mayoclinic.org/diseases-conditions/coronavirus/symptoms-causes/syc-20479963](https://www.mayoclinic.org/diseases-conditions/coronavirus/symptoms-causes/syc-20479963)

[2] Canada: WHO Coronavirus Disease (COVID-19) Dashboard. (2020). Retrieved 19 August 2020, from [https://covid19.who.int/region/amro/country/ca](https://covid19.who.int/region/amro/country/ca)

[3] Vyas, P. (2020). vision14/CAS\_Preprocessing. Retrieved 19 August 2020, from [https://github.com/vision14/CAS\_Preprocessing](https://github.com/vision14/CAS_Preprocessing)

[4] Powell-Morse, A. (2020). Iterative Model: What Is It And When Should You Use It?. Retrieved 19 August 2020, from [https://airbrake.io/blog/sdlc/iterative-model#:~:text=The%20iterative%20model%20is%20a,the%20final%20system%20is%20complete](https://airbrake.io/blog/sdlc/iterative-model#:~:text=The%20iterative%20model%20is%20a,the%20final%20system%20is%20complete)

[5] Bootstrap, S. (2020). SB Admin 2 - Free Bootstrap Admin Theme. Retrieved 19 August 2020, from [https://startbootstrap.com/themes/sb-admin-2/](https://startbootstrap.com/themes/sb-admin-2/)

[6] Vyas, P. (2020). vision14/CAS\_Website. Retrieved 19 August 2020, from [https://github.com/vision14/CAS\_Website](https://github.com/vision14/CAS_Website)
