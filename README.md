# Bus-Pedia
## 0. Environment setup
Please see the readme of each sub folder.
## 1. Introduction
Project Slides: [Click here](https://docs.google.com/presentation/d/1-u91-LjLQ5AKjXK2u0C_ptJ3Dxi05Ltw2ljXOGpBAI0/edit#slide=id.g62b6dc40be_0_54)

Based on a survey from UC Berkeley, the top 3 reasons that people give up public transportations are related to not access to bus arrival information. A typical case is that, there are two nearby stops both having routes to your destination. If you know the bus arrival information for the bus stop you are at as well as nearby stops, you can arrange your trip more easily.

In this project, I build a streaming pipeline to provide transparency of bus arrival information for passengers, which will help to rebuild their confidence on public transportations.

## 2. Data
Historical bus GTFS data for NYC: [http://web.mta.info/developers/MTA-Bus-Time-historical-data.html](http://web.mta.info/developers/MTA-Bus-Time-historical-data.html)

Bus schedule and stop information: [https://transitfeeds.com/p/mta](https://transitfeeds.com/p/mta)

## 3. Pipeline

![Image description](https://github.com/shellzhou2013/When-Next-Bus-Coming/blob/master/images/pipeline.png)

## 4. Engineering challenge
In the spark streaming job, we need to write records to database. If we create a connection to database for each record, it will be very slow. Here it gives the latency for my streaming jobs by using foreachrdd method to create connection to database at normal ingestion rate and 10 x ingestion rate (note my microbatch is 1 sec):
![Image description](https://github.com/shellzhou2013/When-Next-Bus-Coming/blob/master/images/foreachrdd_normal.png)
![Image description](https://github.com/shellzhou2013/When-Next-Bus-Coming/blob/master/images/foreachrdd_10x.png)
With 10 x ingestion rate (only < 300 records/sec), the job crashes because it's not able to finish it in 1 sec.

To solve this problem, instead of using foreachrdd, I used a foreach partiton method. In this case, only one connection to the database is created for each microbatch at each partition. The performance is shown below:
![Image description](https://github.com/shellzhou2013/When-Next-Bus-Coming/blob/master/images/foreachpartition_normal.png)
![Image description](https://github.com/shellzhou2013/When-Next-Bus-Coming/blob/master/images/foreachpartition_10x.png)
![Image description](https://github.com/shellzhou2013/When-Next-Bus-Coming/blob/master/images/foreachpartition_50x.png)
The latency is 80 ms vs 180 ms with foreachrdd. When with a 50 x ingestion rate, which is ~1300 records/sec, it reaches to ~200 ms, but the streaming job still works well.
## 5. Web UI
This is my web UI run at my domain: [http://www.kafkastreampipeline.xyz/](http://www.kafkastreampipeline.xyz/)
![Image description](https://github.com/shellzhou2013/When-Next-Bus-Coming/blob/master/images/demo_screenshot.png)
