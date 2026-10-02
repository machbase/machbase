---
title: Robot Motion Simulation
type: docs
weight: 489
---

Install and run a robot motion app from the Machbase Neo console to replay a public dataset in 3D.

{{< youtube F2Sgs0hPy3c >}}

This demo runs a robot motion app in the Machbase Neo console and replays a public dataset of a KUKA collaborative robot in 3D.

The workflow takes four commands in the JSH terminal: clone the repository, create a table, load the data, and register and start the service. The running app opens directly in a browser.

The dataset contains tasks performed by a person physically guiding the robot arm. Its source and license are listed on the app's DATA SOURCE card. Choose a participant and task to replay the recorded motion at its original speed. You can adjust the range and playback speed on the timeline, inspect all seven joint angles in real time, and save poses and motions you create yourself.

No Node.js installation or separate frontend build is required. See how to run the app, from data ingestion to the 3D view, using only the Machbase Neo executable.