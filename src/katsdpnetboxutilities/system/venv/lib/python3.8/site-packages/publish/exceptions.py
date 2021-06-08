
# Should all parsers (ie. Bibtex and Publish) share syntax error exception class

# This class is a bit simplistic at the moment. It should probably take 
# filename, line number and error message as separate arguments.
class ParseException(Exception) :
  pass
