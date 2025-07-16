# to run this test, execute the command "python3 -m unittest -v <this file>"
import unittest
import parser, parser_impl

class TestList( unittest.TestCase ):
  
  # setUp will be called by the test framework before every test
  def setUp ( self ):
    self.p = parser_impl.Parser_Impl( )
    self.p.set_binding( parser.Binding.DEEP )

  # tearDown will be called by the test framework after every test
  def tearDown( self ):
    pass

  # each test must be self-contained and cannot depend on another
  # tests are executed in lexical order of their names   

  # test basic list functionality   
  def test_1( self ):
    self.assertEqual( self.p.evaluate( """
      ( set lst ( list 1 2 3 4 ) )
      ( select lst 1 )
      """), 2 )
    self.assertEqual( self.p.evaluate( """
      ( select ( list 7 8 9.2 True ) 0 )
      """), 7 )
    self.assertEqual( self.p.evaluate( """
      ( count ( list True ) )
      """), 1 )
    self.assertEqual( self.p.evaluate( """
      ( count ( list ) )
      """), 0 )
    # verify function names can be used in list
    self.assertEqual( self.p.evaluate( """
      ( count ( list not neq select ) )
      """), 3 )

  def test_2( self ):
    self.assertEqual( self.p.evaluate( """
      # we can now compute list averages
      ( set long_list ( list 1 2 3 4 5 6 7 8 9 10 ) )
      ( set ave ( lambda ( lst ) 
        ( / ( * 1.0 ( + lst ) ) ( count lst ) ) ) )
      ( ave long_list )
      """), 5.5 )
    self.assertEqual( self.p.evaluate( """
      ( set lst ( list ( list 1 2 3 ) ( list 4 5 6 ) ) ) # list of 2 lists
      ( count lst )
      """), 2 )
    self.assertEqual( self.p.evaluate( """
      # the + function should combine the two lists into one list
      ( set ll ( + ( list 1 2 3 ) ( list 4 5 6 ) ) )
      # the result list should have 6 elements and the last element is 6
      ( and ( eq ( count ll ) 6 ) ( eq ( select ll 5 ) 6 ) )
      """), True )

  def test_3( self ):
    # list comparison 
    self.assertEqual( self.p.evaluate( """
      ( eq ( list 1 2 3 ) ( list 1 2 3 ) )
      """), True )
    self.assertEqual( self.p.evaluate( """
      ( neq ( list 1 2 3 ) ( list 1 2 ) )
      """), True )    
    # list identity comparison
    self.assertEqual( self.p.evaluate( """
      ( is ( list 1 2 3 ) ( list 1 2 3 ) )
      """), False ) 
    # list identity comparison
    self.assertEqual( self.p.evaluate( """
      ( set ll ( list 1 2 3 ) )
      ( set mm ll ) 
      ( is ll mm )
      """), True ) 

  # test to demonstrate list can be passed to lambda functions
  def test_4( self ):
    self.assertEqual( self.p.evaluate( """ 
      ( set apply ( lambda ( func list ) 
        ( lambda ( i ) ( func list i ) )
        ) )
      ( set pick_one ( apply select ( list 1 5 7 9 ) ) ) 
      ( pick_one 2 )
      """ ), 7 )
        
  # after modifying the parser to allow floating point numbers:
  # test type conversion between integer and float
  def test_5( self ):
    self.assertEqual( self.p.evaluate( "( + 1.5 -2 )" ), -0.5 )
    self.assertEqual( self.p.evaluate( "( * 1.5 -2 )" ), -3.0 )
    self.assertEqual( self.p.evaluate( "( - 2 0.34 0.1 )" ), 1.56 )
    self.assertEqual( self.p.evaluate( "( + ( / 1 2. ) 3 )" ), 3.5 )
    # the following tests should work but we comment them out to make the
    # tests shorter
#     self.assertEqual( self.p.evaluate( "( / ( list 1 -2.0 ) )" ), -0.5 )
#     self.assertEqual( self.p.evaluate( "( * ( list 1.5 -2 4 ) )" ), -12.0 )
#     self.assertEqual( self.p.evaluate( "( - ( list 2 0.34 0.1 ) )" ), 1.56 )
