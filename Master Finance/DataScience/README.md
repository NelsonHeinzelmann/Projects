# Title
Data Science Coursework: Policy Rates Staggered DiD Model
Sept-Dec 2022

# Overview
In this coursework, my group and I implemented a Staggered Differences-in-Differences (DiD) model on policy rates. This project was inspired by recent papers published by Brent Callaway, Andrew Goodman-Bacon, and Pedro H.C. Sant’Anna (2021) on "Differences-in-Differences with a Continuous Treatment" and Callaway and Sant’Anna on "Difference-in-Differences with multiple periods" (2021). To implement this type of model, you can utilize the R package proposed by the authors, which facilitates the implementation of such models (see: https://cran.r-project.org/web/packages/did/vignettes/did-basics.html). However, for greater control over the model, we decided to develop our own Python version. The entire code for this project is available in this section.
Note that I only added the code used for our case study, but not the Data we used therefore the Notebook only serves as an outline of the work done and cannot be run as such. This work has been very well received by the professors as it has been awarded a perfect grade.
# Abstract:
For the first time since 2008, we are facing a continuous increase in prices and
observing relatively sharp inflation. Many studies show that the optimal policy
response to rising inflation is to increase interest rates. Indeed, many central banks
have decided to adopt this strategy. These recent events have therefore aroused our
curiosity and motivated us to study the impact of such decisions. In this paper, we
will attempt to explain how exchange rates behave when a country decides to
increase its interest rates through the case of the Global Financial Crisis and the
years that followed. To achieve this, we will calculate the average treatment effect of
the interest rate change on a country’s exchange rate. The model used is a staggered
diff-in-diff using a Two-way Fixed effect to account for the country and the reaction
speed.
The findings show that an increase in interest rates results in an appreciation of the
currency in the short term. A second implication is that the speed at which banks
react would seem to have a positive impact on the purchasing power of a currency.
Pushing our research further might lead to a better understanding of a country’s
international influence that its exchange rate has following its national policy rate
changes.
