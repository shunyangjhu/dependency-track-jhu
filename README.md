# dependency-track
## Johns Hopkins University MSSI Capstone Project - Postmarket Vulnerabilities Surveillance for Medical Devices

### Table of Contents

1. [Introduction](#introduction)
2. [File Descriptions](#files)
3. [Results](#results)
4. [Licensing, Authors, and Acknowledgements](#licensing)

## Introduction <a name="introduction"></a>
Our project is motivated by the Johns Hopkins University MSSI program Capstone Project requirement. We aim to know the state of medical devices available on third-party markets as it relates to:
- Medical Device Manufacturer exposure to use outside of the medical context (i.e., a security researcher may obtain a device and perform unbounded analysis)
- The security posture of a hospital or clinic that obtains a medical device with known vulnerabilities
The potential users/manufacturers would enter their manufacturer names and specific product names and our program would search the specific and currently available products given such inputs, and analyze the total available on sale products numbers. Additionally, we use NVD API to concern and output potential numbers and descriptions of vulnerabilities for such products given the manufacturer names. Finally, the program utilizes CyclondDX to create the SBOM file and dependency track tool to visualize the final risk profile provided by OWASP.

## File Description <a name=”"files"></a>
There are x files available here and the main file that the manufacturer needs to run is ‘dependency-track.py’
- Git clone our project using $ gh repo clone shunyangjhu/dependency-track-jhu

- Run python3 dependency-track.py -p ‘product_name’ -m ‘manufacturer_name’
- Example: python3 dependency-track.py -p ‘Plum A+’ -m ‘Hospira’
- The program would save a report (csv) file under the current directory you are using

## Licensing, Authors, Acknowledgements<a name="licensing"></a>

Authors: Tianze Ran, Shun Yang, Ziang Liang
