# Use an official Python
FROM resin/raspberrypi3-python

# Set workdit to /app
WORKDIR /rov

#copy current directoyr contents into app
ADD . /rov

# install any needed packages specified in requirements
RUN sudo ./scotty install --pi

# Make oirt 80 available to the outside world throught this container
EXPOSE 80

# Run app.py when container launches
CMD ["sudo","./scotty","run","--pi"]
