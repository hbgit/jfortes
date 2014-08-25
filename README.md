<h1> JFORTES (Java FORmal unit TESt generation) </h1>

================

          .-.
          /v\
         // \\    > L I N U X - GPL <
        /(   )\
         ^^-^^



Goal:
      This tool aims to generate unit test cases automatically based on safety properties.
      
================

<b> Requirements for using the tool </b> 

>> To use this tool is necessary that the system contains the following software already installed properly:

>> - Python
>> - Ctags
>> - Java 1.5
>> - ESC/JAVA

================

<b> How to install Map2Check-Fortes? </b>

In order to install JFortes on your PC, you should download and save the Jfortes_vx.tar.gz file on your disk. 
After that, you should type the following command:

- <b>STEP 1:</b>

>> $ tar -xzvf fortes_vx.tar.gz 

>> or from GITHUB

>> $ git clone https://github.com/hbgit/jfortes.git

- <b>STEP 2:</b>

Open the directory where the JFortes tool was extracted and then you should locate the configure.py and fortes script. After that, you should run the configure.py script, it is worth to say that you should run the configure.py script from inside the directory where JFortes was extracted.

>> Example:

>> 1) $ cd JFortes_vx 
>> 2) $ ls
>>     code_samples  <config.sh>  <fortes>  modules  README  result_claims
>> 3) $ ./configure.py


- <b>STEP 3:</b>

It is advisable that you should set the environment variable PATH in your .bashrc file as follows:

>> $ export PATH=$PATH:/home/user/JFortes_vx/

- <b>STEP 4:</b>

Testing Map2Check-Fortes

>> $ jfortes.py test_cases/primary_tests/Bag.java

================


<b>How running the JFortes?</b>

- <b>Running JFORTES.</b>

>> $ jfortes.py <file.c>

>> For help and others options:

>> $ ./jfortes.py -h