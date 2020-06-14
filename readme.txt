This program is meant to be used as a helper for investors when making decisions related to investments into cryptocurrencies. This program relies heavily on the current trends of cryptocurrencies and gives advice on whether to invest or withdraw cryptocurrencies into flat currency. The method used to measure whether the trend is going upwards or downwards is by instantaneous gradient as well as best line fit of the past 24 hours of data.


Dependencies:

Tkinter
ttk
time
tkMessageBox
tkSimpleDialog
matplotlib
numpy
datetime
bcrypt
gdax
os


Scikit-learn was not used due to the massive impact it had on user experience (loading times), and due to that, along with the volatile nature of cryptocurrencies, the scope at which the graph and data used in this program has been narrowed down to 1 week, and analysis was done using a modified version of OLS regression method.
This decision was taken with the compromise of data prediction accuracy in mind. But in the shorter term of 1 week, such difference in accuracies between the two data analysis approach are marginal compared to the impact of a painful UX.

Help page has eveything a new user would need to know about the program, it is located at the top menu bar in the Main window.


EDIT (5/7/2019): The GDAX API is no longer working as intended, most likely due to the API going deprecated with new API limits, and therefore, the program will crash during the first data fetch.

EDIT (9/9/2019): In case you still want to see the program in action, here is a 4-minute video I made back when I was actively working on it: https://www.youtube.com/watch?v=IRpYheLH-X4

EDIT (6/14/2020): V1.2.0a released. GDAX API issues have been addressed. More fixes underway.
