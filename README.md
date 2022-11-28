# EasyMLServe: Easy Deployment of REST Machine Learning Services

This repository contains the Python implementation of the EasyMLServe framework presented in the paper:
>[O. Neumann](mailto:oliver.neumann@kit.edu), Marcel Schilling, Markus Reischl, and Ralf Mikut, 2022, "EasyMLServe: Easy Deployment of REST Machine Learning Services," in Proceedings. 32. Workshop Computational Intelligence Berlin, 1. – 2. December 2022, H. Schulte, F. Hoffmann, R. Mikut (Eds.), KIT Scientific Publishing Karlsruhe, pp. 11-30.

Available at [KIT Scientific Publishing](https://www.ksp.kit.edu/site/books/e/10.5445/KSP/1000151141/).

## Abstract

Various research domains use machine learning approaches because
they can solve complex tasks by learning from data.
Deploying machine learning models, however, is not trivial
and developers have to implement complete solutions
which are often installed locally and include Graphical User Interfaces (GUIs).
Distributing software to various users on-site has several problems.
Therefore, we propose a concept to deploy software in the cloud.
There are several frameworks available based on Representational State Transfer (REST)
which can be used to implement cloud-based machine learning services.
However, machine learning services for scientific users have special
requirements that state-of-the-art REST frameworks do not cover completely.
We contribute an EasyMLServe software framework to deploy machine learning
services in the cloud using REST interfaces and generic local or web-based GUIs.
Furthermore, we apply our framework on two real-world applications,
i.e., energy time-series forecasting and cell instance segmentation.
The EasyMLServe framework and the use cases are available on GitHub.

## Installation

To install the framework, simply use pip within this directory by calling `pip install .` or `pip install -e .` if you want to change the code and directly test it within your projects.

## Usage

To deploy your own EasyMLServe services, you have to implement your own EasyMLServive class by implementing an `api_call` and an optional `load_model` method. The implemented service can be deployed using our EasyMLServer class which expects an EasyMLService in the initialization method. Additionally, you can deploy an UI using GradioEasyMLUI or QtEasyMLUI classes. For further implementation details, please look at the examples or the paper.

## Examples

All available examples are located in the `examples` directory. Each example has its own `requirementy.txt`. If you want to run the examples, you have to install the `requirements.txt` via `pip install -r requirements.txt`. Some examples may require additional data or models. If so, a download.py is available within the directories. Please call `python download.py` within the directories.

## Funding

This project is funded by the Helmholtz Association’s Initiative and Networking
Fund through Helmholtz AI, the Helmholtz Association under the
Programs “Energy System Design” (ESD) and „Natural, Artificial and Cognitive
Information Processing“ (NACIP), and the German Research Foundation
(DFG) under Germany’s Excellence Strategy – EXC number 2064/1 – Project
number 390727645.


## License

This code is licensed under the [MIT License](LICENSE).