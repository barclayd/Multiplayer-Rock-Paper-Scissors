# Online Multiplayer Rock Paper Scissors

Online Multiplayer Rock Paper Scissors game connected to a Linux server. Built using Python

### Demo

##### One client connected and ready to play, One client open 

<p align="center">
  <img alt="Waiting to connect and launch screen" src='https://user-images.githubusercontent.com/39765499/56475369-16f09300-647f-11e9-883b-d9ca04962d82.png'>
</p>

##### One client has made a move, other client is yet to move  

<p align="center">
  <img alt="One client has made a move, waiting for the other client" src='https://user-images.githubusercontent.com/39765499/56475365-10621b80-647f-11e9-87c6-a4656b21f178.png'>
</p>

##### Both players have made a move  

<p align="center">
  <img alt="Both players have made their move" src='https://user-images.githubusercontent.com/39765499/56475367-13f5a280-647f-11e9-8ae2-7a0fb69735bf.png'>
</p>

### Features

* Scalable game - allows for multiple client games running simultaneously
* GUI
* Use of secure, shared server to facilitate game play

### How to Run

**How to Run the Server**

```
$ git clone https://github.com/barclayd/Multiplayer-Rock-Paper-Scissors.git
$ cd Multiplayer-Rock-Paper-Scissors
$ python server.py
```

Open ``settings.py`` and change the IP to the network IP of the device running the server and change the PORT number to any open port as desired such as ``ip = <Your Local Network IP address>`` and ``port = <CHOSEN PORT NUMBER>``.

**How to Run the Client**

Run infinte instances of the terminal - 2 clients have to open and connected to start a game

```
$ python client.py
```

### Future Improvements:

* Use of images
* Save of high scores
