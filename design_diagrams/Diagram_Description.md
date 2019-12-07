# Diagram Description: OSCAR (Open Social Clustering and Analysis for Reddit)

## How To View The Diagrams
The following is a description of the different compontents found within the diagrams and how they should be interpreted:
* Stick figure - This represents the user
* Vertical, rounded rectangle - This represents a process layer for OSCAR
* Horizontal, sharp rectange - A single step of computation
* Solid arrow - Indicates flow of data
* Dotted line - Indicates a grouping and breadown of steps
* Cylinder - Database

## User Interface Layer
This layer defines how the user will interact with OSCAR.
### Input
The user will be presented with an Angular UI with input fields for a Reddit username or subreddit to perform an analysis on. This allows the user to direct OSCAR on what to analyze.
### Output
The user will be presented with the following visualizations:
* Clustering results
* Social graph analysis results
* User/Subreddit summary statistics
* Recommendations
  
These visualizations should help inform the user about Reddit users and communities.

## Data Visualization Layer
This layer describes the process of taking the results of our algorithms and generating visualizations. Currently, this will be done with libraries like ChartJS. 

## Data Processing Layer
This layer describes what types of algorithms will be run on the acquired data. One can see what sort of conclusions can be made based on these algorithms. The following types of analysis will be performed:
* Clustering 
* Social graph  
* User/Subreddit summary 
* Recommendations

## Data Collection Layer
This layer describes the process for which OSCAR acquires and stores Reddit data. The first method is through downloading historical Reddit data from BigQuery. The second method is used to supplement the historical Reddit data with live Reddit data. This is down through a Python-based Reddit Live API that has access to the following:
* User submission data
* User comment data
* User voting data
* Recent subreddit activity
* Popular subreddit activity 
* Controversial subreddit activity

All of this data is stored in a PostgreSQL database. 