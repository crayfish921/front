from google.appengine.ext import ndb


class Mod(ndb.Model):
    plus=ndb.IntegerProperty()
    
class Summa(ndb.Model):
    first=ndb.IntegerProperty()
    second=ndb.IntegerProperty()
    result= ndb.IntegerProperty()
    
class Sub(ndb.Model):
    first=ndb.IntegerProperty()
    second=ndb.IntegerProperty()
    result= ndb.IntegerProperty()
    
class Division(ndb.Model):
    first=ndb.FloatProperty()
    second=ndb.FloatProperty()
    result= ndb.FloatProperty()
    
class Mul(ndb.Model):
    first=ndb.FloatProperty()
    second=ndb.FloatProperty()
    result= ndb.FloatProperty()
    
class Power(ndb.Model):
    num=ndb.IntegerProperty()
    powersym=ndb.IntegerProperty()
    result= ndb.IntegerProperty()
    
class Cell(ndb.Model):
    value = ndb.StringProperty()

class Row(ndb.Model):
    cells = ndb.LocalStructuredProperty(Cell, repeated=True)

class Table(ndb.Model):
    name = ndb.StringProperty() 
    rows = ndb.LocalStructuredProperty(Row, repeated=True)
    width = ndb.IntegerProperty()
    height = ndb.IntegerProperty()
    round = ndb.IntegerProperty()
    score = ndb.FloatProperty()
    path = ndb.IntegerProperty()
    move_count = ndb.IntegerProperty()
    
