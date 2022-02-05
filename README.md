# Dissertation-on-Data-science
Analysing relevant metrics and improvement methods to address data quality issues in the field of Oil and gas.


In the final year of my undergraduate degree, I had completed a dissertation on data science
at the University of Aberdeen. It was a research conducted by myself with occasional
meetings with my supervisor for guidance. I spent four months on this dissertation and the
submission was a written essay (20,000 words) accompanied by code. The software
component of the dissertation was implemented entirely in Python.

The aim of the dissertation was to analyze relevant improvement methods as well as
metrics used to address data quality issues in the field of Oil&gas. I was given data from a
local Oil&gas company by my supervisor. The data contained a lot of gaps and noise which
needed to be measured and improved/cleaned. I begin my project by researching the data
quality framework which helped me understand what stages the data goes through from the
point it is acquired to the point it in improved. I then narrowed my focus to the two main
components of this process: measuring data quality and improving data quality.

To measure the quality of data, four quality dimensions relevant to the oil&gas company
were looked at; Accuracy, precision, completeness and consistency. I implemented various
metrics for each dimension. Some of these metrics were pre-exisitng and adapted from
research papers. While others were my own inventions that I implemented using my own
knowledge and ideas. Upon passing a data set as input to each of these metrics, a % was
outputted to address the quality of data for that dimension. For example, passing data set A
to a metric that measures accuracy would output something like: Data set A is 89%
accurate. The reason I implemented these metrics is because I believe measuring data
quality is a very important step. This is because if the data quality exceeds a pre-defined
threshold, then cleaning would not be required and hence, that would save a lot of time.

After measuring data quality, I implemented some improvement methods to address data
quality issues: Noise, gaps and outliers. I implemented several improvement methods for
each of these issues using different techniques (ex: KNN, clustering, ARMA etc..) tailored to
the data in use. The aim of this was to clean/improve the quality of the data identified as
‘ dirty ’ data from the previous step. All of this knowledge was acquired purely though
research.

After implementing the metrics and improvement methods, I started analyzing which
improvement method is best to use (for the given quality issue) depending on the context in
which it is used. I explored different scenarios/patterns that the data could be in and
proposed which improvement methods are ideal to use in each case to achieve best results.

Due to the tremendous amount of research carried out for the dissertation, I’ve acquired a
substantial amount of knowledge in the field of data science. I ’ ve gained an in-depth
understanding of the data quality framework and all of its components along with different
tools and techniques used for each. Furthermore, this dissertation might also be published
in the future.in collaboration with my supervisor
