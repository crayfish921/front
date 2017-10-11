import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
import models
import random


size_x, size_j = 5, 5
#maze size

class Score(messages.Message):
    score = messages.StringField(1)
    rounds = messages.StringField(2)
    session_id = messages.StringField(3)

class Scores(messages.Message):
    scores = messages.MessageField(Score, 1, repeated=True) 
      
class Row(messages.Message):
    cell = messages.StringField(1, repeated=True)
    
class Field(messages.Message):
    rows = messages.MessageField(Row, 1, repeated=True)
    
class Direct(messages.Message):
    direction = messages.StringField(1)
    session = messages.StringField(2)
    
class Ses(messages.Message):
    session = messages.StringField(1) 

@endpoints.api(name='labyrinth', version='v1')
class Labyrinth (remote.Service):
    
    
    @endpoints.method(Ses, Field,
                    path='start-button', http_method='GET',
                    name='s.button')
    def start(self, request):
        if (models.Table.query(models.Table.name == request.session).get() == None):
            self.prepare_maze(size_x, size_j, request.session, 1, 0)
        table = self.get_table(request.session)
        return table
    
    def getdir(self, x, y, table, options=(' ',)):
        result = []
        if y + 1 < table.height:
            result.append((x, y + 1,'down'))
        if y - 1 >= 0:
            result.append((x, y - 1, 'up'))
        if x - 1 >= 0:
            result.append((x - 1, y, 'left'))
        if x + 1 < table.width:
            result.append((x + 1, y, 'right'))
            
        result = [r for r in result if table.rows[r[1]].cells[r[0]].value in options]
        return result
    

    def prepare_maze(self, width, height, session, round, score):        
       
       
        def genmaze_dfs(x, y, direction=None):
            table.rows[y].cells[x].value = 'path'
            if (x % 2 != 0 and y % 2 != 0):
                directions = self.getdir(x, y, table)       
                while directions != []:
                    turns = [d for d in directions if d[2] != direction]
                    if turns != []:
                        for _ in range(10):
                            directions += turns
                            
                    xx, yy, direction = directions[random.randint(0,len(directions) - 1)]
                    genmaze_dfs(xx, yy, direction)
                    directions = self.getdir(x, y, table)
            else:
                directions = self.getdir(x, y, table)
                for xx, yy, direction1 in directions:
                    if  direction in ['left', 'right'] and direction1 in ['up', 'down'] or direction in ['up', 'down'] and direction1 in ['left', 'right']:
                        table.rows[yy].cells[xx].value='wall'
                variable = [d for d in directions if d[2] == direction]                            
                if variable != [] and random.random() < 0.8:
                    genmaze_dfs(variable[0][0], variable[0][1], variable[0][2])
                else:
                    table.rows[y].cells[x].value = 'wall'
                    
                    
        
        def genmaze_prim(x, y, direction=None):
            table.rows[y].cells[x].value = 'player'
            start_cell = self.getdir(x, y, table)[0]
            #start_cell = table.width / 2, table.height / 2
            #make start cell path
            table.rows[start_cell[1]].cells[start_cell[0]].value = 'path'
            wall_set = {(x,y) for (x, y, _) in self.getdir(start_cell[0], start_cell[1], table)}
#             for xx, yy, direction in directions:
#                 wall_list.append([xx,yy,direction])  
#             print wall_list
            
            while wall_set != set():
                #print wall_set
                wall = random.sample(wall_set, 1)[0]
                directions = {d[2]: (d[0], d[1]) for d in self.getdir(wall[0], wall[1], table, (' ', 'wall'))}
                #print directions
                next = None
                if ('left' in directions.keys()) != ('right' in directions.keys()):
                    next = directions.get('left', directions.get('right')), 'hor'
                elif ('down' in directions.keys()) != ('up' in directions.keys()):
                    next = directions.get('down', directions.get('up')), 'vert'

                if next is not None:
                    origin = self.getdir(wall[0], wall[1], table, ('path',))[0]
                    #print wall, prev, self.getdir(prev[0], prev[1], table, ('path',))
                    previous = self.getdir(origin[0], origin[1], table, ('path',))
                    if len(previous) > 1 and random.random() > 0.1:
                        continue
#                     
                    if (len(previous) > 0 and random.random() > 0.2 and
                        (next[1] == 'hor' and (previous[0][2] in ['left', 'right']) or
                         next[1] == 'vert' and (previous[0][2] in ['up', 'down']))):
                        
                        continue
                    
                    
                    wall_set |= {(x,y) for (x, y, _) in self.getdir(next[0][0], next[0][1], table)}
                    table.rows[next[0][1]].cells[next[0][0]].value = 'path'
                    table.rows[wall[1]].cells[wall[0]].value = 'path'
                    
                wall_set.remove(wall)
                
            for y, row in enumerate(table.rows):
                for x, cell in enumerate(row.cells):
                    cell.value = 'wall' if cell.value == ' ' else cell.value

        
        for table in models.Table.query(models.Table.name == session):
            table.key.delete()
        table = models.Table(name=session, rows=[], width = width, height = height, round = round, score=score)
                
        table.rows = [models.Row(cells=[models.Cell(value='wall' if (x in [0, width - 1] or y in [0, height - 1]) else ' ')
                                        for x in range(width)]) for y in range(height)]
        
        if random.randint(0, 1) == 1:
            py = (random.randint(1, int(height / 2)) - 1) * 2 + 1
            ey = (random.randint(1, int(height / 2)) - 1) * 2 + 1
            px, ex = sorted([0, width - 1], reverse=random.randint(0, 1))
        else:
            px = (random.randint(1, int(width / 2)) - 1) * 2 + 1
            ex = (random.randint(1, int(width / 2)) - 1) * 2 + 1
            py, ey = sorted([0, height - 1], reverse=random.randint(0, 1))
        table.rows[py].cells[px].value = 'player'
        table.rows[ey].cells[ex].value ='exit'
        table.move_count = 0
#         while table.rows[y].cells[x].value == 'exit':
#             if random.randint(0, 1) == 1:
#                 y, x = (random.randint(1, int(height / 2)) - 1) * 2 + 1, [0, width - 1][random.randint(0, 1)]
#             else:
#                 x, y = (random.randint(1, int(width / 2)) - 1) * 2 + 1, [0, height - 1][random.randint(0, 1)]
        
    
#         genmaze_dfs(x, y, self.getdir(x, y, table)[0][2])

        genmaze_prim(px, py, self.getdir(px, py, table)[0][2])
        table.rows[py].cells[px].value = 'player'
        
        
#         for y, row in enumerate(self.table):
#             row_db = models.Row(cells=[])
#             for x, value in enumerate(row):
#                 cell = models.Cell(value=value)
#                 row_db.cells.append(cell)
#             table.rows.append(row_db)
        
        def solve_maze(py, px, table, prev):
            print px, py 
            direction = self.getdir(px, py, table, ('path','exit'))
            direction = [d for d in direction if (d[0],d[1]) != prev]
            print px, py, direction
            for xx, yy, _ in direction:       
#                 xx, yy, _ = random.sample(direction, 1)[0]
                if(table.rows[yy].cells[xx].value == 'path'):
                    result = solve_maze(yy, xx, table, (px,py))
                    if result:
                        return result + 1
                else:
                    return 1
            return False                          
            
        
        table.path = solve_maze(py, px, table, (-1,-1))
        table.put()
            
        
    @endpoints.method(Direct, Field,
                    path = 'move', http_method = 'GET',
                    name = 'move.click')
    def move(self, request):
        table = None
        while table is None:
            table=models.Table.query(models.Table.name == request.session).get()
        for y, row in enumerate(table.rows):
            for x, cell in enumerate(row.cells):
                if (cell.value == 'player'):
                        a, b = y, x
        future_a, future_b = {"RIGHT": (a, b + 1),
                              "LEFT": (a, b - 1),
                              "UP": (a-1, b),
                              "DOWN":(a+1, b)}[request.direction] 
        if (table.rows[future_a].cells[future_b].value == "path"):
            table.rows[future_a].cells[future_b].value = 'player' 
            table.rows[a].cells[b].value = 'path'
            table.move_count += 1
            table.put()
        if (table.rows[future_a].cells[future_b].value == "exit"):
            self.prepare_maze(table.width+2, table.height+2, table.name, table.round+1, table.score + table.path / float(table.move_count))
        table_message = self.get_table(request.session)
        return table_message  
        
    
    def get_table(self, session):
        result = []
        table = None
        while table is None:
            table=models.Table.query(models.Table.name == session).get()
        for row in table.rows:
            result.append(Row(cell=[]))
            for cell in row.cells:
                result[-1].cell.append(cell.value)

        return Field(rows=result)   
    
    
    @endpoints.method(message_types.VoidMessage, Scores,
                    path='get-score', http_method='GET',
                    name='get.score')              
    def get_scores(self, request):
        result = []
        for table in models.Table.query():
            result.append(Score(rounds=str(table.round), score=str(table.score), session_id=table.name))
        
        return Scores(scores=result)
    
    

            
            
            
            
        
        
        
            
            

        