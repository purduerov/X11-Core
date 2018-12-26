# ROV Test Setup A.K.A Aberdeen

  What is Aberdeen? It is the catch all name for the hardware setup in the IEEE server, the Jenkins Continuous Integration Server on Leyden and the Slack notification channel. I will now go into details about how it is set up, and how to make unit tests to be run. You can skip the system section if you just want to make a test.

## The System

  So you are Johnny Coder, and you made some changes that are on some branch. Thanks Man! It all starts with making a pull request. When you do that, some settings that people with admin powers set fires off a Webhook (It's just an HTTP POST request with all the data needed) to the IEEE server. The IEEE server is hosting a Jenkins Server, which recives the webhook and uses it to launch a job. The specifications of the job are in X11-Core/Jenkinsfile, and basically it says "prepare the server environment, build the rov software in a docker image, lint the software, build the frontend, run some unit tests, and then tell slack + github that everything is all good". If something is not good, it instead tells slack and github that everything is not good. It has a hardware setup connected to an ethernet port as well to run the rov (you can access it by looking into the server in the IEEE office), which people can use to test with an raspberry pi account. That's about it.
## Ok, but how do I make a test?
First, understand that the version of tests that are run are on the development branch. Testing works at the ROS level, uses pythons unittest module, and decouples from hardware with the mock sensor classes. The relevant files are X11-Core/tests/rovtests.py,tests/rovtest.py, and tests/rovcontroller.py.

So, lets say you got a new sensor that talks over can, that we want to integrate into the rov, and you have written a rosnode that communicates to the can controller. Now you want to make a test for it. Heres what to do.

1. Launch your rosnode, with your implementation, and do a `rosbag record` of the output of the CAN controller. Save it into a bag, which you will want to save with your sensor class.

2. Implement a mock sensor class for your sensor instance, which gets called if the ROV can't detect the hardware, which plays your rosbag. It is called by the import statement, an example can be found at X11-Core/rov/sensors/pressure/__init__.py.

3. Now for the unit tests. You make rovtests by implementing a class in X11-Core/tests/rovtests.py, and then explicitly calling it in X11-Core/tests/testem.py, by importing it. Each function in the test class is called in order, and each class itself has a full setup and teardown, specified in the X11-Core/tests/rovtest.py. You can also explicitly send dearflasks down with the calls to self.rovI.

You can find more details about the unittest module here

https://docs.python.org/2/library/unittest.html

## Final Notes
Some hitches that Aberdeen needs worked out. One, rosfront, whatever it turns out to be, and how its implemented, needs to be spun up in the prep environment. Also, note that this setup doesn't test the proper messages are being sent to the CAN node, the idea being that if you implemented the node, and were able to record a rosbag, then cannode down to hardware will work. While one could imagine responsive test benches where the proper responses are prepared so that the nodes meets those requirements, I think the work that would require would be unfeasible.

## Why is it named Aberdeen anyways?

Aberdeen Proving Ground is the United States oldest testing facility for military equipment, founded soon after our entry into the Great War in 1917

https://en.wikipedia.org/wiki/Aberdeen_Proving_Ground
