# Dependencies
## Graphviz
Parts of this project use Graphviz, a package of open-source tools initiated by AT&T Labs Research for drawing graphs 
specified in DOT language scripts, in order to visualize data. This will need to be installed to run all functionality.
### Installation
#### Linux
Run the following command:  
sudo apt-get install python3-dev graphviz libgraphviz-dev pkg-config
 
## Python
Currently, this project uses Python 3.6. It is recommended a virtual environment is set up. Currently, all needed 
packages outside of the default Python 3.6 are listed in src/reddit_live_api/requirements.txt  

Install all necessary packages using the following command:  
pip install -r src/reddit_live_api/requirements.txt  
  
Note that this should occur after all other dependencies are installed.
