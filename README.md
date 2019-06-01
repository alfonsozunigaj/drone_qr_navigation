# Drone QR Navigation
## Environment setup

Assuming you already have [Anaconda](https://www.anaconda.com/distribution/) installed on your computer, follow this instructions to set up the virtual environment for the project. Open the command prompt and navigate to the project's directory. Then, run the following commands:
```
conda create -n drone python=3.6
conda activate drone
pip install -r requirements.txt
```
Here we have created a virtual python environment called "drone", where we've installed all the required libraries needed for the project to run.

---

## Instructions file

Edit the "instructions.csv" file located in InputFileManager to specify the instructions that the drone should execute when reading a specific QR code. The format of each row inside the file is:
```
qr_letter_index,dx,dy,dz,dradians
```
where qr_letter_index is a single capital letter, and the following four elements should be integers. For more information on how this data will be used, read about the **move_relative** function [here](https://pyparrot.readthedocs.io/en/latest/bebopcommands.html#flying).


