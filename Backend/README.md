# Solaro.

## Inspiration
Imagine you’re a prospective homeowner and you want to have an impact on the environment by installing solar panels. This is a big step, which takes a lot of research at times. You’ll want to know the potential efficiency, the type of technology most suitable, and whether the city you’re buying your new house is a hotspot for solar energy. It’s a daunting task and a roadblock for many wanting to install panels. With Solaro, we created an application that can guide you through the process by virtually analyzing your roof.

## What it does
Based on your houses position on Google Maps, our application analyzes your home to see you how much of an impact solar panels can do to your home. Alongside this, we find the overall solar radiation in your region, to detect how much sunlight you are getting. We use machine learning to detect the type of roof, and then calculate an estimated surface area. From this, we make a rough estimate on the number of solar panels your house can use and calculate the initial costs for installation, and the ling term savings of using solar panels.


## How I built it
Our program has three major components: The Frontend Website, the Backend API, and the Machine Learning Framework.

On the Frontend side, we used the Google Maps Javascript API, and a public dataset outlining solar radiation levels in certain regions around Ontario, Canada. Using this API and Dataset we displayed a User Interface to allow users to survey their home.


On the Machine Learning side, we created a machine learning model to identify the type of roof on a house, given its satellite image. The model works with some helper functions to calculate the roof type, shape, and size to determine a usable surface area.


From here we crunched some numbers and provided calculated information about solar energy benefits for specific homes.



## Technical Stack
 The Frontend Service is a static webpage that displays the main dashboard for user interaction. It uses the following technologies:
* Github Pages
* HTML, CSS, Javascript
* SemanticUI
* Chart JS
* Google Maps JS
* Google Places

The Backend Service works as an API that serves as middle-man between the Frontend and the Machine Learning Functions. It uses the following technologies:
* Heroku
* Python
* Flask
* Google Maps Static API
* Google Cloud Vision API


The Machine Learning Framework takes in world coordinates to efficiently determine the houses Roof Data: It uses the following technologies:
* Google Cloud AutoML
* Google Cloud TPU Engine
* Google Cloud Compute Engine
* Google Cloud Storage


## Challenges I ran into
Challenges we ran into include:
* Converting OSM blocks to GeoJSON Data
* Training a model that has an accuracy high enough to make correct predictions.
* Setting Up Google App Engine did not work, so we ended up using Heroku

## Future Plans & Scalability
With Solaro, we envision a seamless process for homeowners and property owners wanting to install solar panels on their property. We want to provide property owners information on how solar panels can make a positive impact to their home and their neighborhood, by using renewable sources of energy. To further scale our operations, we want to directly partner with trusted contractors and solar panel companies across Canada, giving Solaro users a trusted source for their solar panel needs. By guiding Canadians from start to end in the solar panel installation process, we aim to make this beneficial technology accessible to everyone, ultimately decreasing carbon emissions, and increasing .
