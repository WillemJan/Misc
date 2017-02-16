#!/usr/bin/env python

t="""
TTeexxttTTeessttPPrrooggrreessssLLiisstteenneerr
===============================================================================
****** DDeessccrriippttiioonn ******
The class TextTestProgressListener (see _F_i_g_u_r_e_ _C_-_3_5) is a subclass of
TestListener. It prints a textual "progress bar" indicating the progress of a
series of tests as they are run. A sample of its output is shown here:
....F...E...

This shows that 10 tests were run, and 1 failure and 1 error occurred.
TextTestProgressListener belongs to the namespace CppUnit. It is declared in
TextTestProgressListener.h and implemented in TextTestProgressListener.cpp.
             **** FFiigguurree CC--3355.. TThhee ccllaassss TTeexxttTTeessttPPrrooggrreessssLLiisstteenneerr ****
                              [figs/utf_ac35.gif]

****** DDeeccllaarraattiioonn ******
class TextTestProgressListener : public TestListener

****** CCoonnssttrruuccttoorrss//DDeessttrruuccttoorrss ******

      A destructor.
****** PPuubblliicc MMeetthhooddss ******

      A method that informs TextTestProgressListener that a Test is about to be
      run. A period (.) is printed to indicate progress.
****** PPrrootteecctteedd//PPrriivvaattee MMeetthhooddss ******

      A copy operator, scoped private to prevent its use.
****** AAttttrriibbuutteess ******
None.
_[_P_r_e_v_i_o_u_s_ _S_e_c_t_i_o_n_] _ _&lt;_ _D_a_y_ _D_a_y_ _U_p_ _&gt;_  _[_N_e_x_t_ _S_e_c_t_i_o_n_]
</field>
<field name="page_a69db32b22717b1643d946ea2b0471c5">
_[_P_r_e_v_i_o_u_s_ _S_e_c_t_i_o_n_] _ _&lt;_ _D_a_y_ _D_a_y_ _U_p_ _&gt;_  _[_N_e_x_t_ _S_e_c_t_i_o_n_]

******** 66..44 TTeesstt AAsssseerrtt MMeetthhooddss ********
A range of test assert methods are provided by  JUnit. They are implemented as
public static methods of the class Assert, which is a parent class of TestCase.
Thus, every test class inherits these methods.
The most generic test assert method is assertTrue(), which simply passes or
fails based on the value of a Boolean argument. The other test assert methods
are specialized versions of assertTrue( ) that handle particular types of test
conditions. For example, the following test assert statements are equivalent:
assertTrue( book.title.equals("Cosmos") );
assertEquals( "Cosmos", book.title );

These statements are equivalent as well:
assertTrue( false )
fail( )

The specialized test assert methods are useful because they save coding effort,
are easier to read, and allow more specific reporting of the results.
The assert methods all have two variants, one that takes a String message as
the first argument, and one that doesn't. The message allow you to provide a
more detailed description of an assertion failure.
The assertEquals() methods compare the values of two arguments. They assume
that the first value is the correct or "expected" value to which the second
"actual" value should be compared. These methods will work if the arguments are
reversed, but the failure message will be misleading.
The JUnit assert methods are described in the following list:

      Test that always fails. It is equivalent to assertTrue(false).
_[_P_r_e_v_i_o_u_s_ _S_e_c_t_i_o_n_] _ _&lt;_ _D_a_y_ _D_a_y_ _U_p_ _&gt;_  _[_N_e_x_t_ _S_e_c_t_i_o_n_]
</field>
<field name="page_eb0879af25bb3d5be2ab8869bde2e27f">
_[_P_r_e_v_i_o_u_s_ _S_e_c_t_i_o_n_] _ _&lt;_ _D_a_y_ _D_a_y_ _U_p_ _&gt;_  _[_N_e_x_t_ _S_e_c_t_i_o_n_]

TTeexxttTTeessttRReessuulltt
===============================================================================
****** DDeessccrriippttiioonn ******
This class is deprecated and should not be used. The classes
TextTestProgressListener and TextOutputter replace it.
TextTestResult is declared in TextTestResult.h and implemented in
TextTestResult.cpp.
_[_P_r_e_v_i_o_u_s_ _S_e_c_t_i_o_n_] _ _&lt;_ _D_a_y_ _D_a_y_ _U_p_ _&gt;_  _[_N_e_x_t_ _S_e_c_t_i_o_n_]
</field>
<field name="rating">4.0</field>
<field name="page_4c2df64228c2c66c915d9b046d78f3b5">
_[_P_r_e_v_i_o_u_s_ _S_e_c_t_i_o_n_] _ _&lt;_ _D_a_y_ _D_a_y_ _U_p_ _&gt;_  _[_N_e_x_t_ _S_e_c_t_i_o_n_]

SSyynncchhrroonniizzeeddOObbjjeecctt::::EExxcclluussiivveeZZoonnee
===============================================================================
"""

i=0
l=[]
for line in t:
    print(line, ord(line))
    l.append(line)
print("".join(l))
