import ply.lex as lex
import ply.yacc as yacc

class ParserException( Exception ):
  pass

def execute(ast):
  if type(ast) != list:
    return ast
  else:
    return sum([ execute(elem) for elem in ast[1:] ])
    
    
class Parser_Impl:
  
  # lexical rules #
  tokens = [ 'NUM','FUNC' ]
  literals = [ '(', ')', '+']

  # ignore space and tab characters
  t_ignore = ' \t\n'

  t_NUM = r'-?[0-9]+'
  t_FUNC = r'\+'
  
  def t_error( self, t ):
    raise ParserException( "Err: bad character %c at line %d"
      % ( t.value[0], t.lexer.lineno ) )

  # grammar #
  def p_lists(self, p):
    '''lists : list lists
             | list
    '''
    if len(p) == 3:
      p[0] = p[1] + p[2]
    else:
      p[0] = p[1]
  
  def p_list(self, p):
    '''list : '(' ')'
            | '(' atoms ')' '''
    if len(p) == 3:
      p[0] = []  # Empty list
    else:
      p[0] =  p[2]
  
  def p_atoms(self, p):
    
    '''atoms : atom atoms
             | atom
    '''
    if len(p) == 3:
      p[0] = p[1] + p[2]
    else:
      p[0] = p[1]

  def p_atom ( self, p ):
    '''atom : NUM
    '''
    p[0] = [int(p[1])]
    
  def p_atom_lists ( self, p ):
    '''atom : list
            | FUNC
    '''
    p[0] = [p[1]]
       
  def p_atom_unary( self, p ):
    '''atom : '-' NUM
            | '+' NUM
    '''
    if p[1] == '-':
      p[0] = [-1 * int( p[2] )]
    else:
      p[0] = [int( p[2] )]
 
  def p_error( self, p ):
    raise ParserException( "Parse error at '%s'" % p.value )
    return
  
  def evaluate( self, input ):
    ast = yacc.parse( input )
    return execute(ast)

  def __init__( self ):
    lex.lex( module = self )
    yacc.yacc( module = self ) 





