Dependencies:

Tkinter
ttk*
time*
tkMessageBox
tkSimpleDialog
matplotlib
numpy
datetime
bcrypt
gdax
os


Scikit-learn was not used due to the massive impact it had on user experience (loading times), and due to that, along with the volatile nature of cryptocurrencies, the scope at which the graph and data used in this program has been narrowed down to 1 week, and analysis was done using a modified version of Ordinary Least Square regression method.
This decision was taken with the compromise of data prediction accuracy in mind. But in the shorter term of 1 week, such difference in accuracies between the two data analysis approach are marginal and comes at the cost of painful user experience.

Help page has eveything a new user would need to know about the program, it is located at the top menu bar in the Main window.




*For V1.0.1, which features a Progressbar, but the loading screen's behaviour is a bit odd during refreshes. Check it out if you were curious and test with whatever you feel is better.