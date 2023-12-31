# Creating a Highly Scalable Django Application on ECS

## Description

Learning an instrument can be difficult, but as someone who has played musical instruments for a significant part of his life I can say that one single thing has helped me drastically: practicing consistently for short sessions. Practicing for 15-20 minute sessions 3 times a week has remarkably better results than one big session once every 1-2 weeks, and it's much easier to fit in your own schedule. For this reason, I always track my practices in my favorite instrument, the drums, to keep myself motivated and visualize my progress.

Using the Django framework, I've built an application to keep track of my practices, leveraging AWS infrastructure to make this application cost-effective and highly available. This application runs on ECS Fargate containers, and uses an RDS database as its data store. Users can log in to this application to save information on their drumming exercises and sessions, which they can later view in their session history or on their personal dashboard.

The Django application itself is built using a Python Slim image on Fargate, minimizing its weight and making it scalable and easier to maintain. Along the Django app, an Nginx proxy is also running to serve static files. The application is backed by an RDS instance storing user practice data as well as user account data, which is managed with Django's built-in functions. Lastly, the user's dashboard uses a mix of Pandas and Matplotlib to process practice data into informative visuals. The infrastructure running the application uses low-cost, highly available NAT instances and Route53 with ACM to provide a domain with secure data transport. 
