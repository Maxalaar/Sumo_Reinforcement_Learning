# Conda Environment Setup

To set up the required environment for this project, follow these steps:

1. **Create a Conda Environment:**
```bash
conda create --name Sumo_Reinforcement_Learning
```

2. **Activate the Environment**:
```bash
conda activate Sumo_Reinforcement_Learning
```

3. **Packages:**

Install linux packages:
```bash
sudo add-apt-repository ppa:sumo/stable
sudo apt-get update
sudo apt-get install sumo sumo-tools sumo-doc
```

Install python packages:
```bash
pip install libsumo gymnasium sumolib traci numpy
```


4. **Set Environment Variables:**

Move to project directory :

```bash
cd .../Sumo_Reinforcement_Learning
```

Get the `SUMO_HOME` path:
```bash
which sumo-gui
```

After activating the environment, set the PYTHONPATH variable to the current directory:
```bash
export SUMO_HOME="/usr/bin/sumo-gui"
export PYTHONPATH="$SUMO_HOME/tools:$PYTHONPATH"
conda env config vars set PYTHONPATH='.'
conda activate
conda activate Sumo_Reinforcement_Learning
```

# Remove Conda Environment

```bash
conda remove -n Sumo_Reinforcement_Learning --all
```
