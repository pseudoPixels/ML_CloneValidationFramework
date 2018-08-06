# Machine Learning Based Code Clone Validation Framework
A code clone is a pair of code fragments, within or between software systems that are similar. 
Since code clones often negatively impact the maintainability of a software system, a great many 
numbers of code clone detection techniques and tools have been proposed and studied over the last 
decade such as, NiCAD [2], Cloneworks [3], SourcererCC [4] and so on. To detect all possible similar 
source code patterns in general, the clone detection tools work on syntax level (such as texts, tokens, 
AST and so on) while lacking user-specific preferences. This often means the reported clones must be 
manually validated prior to any analysis in order to filter out the true positive clones from task or 
user-specific considerations. This manual clone validation effort is very time-consuming and often error-prone, 
in particular for large-scale clone detection.

This is a machine learning based framework for automatic code clone validation - developed based on our recent 
research study [1]. The method learns to predict tasks or user-specific code clone validation patterns. The current 
machine learning model has been build based on BigCloneBench [5] - a collection of eight million validated clones within 
IJaDataset-2.0, a big data software repository containing 25,000 open-source Java systems. In addition to the useability of 
the trained model locally for code clone classification, this cloud based framework also supports the communication with any 
existing code clone detection tools for valdiation prediction responses using REST API. Please refer to the paper for 
additional details of the framework [1].






# References
[1] Mostaeen, G., Svajlenko, J., Roy, B., Roy, C. K., & Schneider, K. (2018, September). On the Use of Machine Learning Techniques Towards the Design of Cloud Based Automatic Code Clone Validation Tools. In Source Code Analysis and Manipulation (SCAM), 2018 IEEE 18th International Working Conference on. IEEE. 

[2] Roy, C. K., & Cordy, J. R. (2008, June). NICAD: Accurate detection of near-miss intentional clones using flexible pretty-printing and code normalization. In Program Comprehension, 2008. ICPC 2008. The 16th IEEE International Conference on (pp. 172-181). IEEE. 

[3] Svajlenko, J., & Roy, C. K. (2017, May). Cloneworks: A fast and flexible large-scale near-miss clone detection tool. In Proceedings of the 39th International Conference on Software Engineering Companion (pp. 177-179). IEEE Press. 

[4] Sajnani, H., Saini, V., Svajlenko, J., Roy, C. K., & Lopes, C. V. (2016, May). SourcererCC: scaling code clone detection to big-code. In Software Engineering (ICSE), 2016 IEEE/ACM 38th International Conference on (pp. 1157-1168). IEEE. 

[5] Svajlenko, J., & Roy, C. K. (2015, September). Evaluating clone detection tools with bigclonebench. In Software Maintenance and Evolution (ICSME), 2015 IEEE International Conference on (pp. 131-140). IEEE. 

[6] Ambient Software Evoluton Group. IJaDataset 2.0. http://secold.org/projects/seclone.


