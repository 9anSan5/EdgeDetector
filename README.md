# EdgeDetector 
A framework to analyze all steps performed by most common EdgeDetector algorithms and check performance through a benchmark.

## Algorithms

The algorithms that are implemented in this framework are:
- Roberts Cross EdgeDetector (SingleFase);
- Sobel EdgeDetector (SingleFase);
- Prewitt EdgeDetector (SingleFase);
- Canny EdgeDetector (MultiFase - support for all of the precedent operators);
- MarrHildret EdgeDetector (Laplacian).

## Metrics

The metrics used to evaluate benchmark results are:
- Pratt's Figure of Merit;
- Mean Absolute Square;
- Map Quality.

## Getting Started

The module is completely written in python. All you need to do is just to clone the repository and run python scripts, according to the following instructions.

### Prerequisites
#### Python 3.x 
Python >=3 (tested 3.9) recommended and matches the development environment of this module. There may be backwards compatibility with Python 2.7 but it isn't tested because it is deprecated.
##### Installation on APT based linux distribution
```
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3
```
##### Installation on YUM/DNF based linux distribution
```
sudo yum update
sudo yum install python3
```
#### pip
When Python is installed, its package manager pip should be available. If you do not have pip:
##### Installation on APT based linux distribution
```
sudo apt install -y python3-pip
```
##### Installation on YUM/DNF based linux distribution
```
sudo yum install python3-pip
```
#### virtualenv
It is not mandatory but strongly suggested to use a virtual environment to contain the software and deal with dependencies in an isolated way:
##### Installation on APT based linux distribution
```
sudo apt install python3-venv
```
##### Installation on YUM/DNF based linux distribution
```
sudo yum install python3-virtualenv
```
### Installation
If all the dependencies are satisfied, it's time to get a development environment running.
Download the repo:
```
git clone https://github.com/9anSan5/EdgeDetector.git
```
Move to the repository directory
```
cd EdgeDetector
```
Run the virtual environment and install the python requirements:
```
python3 -m venv test_venv
source ./test_venv/bin/activate
pip3 install -r requirements.txt
```
Now the virtual environment is set up and you can run the module and the tests. Then you can exit the virtual environment:
```
deactivate
```
## Visualize Steps for each algorithm

Cloning the repo, you get a file named "Steps.py", inside the "src" folder. This is a launcher that creates a large number of result images, one for each image and algorithm.
Each result images shows each step that the algorithm performs on the original image and a blurred image (No MarrHildret).

### Configuration

In order to configure the execution of the launcher, you have to open Steps.py file with a text editor and edit ONLY these parts (CONFIGURE ME section):
```
############################## CONFIGURE ME #############################
#########################################################################
FilterSIGMA = 1.6                                                       #
FilterDIM = 3*FilterSIGMA                                               #
                                                                        #
directory = 'Steps_Images/'                                             #
result_dir = 'Steps_Result/'                                            #
SINGLE_FASE = ["RobertsCross", "Sobel", "Prewitt"]                      #
MULTI_FASE = { "Canny": ["RobertsCross", "Sobel", "Prewitt"] }          #
ZERO_CROSS = ["MarrHildret"]                                            #
                                                                        #
single_threshold = 100                                                  #    
double_threshold = [0.05, 0.25]                                          #
zeroCrossing_threshold = 0.98                                           #
#########################################################################   
```
The framework came preconfigured to run RobertsCross, Sobel and Prewitt as single-phase detector, to run Canny with all operators as multi-phase detector and to run MarrHildret as zero-crossing detector.

It will use "100" as threshold for single-phase detectors, "0.05" and "0.25" as low and high threshold ratio for multi-phase detectors and "0.98" as threshold ratio for zero-crossing detectors.

To apply a sharpening filter and generate a LaplacianOfGaussian filter it will use a (5 x 5) Gaussian mask with "1.6" standard deviation.

The default folder that contains some images to use with these algorithms is "Steps_Images". The results will be saved in "Steps_Result" directory.

The "Steps_Images" folder includes some images representing some actors that I consider useful to understand how the algorithms work.

### Run
```
python src/Steps.py
```


## Benchmark

Cloning the repo, you get also a file named "Benchmark.py", inside the "src" folder. This is a launcher that performs a benchmark of configured edge detectors on selected images.

The output of each algorithm is compared with the provided ground truth and the information about performances are provided through the metrics described before.

### Configuration

To configure the execution of the launcher, you have to open Steps.py file with a text editor and edit ONLY these parts (CONFIGURE ME section):
```
############################## CONFIGURE ME #############################
#########################################################################
FilterSIGMA = 2.3                                                       #
FilterDIM = 3*FilterSIGMA                                               #
                                                                        #
directory = 'Steps_Images/'                                             #
result_dir = 'Steps_Result/'                                            #
SINGLE_FASE = ["RobertsCross", "Sobel", "Prewitt"]                      #
MULTI_FASE = { "Canny": ["RobertsCross", "Sobel", "Prewitt"] }          #
ZERO_CROSS = ["MarrHildret"]                                            #
                                                                        #
single_threshold = 80                                                   #    
double_threshold = [0.1, 0.30]                                          #
zeroCrossing_threshold = 0.98                                           #
#########################################################################
```
The framework came preconfigured to run RobertsCross, Sobel and Prewitt as single-phase detector, to run Canny with all operators as multi-phase detector and to run MarrHildret as zero-crossing detector.

It will use "80" as threshold for single-phase detectors, "0.1" and "0.3" as low and high threshold ratio for multi-phase detectors and "0.98" as threshold ratio for zero-crossing detectors.

To apply a sharpening filter and generate a LaplacianOfGaussian filter it will use a (7 x 7) Gaussian mask with "2.3" standard deviation.

The default folder that contains some images to use with these algorithms is "Benchmark_Images" and the folder that contains relative ground truth images is "Benchmark_Images/GroundTruth". The results will be saved in "Benchmark_Result" directory

The "Benchmark_Images" folder came with some images and respective ground truths that are part of the Berkeley Segmentation Dataset (BSD500).

### Run
```
python src/Benchmark.py
```

## More details
If you understand Italian, you can read "Relazione.pdf" to get more details about edge detectors implemented in this framework.

## Author

- **Andrea Santangelo**
