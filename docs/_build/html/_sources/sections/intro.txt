Introduction to JFORTES
===================================

Nowadays, software applications need to be developed quickly and meet a high-level
of quality. Formal verification plays an important role to ensure predictability and dependability
in the design of critical applications. Consequently, the application of verification and testing are
indispensable techniques to the development of high-quality
software. However, there is usually a high cost involved in the preparation, execution
and management of tests. One way to deal with such problems is to integrate formal verification
techniques with test environments [#f4]_.

JFORTES  (Java FORmal unit TESt generation) is a method that aims to extract the safety properties generated
by ESC/JAVA [#f1]_ to generate automatically test cases using the rich set of assertions provided by Unit Test
frameworks, such as: TestNG [#f2]_ and JCUTE [#f3]_ . The integration of these two environments aims to ensure software
quality by exploiting formal verification and tests. JFORTES is a extension of FORTES [#f5]_ to Java programs.
We advocate that exploiting the integration between a testing framework and formal verification allows
us to go deeper into the Java program verification.


.. TODO: Show the JFORTES flow


.. rubric:: References

.. [#f1] Available at http://kindsoftware.com/products/opensource/ESCJava2/
.. [#f2] Available at http://testng.org/doc/index.html
.. [#f3] Available at http://osl.cs.illinois.edu/software/jcute/
.. [#f4] Herbert Rocha, Lucas Cordeiro, Raimundo Barreto and José Netto. Exploiting Safety Properties in Bounded Model
         Checking for Test Cases Generation of C Programs. In SAST. SBC. 2010.
.. [#f5] Available at https://sites.google.com/site/fortesmethod/
