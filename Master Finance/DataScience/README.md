Data Science Coursework : A Staggered DiD Model on Policy Rates; Sept-Dec 2022
# More
This was based on the recent papers published by Brent Callaway, Andrew Goodman-Bacon and Pedro
H.C. Sant’Anna (2021) in “Differences-in-Differences with a Continuous Treatment” as well as 
Callaway and Sant’Anna, “Difference-in-Differences with multiple periods” (2021). The author of this paper have proposed a R package that lets you easily
implement this type of models (see: https://cran.r-project.org/web/packages/did/vignettes/did-basics.html) which I Highly reccomend. But to have more control
over our Model, we decided to work on our own package using Python. The entire code is avalaible in this section.

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
