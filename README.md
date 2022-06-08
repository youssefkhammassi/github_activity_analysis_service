# GITHUB ACTIVITY ANALYSIS SERVICE

This service is used to analyze the GitHub activity of a repository.
In This service, we use the GitHub API to get the activity of a repository.
We extract the activity of the repository, handle it then we send it to the frontend in order to display it.

![C4 Model](https://imgur.com/wBO3lRZ.png)

## We implemented the following features:
 - get the activity of a repository and group it by event type
 - get the PullEvent activity of a repository and calculate the average duration of between two PullRequestEvent
 - Send Visualization data to the frontend in order to display:
   - Count of each event per day
## Main implemented design principles & patterns:
 - Code patterns: 
    - Services 
    - Api Data 
    - models 
 - Dependency Injection and Inversion
 - Object Oriented Programming 
 - Reliability, TDD
 - Authorization Handling: the user must be logged in to access the service 
 - Customized errors
## What can be improved:
 - integrate a mongoDB database to store the raw data also to be able to retrieve it later for analysis.
 - add a feature to get the activity of a repository from a specific date to a specific date.
 - Integrate a Publishing/Subscribe pattern (e.g: Kafka) to get the activity of a repository live as webhook  Kafka events